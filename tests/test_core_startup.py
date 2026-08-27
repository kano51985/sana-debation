from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import sys
import unittest

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_startup import (  # noqa: E402
    CORE_ROLES,
    CoreStartupTransaction,
    StartupViolation,
    validate_continuation_packet,
)


def transaction() -> CoreStartupTransaction:
    return CoreStartupTransaction(
        run_id="startup-run-1",
        frame_sha256="a" * 64,
        evidence_ledger_sha256="b" * 64,
        routing_manifest_sha256="c" * 64,
    )


class CoreStartupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(
            (ROOT / "schemas" / "debate-continuation-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_commit_requires_all_three_readiness_receipts(self) -> None:
        startup = transaction()
        startup.record_ready("proposing_tl", "thread-proposer")
        startup.record_ready("peer_tl", "thread-peer")
        with self.assertRaises(StartupViolation) as raised:
            startup.commit()
        self.assertEqual("STARTUP_NOT_PREPARED", raised.exception.code)

        self.assertEqual(
            "PREPARED",
            startup.record_ready("chief_architect", "thread-chief"),
        )
        self.assertEqual("RUNNING", startup.commit())

    def test_thread_limit_at_each_creation_point_never_reaches_commit(self) -> None:
        for failure_index, failing_role in enumerate(CORE_ROLES):
            with self.subTest(failing_role=failing_role):
                startup = transaction()
                for role in CORE_ROLES[:failure_index]:
                    startup.record_ready(role, f"thread-{role}")
                startup.record_capacity_failure(failing_role)

                self.assertEqual("WAITING_FOR_CORE_CAPACITY", startup.state)
                with self.assertRaises(StartupViolation):
                    startup.commit()

                packet = startup.continuation_packet()
                self.validator.validate(packet)
                validate_continuation_packet(packet)
                self.assertFalse(packet["substantive_artifacts_admissible"])
                self.assertEqual([], packet["substantive_exposure_roles"])
                self.assertFalse(packet["resume_requirements"]["reuse_partial_threads"])
                self.assertTrue(
                    packet["resume_requirements"]["observed_capacity_change_required"]
                )

    def test_early_substantive_exposure_aborts_and_is_not_admissible(self) -> None:
        startup = transaction()
        startup.record_ready("proposing_tl", "thread-proposer")
        self.assertEqual(
            "ABORTED_PARTIAL_EXPOSURE",
            startup.record_substantive_exposure("proposing_tl"),
        )
        packet = startup.continuation_packet()
        self.validator.validate(packet)
        validate_continuation_packet(packet)
        self.assertEqual(["proposing_tl"], packet["substantive_exposure_roles"])
        self.assertFalse(packet["substantive_artifacts_admissible"])

    def test_failed_startup_is_terminal_without_capacity_change(self) -> None:
        startup = transaction()
        startup.record_capacity_failure("chief_architect")
        with self.assertRaises(StartupViolation) as raised:
            startup.record_ready("chief_architect", "late-chief")
        self.assertEqual("STARTUP_TERMINAL_OR_PREPARED", raised.exception.code)

    def test_continuation_hash_detects_tampering(self) -> None:
        startup = transaction()
        startup.record_capacity_failure("chief_architect")
        packet = startup.continuation_packet()
        packet["resume_requirements"]["parent_run_id"] = "different-run"
        with self.assertRaises(StartupViolation) as raised:
            validate_continuation_packet(packet)
        self.assertEqual("CONTINUATION_HASH_MISMATCH", raised.exception.code)

    def test_schema_rejects_authority_widening(self) -> None:
        startup = transaction()
        startup.record_capacity_failure("chief_architect")
        packet = copy.deepcopy(startup.continuation_packet())
        packet["substantive_artifacts_admissible"] = True
        with self.assertRaises(ValidationError):
            self.validator.validate(packet)


class SkillPackageTests(unittest.TestCase):
    def test_every_local_markdown_reference_in_skill_exists(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        targets = re.findall(r"\]\((references/[^)]+)\)", skill)
        self.assertGreaterEqual(len(targets), 2)
        for target in targets:
            with self.subTest(target=target):
                self.assertTrue((ROOT / target).is_file())

    def test_skill_requires_prepare_before_commit(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        prepare = skill.index("**PREPARE:**")
        commit = skill.index("**COMMIT:**")
        self.assertLess(prepare, commit)
        self.assertIn("WAITING_FOR_CORE_CAPACITY", skill)
        self.assertIn("ABORTED_PARTIAL_EXPOSURE", skill)


if __name__ == "__main__":
    unittest.main(verbosity=2)

