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
        for role in ("proposing_tl", "peer_tl", "chief_architect"):
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
        records.append(
            {
                "timestamp": "2026-08-25T00:00:21Z",
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "name": "followup_task",
                    "arguments": json.dumps(
                        {"target": "/root/proposing_tl", "message": "produce P0"}
                    ),
                },
            }
        )

        result = audit_records(records)
        self.assertTrue(result["three_distinct_core_threads"])
        self.assertTrue(result["all_core_threads_fork_turns_none"])
        self.assertTrue(result["proposer_readiness_preceded_substantive_exposure"])
        self.assertTrue(result["peer_readiness_preceded_candidate_exposure"])
        self.assertTrue(result["chief_readiness_preceded_terminal_exposure"])
        self.assertTrue(result["all_core_readiness_only"])
        self.assertTrue(result["proposer_activation_after_all_core_readiness"])

    def test_optional_agent_does_not_invalidate_prepared_core(self) -> None:
        records = []
        for index, role in enumerate(("proposing_tl", "peer_tl", "chief_architect"), 1):
            path = f"/root/{role}"
            records.extend(
                [
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "function_call",
                            "name": "spawn_agent",
                            "arguments": json.dumps(
                                {"task_name": role, "fork_turns": "none", "message": "ready"}
                            ),
                        },
                    },
                    {
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
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "agent_message",
                            "author": path,
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        "Message Type: FINAL_ANSWER\nTask name: /root\n"
                                        f"Sender: {path}\nPayload:\nREADY"
                                    ),
                                }
                            ],
                        },
                    },
                ]
            )
        records.extend(
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "spawn_agent",
                        "arguments": json.dumps(
                            {
                                "task_name": "evidence_scout",
                                "fork_turns": "none",
                                "message": "bounded evidence",
                            }
                        ),
                    },
                },
                {
                    "type": "event_msg",
                    "payload": {
                        "type": "item_completed",
                        "item": {
                            "type": "SubAgentActivity",
                            "kind": "started",
                            "agent_path": "/root/evidence_scout",
                            "agent_thread_id": "thread-optional",
                        },
                    },
                },
            ]
        )
        result = audit_records(records)
        self.assertTrue(result["three_distinct_core_threads"])
        self.assertTrue(result["all_core_threads_fork_turns_none"])
        self.assertNotIn("/root/evidence_scout", result["core_threads"])

    def test_rejects_old_partial_start_where_proposer_runs_before_core_ready(self) -> None:
        records = [
            {
                "timestamp": "2026-08-25T00:00:00Z",
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "name": "spawn_agent",
                    "arguments": json.dumps(
                        {
                            "task_name": "proposing_tl",
                            "fork_turns": "none",
                            "message": "produce P0 now",
                        }
                    ),
                },
            },
            {
                "timestamp": "2026-08-25T00:00:01Z",
                "type": "event_msg",
                "payload": {
                    "type": "item_completed",
                    "item": {
                        "type": "SubAgentActivity",
                        "kind": "started",
                        "agent_path": "/root/proposing_tl",
                        "agent_thread_id": "thread-proposer",
                    },
                },
            },
            {
                "timestamp": "2026-08-25T00:00:02Z",
                "type": "response_item",
                "payload": {
                    "type": "agent_message",
                    "author": "/root/proposing_tl",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Message Type: FINAL_ANSWER\nTask name: /root\n"
                                "Sender: /root/proposing_tl\nPayload:\nP0 proposes a design"
                            ),
                        }
                    ],
                },
            },
        ]
        result = audit_records(records)
        self.assertFalse(result["three_distinct_core_threads"])
        self.assertFalse(result["proposer_readiness_preceded_substantive_exposure"])
        self.assertFalse(result["all_core_readiness_only"])
        self.assertFalse(result["proposer_activation_after_all_core_readiness"])

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
