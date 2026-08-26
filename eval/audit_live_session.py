"""Extract observable collaboration facts from one persisted Codex session JSONL."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
from typing import Any


CORE_PATHS = ("/root/proposing_tl", "/root/peer_tl", "/root/chief_architect")


def _text_content(payload: dict[str, Any]) -> str:
    parts = []
    for item in payload.get("content", []):
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            parts.append(item["text"])
    return "\n".join(parts)


def _is_readiness_message(text: str | None, role: str) -> bool:
    if text is None:
        return False
    prefix = (
        "Message Type: FINAL_ANSWER\n"
        "Task name: /root\n"
        f"Sender: {role}\n"
        "Payload:\n"
    )
    if not text.startswith(prefix):
        return False
    payload_lines = [line.strip() for line in text[len(prefix) :].splitlines() if line.strip()]
    if not payload_lines:
        return False
    if payload_lines[0].startswith("READY"):
        return all(line.startswith("NO_") for line in payload_lines[1:])

    # Some agents return a one-line natural-language readiness acknowledgement.
    # Admit only a short, explicitly waiting/blinded declaration, and reject
    # verdict or proposal-content language so this cannot silently bless an
    # early substantive exposure.
    if len(payload_lines) != 1 or len(payload_lines[0]) > 300:
        return False
    acknowledgement = payload_lines[0].casefold()
    ready_prefixes = (
        "ready",
        "peer tl ready",
        "chief architect ready",
        "chief architect thread ready",
    )
    ready_prefix = acknowledgement.startswith(ready_prefixes)
    withheld_until_handoff = "wait" in acknowledgement or "remain blinded" in acknowledgement
    substantive_markers = (
        "approve",
        "reject",
        "defer",
        "looks good",
        "finding",
        "terminal proposal is",
        "p0 is",
        "p0 proposes",
        "p0 should",
        "p1 changes",
    )
    return (
        ready_prefix
        and withheld_until_handoff
        and not any(marker in acknowledgement for marker in substantive_markers)
    )


def audit_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    calls: Counter[str] = Counter()
    spawns: list[dict[str, Any]] = []
    started: dict[str, str] = {}
    messages: dict[str, list[str]] = defaultdict(list)
    timestamps: list[datetime] = []
    session_id = None
    cli_version = None

    for record in records:
        if isinstance(record.get("timestamp"), str):
            timestamps.append(datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00")))
        payload = record.get("payload", {})
        if record.get("type") == "session_meta":
            session_id = payload.get("session_id") or payload.get("id")
            cli_version = payload.get("cli_version")
        if record.get("type") == "response_item" and payload.get("type") == "function_call":
            name = payload.get("name")
            calls[name] += 1
            if name == "spawn_agent":
                arguments = json.loads(payload.get("arguments", "{}"))
                spawns.append(
                    {
                        "task_name": arguments.get("task_name"),
                        "fork_turns": arguments.get("fork_turns"),
                    }
                )
        if record.get("type") == "event_msg" and payload.get("type") == "item_completed":
            item = payload.get("item", {})
            if item.get("type") == "SubAgentActivity" and item.get("kind") == "started":
                started[item.get("agent_path")] = item.get("agent_thread_id")
        if record.get("type") == "response_item" and payload.get("type") == "agent_message":
            messages[payload.get("author")].append(_text_content(payload))

    first_messages = {
        path: (messages[path][0] if messages[path] else None) for path in CORE_PATHS
    }
    return {
        "parent_session_id": session_id,
        "cli_version": cli_version,
        "started_at": min(timestamps).isoformat() if timestamps else None,
        "ended_at": max(timestamps).isoformat() if timestamps else None,
        "elapsed_ms": (
            int((max(timestamps) - min(timestamps)).total_seconds() * 1000)
            if timestamps
            else None
        ),
        "call_counts": {
            "spawn_agent": calls["spawn_agent"],
            "followup_task": calls["followup_task"],
            "wait_agent": calls["wait_agent"],
        },
        "spawn_requests": spawns,
        "core_threads": started,
        "three_distinct_core_threads": (
            set(started) == set(CORE_PATHS)
            and len(set(started.values())) == 3
            and all(started.values())
        ),
        "all_core_threads_fork_turns_none": (
            len(spawns) == 3 and all(item.get("fork_turns") == "none" for item in spawns)
        ),
        "first_role_messages": first_messages,
        "peer_readiness_preceded_candidate_exposure": _is_readiness_message(
            first_messages["/root/peer_tl"], "/root/peer_tl"
        ),
        "chief_readiness_preceded_terminal_exposure": _is_readiness_message(
            first_messages["/root/chief_architect"], "/root/chief_architect"
        ),
    }


def audit_path(path: Path) -> dict[str, Any]:
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return audit_records(records)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_jsonl", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit_path(args.session_jsonl), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
