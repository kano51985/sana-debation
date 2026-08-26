"""Grade matched fixed-three-v1 vs adaptive-axes-v1 E6 result records.

The grader is deterministic. It does not call a model and does not convert
synthetic/dry-run records into behavioral evidence.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
from typing import Any


PROTOCOLS = ("fixed-three-v1", "adaptive-axes-v1")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return records


def grade(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    case_by_id = {case["case_id"]: case for case in cases}
    result_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    errors: list[str] = []
    for result in results:
        key = (result.get("case_id"), result.get("protocol_id"))
        if key[0] not in case_by_id:
            errors.append(f"unknown case: {key[0]}")
            continue
        if key[1] not in PROTOCOLS:
            errors.append(f"unknown protocol for {key[0]}: {key[1]}")
            continue
        if key in result_by_key:
            errors.append(f"duplicate result: {key}")
            continue
        for field in (
            "detected_issue_ids",
            "false_no_material_issue_ids",
            "false_duplicate_issue_ids",
        ):
            values = result.get(field, [])
            if isinstance(values, list) and len(values) != len(set(values)):
                errors.append(f"duplicate issue ID in {field}: {key}")
        result_by_key[key] = result

    summary: dict[str, dict[str, Any]] = {}
    for protocol in PROTOCOLS:
        metrics: dict[str, Any] = defaultdict(float)
        metrics.update(
            {
                "cases": 0,
                "critical_expected": 0,
                "critical_detected": 0,
                "critical_misses": [],
                "post_revision_expected": 0,
                "post_revision_detected": 0,
                "false_no_material": [],
                "false_duplicate": [],
                "unsupported_material_findings": [],
                "audit_invalid_cases": [],
                "trace_specificity_sum": 0.0,
                "input_tokens_total": 0,
                "output_tokens_total": 0,
                "elapsed_ms_total": 0,
                "retries_total": 0,
                "telemetry_unavailable": 0,
                "synthetic_records": 0,
            }
        )
        for case_id, case in case_by_id.items():
            result = result_by_key.get((case_id, protocol))
            if result is None:
                errors.append(f"missing result: {(case_id, protocol)}")
                continue
            metrics["cases"] += 1
            if result.get("evidence_kind") != "live-real-subagents":
                metrics["synthetic_records"] += 1
            detected = set(result.get("detected_issue_ids", []))
            critical = set(case.get("critical_issue_ids", []))
            post_revision = set(case.get("seeded_post_revision_issue_ids", []))
            metrics["critical_expected"] += len(critical)
            metrics["critical_detected"] += len(critical & detected)
            metrics["critical_misses"].extend(
                {"case_id": case_id, "issue_id": issue_id}
                for issue_id in sorted(critical - detected)
            )
            metrics["post_revision_expected"] += len(post_revision)
            metrics["post_revision_detected"] += len(post_revision & detected)
            metrics["false_no_material"].extend(
                {"case_id": case_id, "issue_id": issue_id}
                for issue_id in result.get("false_no_material_issue_ids", [])
            )
            metrics["false_duplicate"].extend(
                {"case_id": case_id, "issue_id": issue_id}
                for issue_id in result.get("false_duplicate_issue_ids", [])
            )
            clean_case = not case.get("seeded_initial_issue_ids") and not case.get(
                "critical_issue_ids"
            )
            if clean_case and result.get("evidence_kind") == "live-real-subagents":
                unsupported = result.get("unsupported_material_finding_refs")
                if not isinstance(unsupported, list):
                    errors.append(
                        f"missing clean-case unsupported findings: {(case_id, protocol)}"
                    )
                else:
                    if len(unsupported) != len(set(unsupported)):
                        errors.append(
                            f"duplicate clean-case finding ref: {(case_id, protocol)}"
                        )
                    metrics["unsupported_material_findings"].extend(
                        {"case_id": case_id, "finding_ref": finding_ref}
                        for finding_ref in unsupported
                    )
            if result.get("audit_valid") is not True:
                metrics["audit_invalid_cases"].append(case_id)
            specificity = result.get("failure_trace_specificity")
            if not isinstance(specificity, (int, float)) or not 0 <= specificity <= 1:
                errors.append(f"invalid trace specificity: {(case_id, protocol, specificity)}")
            else:
                metrics["trace_specificity_sum"] += specificity
            for field in ("input_tokens", "output_tokens", "elapsed_ms", "retries"):
                value = result.get(field)
                if value is None:
                    metrics["telemetry_unavailable"] += 1
                elif not isinstance(value, int) or value < 0:
                    errors.append(f"invalid telemetry: {(case_id, protocol, field, value)}")
                else:
                    metrics[f"{field}_total"] += value

        cases_count = metrics["cases"]
        metrics["critical_detection_rate"] = (
            metrics["critical_detected"] / metrics["critical_expected"]
            if metrics["critical_expected"]
            else 1.0
        )
        metrics["post_revision_detection_rate"] = (
            metrics["post_revision_detected"] / metrics["post_revision_expected"]
            if metrics["post_revision_expected"]
            else 1.0
        )
        metrics["trace_specificity_mean"] = (
            metrics["trace_specificity_sum"] / cases_count if cases_count else 0.0
        )
        del metrics["trace_specificity_sum"]
        summary[protocol] = dict(metrics)

    fixed = summary[PROTOCOLS[0]]
    adaptive = summary[PROTOCOLS[1]]
    live_complete = not errors and all(
        summary[protocol]["synthetic_records"] == 0 for protocol in PROTOCOLS
    )
    behavioral_gate = {
        "complete_matched_live_records": live_complete,
        "adaptive_zero_critical_misses": len(adaptive["critical_misses"]) == 0,
        "adaptive_zero_false_closures": (
            len(adaptive["false_no_material"]) + len(adaptive["false_duplicate"])
        )
        == 0,
        "adaptive_zero_unsupported_material_findings": len(
            adaptive["unsupported_material_findings"]
        )
        == 0,
        "adaptive_all_audits_valid": len(adaptive["audit_invalid_cases"]) == 0,
        "adaptive_not_worse_post_revision_detection": (
            adaptive["post_revision_detection_rate"] >= fixed["post_revision_detection_rate"]
        ),
        "adaptive_not_worse_trace_specificity": (
            adaptive["trace_specificity_mean"] >= fixed["trace_specificity_mean"]
        ),
    }
    passed = all(behavioral_gate.values())
    return {
        "evidence_id": "E6",
        "status": "PASS" if passed else ("HARNESS_ONLY" if not live_complete else "FAIL"),
        "errors": errors,
        "protocol_metrics": summary,
        "behavioral_gate": behavioral_gate,
        "limitations": [
            "A finite seeded suite does not prove general cognitive independence or universal non-inferiority.",
            "Token, elapsed-time, and compaction data are reported only when the host exposes them.",
            "Synthetic records validate the grader only and never satisfy E6.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    report = grade(read_jsonl(args.cases), read_jsonl(args.results))
    print(json.dumps(report, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
