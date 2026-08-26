from __future__ import annotations

import gzip
import json
from pathlib import Path
import struct
import sys
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import e14_admission as admission  # noqa: E402


A1 = ROOT / "e14" / "vendor-acquisition-v2"
NODE = A1 / "objects" / "node-archive.body"
NODE_METADATA = A1 / "objects" / "node-metadata.body"
WHEEL = A1 / "objects" / "python-wheel.body"
PYTHON_METADATA = A1 / "objects" / "python-metadata.body"
SCHEMA = ROOT / "schemas" / "e14-a2-read-only-prescan-v1.schema.json"


def repair_tar_checksum(header: bytearray) -> None:
    header[148:156] = b"        "
    value = sum(header)
    header[148:156] = f"{value:06o}\0 ".encode("ascii")


def first_tar_header_with_type(typeflag: bytes) -> bytes:
    tar_bytes = bytearray(gzip.decompress(NODE.read_bytes()))
    tar_bytes[156:157] = typeflag
    header = bytearray(tar_bytes[:512])
    repair_tar_checksum(header)
    tar_bytes[:512] = header
    return bytes(tar_bytes)


def zip_central_offset(data: bytes) -> int:
    return struct.unpack("<4s4H2LH", data[-22:])[6]


class E14AdmissionTests(unittest.TestCase):
    def test_valid_production_archives_and_prescan(self):
        node = admission.scan_npm_tgz(NODE.read_bytes(), NODE_METADATA.read_bytes())
        wheel = admission.scan_python_wheel(WHEEL.read_bytes(), PYTHON_METADATA.read_bytes())
        report = admission.prescan_acquisition(A1)
        self.assertEqual(len(node.members), 6)
        self.assertEqual(len(wheel.members), 7)
        self.assertEqual(
            report["bundle_root"],
            "73B5CC047F09F39FE2F1A8E50EF398A65104F973F3CE7AC0CF1484990553F716",
        )
        self.assertEqual(report["authority_effect"], "NONE")
        self.assertEqual(report["admission_state"], "NOT_EXECUTED")

    def test_prescan_schema(self):
        report = admission.prescan_acquisition(A1)
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(report)

    def test_domain_roots_are_deterministic_and_domain_separated(self):
        a = admission._domain_root("one", [("b", b"2"), ("a", b"1")])
        b = admission._domain_root("one", [("a", b"1"), ("b", b"2")])
        c = admission._domain_root("two", [("a", b"1"), ("b", b"2")])
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_path_attacks_are_rejected(self):
        unsafe = [
            b"../escape",
            b"/absolute",
            b"C:/drive",
            b"safe\\evil",
            b"safe:stream",
            b"CON.txt",
            b"safe/../evil",
            b"safe./file",
            b"a//b",
        ]
        for path in unsafe:
            with self.subTest(path=path):
                with self.assertRaises(admission.AdmissionError):
                    admission.normalize_member_path(path, strip_prefix=None)

    def test_a1_phys_01_rejects_pax_gnu_sparse_and_unknown_physical_headers(self):
        for typeflag in (b"x", b"g", b"L", b"K", b"S", b"1", b"2", b"5", b"\0"):
            with self.subTest(typeflag=typeflag):
                with self.assertRaisesRegex(admission.AdmissionError, "VENDOR_ARCHIVE_UNSAFE"):
                    admission._scan_ustar_physical(first_tar_header_with_type(typeflag))

    def test_a1_phys_01_rejects_base256_tar_number(self):
        tar_bytes = bytearray(gzip.decompress(NODE.read_bytes()))
        header = bytearray(tar_bytes[:512])
        header[124] = 0x80
        repair_tar_checksum(header)
        tar_bytes[:512] = header
        with self.assertRaisesRegex(admission.AdmissionError, "base-256"):
            admission._scan_ustar_physical(bytes(tar_bytes))

    def test_a1_phys_01_rejects_nonzero_tar_padding(self):
        tar_bytes = bytearray(gzip.decompress(NODE.read_bytes()))
        first_size = admission._parse_tar_number(tar_bytes[124:136], "size")
        tar_bytes[512 + first_size] = 1
        with self.assertRaisesRegex(admission.AdmissionError, "nonzero tar padding"):
            admission._scan_ustar_physical(bytes(tar_bytes))

    def test_a1_phys_01_rejects_concatenated_and_trailing_gzip(self):
        original = NODE.read_bytes()
        for data in (original + original, original + b"trailing"):
            with self.subTest(length=len(data)):
                with self.assertRaises(admission.AdmissionError):
                    admission._decode_gzip_strict(data)

    def test_a1_phys_01_rejects_zip_encryption_or_descriptor_flag(self):
        for flag in (1, 8):
            data = bytearray(WHEEL.read_bytes())
            central = zip_central_offset(data)
            data[central + 8 : central + 10] = struct.pack("<H", flag)
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(admission.AdmissionError, "flags"):
                    admission._scan_zip_physical(bytes(data))

    def test_a1_phys_01_rejects_zip_local_central_mismatch(self):
        data = bytearray(WHEEL.read_bytes())
        data[8:10] = struct.pack("<H", 0)
        with self.assertRaisesRegex(admission.AdmissionError, "local/central"):
            admission._scan_zip_physical(bytes(data))

    def test_a1_phys_01_rejects_zip_symlink_mode(self):
        data = bytearray(WHEEL.read_bytes())
        central = zip_central_offset(data)
        symlink_mode = (0o120777 << 16) | (struct.unpack("<L", data[central + 38 : central + 42])[0] & 0xFFFF)
        data[central + 38 : central + 42] = struct.pack("<L", symlink_mode)
        with self.assertRaisesRegex(admission.AdmissionError, "not an exact"):
            admission._scan_zip_physical(bytes(data))

    def test_a1_phys_01_rejects_zip_comment_and_trailing_bytes(self):
        with self.assertRaisesRegex(admission.AdmissionError, "EOCD"):
            admission._scan_zip_physical(WHEEL.read_bytes() + b"x")

    def test_replay_mutation_changes_physical_root(self):
        original = gzip.decompress(NODE.read_bytes())
        members, first_root = admission._scan_ustar_physical(original)
        mutated = bytearray(original)
        mutated[512] ^= 1
        _, second_root = admission._scan_ustar_physical(bytes(mutated))
        self.assertEqual(len(members), 6)
        self.assertNotEqual(first_root, second_root)

    def test_source_analyzers_reject_dynamic_or_unapproved_imports(self):
        with self.assertRaisesRegex(admission.AdmissionError, "RUNTIME_DYNAMIC_LOAD_PROHIBITED"):
            admission._node_source_closure(
                {"lib/x.js": b"const x = import('ambient');"}, {"main": "lib/x.js"}
            )
        with self.assertRaisesRegex(admission.AdmissionError, "VENDOR_DEPENDENCY_UNEXPECTED"):
            admission._python_source_closure({"pkg/x.py": b"import requests\n"})

    def test_a1_root_is_exact_and_admission_root_remains_absent(self):
        verified = admission.verify_a1_root(A1)
        self.assertEqual(verified["file_count"], 20)
        self.assertFalse((ROOT / "e14" / "vendor-admission-v1").exists())


if __name__ == "__main__":
    unittest.main()
