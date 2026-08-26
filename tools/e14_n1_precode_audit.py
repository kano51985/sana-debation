"""Read-only schema-derived resource audit for the unissued N1 lifecycle-v2 draft.

This is not the production parser, builder, canonicalizer, or root oracle.  It constructs the
largest schema-valid shape for each payload branch and reports structural counts and encoded sizes
so the pre-code safety caps can be reviewed before I0 implementation begins.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "e14-a2-n1-lifecycle-v2.schema.json"

ARTIFACT_PAYLOADS = {
    "N1_ISSUER_POLICY": "issuerPolicyPayload",
    "N1_PROFILE_QUALIFIED": "profileQualifiedPayload",
    "N1_OUTPUT_RESERVED": "outputReservedPayload",
    "N1_CONTAINER_PREPARED": "containerPreparedPayload",
    "G8_N1_RUN_AUTHORIZED": "runAuthorizedPayload",
    "N1_RUN_EVIDENCE_CANDIDATE": "runEvidencePayload",
    "G9_N1_TERMINAL": "terminalPayload",
}

CAPS = {
    "raw_bytes": 262_144,
    "depth": 12,
    "nodes": 4_096,
    "members": 2_048,
    "members_per_object": 128,
}

TYPED_ROOT = "sha256-jcs-e14-n1-v2:" + "f" * 64


class AuditError(ValueError):
    pass


def _resolve(node: Mapping[str, Any], defs: Mapping[str, Any]) -> Mapping[str, Any]:
    while "$ref" in node:
        ref = node["$ref"]
        prefix = "#/$defs/"
        if not isinstance(ref, str) or not ref.startswith(prefix):
            raise AuditError(f"unsupported reference {ref!r}")
        node = defs[ref[len(prefix) :]]
    return node


def _dynamic_key(index: int, length: int) -> str:
    suffix = f"{index:06d}"
    return "k" + "a" * (length - len(suffix) - 1) + suffix


def _max_string(node: Mapping[str, Any]) -> str:
    if "const" in node:
        return str(node["const"])
    if "enum" in node:
        return max((str(value) for value in node["enum"]), key=lambda value: len(value.encode("utf-8")))
    pattern = str(node.get("pattern", ""))
    maximum = int(node.get("maxLength", 160))
    if pattern.startswith("^sha256-jcs-e14-n1-v2:"):
        return TYPED_ROOT
    if pattern == "^[0-9A-F]{64}$":
        return "F" * 64
    if pattern.startswith("^[0-9]{4}-"):
        return "9999-12-31T23:59:59Z"
    if pattern == "^N1_[A-Z0-9_]+$":
        return "N1_" + "A" * (maximum - 3)
    if pattern == "^[A-Za-z0-9][A-Za-z0-9._:-]*$":
        return "A" * maximum
    return "x" * maximum


def maximal_value(node: Mapping[str, Any], defs: Mapping[str, Any]) -> Any:
    node = _resolve(node, defs)
    if "oneOf" in node:
        candidates = [maximal_value(candidate, defs) for candidate in node["oneOf"]]
        return max(candidates, key=lambda value: len(_canonical(value)))
    if "const" in node:
        return node["const"]
    if "enum" in node:
        return max(node["enum"], key=lambda value: len(_canonical(value)))

    kind = node.get("type")
    if kind == "object" or "properties" in node or "additionalProperties" in node:
        properties = node.get("properties", {})
        result = {name: maximal_value(child, defs) for name, child in properties.items()}
        additional = node.get("additionalProperties")
        if isinstance(additional, dict):
            count = int(node.get("maxProperties", len(result))) - len(result)
            key_limit = int(node.get("propertyNames", {}).get("maxLength", 160))
            for index in range(count):
                result[_dynamic_key(index, key_limit)] = maximal_value(additional, defs)
        return result
    if kind == "string":
        return _max_string(node)
    if kind == "integer":
        return int(node.get("maximum", 9_007_199_254_740_991))
    if kind == "boolean":
        return True
    if kind == "null":
        return None
    raise AuditError(f"unsupported schema node {node!r}")


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _metrics(value: Any, depth: int = 1) -> dict[str, int]:
    if isinstance(value, dict):
        child_metrics = [_metrics(child, depth + 1) for child in value.values()]
        return {
            "depth": max([depth, *(item["depth"] for item in child_metrics)]),
            "nodes": 1 + sum(item["nodes"] for item in child_metrics),
            "members": len(value) + sum(item["members"] for item in child_metrics),
            "max_members_in_object": max(
                [len(value), *(item["max_members_in_object"] for item in child_metrics)]
            ),
        }
    if isinstance(value, list):
        child_metrics = [_metrics(child, depth + 1) for child in value]
        return {
            "depth": max([depth, *(item["depth"] for item in child_metrics)]),
            "nodes": 1 + sum(item["nodes"] for item in child_metrics),
            "members": sum(item["members"] for item in child_metrics),
            "max_members_in_object": max(
                [0, *(item["max_members_in_object"] for item in child_metrics)]
            ),
        }
    return {"depth": depth, "nodes": 1, "members": 0, "max_members_in_object": 0}


def audit(schema_path: Path) -> dict[str, Any]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    defs = schema["$defs"]
    rows: list[dict[str, Any]] = []
    for artifact_kind, payload_def in ARTIFACT_PAYLOADS.items():
        payload = maximal_value(defs[payload_def], defs)
        envelope = {
            "schema": "sana.e14.n1.lifecycle-artifact.v2",
            "artifact_kind": artifact_kind,
            "profile_kind": "P3_N1_CONTROL_CLOSURE_V1",
            "content_root": TYPED_ROOT,
            "payload": payload,
        }
        metrics = _metrics(envelope)
        rows.append(
            {
                "artifact_kind": artifact_kind,
                **metrics,
                "canonical_bytes": len(_canonical(envelope)),
                "indented_bytes": len(
                    json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
                ),
            }
        )

    maxima = {
        field: max(row[field] for row in rows)
        for field in (
            "depth",
            "nodes",
            "members",
            "max_members_in_object",
            "canonical_bytes",
            "indented_bytes",
        )
    }
    checks = {
        "depth_has_2x_headroom": CAPS["depth"] >= 2 * maxima["depth"],
        "nodes_have_2x_headroom": CAPS["nodes"] >= 2 * maxima["nodes"],
        "members_have_2x_headroom": CAPS["members"] >= 2 * maxima["members"],
        "raw_bytes_have_2x_canonical_headroom": CAPS["raw_bytes"] >= 2 * maxima["canonical_bytes"],
        "raw_bytes_exceed_largest_indented": CAPS["raw_bytes"] > maxima["indented_bytes"],
        "fixed_and_dynamic_objects_fit_member_cap": (
            maxima["max_members_in_object"] <= CAPS["members_per_object"]
        ),
    }
    return {
        "schema": "sana.e14.n1-precode-cap-audit.v1",
        "authority_effect": "NONE",
        "schema_path": schema_path.relative_to(ROOT).as_posix(),
        "counting_profile": "P3_N1_V2_COUNTS_V1",
        "caps": CAPS,
        "artifacts": rows,
        "maxima": maxima,
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "limitation": "Schema-derived shapes prove fit for the current draft, not real workload demand.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()
    report = audit(args.schema.resolve())
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
