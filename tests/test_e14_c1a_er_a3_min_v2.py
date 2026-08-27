from __future__ import annotations

import hashlib
import json
from pathlib import Path
import socket
import unittest
from unittest import mock

from jsonschema import Draft202012Validator

from src import e14_c1a_er_a3_min_v2 as v2_module
from src.e14_c1a_er_a3_min_v2 import (
    AUTHORITY_EFFECT,
    COMPATIBILITY,
    CONTRACT_STATUS,
    CUSTODY_SEMANTICS,
    FIXTURE_CLASSIFICATION,
    LINEAGE_RELATION,
    MAX_RAW_BYTES,
    PREFERENCE_CLASS,
    PROFILE_ID,
    PROFILE_VERSION,
    SERIALIZATION_SEMANTICS,
    V1_AUDIT_PURPOSE,
    V1_STATUS,
    V2_DESIGN_PURPOSE,
    CandidateAPreferenceProfileV1,
    ERA3V2Error,
    parse_candidate_a_preference_profile,
    resolve_contract,
    resolve_registered_source_instance,
    validate_v1_for_audit,
)
from tests.test_e14_c1a_er_a3_min import valid_package as valid_v1_package
from tests.test_e14_c1a_er_a3_min import wire as v1_wire


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "e14-c1a-er-a3-min-v2.schema.json"
CORPUS_PATH = ROOT / "fixtures" / "e14_c1a_er_a3_min_v2_cases.json"
LIFECYCLE_PATH = ROOT / "evidence" / "e14-c1a-er-a3-min-version-registry.json"


def assert_code(test: unittest.TestCase, code: str, callback) -> ERA3V2Error:
    with test.assertRaises(ERA3V2Error) as raised:
        callback()
    test.assertEqual(raised.exception.code, code)
    return raised.exception


def strict_json_for_schema(raw: bytes) -> object:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate key")
            value[key] = item
        return value

    def reject_float(token: str) -> object:
        raise ValueError(f"floating-point JSON number forbidden: {token}")

    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=no_duplicates,
        parse_float=reject_float,
    )


class ERA3MinV2ProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)
        cls.corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))

    def test_identical_serialized_corpus_has_schema_reader_parity(self) -> None:
        for case in self.corpus["cases"]:
            raw = case["wire"].encode("utf-8")
            try:
                parsed = strict_json_for_schema(raw)
            except (UnicodeError, json.JSONDecodeError, ValueError):
                schema_accepts = False
            else:
                schema_accepts = not tuple(self.validator.iter_errors(parsed))
            try:
                result = parse_candidate_a_preference_profile(raw)
            except ERA3V2Error:
                reader_accepts = False
                result = None
            else:
                reader_accepts = True
            expected = case["expected"] == "ACCEPT"
            with self.subTest(case=case["id"]):
                self.assertEqual(schema_accepts, expected)
                self.assertEqual(reader_accepts, expected)
                self.assertEqual(schema_accepts, reader_accepts)
                if expected:
                    self.assertIsInstance(result, CandidateAPreferenceProfileV1)

    def test_success_returns_one_sealed_non_authorizing_variant(self) -> None:
        raw = self.corpus["cases"][0]["wire"].encode("utf-8")
        profile = parse_candidate_a_preference_profile(raw)
        self.assertEqual(profile.profile_id, PROFILE_ID)
        self.assertEqual(profile.profile_version, PROFILE_VERSION)
        self.assertEqual(
            profile.acquisition_topology,
            "LOCAL_NODE_BY_VALUE_PLUS_SINGLE_REMOTE_OPAQUE_BODY",
        )
        self.assertEqual(
            profile.http_attempt_profile,
            "ONE_DNS_ONE_TCP_ONE_TLS_ONE_GET_IDENTITY_NO_RETRY",
        )
        self.assertEqual(profile.preference_class, PREFERENCE_CLASS)
        self.assertEqual(profile.custody_semantics, CUSTODY_SEMANTICS)
        self.assertEqual(profile.serialization_semantics, SERIALIZATION_SEMANTICS)
        self.assertEqual(profile.compatibility, COMPATIBILITY)
        self.assertEqual(profile.authority_effect, AUTHORITY_EFFECT)
        self.assertFalse(profile.next_stage_authorized)
        with self.assertRaises((AttributeError, TypeError)):
            profile.profile_version = 2  # type: ignore[misc]

    def test_nominal_result_has_no_public_constructor(self) -> None:
        with self.assertRaises(TypeError):
            CandidateAPreferenceProfileV1(_token=None)  # type: ignore[arg-type]

    def test_schema_is_closed_exact_and_has_no_defaults_or_alias_fields(self) -> None:
        self.assertFalse(self.schema["additionalProperties"])
        expected = {
            "profile_id",
            "profile_version",
            "acquisition_topology",
            "http_attempt_profile",
        }
        self.assertEqual(set(self.schema["required"]), expected)
        self.assertEqual(set(self.schema["properties"]), expected)
        self.assertNotIn("default", json.dumps(self.schema))
        self.assertNotIn('"A1"', json.dumps(self.schema))
        self.assertNotIn('"H1"', json.dumps(self.schema))
        self.assertNotIn("ACQUISITION_TOPOLOGY", v2_module.__all__)
        self.assertNotIn("HTTP_ATTEMPT_PROFILE", v2_module.__all__)

    def test_raw_envelope_failures_are_typed(self) -> None:
        assert_code(
            self,
            "ER_A3_V2_RAW_TOO_LARGE",
            lambda: parse_candidate_a_preference_profile(b" " * (MAX_RAW_BYTES + 1)),
        )
        assert_code(self, "ER_A3_V2_JSON_BOM", lambda: parse_candidate_a_preference_profile(b"\xef\xbb\xbf{}"))
        assert_code(
            self,
            "ER_A3_V2_JSON_INVALID_UTF8",
            lambda: parse_candidate_a_preference_profile(b'{"profile_id":"\xff"}'),
        )
        assert_code(self, "ER_A3_V2_JSON_INVALID", lambda: parse_candidate_a_preference_profile(b"{"))
        assert_code(self, "ER_A3_V2_JSON_INVALID", lambda: parse_candidate_a_preference_profile(b"[]"))
        assert_code(
            self,
            "ER_A3_V2_JSON_DUPLICATE_KEY",
            lambda: parse_candidate_a_preference_profile(b'{"profile_id":1,"profile_id":2}'),
        )

    def test_reader_does_not_touch_filesystem_or_network(self) -> None:
        raw = self.corpus["cases"][0]["wire"].encode("utf-8")
        with (
            mock.patch("builtins.open", side_effect=AssertionError("filesystem access")) as opened,
            mock.patch.object(socket, "socket", side_effect=AssertionError("network access")) as sock,
        ):
            parse_candidate_a_preference_profile(raw)
        opened.assert_not_called()
        sock.assert_not_called()


class ERA3MinV2LifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lifecycle = json.loads(LIFECYCLE_PATH.read_text(encoding="utf-8"))

    def test_v1_artifacts_are_digest_locked_without_modification(self) -> None:
        artifacts = self.lifecycle["v1"]["artifacts"]
        self.assertGreaterEqual(len(artifacts), 3)
        for artifact in artifacts:
            actual = hashlib.sha256((ROOT / artifact["path"]).read_bytes()).hexdigest().upper()
            with self.subTest(path=artifact["path"]):
                self.assertEqual(actual, artifact["sha256"])
        self.assertEqual(self.lifecycle["v1"]["lifecycle_status"], V1_STATUS)
        self.assertEqual(self.lifecycle["v1"]["issued_source_instance_inventory"], [])

    def test_design_basis_document_and_exact_raw_spans_match(self) -> None:
        basis = self.lifecycle["v2"]["design_basis"]
        raw = (ROOT / basis["path"]).read_bytes()
        self.assertEqual(len(raw), basis["bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest().upper(), basis["sha256"])
        lines = raw.splitlines(keepends=True)
        for span in basis["spans"]:
            expected_start = sum(len(line) for line in lines[: span["start_line"] - 1])
            expected_end = sum(len(line) for line in lines[: span["end_line"]])
            selected = raw[span["byte_start"] : span["byte_end_exclusive"]]
            with self.subTest(role=span["role"]):
                self.assertGreater(len(selected), 0)
                self.assertEqual(span["byte_start"], expected_start)
                self.assertEqual(span["byte_end_exclusive"], expected_end)
                self.assertEqual(hashlib.sha256(selected).hexdigest().upper(), span["sha256"])

    def test_v1_is_audit_only_and_normal_use_fails_closed(self) -> None:
        audit = resolve_contract(1, V1_AUDIT_PURPOSE)
        self.assertEqual(audit.lifecycle_status, V1_STATUS)
        self.assertTrue(audit.audit_reproduction_only)
        self.assertFalse(audit.normal_use_available)
        self.assertFalse(audit.next_stage_authorized)
        for purpose in ("NORMAL_USE", "ISSUE", "ADMIT", "MIGRATE", V2_DESIGN_PURPOSE):
            with self.subTest(purpose=purpose):
                assert_code(
                    self,
                    "ER_A3_V1_RETIRED_UNISSUED",
                    lambda purpose=purpose: resolve_contract(1, purpose),
                )

    def test_v1_validation_route_is_explicitly_non_admitting(self) -> None:
        result = validate_v1_for_audit(v1_wire(valid_v1_package()))
        self.assertEqual(result.lifecycle_status, V1_STATUS)
        self.assertEqual(result.purpose, V1_AUDIT_PURPOSE)
        self.assertEqual(result.package_shape, "VALID")
        self.assertEqual(result.admission_effect, "NONE")
        self.assertEqual(result.authority_effect, "NONE")
        self.assertFalse(result.next_stage_authorized)

    def test_v2_resolves_only_as_design_contract_with_no_instance(self) -> None:
        resolution = resolve_contract(2, V2_DESIGN_PURPOSE)
        self.assertEqual(resolution.lifecycle_status, CONTRACT_STATUS)
        self.assertEqual(resolution.lineage_relation, LINEAGE_RELATION)
        self.assertTrue(resolution.normal_use_available)
        self.assertEqual(resolution.compatibility, "UNASSESSED")
        self.assertEqual(resolution.authority_effect, "NONE")
        self.assertFalse(resolution.next_stage_authorized)
        for purpose in ("ISSUE", "ADMIT", "MIGRATE", V1_AUDIT_PURPOSE):
            with self.subTest(purpose=purpose):
                assert_code(
                    self,
                    "ER_A3_CONTRACT_PURPOSE_UNSUPPORTED",
                    lambda purpose=purpose: resolve_contract(2, purpose),
                )
        self.assertIsNone(resolve_registered_source_instance(1))
        self.assertIsNone(resolve_registered_source_instance(2))
        self.assertEqual(self.lifecycle["v2"]["registered_source_instance_inventory"], [])

    def test_no_converter_fallback_or_compatibility_claim_exists(self) -> None:
        v2 = self.lifecycle["v2"]
        self.assertEqual(v2["lineage_relation_to_v1"], LINEAGE_RELATION)
        self.assertFalse(v2["correction_of_v1"])
        self.assertFalse(v2["reinterpretation_of_v1"])
        self.assertEqual(v2["conversion_from_v1"], "NONE")
        self.assertEqual(self.lifecycle["compatibility"], "UNASSESSED")

    def test_rollback_never_reactivates_v1(self) -> None:
        rollback = self.lifecycle["rollback"]
        self.assertEqual(rollback["v1_lifecycle_after_v2_removal"], V1_STATUS)
        self.assertEqual(rollback["current_successor_after_v2_removal"], "NONE")
        self.assertFalse(rollback["reactivate_v1"])


class ERA3MinV2FixtureExclusionTests(unittest.TestCase):
    def test_fixture_is_explicitly_non_normative_and_has_no_effects(self) -> None:
        corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
        self.assertEqual(corpus["classification"], FIXTURE_CLASSIFICATION)
        for field in (
            "registry_membership",
            "catalog_membership",
            "recommendation_effect",
            "freeze_effect",
            "authority_effect",
            "admission_effect",
        ):
            self.assertEqual(corpus[field], "NONE")
        self.assertFalse(corpus["next_stage_authorized"])
        self.assertIsNone(resolve_registered_source_instance(2))

    def test_no_registered_v2_source_instance_file_exists(self) -> None:
        candidates = tuple((ROOT / "evidence").glob("*er-a3-min*v2*source-instance*.json"))
        self.assertEqual(candidates, ())


if __name__ == "__main__":
    unittest.main()
