from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest import mock

from src.e14_n1_artifacts import (
    DOMAIN,
    MEDIA_TYPE,
    PROFILE_KIND,
    ROOT_PREFIX,
    SCHEMA,
    SELECTOR,
    LifecycleV2Route,
    N1ArtifactError,
    N1LifecycleV2Root,
    PAYLOAD_RULES,
    RevocationSnapshot,
    VerifiedLifecycleArtifactV2,
    _canonical_bytes,
    _parse_raw,
    evaluate_use,
    verify_content,
)
from tests.test_e14_n1_static_fixtures import valid_schema_examples
from tools.e14_n1_precode_audit import audit as run_precode_audit


ROOT = Path(__file__).resolve().parents[1]
ROUTE = LifecycleV2Route(selector=SELECTOR, media_type=MEDIA_TYPE)


def oracle_canonical(value: object) -> bytes:
    """Independent test oracle for the accepted ASCII-key/integer subset."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def oracle_root(envelope: dict) -> tuple[bytes, str]:
    commitment = {
        "schema": envelope["schema"],
        "artifact_kind": envelope["artifact_kind"],
        "profile_kind": envelope["profile_kind"],
        "payload": envelope["payload"],
    }
    canonical = oracle_canonical(commitment)
    return canonical, ROOT_PREFIX + hashlib.sha256(DOMAIN + canonical).hexdigest()


def issued(example: dict) -> dict:
    result = copy.deepcopy(example)
    _, result["content_root"] = oracle_root(result)
    return result


def wire(envelope: dict, *, indent: int | None = None) -> bytes:
    return json.dumps(envelope, ensure_ascii=False, separators=(",", ":"), indent=indent).encode(
        "utf-8"
    )


def assert_code(test: unittest.TestCase, code: str, callback) -> N1ArtifactError:
    with test.assertRaises(N1ArtifactError) as raised:
        callback()
    test.assertEqual(raised.exception.code, code)
    return raised.exception


class N1V2HappyPathTests(unittest.TestCase):
    def test_all_seven_kinds_verify_against_independent_oracle(self) -> None:
        for example in valid_schema_examples():
            artifact = issued(example)
            canonical, expected_root = oracle_root(artifact)
            with self.subTest(kind=artifact["artifact_kind"]):
                verified = verify_content(wire(artifact, indent=2), ROUTE)
                self.assertEqual(verified.content_root.value, expected_root)
                self.assertEqual(verified.commitment_bytes, canonical)
                self.assertEqual(verified.schema, SCHEMA)
                self.assertEqual(verified.profile_kind, PROFILE_KIND)

    def test_frozen_issuer_policy_golden_root(self) -> None:
        verified = verify_content(wire(issued(valid_schema_examples()[0])), ROUTE)
        self.assertEqual(
            verified.content_root.value,
            "sha256-jcs-e14-n1-v2:7f62ca076e77d70d475b1569efd4ffc5df5d781a494bdda79bdf34175f1a44c3",
        )

    def test_root_binds_payload_and_does_not_trust_presented_root(self) -> None:
        artifact = issued(valid_schema_examples()[0])
        artifact["payload"]["revocation_epoch"] = 2
        error = assert_code(
            self,
            "N1_CONTENT_ROOT_MISMATCH",
            lambda: verify_content(wire(artifact), ROUTE),
        )
        self.assertEqual(error.pointer, "/content_root")

    def test_reordered_and_escaped_input_has_same_commitment(self) -> None:
        artifact = issued(valid_schema_examples()[0])
        raw = wire(artifact).replace(b'"scope":"A2"', b'"scope":"\\u0041\\u0032"')
        verified = verify_content(raw, ROUTE)
        canonical, expected_root = oracle_root(artifact)
        self.assertEqual(verified.commitment_bytes, canonical)
        self.assertEqual(verified.content_root.value, expected_root)

    def test_verified_payload_is_immutable(self) -> None:
        verified = verify_content(wire(issued(valid_schema_examples()[0])), ROUTE)
        with self.assertRaises(TypeError):
            verified.payload["scope"] = "other"  # type: ignore[index]
        with self.assertRaises(TypeError):
            verified.payload["roles"]["policy_issuer"] = "other"  # type: ignore[index]

    def test_verified_nominal_types_cannot_be_forged_through_public_constructors(self) -> None:
        with self.assertRaises(TypeError):
            N1LifecycleV2Root(ROOT_PREFIX + "0" * 64)
        with self.assertRaises(TypeError):
            VerifiedLifecycleArtifactV2(
                schema=SCHEMA,
                artifact_kind="N1_ISSUER_POLICY",
                profile_kind=PROFILE_KIND,
                content_root=None,  # type: ignore[arg-type]
                payload={},
                commitment_bytes=b"{}",
            )

    def test_restricted_canonicalizer_matches_independent_oracle_for_unicode(self) -> None:
        values = (
            {"a": "é", "b": "e\u0301", "c": " ", "d": "\b\t\n\f\r"},
            {"ascii": "😀", "integer": -9007199254740991, "null": None},
            {"z": {"b": False, "a": True}, "a": "slash/quote\"backslash\\"},
        )
        for value in values:
            with self.subTest(value=value):
                self.assertEqual(_canonical_bytes(value), oracle_canonical(value))
        self.assertNotEqual(_canonical_bytes({"x": "é"}), _canonical_bytes({"x": "e\u0301"}))

    def test_surrogate_pair_input_decodes_to_one_preserved_scalar(self) -> None:
        parsed = _parse_raw(b'{"x":"\\uD83D\\uDE00"}')
        self.assertEqual(parsed, {"x": "😀"})
        self.assertEqual(_canonical_bytes(parsed), '{"x":"😀"}'.encode("utf-8"))


class N1V2SchemaParityTests(unittest.TestCase):
    _DEFS_BY_KIND = {
        "N1_ISSUER_POLICY": "issuerPolicyPayload",
        "N1_PROFILE_QUALIFIED": "profileQualifiedPayload",
        "N1_OUTPUT_RESERVED": "outputReservedPayload",
        "N1_CONTAINER_PREPARED": "containerPreparedPayload",
        "G8_N1_RUN_AUTHORIZED": "runAuthorizedPayload",
        "N1_RUN_EVIDENCE_CANDIDATE": "runEvidencePayload",
        "G9_N1_TERMINAL": "terminalPayload",
    }

    def test_embedded_payload_field_contracts_match_frozen_schema(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "e14-a2-n1-lifecycle-v2.schema.json").read_text(
                encoding="utf-8"
            )
        )
        for kind, definition in self._DEFS_BY_KIND.items():
            embedded_fields = [name for name, _ in PAYLOAD_RULES[kind][1]]
            schema_node = schema["$defs"][definition]
            with self.subTest(kind=kind):
                self.assertEqual(embedded_fields, schema_node["required"])
                self.assertEqual(set(embedded_fields), set(schema_node["properties"]))
                self.assertFalse(schema_node["additionalProperties"])

    def test_every_payload_rejects_missing_extra_and_wrong_typed_fields(self) -> None:
        for example in valid_schema_examples():
            kind = example["artifact_kind"]
            for field, value in tuple(example["payload"].items()):
                missing = copy.deepcopy(example)
                del missing["payload"][field]
                with self.subTest(kind=kind, mutation=f"missing:{field}"):
                    error = assert_code(
                        self,
                        "N1_PAYLOAD_INVALID",
                        lambda missing=missing: verify_content(wire(missing), ROUTE),
                    )
                    self.assertEqual(error.pointer, f"/payload/{field}")

                wrong_type = copy.deepcopy(example)
                wrong_type["payload"][field] = (
                    "wrong" if type(value) is not str else {"wrong": "type"}
                )
                with self.subTest(kind=kind, mutation=f"type:{field}"):
                    assert_code(
                        self,
                        "N1_PAYLOAD_INVALID",
                        lambda wrong_type=wrong_type: verify_content(wire(wrong_type), ROUTE),
                    )

            extra = copy.deepcopy(example)
            extra["payload"]["zzz_unknown"] = 0
            with self.subTest(kind=kind, mutation="extra"):
                error = assert_code(
                    self,
                    "N1_PAYLOAD_INVALID",
                    lambda extra=extra: verify_content(wire(extra), ROUTE),
                )
                self.assertEqual(error.pointer, "/payload/zzz_unknown")


class N1V2RouteAndSemanticFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = issued(valid_schema_examples()[0])

    def test_route_failures_precede_malformed_json(self) -> None:
        assert_code(self, "N1_ROUTE_SELECTOR_MISSING", lambda: verify_content(b"{", None))
        bad_selector = LifecycleV2Route(selector="OTHER", media_type=MEDIA_TYPE)
        assert_code(
            self,
            "N1_ROUTE_SELECTOR_UNSUPPORTED",
            lambda: verify_content(b"{", bad_selector),
        )
        bad_media = LifecycleV2Route(selector=SELECTOR, media_type="application/json")
        assert_code(
            self,
            "N1_ROUTE_MEDIA_TYPE_MISMATCH",
            lambda: verify_content(b"{", bad_media),
        )

    def test_v1_is_rejected_without_conversion(self) -> None:
        old = copy.deepcopy(self.artifact)
        old["schema"] = "sana.e14.n1.lifecycle-artifact." + "v1"
        old["content_root"] = "sha256-jcs-e14-n1-" + "v1:" + "a" * 64
        assert_code(self, "N1_SCHEMA_UNSUPPORTED", lambda: verify_content(wire(old), ROUTE))

    def test_wrong_profile_and_kind_are_nominal_failures(self) -> None:
        wrong_profile = copy.deepcopy(self.artifact)
        wrong_profile["profile_kind"] = "P3_N1_OTHER"
        assert_code(
            self,
            "N1_PROFILE_KIND_MISMATCH",
            lambda: verify_content(wire(wrong_profile), ROUTE),
        )
        wrong_kind = copy.deepcopy(self.artifact)
        wrong_kind["artifact_kind"] = "N1_UNKNOWN"
        assert_code(
            self,
            "N1_ARTIFACT_KIND_UNSUPPORTED",
            lambda: verify_content(wire(wrong_kind), ROUTE),
        )

    def test_extra_and_removed_draft_fields_are_rejected(self) -> None:
        for field, value in (("extra", 1), ("fixture_only", False), ("authority_effect", "NONE")):
            bad = copy.deepcopy(self.artifact)
            bad[field] = value
            with self.subTest(field=field):
                error = assert_code(
                    self,
                    "N1_ENVELOPE_FIELD_SET",
                    lambda bad=bad: verify_content(wire(bad), ROUTE),
                )
                self.assertEqual(error.pointer, f"/{field}")

    def test_payload_unknown_field_and_wrong_constant_are_rejected(self) -> None:
        extra = copy.deepcopy(self.artifact)
        extra["payload"]["zzz"] = 1
        error = assert_code(
            self, "N1_PAYLOAD_INVALID", lambda: verify_content(wire(extra), ROUTE)
        )
        self.assertEqual(error.pointer, "/payload/zzz")

        wrong = copy.deepcopy(self.artifact)
        wrong["payload"]["scope"] = "A3"
        error = assert_code(
            self, "N1_PAYLOAD_INVALID", lambda: verify_content(wire(wrong), ROUTE)
        )
        self.assertEqual(error.pointer, "/payload/scope")

    def test_content_root_format_precedes_root_comparison(self) -> None:
        self.artifact["content_root"] = "not-a-root"
        assert_code(
            self,
            "N1_CONTENT_ROOT_FORMAT",
            lambda: verify_content(wire(self.artifact), ROUTE),
        )


class N1V2RawParserTests(unittest.TestCase):
    def test_raw_size_bom_utf8_and_trailing_data(self) -> None:
        exact_raw = assert_code(
            self, "N1_JSON_SYNTAX", lambda: verify_content(b" " * 262144, ROUTE)
        )
        self.assertEqual(exact_raw.byte_offset, 262144)
        assert_code(self, "N1_RAW_TOO_LARGE", lambda: verify_content(b" " * 262145, ROUTE))
        assert_code(self, "N1_JSON_BOM", lambda: verify_content(b"\xef\xbb\xbf{}", ROUTE))
        invalid = assert_code(
            self, "N1_JSON_INVALID_UTF8", lambda: verify_content(b'{"x":"\xff"}', ROUTE)
        )
        self.assertEqual(invalid.byte_offset, 6)
        invalid_trailing = assert_code(
            self, "N1_JSON_INVALID_UTF8", lambda: verify_content(b"{}\xff", ROUTE)
        )
        self.assertEqual(invalid_trailing.byte_offset, 2)
        trailing = assert_code(
            self, "N1_JSON_TRAILING_DATA", lambda: verify_content(b"{} {}", ROUTE)
        )
        self.assertEqual(trailing.byte_offset, 3)

    def test_duplicate_keys_use_decoded_identity_and_second_key_offset(self) -> None:
        raw = b'{"schema":1,"\\u0073chema":2}'
        error = assert_code(self, "N1_JSON_DUPLICATE_KEY", lambda: verify_content(raw, ROUTE))
        self.assertEqual(error.byte_offset, 12)

    def test_arrays_numbers_and_surrogates_are_rejected_during_parse(self) -> None:
        assert_code(self, "N1_JSON_ARRAY_FORBIDDEN", lambda: verify_content(b'{"x":[]}', ROUTE))
        for token, decisive_delta in ((b"1.0", 1), (b"1e0", 1), (b"-0", 1), (b"01", 1)):
            with self.subTest(token=token):
                error = assert_code(
                    self,
                    "N1_JSON_NUMBER_FORBIDDEN",
                    lambda token=token: verify_content(b'{"x":' + token + b"}", ROUTE),
                )
                self.assertEqual(error.byte_offset, 5 + decisive_delta)
        range_error = assert_code(
            self,
            "N1_JSON_INTEGER_RANGE",
            lambda: verify_content(b'{"x":9007199254740992}', ROUTE),
        )
        self.assertEqual(range_error.byte_offset, 20)
        for escaped in (b"\\uD800", b"\\uDC00", b"\\uD800x"):
            with self.subTest(escaped=escaped):
                assert_code(
                    self,
                    "N1_JSON_SURROGATE_INVALID",
                    lambda escaped=escaped: verify_content(b'{"x":"' + escaped + b'"}', ROUTE),
                )

    def test_depth_object_member_total_member_and_string_limits(self) -> None:
        at_depth = b"{}"
        for _ in range(11):
            at_depth = b'{"x":' + at_depth + b"}"
        assert_code(self, "N1_ENVELOPE_FIELD_SET", lambda: verify_content(at_depth, ROUTE))

        nested = b"{}"
        for _ in range(12):
            nested = b'{"x":' + nested + b"}"
        assert_code(self, "N1_JSON_DEPTH_LIMIT", lambda: verify_content(nested, ROUTE))

        too_many = {f"k{i}": 0 for i in range(129)}
        assert_code(
            self,
            "N1_JSON_OBJECT_MEMBER_LIMIT",
            lambda: verify_content(wire(too_many), ROUTE),
        )

        exact_object = {f"k{i}": 0 for i in range(128)}
        assert_code(
            self,
            "N1_ENVELOPE_FIELD_SET",
            lambda: verify_content(wire(exact_object), ROUTE),
        )

        exact_members = {f"k{i}": {f"v{j}": 0 for j in range(16)} for i in range(119)}
        exact_members["k119"] = {f"v{j}": 0 for j in range(24)}
        assert_code(
            self,
            "N1_ENVELOPE_FIELD_SET",
            lambda: verify_content(wire(exact_members), ROUTE),
        )
        one_over_members = copy.deepcopy(exact_members)
        one_over_members["k119"]["v24"] = 0
        assert_code(
            self,
            "N1_JSON_MEMBER_LIMIT",
            lambda: verify_content(wire(one_over_members), ROUTE),
        )

        broad = {f"k{i}": {f"v{j}": 0 for j in range(16)} for i in range(128)}
        assert_code(
            self,
            "N1_JSON_MEMBER_LIMIT",
            lambda: verify_content(wire(broad), ROUTE),
        )

        assert_code(
            self,
            "N1_JSON_STRING_SCALAR_LIMIT",
            lambda: verify_content(wire({"x": "a" * 1025}), ROUTE),
        )
        assert_code(
            self,
            "N1_ENVELOPE_FIELD_SET",
            lambda: verify_content(wire({"x": "😀" * 1024}), ROUTE),
        )

    def test_key_boundaries_are_measured_after_unescaping(self) -> None:
        qualified = issued(valid_schema_examples()[1])
        qualified["payload"]["closure_roots"] = {
            "a" * 159 + f"{index:x}"[-1]: qualified["content_root"] for index in range(16)
        }
        qualified["payload"]["closure_roots"].update(
            {f"b{index:03d}": qualified["content_root"] for index in range(112)}
        )
        self.assertEqual(len(qualified["payload"]["closure_roots"]), 128)
        qualified = issued(qualified)
        verify_content(wire(qualified), ROUTE)

        raw = wire({"a" * 161: 0})
        assert_code(self, "N1_JSON_KEY_TOO_LONG", lambda: verify_content(raw, ROUTE))
        assert_code(
            self,
            "N1_JSON_KEY_NON_ASCII",
            lambda: verify_content('{"é":0}'.encode("utf-8"), ROUTE),
        )


class N1V2UseEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.qualified = verify_content(wire(issued(valid_schema_examples()[1])), ROUTE)

    def test_explicit_time_boundaries(self) -> None:
        empty = RevocationSnapshot()
        self.assertEqual(
            evaluate_use(self.qualified, "2026-08-26T23:59:59Z", empty).status,
            "N1_USE_NOT_YET_VALID",
        )
        self.assertEqual(
            evaluate_use(self.qualified, "2026-08-27T00:00:00Z", empty).status,
            "N1_USE_VALID",
        )
        self.assertEqual(
            evaluate_use(self.qualified, "2026-08-27T01:00:00Z", empty).status,
            "N1_USE_EXPIRED",
        )

    def test_explicit_root_and_epoch_revocation(self) -> None:
        by_root = RevocationSnapshot(revoked_content_roots=frozenset({self.qualified.content_root.value}))
        self.assertEqual(
            evaluate_use(self.qualified, "2026-08-27T00:00:00Z", by_root).status,
            "N1_USE_REVOKED",
        )
        policy_root = self.qualified.payload["issuer_policy_root"]
        by_epoch = RevocationSnapshot(minimum_epoch_by_policy=((policy_root, 2),))
        self.assertEqual(
            evaluate_use(self.qualified, "2026-08-27T00:00:00Z", by_epoch).status,
            "N1_USE_REVOKED",
        )

    def test_invalid_explicit_time_is_not_read_from_clock(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_use(self.qualified, "now", RevocationSnapshot())


class N1V2PurityAndInventoryTests(unittest.TestCase):
    def test_precode_cap_report_is_reproducible_from_frozen_schema(self) -> None:
        report_path = ROOT / "evidence" / "e14-n1-v2-precode-cap-report-v1.json"
        persisted = json.loads(report_path.read_text(encoding="utf-8"))
        generated = run_precode_audit(
            ROOT / "schemas" / "e14-a2-n1-lifecycle-v2.schema.json"
        )
        for key in (
            "artifacts",
            "caps",
            "checks",
            "counting_profile",
            "maxima",
            "schema",
            "schema_path",
            "status",
        ):
            with self.subTest(key=key):
                self.assertEqual(persisted[key], generated[key])

    def test_verify_and_evaluate_do_not_touch_ambient_io_or_clock(self) -> None:
        raw = wire(issued(valid_schema_examples()[1]))
        with (
            mock.patch("builtins.open", side_effect=AssertionError("filesystem access")),
            mock.patch("socket.socket", side_effect=AssertionError("network access")),
            mock.patch("os.getenv", side_effect=AssertionError("environment access")),
            mock.patch("time.time", side_effect=AssertionError("clock access")),
        ):
            verified = verify_content(raw, ROUTE)
            result = evaluate_use(verified, "2026-08-27T00:00:00Z", RevocationSnapshot())
        self.assertEqual(result.status, "N1_USE_VALID")

    def test_v1_references_are_confined_to_historical_audit_files(self) -> None:
        allowed = {
            ROOT / "evidence" / "e14-n1-draft-v1-retirement-v1.json",
            ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-08-27-p6-p3-1-e14-a2-n1-i0-hash-envelope-correction-debate.md",
        }
        needles = (
            "lifecycle-" + "v1",
            "lifecycle-artifact." + "v1",
            "sha256-jcs-e14-n1-" + "v1",
            "N1_LIFECYCLE_ARTIFACT_" + "V1",
        )
        offenders: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path in allowed:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if any(needle in text for needle in needles):
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
