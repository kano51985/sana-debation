from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import socket
import unittest
from unittest import mock

from src.e14_c1a_er_a3_min import (
    MAX_RAW_BYTES,
    PROFILE,
    SCHEMA,
    ERA3MinError,
    VerifiedERA3MinPackageV1,
    verify_package,
)


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = (
    "docs/superpowers/specs/"
    "2026-08-27-p6-p3-1-e14-a2-n1-c1a-acquisition-architecture-spec.md"
)


def source_span(path: str = SPEC_PATH, digest: str = "A" * 64) -> dict:
    return {"path": path, "sha256": digest, "start_line": 1, "end_line": 2}


def domain(kind: str) -> dict:
    if kind == "STRING_ENUM":
        return {"kind": kind, "values": ["SYNTHETIC_OPTION"]}
    if kind == "INTEGER_RANGE":
        return {"kind": kind, "minimum": 0, "maximum": 3}
    if kind == "BOOLEAN":
        return {"kind": kind}
    if kind == "OBJECT_SCHEMA_REF":
        return {
            "kind": kind,
            "schema_id": "SYNTHETIC_OBJECT_SCHEMA.v1",
            "schema_version": "v1",
            "schema_sha256": "B" * 64,
        }
    raise AssertionError(kind)


def anchor(alias: str, wire_name: str, field_id: str, kind: str) -> dict:
    json_type = {
        "STRING_ENUM": "STRING",
        "INTEGER_RANGE": "INTEGER",
        "BOOLEAN": "BOOLEAN",
        "OBJECT_SCHEMA_REF": "OBJECT",
    }[kind]
    legal_domain = domain(kind)
    return {
        "alias": alias,
        "canonical_field_id": field_id,
        "semantic_class": "MIXED",
        "meaning": "Synthetic test-only meaning; not evidence.",
        "fact_preference_boundary": "Synthetic fact/preference split used only by tests.",
        "accountable_source": {
            "source_id": f"SYNTHETIC_{alias}_SOURCE.v1",
            "authority_status": "ACCOUNTABLE_SOURCE_IDENTIFIED",
            "authority_scope": "Synthetic contract test only.",
            "spans": [source_span()],
            "limitations": ["This fixture does not establish source truth or authority."],
        },
        "field_schema": {
            "schema_version": "v1",
            "wire_name": wire_name,
            "json_type": json_type,
            "required": True,
            "default_behavior": "NO_DEFAULT",
            "legal_domain": copy.deepcopy(legal_domain),
        },
        "reader_contract": {
            "reader_id": f"SYNTHETIC_{alias}_READER.v1",
            "reader_version": "v1",
            "consumes_schema_version": "v1",
            "wire_name": wire_name,
            "json_type": json_type,
            "required": True,
            "default_behavior": "NO_DEFAULT",
            "legal_domain": copy.deepcopy(legal_domain),
            "unknown_input_behavior": "REJECT",
            "interpretation": "Synthetic interpretation used only to test parity.",
        },
    }


def valid_package() -> dict:
    return {
        "schema": SCHEMA,
        "profile": PROFILE,
        "candidate": "A",
        "source_spec": {
            "path": SPEC_PATH,
            "sha256": "A" * 64,
            "declared_version": "2026-08-27",
            "status": "SPECIFICATION_ONLY",
            "authority_effect": "NONE",
        },
        "anchors": [
            anchor("A1", "synthetic_acquisition_field", "C1A_SYNTHETIC_ACQUISITION_FIELD.v1", "STRING_ENUM"),
            anchor("H1", "synthetic_http_field", "C1A_SYNTHETIC_HTTP_FIELD.v1", "BOOLEAN"),
        ],
        "canonical_profile": {
            "alias": "J1",
            "profile_id": "RFC8785_JCS_IJSON_V1",
            "scope": "SERIALIZATION_ONLY",
            "source_spans": [
                source_span(
                    "e14/vendor-acquisition-v2/objects/rfc8785-text.body",
                    "63D52294EB0E3F0014174288186D388B4DDBF2C67D1CE8AF1D9726EB0C3AB240",
                )
            ],
        },
        "compatibility": "UNASSESSED",
        "authority_effect": "NONE",
        "next_stage_authorized": False,
        "limitations": ["Synthetic valid shape; no semantic or authority claim."],
    }


def wire(package: dict) -> bytes:
    return json.dumps(package, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def assert_code(test: unittest.TestCase, code: str, callback) -> ERA3MinError:
    with test.assertRaises(ERA3MinError) as raised:
        callback()
    test.assertEqual(raised.exception.code, code)
    return raised.exception


class ERA3MinHappyPathTests(unittest.TestCase):
    def test_valid_package_returns_nominal_non_authorizing_result(self) -> None:
        raw = wire(valid_package())
        verified = verify_package(raw)
        self.assertEqual(verified.raw_sha256, hashlib.sha256(raw).hexdigest().upper())
        self.assertEqual(verified.package_shape, "VALID")
        self.assertEqual(verified.declared_schema_reader_parity, "MATCHED")
        self.assertEqual(verified.source_truth, "NOT_PROVEN_BY_VALIDATOR")
        self.assertEqual(verified.source_authority, "NOT_PROVEN_BY_VALIDATOR")
        self.assertEqual(verified.compatibility, "UNASSESSED")
        self.assertEqual(verified.authority_effect, "NONE")
        self.assertFalse(verified.next_stage_authorized)

    def test_all_four_domain_forms_are_accepted_when_schema_and_reader_match(self) -> None:
        for kind in ("STRING_ENUM", "INTEGER_RANGE", "BOOLEAN", "OBJECT_SCHEMA_REF"):
            package = valid_package()
            package["anchors"][0] = anchor(
                "A1", "synthetic_acquisition_field", "C1A_SYNTHETIC_ACQUISITION_FIELD.v1", kind
            )
            with self.subTest(kind=kind):
                verify_package(wire(package))

    def test_anchor_order_is_not_semantic(self) -> None:
        package = valid_package()
        package["anchors"].reverse()
        verify_package(wire(package))

    def test_verified_payload_is_deeply_immutable(self) -> None:
        verified = verify_package(wire(valid_package()))
        with self.assertRaises(TypeError):
            verified.payload["candidate"] = "B"  # type: ignore[index]
        with self.assertRaises(TypeError):
            verified.payload["anchors"][0]["alias"] = "H1"  # type: ignore[index]

    def test_nominal_result_cannot_be_directly_constructed(self) -> None:
        with self.assertRaises(TypeError):
            VerifiedERA3MinPackageV1({}, "0" * 64, _token=None)  # type: ignore[arg-type]


class ERA3MinRawAndEnvelopeFailureTests(unittest.TestCase):
    def test_raw_failures(self) -> None:
        assert_code(self, "ER_A3_RAW_TOO_LARGE", lambda: verify_package(b" " * (MAX_RAW_BYTES + 1)))
        assert_code(self, "ER_A3_JSON_BOM", lambda: verify_package(b"\xef\xbb\xbf{}"))
        assert_code(self, "ER_A3_JSON_INVALID_UTF8", lambda: verify_package(b'{"x":"\xff"}'))
        assert_code(self, "ER_A3_JSON_INVALID", lambda: verify_package(b"{"))
        assert_code(
            self,
            "ER_A3_JSON_DUPLICATE_KEY",
            lambda: verify_package(b'{"schema":1,"schema":2}'),
        )

    def test_exact_top_level_field_set(self) -> None:
        for mutation in ("missing", "extra"):
            package = valid_package()
            if mutation == "missing":
                del package["limitations"]
            else:
                package["extra"] = None
            with self.subTest(mutation=mutation):
                assert_code(
                    self, "ER_A3_PACKAGE_FIELD_SET", lambda package=package: verify_package(wire(package))
                )

    def test_discriminators_fail_nominally(self) -> None:
        mutations = (
            ("schema", "other", "ER_A3_SCHEMA_UNSUPPORTED"),
            ("profile", "other", "ER_A3_PROFILE_UNSUPPORTED"),
            ("candidate", "B", "ER_A3_CANDIDATE_UNSUPPORTED"),
        )
        for field, value, code in mutations:
            package = valid_package()
            package[field] = value
            with self.subTest(field=field):
                assert_code(self, code, lambda package=package: verify_package(wire(package)))

    def test_authority_and_compatibility_cannot_be_promoted(self) -> None:
        mutations = (
            ("authority_effect", "GRANT", "ER_A3_PACKAGE_INVALID"),
            ("compatibility", "PASS", "ER_A3_PACKAGE_INVALID"),
            ("next_stage_authorized", True, "ER_A3_PACKAGE_INVALID"),
        )
        for field, value, code in mutations:
            package = valid_package()
            package[field] = value
            with self.subTest(field=field):
                assert_code(self, code, lambda package=package: verify_package(wire(package)))


class ERA3MinAnchorAndSourceFailureTests(unittest.TestCase):
    def test_exact_alias_set_and_collision_free_names(self) -> None:
        mutations = []
        duplicate_alias = valid_package()
        duplicate_alias["anchors"][1]["alias"] = "A1"
        mutations.append(duplicate_alias)
        alias_as_field = valid_package()
        alias_as_field["anchors"][0]["canonical_field_id"] = "A1"
        mutations.append(alias_as_field)
        duplicate_field = valid_package()
        duplicate_field["anchors"][1]["canonical_field_id"] = duplicate_field["anchors"][0][
            "canonical_field_id"
        ]
        mutations.append(duplicate_field)
        duplicate_wire = valid_package()
        duplicate_wire["anchors"][1]["field_schema"]["wire_name"] = duplicate_wire["anchors"][0][
            "field_schema"
        ]["wire_name"]
        duplicate_wire["anchors"][1]["reader_contract"]["wire_name"] = duplicate_wire["anchors"][0][
            "reader_contract"
        ]["wire_name"]
        mutations.append(duplicate_wire)
        for index, package in enumerate(mutations):
            with self.subTest(index=index):
                assert_code(
                    self, "ER_A3_ANCHOR_SET_INVALID", lambda package=package: verify_package(wire(package))
                )

    def test_source_path_digest_span_and_authority_are_strict(self) -> None:
        mutations = (
            ("source_spec_path", "../outside"),
            ("span_digest", "a" * 64),
            ("span_order", 0),
            ("authority_status", "SELF_ASSERTED"),
        )
        for mutation, value in mutations:
            package = valid_package()
            if mutation == "source_spec_path":
                package["source_spec"]["path"] = value
            elif mutation == "span_digest":
                package["anchors"][0]["accountable_source"]["spans"][0]["sha256"] = value
            elif mutation == "span_order":
                package["anchors"][0]["accountable_source"]["spans"][0]["end_line"] = value
            else:
                package["anchors"][0]["accountable_source"]["authority_status"] = value
            with self.subTest(mutation=mutation):
                assert_code(self, "ER_A3_SOURCE_INVALID", lambda package=package: verify_package(wire(package)))

    def test_source_declarations_are_not_resolved_from_filesystem(self) -> None:
        package = valid_package()
        package["source_spec"]["path"] = "does/not/exist.md"
        with mock.patch("builtins.open", side_effect=AssertionError("filesystem access")) as opened:
            verified = verify_package(wire(package))
        opened.assert_not_called()
        self.assertEqual(verified.source_truth, "NOT_PROVEN_BY_VALIDATOR")


class ERA3MinParityFailureTests(unittest.TestCase):
    def test_schema_reader_version_wire_type_required_and_domain_must_match(self) -> None:
        mutations = ("version", "wire", "type", "required", "domain")
        for mutation in mutations:
            package = valid_package()
            reader = package["anchors"][0]["reader_contract"]
            if mutation == "version":
                reader["consumes_schema_version"] = "v2"
            elif mutation == "wire":
                reader["wire_name"] = "different_name"
            elif mutation == "type":
                reader["json_type"] = "BOOLEAN"
                reader["legal_domain"] = domain("BOOLEAN")
            elif mutation == "required":
                reader["required"] = False
            else:
                reader["legal_domain"] = {"kind": "STRING_ENUM", "values": ["DIFFERENT"]}
            with self.subTest(mutation=mutation):
                assert_code(
                    self,
                    "ER_A3_SCHEMA_READER_MISMATCH",
                    lambda package=package: verify_package(wire(package)),
                )

    def test_defaults_unknown_fallback_and_invalid_domain_are_rejected(self) -> None:
        mutations = ("field_default", "reader_default", "unknown_fallback", "domain_type")
        expected = (
            "ER_A3_FIELD_SCHEMA_INVALID",
            "ER_A3_READER_CONTRACT_INVALID",
            "ER_A3_READER_CONTRACT_INVALID",
            "ER_A3_FIELD_SCHEMA_INVALID",
        )
        for mutation, code in zip(mutations, expected, strict=True):
            package = valid_package()
            if mutation == "field_default":
                package["anchors"][0]["field_schema"]["default_behavior"] = "USE_ZERO"
            elif mutation == "reader_default":
                package["anchors"][0]["reader_contract"]["default_behavior"] = "USE_ZERO"
            elif mutation == "unknown_fallback":
                package["anchors"][0]["reader_contract"]["unknown_input_behavior"] = "IGNORE"
            else:
                package["anchors"][0]["field_schema"]["json_type"] = "INTEGER"
            with self.subTest(mutation=mutation):
                assert_code(self, code, lambda package=package: verify_package(wire(package)))


class ERA3MinSchemaAndPurityTests(unittest.TestCase):
    def test_json_schema_field_contract_matches_embedded_validator(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "e14-c1a-er-a3-min-v1.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(schema["properties"]["schema"]["const"], SCHEMA)
        self.assertEqual(schema["properties"]["profile"]["const"], PROFILE)
        self.assertEqual(
            set(schema["required"]),
            {
                "schema",
                "profile",
                "candidate",
                "source_spec",
                "anchors",
                "canonical_profile",
                "compatibility",
                "authority_effect",
                "next_stage_authorized",
                "limitations",
            },
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["$defs"]["anchor"]["properties"]["alias"]["enum"]), {"A1", "H1"})

    def test_verifier_has_no_network_or_filesystem_dependency(self) -> None:
        with (
            mock.patch("builtins.open", side_effect=AssertionError("filesystem access")) as opened,
            mock.patch.object(socket, "socket", side_effect=AssertionError("network access")) as sock,
        ):
            verify_package(wire(valid_package()))
        opened.assert_not_called()
        sock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
