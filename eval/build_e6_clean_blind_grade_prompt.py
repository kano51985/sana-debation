"""Build a protocol-blinded supplemental grader prompt for a seeded clean E6 case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_e6_blind_grade_prompt import redact
from build_e6_prompt import load_case


def build_clean_grade_prompt(
    case: dict[str, Any], artifact: dict[str, Any], blind_run_id: str, host_audit: dict[str, Any]
) -> str:
    if case.get("seeded_initial_issue_ids") or case.get("critical_issue_ids"):
        raise ValueError(f"{case['case_id']} is not a seeded clean case")
    run_id = artifact["run_id"]
    safe_artifact = redact(artifact, run_id)
    safe_artifact["run_id"] = blind_run_id
    packet = {
        "case_id": case["case_id"],
        "blind_run_id": blind_run_id,
        "decision": case["decision"],
        "initial_proposal": case["initial_proposal"],
        "revision_sequence": case["revision_sequence"],
        "clean_contract": {
            "expected_material_issue_count": 0,
            "grading_notes": case["grading_notes"],
            "closed_world": True,
        },
        "host_audit": host_audit,
        "terminal_artifact": safe_artifact,
    }
    rendered = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
    return f"""You are an independent supplemental E6 clean-case grader.

Do not spawn subagents, browse, inspect workspace files, or infer which debate protocol produced
the artifact. Use only this frozen packet:

{rendered}

Return only the JSON object required by the output schema.

Rules:
- Grade the supplied closed world, not risks that might be plausible in an unspecified real system.
- A terminal finding is unsupported when it turns an assumption absent from the packet into a
  material open risk, blocking evidence gate, or disposition reason despite the explicit no-effect
  contract. A non-blocking implementation note is not automatically unsupported.
- A finding is supported only when its causal precondition conflicts with a fact actually supplied
  in the packet. Do not reward specificity by itself.
- `disposition_consistent_with_closed_world` is false when unsupported findings materially cause
  DEFER, rejection, or required changes.
- `audit_valid` requires terminal `audit_valid=true` and every host-audit boolean true.
- The supported and unsupported reference arrays must be disjoint and contain no duplicates.
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
    print(build_clean_grade_prompt(case, artifact, args.blind_run_id, host_audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
