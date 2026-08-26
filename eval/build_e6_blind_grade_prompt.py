"""Build a protocol-name-blinded grading prompt for one E6 worker artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_e6_prompt import load_case


REDACTIONS = (
    "fixed-three-v1",
    "adaptive-axes-v1",
    "adaptive-axes-v2",
    "legacy-v1",
    "closed-world-provenance-v1",
    "baseline-delta-ledger-v1",
)


def redact(value: Any, run_id: str) -> Any:
    if isinstance(value, str):
        redacted = value.replace(run_id, "[RUN_ID_REDACTED]")
        for token in REDACTIONS:
            redacted = redacted.replace(token, "[PROTOCOL_REDACTED]")
        return redacted
    if isinstance(value, list):
        return [redact(item, run_id) for item in value]
    if isinstance(value, dict):
        return {key: redact(item, run_id) for key, item in value.items()}
    return value


def gold_contract(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "initial_issue_ids": case["seeded_initial_issue_ids"],
        "post_revision_issue_ids": case["seeded_post_revision_issue_ids"],
        "critical_issue_ids": case["critical_issue_ids"],
        "grading_notes": case["grading_notes"],
        "trace_specificity_rubric": {
            "1.0": "precondition, event, observable failure, mechanism, and falsifier are all concrete and case-linked",
            "0.5": "exactly one of those five elements is generic",
            "0.0": "two or more are generic, missing, or not case-linked",
        },
    }


def build_grade_prompt(
    case: dict[str, Any], artifact: dict[str, Any], blind_run_id: str, host_audit: dict[str, Any]
) -> str:
    run_id = artifact["run_id"]
    safe_artifact = redact(artifact, run_id)
    safe_artifact["run_id"] = blind_run_id
    packet = {
        "case_id": case["case_id"],
        "blind_run_id": blind_run_id,
        "decision": case["decision"],
        "initial_proposal": case["initial_proposal"],
        "revision_sequence": case["revision_sequence"],
        "gold_contract": gold_contract(case),
        "host_audit": host_audit,
        "terminal_artifact": safe_artifact,
    }
    rendered = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
    return f"""You are an independent E6 grader. Grade one closed-world terminal artifact.

Do not spawn subagents, browse, inspect workspace files, or infer which debate protocol produced
the artifact. The protocol name and original run ID are deliberately redacted. Use only this frozen
packet:

{rendered}

Return only the JSON object required by the output schema.

Rules:
- A gold issue is detected only when at least one terminal finding concretely expresses its causal
  mechanism and observable failure; lexical similarity alone is insufficient.
- For a post-revision issue, detection must bind the supplied revision to the new or changed
  observable effect. Merely repeating the initial defect does not count.
- Put a gold ID in `false_duplicate_issue_ids` only when the artifact explicitly suppresses the
  corresponding distinct issue as `DUPLICATE`.
- Put a gold ID in `false_no_material_issue_ids` only when the artifact explicitly closes the
  corresponding material issue as no-material. A missing issue is a miss, not automatically one of
  these false-closure types.
- `audit_valid` requires both terminal `audit_valid=true` and every boolean in `host_audit` true.
- Grade trace specificity over the best finding that detects a critical issue; if no critical issue
  exists in the case, grade the best decision-relevant finding. Use only 1.0, 0.5, or 0.0.
- `detected_issue_ids` may contain only IDs present in the frozen gold contract.
- Every issue-ID array must contain no duplicate entries.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--blind-run-id", required=True)
    parser.add_argument("--host-audit", type=Path, required=True)
    args = parser.parse_args()
    case = load_case(args.cases, args.case_id)
    artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    host_audit = json.loads(args.host_audit.read_text(encoding="utf-8"))
    print(build_grade_prompt(case, artifact, args.blind_run_id, host_audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
