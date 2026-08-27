"""Extract observable collaboration facts from one persisted Codex session JSONL."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
from typing import Any


CORE_PATHS = ("/root/proposing_tl", "/root/peer_tl", "/root/chief_architect")
CORE_TASK_NAMES = tuple(path.rsplit("/", 1)[-1] for path in CORE_PATHS)


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
    readiness_positions: dict[str, int] = {}
    proposer_activation_positions: list[int] = []
    timestamps: list[datetime] = []
    session_id = None
    cli_version = None

    for position, record in enumerate(records):
        if isinstance(record.get("timestamp"), str):
            timestamps.append(datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00")))
        payload = record.get("payload", {})
        if record.get("type") == "session_meta":
            session_id = payload.get("session_id") or payload.get("id")
            cli_version = payload.get("cli_version")
        if record.get("type") == "response_item" and payload.get("type") == "function_call":
            name = payload.get("name")
            calls[name] += 1
            arguments = json.loads(payload.get("arguments", "{}"))
            if name == "spawn_agent":
                spawns.append(
                    {
                        "task_name": arguments.get("task_name"),
                        "fork_turns": arguments.get("fork_turns"),
                    }
                )
            if name == "followup_task" and arguments.get("target") in {
                "proposing_tl",
                "/root/proposing_tl",
            }:
                proposer_activation_positions.append(position)
        if record.get("type") == "event_msg" and payload.get("type") == "item_completed":
            item = payload.get("item", {})
            if item.get("type") == "SubAgentActivity" and item.get("kind") == "started":
                started[item.get("agent_path")] = item.get("agent_thread_id")
        if record.get("type") == "response_item" and payload.get("type") == "agent_message":
            author = payload.get("author")
            text = _text_content(payload)
            messages[author].append(text)
            if author in CORE_PATHS and author not in readiness_positions:
                if _is_readiness_message(text, author):
                    readiness_positions[author] = position

    first_messages = {
        path: (messages[path][0] if messages[path] else None) for path in CORE_PATHS
    }
    core_started = {path: thread_id for path, thread_id in started.items() if path in CORE_PATHS}
    core_spawns = [item for item in spawns if item.get("task_name") in CORE_TASK_NAMES]
    all_core_readiness_only = set(readiness_positions) == set(CORE_PATHS)
    commit_after_readiness = (
        all_core_readiness_only
        and bool(proposer_activation_positions)
        and min(proposer_activation_positions) > max(readiness_positions.values())
    )
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
        "core_threads": core_started,
        "three_distinct_core_threads": (
            set(core_started) == set(CORE_PATHS)
            and len(set(core_started.values())) == 3
            and all(core_started.values())
        ),
        "all_core_threads_fork_turns_none": (
            len(core_spawns) == 3
            and {item.get("task_name") for item in core_spawns} == set(CORE_TASK_NAMES)
            and all(item.get("fork_turns") == "none" for item in core_spawns)
        ),
        "first_role_messages": first_messages,
        "proposer_readiness_preceded_substantive_exposure": _is_readiness_message(
            first_messages["/root/proposing_tl"], "/root/proposing_tl"
        ),
        "peer_readiness_preceded_candidate_exposure": _is_readiness_message(
            first_messages["/root/peer_tl"], "/root/peer_tl"
        ),
        "chief_readiness_preceded_terminal_exposure": _is_readiness_message(
            first_messages["/root/chief_architect"], "/root/chief_architect"
        ),
        "all_core_readiness_only": all_core_readiness_only,
        "proposer_activation_after_all_core_readiness": commit_after_readiness,
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
