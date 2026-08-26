"""Fail-closed, read-only E14 A2 archive pre-scanner.

This module never imports or executes vendor code and never creates an admission root.
It is the production scanner whose exact bytes are bound by the G1 evidence manifest.
"""

from __future__ import annotations

import ast
import base64
import binascii
import csv
from dataclasses import dataclass
from email import policy as email_policy
from email.parser import BytesParser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import struct
from typing import Any, Iterable
import zlib


MIB = 1024 * 1024
MAX_INPUT_FILES = 32
MAX_INPUT_BYTES = 16 * MIB
MAX_MEMBERS = 512
MAX_EXPANDED_FILES = 512
MAX_EXPANDED_BYTES = 32 * MIB
MAX_SINGLE_FILE = 2 * MIB
MAX_PATH_DEPTH = 12
MAX_TAR_STREAM = MAX_EXPANDED_BYTES + MAX_MEMBERS * 1024 + 1024

NODE_ARCHIVE_SHA256 = "AE9A1851B4D3489FBA0D6A45A6B779296C5FE7F9DD626EB2C6D12045D47CBA87"
PYTHON_WHEEL_SHA256 = "520D690B448ECF0703691C76E1A34A24DDCD4FC5BC41D589CB7C58EC651BCD48"
A1_TERMINAL_SHA256 = "33C3035DC90D7758A6D92BDE3D9CA629088AB94B1347881E929CEA21AED11879"
NODE_LICENSE_SHA256 = "C71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4"
PYTHON_LICENSE_SHA256 = "0D542E0C8804E39AA7F37EB00DA5A762149DC682D7829451287E11B938E94594"

NODE_FILES = {
    "LICENSE",
    "README.md",
    "bin/canonicalize.js",
    "lib/canonicalize.d.ts",
    "lib/canonicalize.js",
    "package.json",
}
PYTHON_FILES = {
    "rfc8785/__init__.py",
    "rfc8785/_impl.py",
    "rfc8785/py.typed",
    "rfc8785-0.1.4.dist-info/LICENSE",
    "rfc8785-0.1.4.dist-info/METADATA",
    "rfc8785-0.1.4.dist-info/RECORD",
    "rfc8785-0.1.4.dist-info/WHEEL",
}
PROHIBITED_NPM_HOOKS = {
    "preinstall",
    "install",
    "postinstall",
    "prepare",
    "prepublish",
    "prepublishOnly",
}
PYTHON_STDLIB_ALLOWLIST = {"__future__", "io", "math", "re", "typing"}
DOS_DEVICES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


class AdmissionError(ValueError):
    """A typed fail-closed vendor rejection or operational inconclusive result."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def reject(code: str, detail: str) -> None:
    raise AdmissionError(code, detail)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _json_no_duplicates(data: bytes, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                reject("VENDOR_METADATA_INVALID", f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(data.decode("utf-8", "strict"), object_pairs_hook=pairs_hook)
    except AdmissionError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        reject("VENDOR_METADATA_INVALID", f"{label}: {exc}")


def _domain_root(domain: str, records: Iterable[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256()
    domain_bytes = domain.encode("ascii")
    digest.update(struct.pack(">H", len(domain_bytes)))
    digest.update(domain_bytes)
    ordered = sorted(records, key=lambda item: item[0].encode("utf-8"))
    digest.update(struct.pack(">I", len(ordered)))
    for path, content in ordered:
        path_bytes = path.encode("utf-8")
        digest.update(struct.pack(">I", len(path_bytes)))
        digest.update(path_bytes)
        digest.update(struct.pack(">Q", len(content)))
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest().upper()


def _record_root(domain: str, records: list[dict[str, Any]]) -> str:
    return _domain_root(domain, ((f"{i:06d}", canonical_json_bytes(r)) for i, r in enumerate(records)))


def normalize_member_path(raw_name: bytes, *, strip_prefix: str | None) -> str:
    try:
        name = raw_name.decode("ascii", "strict")
    except UnicodeDecodeError:
        reject("VENDOR_PATH_UNSAFE", "member name is not ASCII")
    if not name or "\x00" in name:
        reject("VENDOR_PATH_UNSAFE", "empty or NUL-containing member name")
    if "\\" in name or ":" in name:
        reject("VENDOR_PATH_UNSAFE", f"backslash or colon in {name!r}")
    if name.startswith("/") or name.startswith("//") or re.match(r"^[A-Za-z]:", name):
        reject("VENDOR_PATH_UNSAFE", f"absolute, UNC, or drive path {name!r}")
    if strip_prefix is not None:
        prefix = strip_prefix + "/"
        if not name.startswith(prefix):
            reject("VENDOR_PATH_UNSAFE", f"missing exact archive prefix {prefix!r}")
        name = name[len(prefix) :]
    parts = name.split("/")
    if not parts or len(parts) > MAX_PATH_DEPTH:
        reject("VENDOR_PATH_UNSAFE", f"path depth outside cap: {name!r}")
    for part in parts:
        if part in {"", ".", ".."}:
            reject("VENDOR_PATH_UNSAFE", f"empty, dot, or traversal segment in {name!r}")
        if part[-1:] in {" ", "."}:
            reject("VENDOR_PATH_UNSAFE", f"Windows-trim collision in {name!r}")
        stem = part.split(".", 1)[0].upper()
        if stem in DOS_DEVICES:
            reject("VENDOR_PATH_UNSAFE", f"reserved Windows device in {name!r}")
        if any(ord(char) < 0x20 or ord(char) == 0x7F for char in part):
            reject("VENDOR_PATH_UNSAFE", f"control character in {name!r}")
    normalized = "/".join(parts)
    if str(PurePosixPath(normalized)) != normalized:
        reject("VENDOR_PATH_UNSAFE", f"non-canonical path {name!r}")
    return normalized


@dataclass(frozen=True)
class Member:
    path: str
    raw_path: str
    content: bytes
    mode: int

    def report(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "raw_path": self.raw_path,
            "bytes": len(self.content),
            "sha256": sha256(self.content),
            "mode": self.mode,
        }


@dataclass
class ArchiveScan:
    kind: str
    raw_sha256: str
    physical_root: str
    members: list[Member]
    package: dict[str, Any]
    dependency: dict[str, Any]
    source_closure: dict[str, Any]

    def report(self) -> dict[str, Any]:
        member_reports = [member.report() for member in sorted(self.members, key=lambda x: x.path)]
        inventory_root = _record_root(f"sana.e14.{self.kind}.inventory.v1", member_reports)
        source_members = [
            (member.path, member.content)
            for member in self.members
            if (self.kind == "npm" and member.path.endswith(".js"))
            or (self.kind == "wheel" and member.path.endswith(".py"))
        ]
        source_root = _domain_root(f"sana.e14.{self.kind}.source.v1", source_members)
        return {
            "kind": self.kind,
            "raw_sha256": self.raw_sha256,
            "physical_root": self.physical_root,
            "member_count": len(self.members),
            "expanded_bytes": sum(len(member.content) for member in self.members),
            "members": member_reports,
            "inventory_root": inventory_root,
            "source_root": source_root,
            "package": self.package,
            "declared_dependency_set": self.dependency,
            "runtime_dependency_closure": self.source_closure,
        }


def _parse_tar_number(field: bytes, label: str) -> int:
    if not field or field[0] & 0x80:
        reject("VENDOR_ARCHIVE_UNSAFE", f"{label}: base-256 or empty numeric field")
    stripped = field.rstrip(b"\x00 ")
    if not stripped:
        return 0
    if any(byte not in b"01234567" for byte in stripped):
        reject("VENDOR_ARCHIVE_UNSAFE", f"{label}: non-octal numeric field")
    return int(stripped, 8)


def _c_string(field: bytes, label: str) -> bytes:
    if b"\x00" in field:
        value, tail = field.split(b"\x00", 1)
        if any(tail):
            reject("VENDOR_ARCHIVE_UNSAFE", f"{label}: nonzero bytes after NUL")
        return value
    return field


def _inflate_raw(payload: bytes, expected_size: int, cap: int, label: str) -> bytes:
    decompressor = zlib.decompressobj(-15)
    output = bytearray()
    for offset in range(0, len(payload), 65536):
        chunk = payload[offset : offset + 65536]
        while chunk:
            remaining = cap + 1 - len(output)
            if remaining <= 0:
                reject("VENDOR_ARCHIVE_CAP_EXCEEDED", f"{label}: expanded byte cap")
            output.extend(decompressor.decompress(chunk, remaining))
            chunk = decompressor.unconsumed_tail
    remaining = cap + 1 - len(output)
    output.extend(decompressor.flush(max(0, remaining)))
    if len(output) > cap:
        reject("VENDOR_ARCHIVE_CAP_EXCEEDED", f"{label}: expanded byte cap")
    if not decompressor.eof or decompressor.unused_data or decompressor.unconsumed_tail:
        reject("VENDOR_ARCHIVE_UNSAFE", f"{label}: incomplete or trailing deflate stream")
    if len(output) != expected_size:
        reject("VENDOR_ARCHIVE_UNSAFE", f"{label}: uncompressed size mismatch")
    return bytes(output)


def _decode_gzip_strict(data: bytes) -> bytes:
    if len(data) < 18 or data[:3] != b"\x1f\x8b\x08":
        reject("VENDOR_ARCHIVE_UNSAFE", "invalid gzip signature or compression method")
    if data[3] != 0:
        reject("VENDOR_ARCHIVE_UNSAFE", "gzip optional/reserved flags are prohibited")
    expected_crc, expected_size = struct.unpack("<II", data[-8:])
    compressed = data[10:-8]
    decompressor = zlib.decompressobj(-15)
    output = bytearray()
    for offset in range(0, len(compressed), 65536):
        chunk = compressed[offset : offset + 65536]
        while chunk:
            remaining = MAX_TAR_STREAM + 1 - len(output)
            if remaining <= 0:
                reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "gzip expanded stream cap")
            output.extend(decompressor.decompress(chunk, remaining))
            chunk = decompressor.unconsumed_tail
    output.extend(decompressor.flush(MAX_TAR_STREAM + 1 - len(output)))
    if len(output) > MAX_TAR_STREAM:
        reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "gzip expanded stream cap")
    if not decompressor.eof or decompressor.unused_data or decompressor.unconsumed_tail:
        reject("VENDOR_ARCHIVE_UNSAFE", "concatenated, trailing, or incomplete gzip deflate")
    if len(output) & 0xFFFFFFFF != expected_size:
        reject("VENDOR_ARCHIVE_UNSAFE", "gzip ISIZE mismatch")
    if binascii.crc32(output) & 0xFFFFFFFF != expected_crc:
        reject("VENDOR_ARCHIVE_UNSAFE", "gzip CRC32 mismatch")
    return bytes(output)


def _scan_ustar_physical(tar_bytes: bytes) -> tuple[list[Member], str]:
    members: list[Member] = []
    transcript: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    expanded = 0
    offset = 0
    terminal_seen = False
    while offset + 512 <= len(tar_bytes):
        header = tar_bytes[offset : offset + 512]
        if not any(header):
            if len(tar_bytes) - offset < 1024 or any(tar_bytes[offset:]):
                reject("VENDOR_ARCHIVE_UNSAFE", "tar end marker/trailing bytes invalid")
            terminal_seen = True
            break
        if len(members) >= MAX_MEMBERS:
            reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "tar member cap")
        stored_checksum = _parse_tar_number(header[148:156], "tar checksum")
        checksum_header = header[:148] + b" " * 8 + header[156:]
        if sum(checksum_header) != stored_checksum:
            reject("VENDOR_ARCHIVE_UNSAFE", "tar header checksum mismatch")
        if header[257:263] != b"ustar\x00" or header[263:265] != b"00":
            reject("VENDOR_ARCHIVE_UNSAFE", "only strict POSIX ustar headers are accepted")
        if header[156:157] != b"0":
            reject("VENDOR_ARCHIVE_UNSAFE", "only explicit regular typeflag 0 is accepted")
        if _c_string(header[345:500], "tar prefix"):
            reject("VENDOR_ARCHIVE_UNSAFE", "ustar prefix field is prohibited")
        if _c_string(header[157:257], "tar linkname"):
            reject("VENDOR_ARCHIVE_UNSAFE", "tar linkname is prohibited")
        size = _parse_tar_number(header[124:136], "tar size")
        mode = _parse_tar_number(header[100:108], "tar mode")
        _parse_tar_number(header[108:116], "tar uid")
        _parse_tar_number(header[116:124], "tar gid")
        _parse_tar_number(header[136:148], "tar mtime")
        _parse_tar_number(header[329:337], "tar devmajor")
        _parse_tar_number(header[337:345], "tar devminor")
        if size > MAX_SINGLE_FILE:
            reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "tar single-file cap")
        raw_name = _c_string(header[:100], "tar name")
        path = normalize_member_path(raw_name, strip_prefix="package")
        collision_key = path.casefold()
        if collision_key in seen:
            reject("VENDOR_PATH_COLLISION", f"{path!r} collides with {seen[collision_key]!r}")
        payload_start = offset + 512
        payload_end = payload_start + size
        padded_end = payload_start + ((size + 511) // 512) * 512
        if padded_end > len(tar_bytes):
            reject("VENDOR_ARCHIVE_UNSAFE", "tar member exceeds physical stream")
        content = tar_bytes[payload_start:payload_end]
        if any(tar_bytes[payload_end:padded_end]):
            reject("VENDOR_ARCHIVE_UNSAFE", "nonzero tar padding")
        expanded += size
        if expanded > MAX_EXPANDED_BYTES or len(members) + 1 > MAX_EXPANDED_FILES:
            reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "tar expanded aggregate cap")
        seen[collision_key] = path
        raw_name_text = raw_name.decode("ascii")
        members.append(Member(path, raw_name_text, content, mode))
        transcript.append(
            {
                "offset": offset,
                "raw_path": raw_name_text,
                "path": path,
                "typeflag": "0",
                "size": size,
                "header_sha256": sha256(header),
                "payload_sha256": sha256(content),
                "padding_bytes": padded_end - payload_end,
            }
        )
        offset = padded_end
    if not terminal_seen:
        reject("VENDOR_ARCHIVE_UNSAFE", "missing two-block tar terminator")
    return members, _record_root("sana.e14.npm.physical-ustar.v1", transcript)


def _check_exact_inventory(members: list[Member], expected: set[str], label: str) -> None:
    actual = {member.path for member in members}
    if actual != expected or len(actual) != len(members):
        reject(
            "VENDOR_INVENTORY_MISMATCH",
            f"{label}: missing={sorted(expected - actual)!r} extra={sorted(actual - expected)!r}",
        )


def _member_map(members: list[Member]) -> dict[str, bytes]:
    return {member.path: member.content for member in members}


def _node_source_closure(files: dict[str, bytes], package_json: dict[str, Any]) -> dict[str, Any]:
    references: list[dict[str, str]] = []
    risky = re.compile(
        r"\b(?:require\s*\(|import\s*\(|eval\s*\(|Function\s*\(|WebAssembly\b|"
        r"process\.(?:binding|dlopen)\b|createRequire\b)"
    )
    static_import = re.compile(
        r"\bimport\s+(?:(?:[\w*$,\s{}]+)\s+from\s+)?([\"'])([^\"']+)\1\s*;"
    )
    default_export = re.compile(
        r"\bexport\s+default\s+(?:function\s+[A-Za-z_$][\w$]*\s*\(|"
        r"[A-Za-z_$][\w$]*\s*;)"
    )
    for path in sorted(name for name in files if name.endswith(".js")):
        try:
            text = files[path].decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            reject("RUNTIME_CLOSURE_INCOMPLETE", f"{path}: {exc}")
        match = risky.search(text)
        if match:
            reject("RUNTIME_DYNAMIC_LOAD_PROHIBITED", f"{path}: {match.group(0)!r}")
        spans: list[tuple[int, int]] = []
        for match in static_import.finditer(text):
            spans.append(match.span())
            target = match.group(2)
            if not target.startswith("."):
                reject("VENDOR_DEPENDENCY_UNEXPECTED", f"{path}: bare import {target!r}")
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            if resolved not in files:
                reject("RUNTIME_REFERENCE_UNRESOLVED", f"{path}: {target!r} -> {resolved!r}")
            references.append({"source": path, "kind": "static-import", "target": resolved})
        for token in re.finditer(r"\bimport\b", text):
            if not any(start <= token.start() < end for start, end in spans):
                reject("RUNTIME_CLOSURE_INCOMPLETE", f"{path}: unrecognized import syntax")
        export_spans = [match.span() for match in default_export.finditer(text)]
        for token in re.finditer(r"\bexport\b", text):
            if not any(start <= token.start() < end for start, end in export_spans):
                reject("RUNTIME_CLOSURE_INCOMPLETE", f"{path}: unrecognized export syntax")
    entry_fields = {"main": package_json.get("main"), "types": package_json.get("types")}
    exports = package_json.get("exports")
    if isinstance(exports, dict) and isinstance(exports.get("."), dict):
        entry_fields["exports.import"] = exports["."].get("import")
        entry_fields["exports.types"] = exports["."].get("types")
    bin_field = package_json.get("bin")
    if isinstance(bin_field, dict):
        for key, value in sorted(bin_field.items()):
            entry_fields[f"bin.{key}"] = value
    for field, value in sorted(entry_fields.items()):
        if value is None:
            continue
        if not isinstance(value, str):
            reject("VENDOR_METADATA_INVALID", f"package entry {field} is not a string")
        target = value[2:] if value.startswith("./") else value
        if target not in files:
            reject("RUNTIME_REFERENCE_UNRESOLVED", f"package entry {field}: {value!r}")
        references.append({"source": "package.json", "kind": field, "target": target})
    return {
        "analyzer": "node-conservative-static-v1",
        "runtime_boundary": "Node.js >=18 plus built-in globals; no bare module references",
        "external_allowlist": [],
        "references": references,
        "dynamic_loading": "ABSENT_BY_CONSERVATIVE_SCAN",
        "structural_coverage": "COMPLETE_FOR_FROZEN_SOURCE_ROOT",
        "semantic_completeness": False,
        "semantic_attestation_required": True,
    }


def scan_npm_tgz(data: bytes, registry_metadata: bytes | None = None) -> ArchiveScan:
    if len(data) > MAX_INPUT_BYTES:
        reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "npm archive input cap")
    raw_hash = sha256(data)
    if raw_hash != NODE_ARCHIVE_SHA256:
        reject("VENDOR_ARCHIVE_HASH_MISMATCH", f"npm archive {raw_hash}")
    tar_bytes = _decode_gzip_strict(data)
    members, physical_root = _scan_ustar_physical(tar_bytes)
    _check_exact_inventory(members, NODE_FILES, "npm")
    files = _member_map(members)
    package_json = _json_no_duplicates(files["package.json"], "npm package.json")
    if package_json.get("name") != "canonicalize" or package_json.get("version") != "4.0.0":
        reject("VENDOR_PACKAGE_IDENTITY_MISMATCH", "npm name/version")
    if package_json.get("license") != "Apache-2.0":
        reject("VENDOR_LICENSE_MISMATCH", "npm SPDX declaration")
    if sha256(files["LICENSE"]) != NODE_LICENSE_SHA256:
        reject("VENDOR_LICENSE_MISMATCH", "npm LICENSE bytes")
    dependency_fields = [
        "dependencies",
        "peerDependencies",
        "optionalDependencies",
        "bundledDependencies",
        "bundleDependencies",
    ]
    declared: dict[str, Any] = {}
    for field in dependency_fields:
        value = package_json.get(field)
        if value not in (None, {}, []):
            reject("VENDOR_DEPENDENCY_UNEXPECTED", f"npm {field} is not empty")
        declared[field] = [] if isinstance(value, list) else {}
    scripts = package_json.get("scripts", {})
    if not isinstance(scripts, dict) or any(not isinstance(k, str) for k in scripts):
        reject("VENDOR_METADATA_INVALID", "npm scripts")
    prohibited = sorted(PROHIBITED_NPM_HOOKS.intersection(scripts))
    if prohibited:
        reject("VENDOR_INSTALL_HOOK_PRESENT", ", ".join(prohibited))
    if registry_metadata is not None:
        metadata = _json_no_duplicates(registry_metadata, "npm registry metadata")
        dist = metadata.get("dist", {})
        if metadata.get("name") != "canonicalize" or metadata.get("version") != "4.0.0":
            reject("VENDOR_PACKAGE_IDENTITY_MISMATCH", "npm registry name/version")
        expected_sri = "sha512-FEdXzwWs+N3rZqEqpqleiY9M1A6IAf9oo1zHFABnLW9FcJ/jzsu+G/Ks3Hq3FglmPKe80GeGBw8ZXLEnwPB0vQ=="
        if dist.get("integrity") != expected_sri:
            reject("VENDOR_ARCHIVE_HASH_MISMATCH", "npm registry SRI")
        if hashlib.sha512(data).digest() != base64.b64decode(expected_sri.split("-", 1)[1]):
            reject("VENDOR_ARCHIVE_HASH_MISMATCH", "npm SHA-512 SRI bytes")
        if hashlib.sha1(data).hexdigest() != dist.get("shasum"):
            reject("VENDOR_ARCHIVE_HASH_MISMATCH", "npm SHA-1 shasum")
    dependency = {
        "registry_runtime": [],
        "peer": [],
        "optional": [],
        "bundled": [],
        "scripts_recorded_not_executed": {k: scripts[k] for k in sorted(scripts)},
        "prohibited_hooks": [],
    }
    package = {
        "name": "canonicalize",
        "version": "4.0.0",
        "license_decision": "Apache-2.0",
        "license_sha256": NODE_LICENSE_SHA256,
    }
    return ArchiveScan(
        "npm",
        raw_hash,
        physical_root,
        members,
        package,
        dependency,
        _node_source_closure(files, package_json),
    )


@dataclass(frozen=True)
class _CentralEntry:
    raw_name: bytes
    path: str
    version_needed: int
    flags: int
    method: int
    mtime: int
    mdate: int
    crc32: int
    compressed_size: int
    size: int
    external_attr: int
    local_offset: int


def _scan_zip_physical(data: bytes) -> tuple[list[Member], str]:
    if len(data) < 22 or data[-22:-18] != b"PK\x05\x06":
        reject("VENDOR_ARCHIVE_UNSAFE", "ZIP EOCD is not exact and comment-free")
    (
        signature,
        disk,
        central_disk,
        disk_entries,
        total_entries,
        central_size,
        central_offset,
        comment_length,
    ) = struct.unpack("<4s4H2LH", data[-22:])
    if signature != b"PK\x05\x06" or any((disk, central_disk, comment_length)):
        reject("VENDOR_ARCHIVE_UNSAFE", "multi-disk ZIP or archive comment")
    if disk_entries != total_entries or total_entries > MAX_MEMBERS:
        reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "ZIP member count")
    eocd_offset = len(data) - 22
    if central_offset + central_size != eocd_offset:
        reject("VENDOR_ARCHIVE_UNSAFE", "ZIP central directory boundary mismatch")
    cursor = central_offset
    entries: list[_CentralEntry] = []
    seen: dict[str, str] = {}
    transcript: list[dict[str, Any]] = []
    for index in range(total_entries):
        if cursor + 46 > eocd_offset:
            reject("VENDOR_ARCHIVE_UNSAFE", "truncated ZIP central record")
        fields = struct.unpack("<4s6H3L5H2L", data[cursor : cursor + 46])
        (
            central_signature,
            version_made,
            version_needed,
            flags,
            method,
            mtime,
            mdate,
            crc32_value,
            compressed_size,
            size,
            name_length,
            extra_length,
            member_comment_length,
            disk_start,
            internal_attr,
            external_attr,
            local_offset,
        ) = fields
        if central_signature != b"PK\x01\x02":
            reject("VENDOR_ARCHIVE_UNSAFE", "invalid ZIP central signature")
        if 0xFFFF in (disk_entries, total_entries, name_length, extra_length, member_comment_length):
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP64/sentinel field prohibited")
        if 0xFFFFFFFF in (central_size, central_offset, compressed_size, size, local_offset):
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP64 size/offset prohibited")
        name_start = cursor + 46
        raw_name = data[name_start : name_start + name_length]
        record_end = name_start + name_length + extra_length + member_comment_length
        if record_end > eocd_offset:
            reject("VENDOR_ARCHIVE_UNSAFE", "truncated ZIP central variable fields")
        if extra_length or member_comment_length or disk_start or internal_attr:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP extra/comment/disk/internal attributes prohibited")
        if flags != 0 or method != 8:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP encryption, descriptors, flags, or method prohibited")
        if version_made != 0x0314 or version_needed != 20:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP creator/required version must be Unix 2.0")
        mode = external_attr >> 16
        if stat.S_IFMT(mode) != stat.S_IFREG or mode != 0o100644:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP member is not an exact 0644 regular file")
        path = normalize_member_path(raw_name, strip_prefix=None)
        collision_key = path.casefold()
        if collision_key in seen:
            reject("VENDOR_PATH_COLLISION", f"{path!r} collides with {seen[collision_key]!r}")
        if size > MAX_SINGLE_FILE:
            reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "ZIP single-file cap")
        seen[collision_key] = path
        entries.append(
            _CentralEntry(
                raw_name,
                path,
                version_needed,
                flags,
                method,
                mtime,
                mdate,
                crc32_value,
                compressed_size,
                size,
                external_attr,
                local_offset,
            )
        )
        transcript.append(
            {
                "central_index": index,
                "central_offset": cursor,
                "path": path,
                "size": size,
                "compressed_size": compressed_size,
                "crc32": f"{crc32_value:08X}",
                "local_offset": local_offset,
                "central_record_sha256": sha256(data[cursor:record_end]),
            }
        )
        cursor = record_end
    if cursor != eocd_offset:
        reject("VENDOR_ARCHIVE_UNSAFE", "central directory contains hidden/trailing records")
    members: list[Member] = []
    expanded = 0
    local_cursor = 0
    for entry in sorted(entries, key=lambda item: item.local_offset):
        if entry.local_offset != local_cursor or local_cursor + 30 > central_offset:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP local records are non-contiguous or overlap")
        fields = struct.unpack("<4s5H3L2H", data[local_cursor : local_cursor + 30])
        (
            local_signature,
            version_needed,
            flags,
            method,
            mtime,
            mdate,
            crc32_value,
            compressed_size,
            size,
            name_length,
            extra_length,
        ) = fields
        name_start = local_cursor + 30
        raw_name = data[name_start : name_start + name_length]
        payload_start = name_start + name_length + extra_length
        payload_end = payload_start + compressed_size
        if payload_end > central_offset:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP local payload exceeds central boundary")
        local_tuple = (
            version_needed,
            flags,
            method,
            mtime,
            mdate,
            crc32_value,
            compressed_size,
            size,
            raw_name,
        )
        central_tuple = (
            entry.version_needed,
            entry.flags,
            entry.method,
            entry.mtime,
            entry.mdate,
            entry.crc32,
            entry.compressed_size,
            entry.size,
            entry.raw_name,
        )
        if local_signature != b"PK\x03\x04" or extra_length or local_tuple != central_tuple:
            reject("VENDOR_ARCHIVE_UNSAFE", "ZIP local/central header mismatch")
        content = _inflate_raw(data[payload_start:payload_end], entry.size, MAX_SINGLE_FILE, entry.path)
        if binascii.crc32(content) & 0xFFFFFFFF != entry.crc32:
            reject("VENDOR_ARCHIVE_UNSAFE", f"{entry.path}: ZIP CRC32 mismatch")
        expanded += len(content)
        if expanded > MAX_EXPANDED_BYTES or len(members) + 1 > MAX_EXPANDED_FILES:
            reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "ZIP expanded aggregate cap")
        members.append(Member(entry.path, entry.raw_name.decode("ascii"), content, entry.external_attr >> 16))
        transcript.append(
            {
                "local_offset": local_cursor,
                "path": entry.path,
                "local_header_sha256": sha256(data[local_cursor:payload_start]),
                "compressed_sha256": sha256(data[payload_start:payload_end]),
                "payload_sha256": sha256(content),
            }
        )
        local_cursor = payload_end
    if local_cursor != central_offset:
        reject("VENDOR_ARCHIVE_UNSAFE", "hidden bytes before ZIP central directory")
    return members, _record_root("sana.e14.wheel.physical-zip.v1", transcript)


def _verify_wheel_record(files: dict[str, bytes]) -> None:
    record_path = "rfc8785-0.1.4.dist-info/RECORD"
    try:
        rows = list(csv.reader(io.StringIO(files[record_path].decode("utf-8", "strict"), newline="")))
    except (UnicodeDecodeError, csv.Error) as exc:
        reject("VENDOR_RECORD_INVALID", str(exc))
    if len(rows) != len(files):
        reject("VENDOR_RECORD_INVALID", "RECORD row count")
    seen: set[str] = set()
    for row in rows:
        if len(row) != 3:
            reject("VENDOR_RECORD_INVALID", "RECORD row width")
        path, digest_field, size_field = row
        if path in seen or path not in files:
            reject("VENDOR_RECORD_INVALID", f"RECORD path {path!r}")
        seen.add(path)
        if path == record_path:
            if digest_field or size_field:
                reject("VENDOR_RECORD_INVALID", "RECORD self row must be unhashed")
            continue
        expected_digest = base64.urlsafe_b64encode(hashlib.sha256(files[path]).digest()).rstrip(b"=").decode()
        if digest_field != "sha256=" + expected_digest or size_field != str(len(files[path])):
            reject("VENDOR_RECORD_INVALID", f"RECORD digest/size mismatch for {path}")
    if seen != set(files):
        reject("VENDOR_RECORD_INVALID", "RECORD coverage mismatch")


def _python_source_closure(files: dict[str, bytes]) -> dict[str, Any]:
    references: list[dict[str, str]] = []
    for path in sorted(name for name in files if name.endswith(".py")):
        try:
            tree = ast.parse(files[path].decode("utf-8", "strict"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            reject("RUNTIME_CLOSURE_INCOMPLETE", f"{path}: {exc}")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root not in PYTHON_STDLIB_ALLOWLIST:
                        reject("VENDOR_DEPENDENCY_UNEXPECTED", f"{path}: import {alias.name}")
                    references.append({"source": path, "kind": "stdlib-import", "target": alias.name})
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    package_dir = posixpath.dirname(path)
                    ascend = node.level - 1
                    for _ in range(ascend):
                        package_dir = posixpath.dirname(package_dir)
                    module = node.module or ""
                    target_base = posixpath.normpath(posixpath.join(package_dir, module.replace(".", "/")))
                    candidates = {target_base + ".py", target_base + "/__init__.py"}
                    resolved = sorted(candidates.intersection(files))
                    if len(resolved) != 1:
                        reject("RUNTIME_REFERENCE_UNRESOLVED", f"{path}: relative import {node.module!r}")
                    references.append({"source": path, "kind": "relative-import", "target": resolved[0]})
                else:
                    module = node.module or ""
                    root = module.split(".", 1)[0]
                    if root not in PYTHON_STDLIB_ALLOWLIST:
                        reject("VENDOR_DEPENDENCY_UNEXPECTED", f"{path}: from {module}")
                    references.append({"source": path, "kind": "stdlib-from", "target": module})
            elif isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else None
                if name in {"__import__", "eval", "exec", "compile"}:
                    reject("RUNTIME_DYNAMIC_LOAD_PROHIBITED", f"{path}: call to {name}")
    return {
        "analyzer": "python-ast-v1",
        "runtime_boundary": "image-bound CPython 3.12.x interpreter plus exact standard-library allowlist",
        "external_allowlist": sorted(PYTHON_STDLIB_ALLOWLIST),
        "references": references,
        "dynamic_loading": "ABSENT_BY_AST_SCAN",
        "structural_coverage": "COMPLETE_FOR_FROZEN_SOURCE_ROOT",
        "semantic_completeness": False,
        "semantic_attestation_required": True,
    }


def scan_python_wheel(data: bytes, registry_metadata: bytes | None = None) -> ArchiveScan:
    if len(data) > MAX_INPUT_BYTES:
        reject("VENDOR_ARCHIVE_CAP_EXCEEDED", "wheel input cap")
    raw_hash = sha256(data)
    if raw_hash != PYTHON_WHEEL_SHA256:
        reject("VENDOR_ARCHIVE_HASH_MISMATCH", f"wheel {raw_hash}")
    members, physical_root = _scan_zip_physical(data)
    _check_exact_inventory(members, PYTHON_FILES, "wheel")
    files = _member_map(members)
    _verify_wheel_record(files)
    metadata = BytesParser(policy=email_policy.default).parsebytes(
        files["rfc8785-0.1.4.dist-info/METADATA"]
    )
    if metadata.get("Name") != "rfc8785" or metadata.get("Version") != "0.1.4":
        reject("VENDOR_PACKAGE_IDENTITY_MISMATCH", "wheel METADATA name/version")
    classifiers = metadata.get_all("Classifier", [])
    if "License :: OSI Approved :: Apache Software License" not in classifiers:
        reject("VENDOR_LICENSE_MISMATCH", "wheel Apache classifier")
    if sha256(files["rfc8785-0.1.4.dist-info/LICENSE"]) != PYTHON_LICENSE_SHA256:
        reject("VENDOR_LICENSE_MISMATCH", "wheel LICENSE bytes")
    extras = set(metadata.get_all("Provides-Extra", []))
    requires_dist = metadata.get_all("Requires-Dist", [])
    extra_requirements: list[dict[str, str]] = []
    marker_pattern = re.compile(r'^(.+);\s*extra\s*==\s*"([A-Za-z0-9_.-]+)"$')
    for requirement in requires_dist:
        match = marker_pattern.fullmatch(requirement)
        if not match or match.group(2) not in extras:
            reject("VENDOR_DEPENDENCY_UNEXPECTED", f"wheel Requires-Dist {requirement!r}")
        extra_requirements.append({"requirement": match.group(1), "extra": match.group(2)})
    wheel_metadata = BytesParser(policy=email_policy.default).parsebytes(
        files["rfc8785-0.1.4.dist-info/WHEEL"]
    )
    if wheel_metadata.get("Root-Is-Purelib") != "true":
        reject("VENDOR_METADATA_INVALID", "wheel is not purelib")
    if wheel_metadata.get_all("Tag", []) != ["py3-none-any"]:
        reject("VENDOR_METADATA_INVALID", "wheel tag")
    if registry_metadata is not None:
        registry = _json_no_duplicates(registry_metadata, "PyPI registry metadata")
        info = registry.get("info", {})
        if info.get("name") != "rfc8785" or info.get("version") != "0.1.4":
            reject("VENDOR_PACKAGE_IDENTITY_MISMATCH", "PyPI name/version")
        matching = [
            item
            for item in registry.get("urls", [])
            if item.get("filename") == "rfc8785-0.1.4-py3-none-any.whl"
        ]
        if len(matching) != 1:
            reject("VENDOR_METADATA_INVALID", "PyPI wheel record")
        item = matching[0]
        if item.get("size") != len(data) or str(item.get("digests", {}).get("sha256", "")).upper() != raw_hash:
            reject("VENDOR_ARCHIVE_HASH_MISMATCH", "PyPI wheel size/hash")
    package = {
        "name": "rfc8785",
        "version": "0.1.4",
        "license_decision": "Apache-2.0",
        "license_basis": "exact LICENSE hash plus Apache classifier; registry SPDX field absent",
        "license_sha256": PYTHON_LICENSE_SHA256,
    }
    dependency = {
        "registry_runtime": [],
        "extras_not_installed": sorted(extras),
        "extra_requirements_not_installed": sorted(
            extra_requirements, key=lambda item: (item["extra"], item["requirement"])
        ),
        "entry_points": [],
        "install_hooks": [],
    }
    return ArchiveScan(
        "wheel",
        raw_hash,
        physical_root,
        members,
        package,
        dependency,
        _python_source_closure(files),
    )


def verify_a1_root(root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    terminal_path = root / "terminal-receipt.json"
    terminal_bytes = terminal_path.read_bytes()
    if sha256(terminal_bytes) != A1_TERMINAL_SHA256:
        reject("A1_SEAL_MISMATCH", "terminal receipt hash")
    terminal = _json_no_duplicates(terminal_bytes, "A1 terminal receipt")
    if terminal.get("state") != "ACQUISITION_COMPLETE_AWAITING_G1":
        reject("A1_SEAL_MISMATCH", "terminal state")
    inventory = terminal.get("inventory")
    if not isinstance(inventory, list) or len(inventory) + 1 != 20:
        reject("A1_SEAL_MISMATCH", "terminal inventory count")
    expected_paths: set[str] = {"terminal-receipt.json"}
    total_bytes = len(terminal_bytes)
    for entry in inventory:
        if not isinstance(entry, dict):
            reject("A1_SEAL_MISMATCH", "inventory entry type")
        path = entry.get("path")
        if not isinstance(path, str):
            reject("A1_SEAL_MISMATCH", "inventory path type")
        try:
            path_bytes = path.encode("ascii", "strict")
        except UnicodeEncodeError:
            reject("A1_SEAL_MISMATCH", f"non-ASCII inventory path {path!r}")
        normalized = normalize_member_path(path_bytes, strip_prefix=None)
        if normalized != path or path in expected_paths:
            reject("A1_SEAL_MISMATCH", f"inventory path {path!r}")
        candidate = (root / Path(*path.split("/"))).resolve(strict=True)
        try:
            candidate.relative_to(root)
        except ValueError:
            reject("A1_SEAL_MISMATCH", f"inventory escape {path!r}")
        if not candidate.is_file() or candidate.is_symlink():
            reject("A1_SEAL_MISMATCH", f"inventory non-regular {path!r}")
        content = candidate.read_bytes()
        if len(content) != entry.get("bytes") or sha256(content) != entry.get("sha256"):
            reject("A1_SEAL_MISMATCH", f"inventory bytes/hash {path!r}")
        expected_paths.add(path)
        total_bytes += len(content)
    physical_entries = list(root.rglob("*"))
    if any(path.is_symlink() for path in physical_entries):
        reject("A1_SEAL_MISMATCH", "symlink present in A1 root")
    actual_paths = {path.relative_to(root).as_posix() for path in physical_entries if path.is_file()}
    if actual_paths != expected_paths or len(actual_paths) > MAX_INPUT_FILES or total_bytes > MAX_INPUT_BYTES:
        reject("A1_SEAL_MISMATCH", "physical file set or cap")
    return {
        "root": str(root),
        "terminal_sha256": sha256(terminal_bytes),
        "file_count": len(actual_paths),
        "total_bytes": total_bytes,
        "terminal_state": terminal["state"],
    }


def prescan_acquisition(root: Path) -> dict[str, Any]:
    a1 = verify_a1_root(root)
    objects = root.resolve() / "objects"
    npm = scan_npm_tgz(
        (objects / "node-archive.body").read_bytes(),
        (objects / "node-metadata.body").read_bytes(),
    )
    wheel = scan_python_wheel(
        (objects / "python-wheel.body").read_bytes(),
        (objects / "python-metadata.body").read_bytes(),
    )
    package_reports = [npm.report(), wheel.report()]
    bundle_material = {
        "schema": "sana.e14.a2-read-only-prescan.v1",
        "a1_terminal_sha256": a1["terminal_sha256"],
        "packages": package_reports,
        "authority_effect": "NONE",
        "admission_state": "NOT_EXECUTED",
        "semantic_attestation": "REQUIRED",
    }
    bundle_root = sha256(canonical_json_bytes(bundle_material))
    return {
        **bundle_material,
        "a1": a1,
        "bundle_root": bundle_root,
        "next_gate": "G4_G5_EVIDENCE_ONLY",
    }


__all__ = [
    "AdmissionError",
    "ArchiveScan",
    "Member",
    "canonical_json_bytes",
    "normalize_member_path",
    "prescan_acquisition",
    "scan_npm_tgz",
    "scan_python_wheel",
    "sha256",
    "verify_a1_root",
]
