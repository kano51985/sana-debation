from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "e14-a2-n1-lifecycle-v1.schema.json"
FIXTURE_PATH = ROOT / "fixtures" / "e14_n1_static_cases_v1.json"

TYPED_ROOT = "sha256-jcs-e14-n1-v1:" + "a" * 64
SECOND_ROOT = "sha256-jcs-e14-n1-v1:" + "b" * 64
SHA256 = "A" * 64
NOW = "2026-08-27T00:00:00Z"
LATER = "2026-08-27T01:00:00Z"


def envelope(kind: str, effect: str, payload: dict) -> dict:
    return {
        "schema": "sana.e14.n1.lifecycle-artifact.v1",
        "artifact_kind": kind,
        "profile_kind": "P3_N1_CONTROL_CLOSURE_V1",
        "content_root": TYPED_ROOT,
        "fixture_only": False,
        "authority_effect": effect,
        "payload": payload,
    }


def validity() -> dict:
    return {"issued_at": NOW, "not_before": NOW, "expires_at": LATER}


def platform() -> dict:
    return {
        "host_os_build": "host.fixture.v1",
        "virtualization_backend": "vm.fixture.v1",
        "docker_desktop_build": "desktop.fixture.v1",
        "engine_build": "engine.fixture.v1",
        "containerd_build": "containerd.fixture.v1",
        "runc_build": "runc.fixture.v1",
        "linux_kernel_build": "kernel.fixture.v1",
        "architecture": "amd64",
        "cgroup_mode": "v2",
        "security_options_root": TYPED_ROOT,
        "seccomp_policy_sha256": SHA256,
    }


def valid_schema_examples() -> list[dict]:
    roots = {"required": TYPED_ROOT}
    policy = envelope(
        "N1_ISSUER_POLICY",
        "NONE",
        {
            "scope": "A2",
            "roles": {
                "policy_issuer": "fixture.policy",
                "qualification_issuer": "fixture.qualification",
                "g8_authorizer": "fixture.g8",
                "controller": "fixture.controller",
                "g9_finalizer": "fixture.g9",
            },
            "environment_predicates_root": TYPED_ROOT,
            "evidence_predicates_root": SECOND_ROOT,
            "maximum_qualification_validity_seconds": 3600,
            "maximum_authorization_validity_seconds": 300,
            "revocation_authority": "fixture.revocation",
            "revocation_epoch": 1,
            "compatibility_profile": "N1_STRICT_MUTUAL_REJECTION_V1",
        },
    )
    qualified = envelope(
        "N1_PROFILE_QUALIFIED",
        "NONE",
        {
            "issuer_policy_root": TYPED_ROOT,
            "qualification_id": "fixture.qualification.1",
            "issued_by": "fixture.qualification",
            "validity": validity(),
            "revocation_epoch": 1,
            "dedicated_image_sha256": SHA256,
            "normative_final_view_manifest_root": TYPED_ROOT,
            "interpreter_sha256": SHA256,
            "closure_roots": roots,
            "tool_roots": roots,
            "platform": platform(),
            "negative_suite_root": TYPED_ROOT,
            "consumer_conformance_root": TYPED_ROOT,
            "authority_effect": "NONE",
        },
    )
    reserved = envelope(
        "N1_OUTPUT_RESERVED",
        "NONE",
        {
            "qualification_root": TYPED_ROOT,
            "reservation_id": "fixture.reservation.1",
            "immutable_object_identity": "fixture.output.1",
            "empty_initial_inventory_root": TYPED_ROOT,
            "lease_token_sha256": SHA256,
            "creation_event_root": TYPED_ROOT,
            "attachment_history_root": TYPED_ROOT,
            "exclusive_single_use": True,
            "authority_effect": "NONE",
        },
    )
    prepared = envelope(
        "N1_CONTAINER_PREPARED",
        "NONE",
        {
            "qualification_root": TYPED_ROOT,
            "output_reservation_root": TYPED_ROOT,
            "container_id": "fixture.container.1",
            "container_config_sha256": SHA256,
            "dedicated_image_sha256": SHA256,
            "launch_root": TYPED_ROOT,
            "mount_view_root": TYPED_ROOT,
            "environment_root": TYPED_ROOT,
            "platform_root": TYPED_ROOT,
            "guest_execution_during_prepare": False,
            "unqualified_hook_execution": False,
            "exclusive_start_controller": "fixture.controller",
            "state": "STOPPED_NOT_AUTHORIZED",
            "authority_effect": "NONE",
        },
    )
    authorized = envelope(
        "G8_N1_RUN_AUTHORIZED",
        "START_ONCE",
        {
            "issuer_policy_root": TYPED_ROOT,
            "qualification_root": TYPED_ROOT,
            "output_reservation_root": TYPED_ROOT,
            "prepared_container_root": TYPED_ROOT,
            "authorization_id": "fixture.authorization.1",
            "issued_by": "fixture.g8",
            "fresh_run_nonce_sha256": SHA256,
            "request_id": "fixture.request.1",
            "input_roots": roots,
            "g1_g6_roots": roots,
            "stopped_container_id": "fixture.container.1",
            "container_config_sha256": SHA256,
            "launch_root": TYPED_ROOT,
            "mount_view_root": TYPED_ROOT,
            "environment_root": TYPED_ROOT,
            "output_object_identity": "fixture.output.1",
            "lease_token_sha256": SHA256,
            "controller_root": TYPED_ROOT,
            "finalizer_root": TYPED_ROOT,
            "platform_root": TYPED_ROOT,
            "validity": validity(),
            "run_sequence": 1,
            "predecessor_final_record_root": "GENESIS",
            "single_use": True,
            "authority_effect": "START_ONCE",
        },
    )
    candidate = envelope(
        "N1_RUN_EVIDENCE_CANDIDATE",
        "NONE",
        {
            "authorization_root": TYPED_ROOT,
            "qualification_root": TYPED_ROOT,
            "run_nonce_sha256": SHA256,
            "request_id": "fixture.request.1",
            "input_roots": roots,
            "actual_container_id": "fixture.container.1",
            "actual_launch_root": TYPED_ROOT,
            "actual_mount_view_root": TYPED_ROOT,
            "start_stop_exit_root": TYPED_ROOT,
            "network_observation_root": TYPED_ROOT,
            "process_observation_root": TYPED_ROOT,
            "resource_observation_root": TYPED_ROOT,
            "output_object_identity": "fixture.output.1",
            "attachment_history_root": TYPED_ROOT,
            "initial_output_root": TYPED_ROOT,
            "final_output_root": SECOND_ROOT,
            "runner_evidence_root": TYPED_ROOT,
            "controller_evidence_root": TYPED_ROOT,
            "guest_authority_claim": False,
            "authority_effect": "NONE",
        },
    )
    terminal = envelope(
        "G9_N1_TERMINAL",
        "ADMISSION_TERMINAL",
        {
            "issuer_policy_root": TYPED_ROOT,
            "qualification_root": TYPED_ROOT,
            "authorization_root": TYPED_ROOT,
            "candidate_root": TYPED_ROOT,
            "finalizer_root": TYPED_ROOT,
            "ledger_head_before": "GENESIS",
            "ledger_head_after": SECOND_ROOT,
            "nonce_single_use_verified": True,
            "predecessor_verified": True,
            "qualification_current": True,
            "revocation_clear": True,
            "candidate_unique_fresh": True,
            "container_identity_verified": True,
            "output_identity_verified": True,
            "evidence_complete": True,
            "terminal_outcome": "N1_FINAL_PASS",
            "detail_code": None,
            "authority_effect": "ADMISSION_TERMINAL",
        },
    )
    return [policy, qualified, reserved, prepared, authorized, candidate, terminal]


def decide(state: dict) -> dict:
    phase = state["phase"]

    if phase == "ROUTING":
        if state["selector"] == "ABSENT":
            return {"decision": "ROUTE_STRICT_LEGACY", "detail_code": None}
        if state["consumer"] == "LEGACY" and state["selector"] == "N1":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_LEGACY_MAPPING_FORBIDDEN"}
        if state["consumer"] == "N1" and state["selector"] != "N1":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_PROFILE_KIND_MISMATCH"}
        if state["schema_status"] != "SUPPORTED":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_SCHEMA_UNSUPPORTED"}

    if phase == "QUALIFICATION":
        if state["actor_role"] != "QUALIFICATION_ISSUER" or state["role_scope"] != "VALID":
            return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_ROLE_SCOPE_MISMATCH"}
        if state["issuer_policy"] != "VALID":
            return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_ISSUER_POLICY_INVALID"}
        if state["manifest_equality"] != "MATCH":
            return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_NORMATIVE_MANIFEST_MISMATCH"}
        if state["scanner_noninterpretation"] != "PASS":
            return {
                "decision": "N1_UNAVAILABLE",
                "detail_code": "N1_INPUT_NONINTERPRETATION_UNPROVEN",
            }
        if state["executable_store_closure"] != "PASS":
            return {
                "decision": "N1_UNAVAILABLE",
                "detail_code": "N1_EXECUTABLE_STORE_CLOSURE_UNPROVEN",
            }
        if state["ledger_qualification"] != "PASS":
            return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_LEDGER_UNQUALIFIED"}
        return {"decision": "N1_PROFILE_QUALIFIED", "detail_code": None}

    if phase == "PREPARATION":
        if state["qualification"] != "VALID":
            return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_QUALIFICATION_MISSING"}
        if state["preparation_execution"] != "NONE":
            return {
                "decision": "N1_UNAVAILABLE",
                "detail_code": "N1_PREPARATION_EXECUTION_DETECTED",
            }
        if state["unqualified_hooks"] != "NONE":
            return {
                "decision": "N1_UNAVAILABLE",
                "detail_code": "N1_UNQUALIFIED_HOOK_EXECUTION",
            }
        if state["exclusive_start"] != "PROVEN":
            return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_EXCLUSIVE_START_UNPROVEN"}
        return {"decision": "N1_CONTAINER_PREPARED", "detail_code": None}

    if phase == "AUTHORIZATION":
        if state["actor_role"] != "G8_AUTHORIZER" or state["role_scope"] != "VALID":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_ROLE_SCOPE_MISMATCH"}
        if state["qualification"] != "VALID" or state["revocation"] != "CLEAR":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_QUALIFICATION_REVOKED"}
        if state["nonce"] != "FRESH":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_AUTH_NONCE_REPLAY"}
        if state["predecessor"] != "MATCH":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_PREDECESSOR_MISMATCH"}
        if state["output_reservation"] != "EXCLUSIVE":
            return {
                "decision": "NO_TERMINAL_STOP",
                "detail_code": "N1_OUTPUT_RESERVATION_NOT_EXCLUSIVE",
            }
        if state["output_initial"] != "EMPTY":
            return {"decision": "NO_TERMINAL_STOP", "detail_code": "N1_OUTPUT_INITIAL_ROOT_NONEMPTY"}
        return {"decision": "G8_N1_RUN_AUTHORIZED", "detail_code": None}

    if phase == "FINALIZATION":
        if state["finalizer_identity"] != "MATCH":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_FINALIZER_IDENTITY_MISMATCH",
            }
        if state["revocation"] != "CLEAR":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_QUALIFICATION_REVOKED",
            }
        if state["ledger"] != "AVAILABLE":
            return {"decision": "N1_INDETERMINATE_BLOCK", "detail_code": "N1_LEDGER_UNAVAILABLE"}
        if state["ledger_cas"] != "SUCCEEDS":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_FINAL_STATE_CAS_FAILED",
            }
        if state["output_identity"] != "MATCH":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_OUTPUT_IDENTITY_CHANGED",
            }
        if state["output_attachment"] != "EXCLUSIVE":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_OUTPUT_CONCURRENT_ATTACHMENT",
            }
        if state["container_identity"] != "MATCH":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_CONTAINER_ID_MISMATCH",
            }
        candidate_failures = {
            "MISSING": "N1_CANDIDATE_MISSING",
            "REPLAYED": "N1_CANDIDATE_REPLAY",
            "CONFLICTING": "N1_CANDIDATE_CONFLICT",
        }
        if state["candidate"] in candidate_failures:
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": candidate_failures[state["candidate"]],
            }
        if state["candidate_authority_claim"] != "NONE":
            return {
                "decision": "N1_INDETERMINATE_BLOCK",
                "detail_code": "N1_GUEST_AUTHORITY_CLAIM",
            }
        if state["evidence"] != "COMPLETE":
            return {"decision": "N1_INDETERMINATE_BLOCK", "detail_code": "N1_EVIDENCE_TIMEOUT"}
        if state["scanner_result"] == "REJECT":
            return {"decision": "N1_FINAL_DENY", "detail_code": "N1_SCANNER_POLICY_REJECTION"}
        return {"decision": "N1_FINAL_PASS", "detail_code": None}

    if phase == "ROLLBACK":
        if state["fallback"] != "NONE":
            return {"decision": "N1_INDETERMINATE_BLOCK", "detail_code": "N1_FALLBACK_FORBIDDEN"}
        return {"decision": "N1_UNAVAILABLE", "detail_code": "N1_QUALIFICATION_REVOKED"}

    raise AssertionError(f"unsupported fixture phase {phase!r}")


class N1LifecycleSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_each_lifecycle_artifact_has_a_valid_example(self) -> None:
        examples = valid_schema_examples()
        self.assertEqual(len(examples), 7)
        for example in examples:
            with self.subTest(kind=example["artifact_kind"]):
                errors = sorted(self.validator.iter_errors(example), key=lambda error: list(error.path))
                self.assertEqual(errors, [], [error.message for error in errors])

    def test_fixture_only_artifact_cannot_carry_start_or_terminal_authority(self) -> None:
        for example in valid_schema_examples():
            if example["authority_effect"] == "NONE":
                continue
            fixture = copy.deepcopy(example)
            fixture["fixture_only"] = True
            self.assertFalse(self.validator.is_valid(fixture))

    def test_guest_authority_and_prepare_execution_are_schema_rejected(self) -> None:
        examples = {item["artifact_kind"]: item for item in valid_schema_examples()}
        candidate = copy.deepcopy(examples["N1_RUN_EVIDENCE_CANDIDATE"])
        candidate["payload"]["guest_authority_claim"] = True
        self.assertFalse(self.validator.is_valid(candidate))

        prepared = copy.deepcopy(examples["N1_CONTAINER_PREPARED"])
        prepared["payload"]["guest_execution_during_prepare"] = True
        self.assertFalse(self.validator.is_valid(prepared))


class N1StaticFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_corpus_is_explicitly_nonauthoritative(self) -> None:
        self.assertEqual(self.corpus["authority_effect"], "NONE")
        self.assertEqual(self.corpus["fixture_identifiers"], "NONAUTHORITATIVE_PLACEHOLDERS")
        serialized = FIXTURE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("content_root", serialized)
        self.assertIsNone(re.search(r"[0-9A-Fa-f]{64}", serialized))

    def test_case_ids_are_unique_and_overrides_are_bounded(self) -> None:
        defaults = self.corpus["defaults"]
        case_ids = [case["case_id"] for case in self.corpus["cases"]]
        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertEqual(len(case_ids), 35)
        for case in self.corpus["cases"]:
            with self.subTest(case=case["case_id"]):
                self.assertRegex(case["case_id"], r"^N1-[A-Z]+-[0-9]{2}$")
                self.assertTrue(set(case["overrides"]).issubset(defaults))
                self.assertEqual(set(case["expected"]), {"decision", "detail_code"})

    def test_fixture_corpus_covers_every_required_failure_family(self) -> None:
        prefixes = {case["case_id"].rsplit("-", 1)[0] for case in self.corpus["cases"]}
        self.assertEqual(
            prefixes,
            {"N1-ROUTE", "N1-QUAL", "N1-PREP", "N1-AUTH", "N1-FINAL", "N1-ROLLBACK"},
        )
        details = {case["expected"]["detail_code"] for case in self.corpus["cases"]}
        required = {
            "N1_LEGACY_MAPPING_FORBIDDEN",
            "N1_ROLE_SCOPE_MISMATCH",
            "N1_NORMATIVE_MANIFEST_MISMATCH",
            "N1_INPUT_NONINTERPRETATION_UNPROVEN",
            "N1_EXECUTABLE_STORE_CLOSURE_UNPROVEN",
            "N1_PREPARATION_EXECUTION_DETECTED",
            "N1_AUTH_NONCE_REPLAY",
            "N1_PREDECESSOR_MISMATCH",
            "N1_OUTPUT_IDENTITY_CHANGED",
            "N1_OUTPUT_CONCURRENT_ATTACHMENT",
            "N1_CANDIDATE_REPLAY",
            "N1_GUEST_AUTHORITY_CLAIM",
            "N1_FINAL_STATE_CAS_FAILED",
            "N1_FALLBACK_FORBIDDEN",
        }
        self.assertTrue(required.issubset(details))

    def test_all_static_cases_match_the_read_only_reference_oracle(self) -> None:
        defaults = self.corpus["defaults"]
        for case in self.corpus["cases"]:
            state = {**defaults, **case["overrides"]}
            with self.subTest(case=case["case_id"]):
                self.assertEqual(decide(state), case["expected"])

    def test_only_complete_determinate_rejection_can_deny(self) -> None:
        for case in self.corpus["cases"]:
            if case["expected"]["decision"] != "N1_FINAL_DENY":
                continue
            state = {**self.corpus["defaults"], **case["overrides"]}
            self.assertEqual(state["phase"], "FINALIZATION")
            self.assertEqual(state["evidence"], "COMPLETE")
            self.assertEqual(state["scanner_result"], "REJECT")
        deny_cases = [
            case for case in self.corpus["cases"] if case["expected"]["decision"] == "N1_FINAL_DENY"
        ]
        self.assertEqual([case["case_id"] for case in deny_cases], ["N1-FINAL-02"])


if __name__ == "__main__":
    unittest.main()
