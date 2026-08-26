from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))

from audit_live_session import audit_records  # noqa: E402


class SessionAuditTests(unittest.TestCase):
    def test_extracts_three_fresh_core_threads_and_readiness(self) -> None:
        records = [
            {
                "timestamp": "2026-08-25T00:00:00Z",
                "type": "session_meta",
                "payload": {"session_id": "parent", "cli_version": "0.149.1"},
            }
        ]
        for index, role in enumerate(("proposing_tl", "peer_tl", "chief_architect"), 1):
            path = f"/root/{role}"
            records.extend(
                [
                    {
                        "timestamp": f"2026-08-25T00:00:0{index}Z",
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "name": "spawn_agent",
                            "arguments": json.dumps(
                                {"task_name": role, "fork_turns": "none", "message": "x"}
                            ),
                        },
                    },
                    {
                        "timestamp": f"2026-08-25T00:00:1{index}Z",
                        "type": "event_msg",
                        "payload": {
                            "type": "item_completed",
                            "item": {
                                "type": "SubAgentActivity",
                                "kind": "started",
                                "agent_path": path,
                                "agent_thread_id": f"thread-{index}",
                            },
                        },
                    },
                ]
            )
        for role in ("peer_tl", "chief_architect"):
            records.append(
                {
                    "timestamp": "2026-08-25T00:00:20Z",
                    "type": "response_item",
                    "payload": {
                        "type": "agent_message",
                        "author": f"/root/{role}",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Message Type: FINAL_ANSWER\nTask name: /root\nSender: "
                                    f"/root/{role}\nPayload:\nREADY"
                                ),
                            }
                        ],
                    },
                }
            )

        result = audit_records(records)
        self.assertTrue(result["three_distinct_core_threads"])
        self.assertTrue(result["all_core_threads_fork_turns_none"])
        self.assertTrue(result["peer_readiness_preceded_candidate_exposure"])
        self.assertTrue(result["chief_readiness_preceded_terminal_exposure"])

    def test_accepts_bounded_readiness_variant_but_not_substantive_payload(self) -> None:
        base = (
            "Message Type: FINAL_ANSWER\nTask name: /root\nSender: /root/peer_tl\n"
            "Payload:\n"
        )
        from audit_live_session import _is_readiness_message

        self.assertTrue(
            _is_readiness_message(
                base + "READY_PEER\nNO_PROPOSAL_OR_PREFERENCE_PROVIDED", "/root/peer_tl"
            )
        )
        self.assertFalse(
            _is_readiness_message(base + "READY\nProposal looks good", "/root/peer_tl")
        )

    def test_accepts_explicit_natural_language_wait_without_accepting_a_verdict(self) -> None:
        from audit_live_session import _is_readiness_message

        peer_base = (
            "Message Type: FINAL_ANSWER\nTask name: /root\nSender: /root/peer_tl\n"
            "Payload:\n"
        )
        chief_base = (
            "Message Type: FINAL_ANSWER\nTask name: /root\nSender: /root/chief_architect\n"
            "Payload:\n"
        )
        self.assertTrue(
            _is_readiness_message(
                peer_base
                + "Ready. I'll wait for the frozen frame and current proposal before inspecting.",
                "/root/peer_tl",
            )
        )
        self.assertTrue(
            _is_readiness_message(
                chief_base
                + "Chief Architect ready. I will remain blinded and inspect nothing substantive "
                "until the complete-record handoff.",
                "/root/chief_architect",
            )
        )
        self.assertTrue(
            _is_readiness_message(
                peer_base
                + "Peer TL ready. I'll wait for the frozen frame, ledger, and P0; no substantive "
                "review, inspection, inference, or proposal until activated.",
                "/root/peer_tl",
            )
        )
        self.assertTrue(
            _is_readiness_message(
                chief_base
                + "Chief Architect thread ready. I'll remain blinded and take no substantive "
                "action until the completed three-round handoff arrives.",
                "/root/chief_architect",
            )
        )
        self.assertFalse(
            _is_readiness_message(
                peer_base + "Ready. The proposal looks good; I'll wait for the next stage.",
                "/root/peer_tl",
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
