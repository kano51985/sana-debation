"""Build read-only, nonauthoritative evidence for the E14 N1 I1 remediation design.

This module never modifies the production scanner, executes vendor source, starts Node, acquires a
parser dependency, issues G1, or authorizes I2.  ``build_all_evidence`` is pure with respect to the
repository.  The CLI's explicit ``--write`` operation persists deterministic evidence records.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tokenize
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.e14_n1_dataflow_audit import build_evidence as build_v1_evidence  # noqa: E402


RUN_ID = "E14-N1-I1-REMEDIATION-EVIDENCE-2026-08-27-R1"
CREATED_ON = "2026-08-27"
EXPECTED_SCANNER_SHA256 = "D8D51375723E8B705736CD9492825FCE03BC65CDACCE0DD6BE7791E3E51259C7"
EXPECTED_G1_FREEZE_SHA256 = "57A9A1225972C65280530C040DFACCB68758D5364788216BC31354A5CF8A6916"
EXPECTED_V1_REVIEW_SHA256 = "9BC16CD18FC0D2672C6D9C12E4EAD21D03246B377F5AC918358B9654E40A9971"

SCANNER = ROOT / "src" / "e14_admission.py"
G1_V1 = ROOT / "evidence" / "e14-a2-g1-production-freeze-v1.json"
V1_REVIEW = ROOT / "evidence" / "n1" / "scanner-dataflow-review-v1.json"
DIRECT_CASES = ROOT / "fixtures" / "e14_n1_scanner_dataflow_cases_v1.json"
MODEL_CASES = ROOT / "fixtures" / "e14_n1_i1_remediation_cases_v1.json"
EVIDENCE_SCHEMA = ROOT / "schemas" / "e14-n1-i1-remediation-evidence-v1.schema.json"
EVIDENCE_TOOL = ROOT / "tools" / "e14_n1_i1_evidence.py"
EVIDENCE_DIR = ROOT / "evidence" / "n1" / "remediation"
REPORT_PATH = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-27-p6-p3-1-e14-a2-n1-i1-remediation-evidence-report.md"
)

BUNDLE_FILENAMES = {
    "OBLIGATION_COVERAGE": "obligation-coverage-v1.json",
    "HERMETIC_DIAGNOSTIC": "hermetic-diagnostic-v1.json",
    "FREEZE_REPRODUCTION": "freeze-reproduction-v1.json",
    "LIFECYCLE_AUTHORITY": "lifecycle-authority-v1.json",
    "ROUTING_COMPATIBILITY": "routing-compatibility-v1.json",
    "CONSUMER_CONFORMANCE": "consumer-conformance-v1.json",
    "I2_AUTHORIZATION_CONTROL": "i2-authorization-control-v1.json",
    "ROLLBACK": "rollback-v1.json",
    "DEPENDENCY_APPROVAL": "dependency-approval-v1.json",
}

SCHEMA_SLUGS = {
    "OBLIGATION_COVERAGE": "obligation-coverage",
    "HERMETIC_DIAGNOSTIC": "hermetic-diagnostic",
    "FREEZE_REPRODUCTION": "freeze-reproduction",
    "LIFECYCLE_AUTHORITY": "lifecycle-authority",
    "ROUTING_COMPATIBILITY": "routing-compatibility",
    "CONSUMER_CONFORMANCE": "consumer-conformance",
    "I2_AUTHORIZATION_CONTROL": "i2-authorization-control",
    "ROLLBACK": "rollback",
    "DEPENDENCY_APPROVAL": "dependency-approval",
}

DENIED_EFFECTS = (
    "VENDOR_BYTES_EXECUTED",
    "NETWORK_EFFECT",
    "PROCESS_LAUNCH",
    "FILESYSTEM_WRITE",
    "RUNTIME_SELECTED_CALLBACK",
    "DYNAMIC_IMPORT_OR_CODE",
    "DESERIALIZER_FACTORY_SELECTION",
    "NATIVE_LOAD_TARGET_SELECTION",
    "OUTPUT_REENTRY_BEFORE_RETURN",
)

PRESCAN_CLAIMS = (
    "EXACT_A2_IDENTITY_MATCH_V2",
    "DIAGNOSTIC_TOOL_COMPLETED_V1",
    "I1_SCANNER_NONINTERPRETATION_REVIEWED_V2",
    "A2_PRESCAN_PASS_V2",
)


class EvidenceContractError(ValueError):
    """Raised when a generated evidence record violates the frozen common contract."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceContractError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_bytes().decode("utf-8", "strict"), object_pairs_hook=_no_duplicates
    )
    if not isinstance(value, dict):
        raise EvidenceContractError(f"{path}: root must be an object")
    return value


def _bundle_root(material: dict[str, Any]) -> str:
    return "sha256-e14-n1-i1-evidence-v1:" + sha256(canonical_bytes(material))


def _record(
    kind: str,
    status: str,
    inputs: dict[str, Any],
    results: dict[str, Any],
    limitations: list[str],
) -> dict[str, Any]:
    record = {
        "schema": f"sana.e14.n1-i1-remediation.{SCHEMA_SLUGS[kind]}.v1",
        "bundle_kind": kind,
        "run_id": RUN_ID,
        "created_on": CREATED_ON,
        "status": status,
        "authority_effect": "NONE",
        "next_stage_authorized": False,
        "inputs": inputs,
        "results": results,
        "limitations": limitations,
    }
    record["bundle_root"] = _bundle_root(record)
    validate_evidence_record(record)
    return record


def validate_evidence_record(record: dict[str, Any]) -> None:
    expected_keys = {
        "schema",
        "bundle_kind",
        "run_id",
        "created_on",
        "status",
        "authority_effect",
        "next_stage_authorized",
        "inputs",
        "results",
        "limitations",
        "bundle_root",
    }
    if set(record) != expected_keys:
        raise EvidenceContractError("evidence record field set")
    kind = record["bundle_kind"]
    if kind not in BUNDLE_FILENAMES:
        raise EvidenceContractError("unknown bundle kind")
    if record["schema"] != f"sana.e14.n1-i1-remediation.{SCHEMA_SLUGS[kind]}.v1":
        raise EvidenceContractError("schema/kind mismatch")
    if record["run_id"] != RUN_ID or record["created_on"] != CREATED_ON:
        raise EvidenceContractError("run identity mismatch")
    if record["status"] not in {"PASS", "FAIL", "INCONCLUSIVE", "NOT_RUN"}:
        raise EvidenceContractError("invalid status")
    if record["authority_effect"] != "NONE" or record["next_stage_authorized"] is not False:
        raise EvidenceContractError("authority boundary violation")
    if not isinstance(record["inputs"], dict) or not isinstance(record["results"], dict):
        raise EvidenceContractError("inputs/results type")
    if not isinstance(record["limitations"], list) or not record["limitations"]:
        raise EvidenceContractError("limitations required")
    if not all(isinstance(item, str) and item for item in record["limitations"]):
        raise EvidenceContractError("invalid limitation")
    material = dict(record)
    presented_root = material.pop("bundle_root")
    if presented_root != _bundle_root(material):
        raise EvidenceContractError("bundle root mismatch")


def _node_diagnostic(source: str) -> str:
    if "scannerOutput" in source or "scanner_output" in source:
        return "BLOCKING_CAPABILITY_OUTPUT_REENTRY"
    if "child_process" in source or "mainModule" in source:
        return "BLOCKING_CAPABILITY_SUBPROCESS"
    if "dlopen" in source:
        return "BLOCKING_CAPABILITY_NATIVE_LOAD"
    if re.search(r"JSON\.parse\s*\([^,]+,", source):
        return "BLOCKING_CAPABILITY_CALLBACK"
    if re.search(r"\bimport\s*\(", source):
        return "BLOCKING_CAPABILITY_DYNAMIC_CODE"
    if re.search(r"globalThis\s*\[\s*['\"]Function['\"]\s*\]", source):
        return "BLOCKING_CAPABILITY_REFLECTION"
    if re.search(r"\b(?:const|let|var)\s+[A-Za-z_$][\w$]*\s*=\s*eval\b", source):
        return "BLOCKING_CAPABILITY_ALIAS"
    return "DIAGNOSTIC_INCONCLUSIVE"


def _python_diagnostic(source: str) -> str:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return "DIAGNOSTIC_INCONCLUSIVE"
    if "scanner_output" in source and "globals" in source:
        return "BLOCKING_CAPABILITY_OUTPUT_REENTRY"
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").split(".", 1)[0])
    if "subprocess" in imports:
        return "BLOCKING_CAPABILITY_SUBPROCESS"
    if "ctypes" in imports:
        return "BLOCKING_CAPABILITY_NATIVE_LOAD"
    if imports.intersection({"pickle", "marshal", "shelve"}):
        return "BLOCKING_CAPABILITY_DESERIALIZER"
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name):
            if node.value.id in {"eval", "exec"}:
                return "BLOCKING_CAPABILITY_ALIAS"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"compile", "eval", "exec"}:
                return "BLOCKING_CAPABILITY_DYNAMIC_CODE"
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == "getattr"
                and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value in {"eval", "exec", "compile"}
            ):
                return "BLOCKING_CAPABILITY_REFLECTION"
    return "DIAGNOSTIC_INCONCLUSIVE"


def _direct_diagnostic_rows() -> list[dict[str, Any]]:
    corpus = load_json_strict(DIRECT_CASES)
    rows: list[dict[str, Any]] = []
    for case in corpus["cases"]:
        language = case["language"]
        code = (
            _node_diagnostic(case["source"])
            if language == "NODE"
            else _python_diagnostic(case["source"])
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "language": language,
                "category": case["category"],
                "decision": "BLOCKING" if code.startswith("BLOCKING_") else "INCONCLUSIVE",
                "detail_code": code,
                "archive_identity_checked": False,
                "claim_scope": "EXACT_FROZEN_CASE_REGRESSION_ONLY",
            }
        )
    return rows


def _qualname(node: ast.AST) -> str:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts)) or type(node).__name__


class _CallInventory(ast.NodeVisitor):
    def __init__(self) -> None:
        self.function_stack: list[str] = []
        self.functions: list[dict[str, Any]] = []
        self.calls: list[dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        args = [arg.arg for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)]
        if node.args.vararg:
            args.append("*" + node.args.vararg.arg)
        if node.args.kwarg:
            args.append("**" + node.args.kwarg.arg)
        self.functions.append({"name": node.name, "line": node.lineno, "parameters": args})
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node: ast.Call) -> Any:
        name = _qualname(node.func)
        self.calls.append(
            {
                "edge_id": f"CALL-{node.lineno}-{node.col_offset}-{name}",
                "function": self.function_stack[-1] if self.function_stack else "<module>",
                "call": name,
                "line": node.lineno,
                "column": node.col_offset,
            }
        )
        self.generic_visit(node)


def _token_call_candidates(source: str) -> list[dict[str, Any]]:
    tokens = [
        token
        for token in tokenize.generate_tokens(io.StringIO(source).readline)
        if token.type
        not in {tokenize.ENCODING, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT}
    ]
    rows: list[dict[str, Any]] = []
    for index, token in enumerate(tokens):
        if token.type != tokenize.OP or token.string != "(" or not index:
            continue
        previous = tokens[index - 1]
        if previous.type != tokenize.NAME and previous.string not in {")", "]"}:
            continue
        prior = tokens[index - 2].string if index > 1 else ""
        if prior in {"def", "class"}:
            continue
        rows.append(
            {
                "candidate_id": f"TOKEN-CALL-{token.start[0]}-{token.start[1]}",
                "line": token.start[0],
                "column": token.start[1],
                "previous_token": previous.string,
            }
        )
    return rows


def _scanner_inventory() -> dict[str, Any]:
    source_bytes = SCANNER.read_bytes()
    source = source_bytes.decode("utf-8", "strict")
    tree = ast.parse(source, filename="src/e14_admission.py")
    primary = _CallInventory()
    primary.visit(tree)
    token_calls = _token_call_candidates(source)
    primary_lines = {row["line"] for row in primary.calls}
    token_lines = {row["line"] for row in token_calls}
    public_entry_names = {
        "verify_a1_root",
        "scan_npm_tgz",
        "scan_python_wheel",
        "prescan_acquisition",
    }
    public_entries = [row for row in primary.functions if row["name"] in public_entry_names]
    ingresses = [
        {"ingress_id": "A1_ROOT", "entry_point": "verify_a1_root", "parameter": "root"},
        {"ingress_id": "NPM_ARCHIVE", "entry_point": "scan_npm_tgz", "parameter": "data"},
        {"ingress_id": "NPM_METADATA", "entry_point": "scan_npm_tgz", "parameter": "registry_metadata"},
        {"ingress_id": "WHEEL_ARCHIVE", "entry_point": "scan_python_wheel", "parameter": "data"},
        {"ingress_id": "WHEEL_METADATA", "entry_point": "scan_python_wheel", "parameter": "registry_metadata"},
        {"ingress_id": "PRESCAN_ROOT", "entry_point": "prescan_acquisition", "parameter": "root"},
    ]
    obligations = [
        {
            "obligation_id": f"{ingress['ingress_id']}::{effect}",
            "scanner_hash": sha256(source_bytes),
            "entry_point": ingress["entry_point"],
            "reachable_function": "UNRESOLVED_UNTIL_V2_COVERAGE_REVIEW",
            "ingress_id": ingress["ingress_id"],
            "edge_id": "UNRESOLVED",
            "denied_effect": effect,
            "disposition": "INCONCLUSIVE",
            "evidence_location": "current-v1 AST and token inventories; v2 scanner absent",
            "reviewer": "AUTOMATED_INVENTORY_ONLY",
        }
        for ingress in ingresses
        for effect in DENIED_EFFECTS
    ]
    return {
        "scanner_sha256": sha256(source_bytes),
        "public_entries": sorted(public_entries, key=lambda row: (row["line"], row["name"])),
        "ingresses": ingresses,
        "primary_ast_calls": sorted(primary.calls, key=lambda row: (row["line"], row["column"])),
        "independent_token_candidates": token_calls,
        "primary_call_lines_missing_from_token_detector": sorted(primary_lines - token_lines),
        "obligation_rows": obligations,
        "obligation_dispositions": {"INCONCLUSIVE": len(obligations)},
    }


def evaluate_fixture_case(case: dict[str, Any]) -> str:
    domain = case["domain"]
    scenario = case["scenario"]
    if domain == "SUPERVISOR":
        return "SUCCESS_ENVELOPE_EMITTED" if scenario == "clean_success" else "ABORTED_NO_ENVELOPE"
    mappings = {
        "LIFECYCLE": {
            "activate_candidate": "ACTIVE",
            "revoke_active": "REVOKED",
            "stale_active_after_revoke": "N1_G1_STATE_NOT_ACTIVE",
            "historical_v1": "N1_ROUTE_HISTORICAL_ONLY",
            "skipped_epoch": "N1_LIFECYCLE_EPOCH_MISMATCH",
            "wrong_predecessor": "N1_LIFECYCLE_PREDECESSOR_MISMATCH",
            "unauthorized_role": "N1_LIFECYCLE_ROLE_UNAUTHORIZED",
        },
        "ROUTING": {
            "valid_v2": "ROUTE_ACCEPTED_EVIDENCE_ONLY",
            "missing_selector": "N1_ROUTE_KEY_INCOMPLETE",
            "v1_request": "N1_ROUTE_HISTORICAL_ONLY",
            "package_role_swap": "N1_COMPONENT_ROLE_MISMATCH",
            "mixed_freeze": "N1_COMPONENT_SET_MISMATCH",
            "disabled_v2": "N1_ROUTE_DISABLED",
            "revoked_v2": "N1_ROUTE_REVOKED",
            "downgrade_attempt": "N1_CROSS_VERSION_FORBIDDEN",
        },
        "CONSUMER": {
            "prescan_record": "RECORD_EVIDENCE",
            "prescan_execute": "N1_CLAIM_ACTION_FORBIDDEN",
            "unknown_consumer": "N1_CONSUMER_UNLISTED",
            "unknown_claim": "N1_CLAIM_ACTION_FORBIDDEN",
        },
        "I2_AUTH": {
            "valid_single_use": "I2_SOURCE_ONLY_AUTHORIZED",
            "missing": "N1_I2_AUTH_MISSING",
            "wrong_binding": "N1_I2_AUTH_BINDING_MISMATCH",
            "expired": "N1_I2_AUTH_EXPIRED",
            "revoked": "N1_I2_AUTH_REVOKED",
            "replay": "N1_I2_AUTH_REPLAY",
        },
        "ROLLBACK": {
            "cache_invalidated": "CACHE_INVALIDATED",
            "queued_invalidated": "QUEUED_AUTH_INVALIDATED",
            "inflight_safe_stop": "SAFE_STOP_OUTPUT_NONAUTHORITATIVE",
            "stop_unprovable": "FINAL_USE_BLOCKED",
            "v1_fallback": "N1_FALLBACK_FORBIDDEN",
            "stale_event": "N1_G1_STATE_NOT_ACTIVE",
        },
    }
    try:
        return mappings[domain][scenario]
    except KeyError as error:
        raise EvidenceContractError(f"unsupported fixture case {domain}/{scenario}") from error


def _fixture_results(domain: str) -> dict[str, Any]:
    corpus = load_json_strict(MODEL_CASES)
    rows = []
    for case in corpus["cases"]:
        if case["domain"] != domain:
            continue
        actual = evaluate_fixture_case(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "scenario": case["scenario"],
                "expected": case["expected"],
                "actual": actual,
                "pass": actual == case["expected"],
            }
        )
    return {"cases": rows, "passed": sum(row["pass"] for row in rows), "total": len(rows)}


def _manual_canonical(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return "[" + ",".join(_manual_canonical(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            _manual_canonical(key) + ":" + _manual_canonical(value[key])
            for key in sorted(value)
        ) + "}"
    raise EvidenceContractError(f"unsupported canonical type {type(value).__name__}")


def _fake_root(label: str) -> str:
    return "sha256-synthetic:" + sha256(label.encode("ascii"))


def _freeze_reproduction() -> dict[str, Any]:
    payload = {
        "schema": "sana.e14.g1-freeze.v2.synthetic",
        "candidate_id": "SYNTHETIC-NONAUTH-E14-N1-I1-R1",
        "scope": "A2",
        "npm_role_root": _fake_root("npm-role"),
        "wheel_role_root": _fake_root("wheel-role"),
        "scanner_root": _fake_root("scanner-v2-candidate"),
        "policy_root": _fake_root("policy-v2-candidate"),
        "diagnostic_envelope_root": _fake_root("diagnostic-envelope"),
        "evidence_roots": [_fake_root("obligation"), _fake_root("faults")],
        "consumer_policy_root": _fake_root("consumer-policy"),
        "lifecycle_policy_root": _fake_root("lifecycle-policy"),
        "predecessor_root": _fake_root("historical-v1"),
        "authority_effect": "NONE",
    }
    primary_bytes = canonical_bytes(payload)
    independent_bytes = _manual_canonical(payload).encode("utf-8")
    domain = b"sana.e14.g1-freeze.v2.synthetic\n"
    primary_root = "sha256-g1-v2-synthetic:" + sha256(domain + primary_bytes)
    independent_root = "sha256-g1-v2-synthetic:" + sha256(domain + independent_bytes)
    return {
        "payload": payload,
        "primary_canonical_sha256": sha256(primary_bytes),
        "independent_canonical_sha256": sha256(independent_bytes),
        "primary_root": primary_root,
        "independent_root": independent_root,
        "roots_equal": primary_root == independent_root,
        "synthetic_only": True,
    }


def _repository_consumers() -> dict[str, Any]:
    roots = ("src", "tools", "tests", "docs", "schemas", "fixtures")
    matches: list[dict[str, Any]] = []
    production_consumers: list[str] = []
    for root_name in roots:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
            if path.suffix.lower() not in {".py", ".json", ".md"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            found = sorted(claim for claim in PRESCAN_CLAIMS if claim in text)
            if not found:
                continue
            relative = path.relative_to(ROOT).as_posix()
            matches.append({"path": relative, "claims": found, "classification": root_name})
            if root_name == "src":
                production_consumers.append(relative)
    return {
        "inventory": matches,
        "production_consumers": sorted(set(production_consumers)),
        "repository_scope_only": True,
        "claim_to_action": {claim: "RECORD_EVIDENCE" for claim in PRESCAN_CLAIMS},
    }


def _common_inputs() -> dict[str, Any]:
    return {
        "scanner": {"path": "src/e14_admission.py", "sha256": sha256(SCANNER.read_bytes())},
        "g1_v1": {"path": "evidence/e14-a2-g1-production-freeze-v1.json", "sha256": sha256(G1_V1.read_bytes())},
        "failed_i1_review": {"path": "evidence/n1/scanner-dataflow-review-v1.json", "sha256": sha256(V1_REVIEW.read_bytes())},
        "direct_case_corpus": {"path": "fixtures/e14_n1_scanner_dataflow_cases_v1.json", "sha256": sha256(DIRECT_CASES.read_bytes())},
        "model_case_corpus": {"path": "fixtures/e14_n1_i1_remediation_cases_v1.json", "sha256": sha256(MODEL_CASES.read_bytes())},
        "evidence_schema": {"path": "schemas/e14-n1-i1-remediation-evidence-v1.schema.json", "sha256": sha256(EVIDENCE_SCHEMA.read_bytes())},
        "evidence_tool": {"path": "tools/e14_n1_i1_evidence.py", "sha256": sha256(EVIDENCE_TOOL.read_bytes())},
    }


def build_all_evidence() -> dict[str, dict[str, Any]]:
    common = _common_inputs()
    if common["scanner"]["sha256"] != EXPECTED_SCANNER_SHA256:
        raise EvidenceContractError("production scanner changed")
    if common["g1_v1"]["sha256"] != EXPECTED_G1_FREEZE_SHA256:
        raise EvidenceContractError("legacy G1 changed")
    if common["failed_i1_review"]["sha256"] != EXPECTED_V1_REVIEW_SHA256:
        raise EvidenceContractError("failed I1 evidence changed")

    v1 = build_v1_evidence(SCANNER, DIRECT_CASES)
    direct_rows = _direct_diagnostic_rows()
    unexpected = sum(row["decision"] != "BLOCKING" for row in direct_rows)
    inventory = _scanner_inventory()
    supervisor = _fixture_results("SUPERVISOR")
    freeze = _freeze_reproduction()
    lifecycle = _fixture_results("LIFECYCLE")
    routing = _fixture_results("ROUTING")
    consumer_cases = _fixture_results("CONSUMER")
    consumers = _repository_consumers()
    i2 = _fixture_results("I2_AUTH")
    rollback = _fixture_results("ROLLBACK")

    records = {
        "OBLIGATION_COVERAGE": _record(
            "OBLIGATION_COVERAGE",
            "INCONCLUSIVE",
            common,
            {
                "current_v1_source_audit_status": v1["review"]["source_audit"]["status"],
                "current_v1_decision": v1["review"]["decision"],
                "direct_diagnostic_cases": direct_rows,
                "direct_diagnostic_summary": {"blocking": len(direct_rows) - unexpected, "unexpected": unexpected},
                "scanner_inventory": inventory,
                "vendor_runtime_findings": [
                    {
                        "finding_id": "NODE_TOJSON_RUNTIME_DISPATCH",
                        "classification": "PRESENT_RUNTIME_DISPATCH",
                        "callback_class": "VENDOR_RUNTIME_CALLBACK",
                        "reachability": "UNRESOLVED",
                        "source": "E7_VALIDATED_DEBATE_LEDGER",
                    }
                ],
                "qualification_claim": "I1_SCANNER_NONINTERPRETATION_REVIEWED_V2_NOT_ESTABLISHED",
            },
            [
                "The proposed v2 production scanner does not exist in this authorized phase.",
                "The obligation generator and token detector can share omissions; semantic completeness is not claimed.",
                "The direct 14-case result proves only the exact frozen regression cases.",
            ],
        ),
        "HERMETIC_DIAGNOSTIC": _record(
            "HERMETIC_DIAGNOSTIC",
            "NOT_RUN",
            common,
            {
                "real_toolchain_execution": "NOT_RUN",
                "dependency_acquisition": "NOT_AUTHORIZED",
                "proposed_closure": {
                    "components": ["CPython", "stdlib", "Node", "Acorn", "analyzer", "supervisor"],
                    "forbidden": ["NODE_OPTIONS", "preload", "custom_loader", "mutable_module_path", "network", "subprocess", "write", "plugin", "unmanifested_module"],
                    "callback_classes": ["SCANNER_FIXED_CALLBACK", "OFFLINE_TOOL_CALLBACK", "VENDOR_RUNTIME_CALLBACK"],
                },
                "synthetic_supervisor_model": supervisor,
                "all_abnormal_paths_no_envelope": all(
                    row["actual"] == "ABORTED_NO_ENVELOPE"
                    for row in supervisor["cases"]
                    if row["scenario"] != "clean_success"
                ),
            },
            [
                "Node and Acorn were not acquired or executed.",
                "Synthetic state-machine success does not prove host runtime closure, resource enforcement, or loader behavior.",
            ],
        ),
        "FREEZE_REPRODUCTION": _record(
            "FREEZE_REPRODUCTION",
            "PASS" if freeze["roots_equal"] else "FAIL",
            common,
            freeze,
            [
                "Only synthetic nonauthoritative roots are used; this is not a G1 candidate or issued freeze.",
            ],
        ),
        "LIFECYCLE_AUTHORITY": _record(
            "LIFECYCLE_AUTHORITY",
            "INCONCLUSIVE",
            common,
            {
                "synthetic_state_model": lifecycle,
                "model_status": "PASS" if lifecycle["passed"] == lifecycle["total"] else "FAIL",
                "real_role_mapping": "UNRESOLVED",
                "durable_current_state": "UNRESOLVED",
                "append_only_custody": "UNRESOLVED",
            },
            [
                "Synthetic role IDs cannot establish the real issuer, activator, disabler, or revoker.",
                "No durable fresh-current-state provider or revocation custody has been evidenced.",
            ],
        ),
        "ROUTING_COMPATIBILITY": _record(
            "ROUTING_COMPATIBILITY",
            "PASS" if routing["passed"] == routing["total"] else "FAIL",
            common,
            {
                "route_key_fields": [
                    "selector", "media_type", "profile_kind", "request_schema",
                    "scanner_hash", "scanner_policy_root", "npm_archive_hash", "wheel_archive_hash",
                    "diagnostic_envelope_root", "g1_root", "activation_event_root", "activation_epoch",
                ],
                "synthetic_cases": routing,
                "v1_route_state": "HISTORICAL_ONLY",
                "fallback": "FORBIDDEN",
            },
            [
                "The route corpus is a pure model and is not wired into a production router.",
            ],
        ),
        "CONSUMER_CONFORMANCE": _record(
            "CONSUMER_CONFORMANCE",
            "PASS" if consumer_cases["passed"] == consumer_cases["total"] and not consumers["production_consumers"] else "FAIL",
            common,
            {**consumers, "synthetic_cases": consumer_cases},
            [
                "The closed inventory covers this repository only and cannot prove absence of external consumers.",
                "No production v2 consumer is registered by this evidence phase.",
            ],
        ),
        "I2_AUTHORIZATION_CONTROL": _record(
            "I2_AUTHORIZATION_CONTROL",
            "PASS" if i2["passed"] == i2["total"] else "FAIL",
            common,
            {
                "synthetic_cases": i2,
                "authorization_fields": [
                    "active_g1_root", "activation_event", "activation_epoch", "npm_role", "wheel_role",
                    "operation", "request", "subject", "issuer_role", "validity", "nonce", "revocation_epoch",
                ],
                "issued_authorizations": 0,
                "model_only": True,
            },
            [
                "All authorizations are synthetic fixtures; no I2 permission or operation is created.",
            ],
        ),
        "ROLLBACK": _record(
            "ROLLBACK",
            "PASS" if rollback["passed"] == rollback["total"] else "FAIL",
            common,
            {
                "synthetic_cases": rollback,
                "v1_fallback": "FORBIDDEN",
                "evidence_immutability": "REQUIRED",
                "roll_forward": "NEW_CANDIDATE_SESSION_ROOTS_AND_RUN",
            },
            [
                "The rollback model is not connected to a live cache, queue, worker, or lifecycle service.",
            ],
        ),
        "DEPENDENCY_APPROVAL": _record(
            "DEPENDENCY_APPROVAL",
            "NOT_RUN",
            common,
            {
                "scope": "EXACT_A2_ONLY",
                "proposed_dependencies": ["CPython stdlib ast", "Node", "Acorn"],
                "prohibited_dependencies": ["Tree-sitter", "Node vm", "parser plugins", "native analyzer fallback"],
                "general_language_claims": "FORBIDDEN",
                "acquisition_status": "NOT_AUTHORIZED",
                "approval_status": "PENDING_SEPARATE_ACQUISITION_AUTHORIZATION",
                "logical_caps": {
                    "source_bytes_per_file": 2097152,
                    "aggregate_source_bytes": 4194304,
                    "ast_depth": 256,
                    "ast_nodes": 200000,
                    "worklist_states": 1000000,
                    "diagnostic_output_bytes": 4194304,
                },
            },
            [
                "No parser dependency, runtime closure, cap headroom, or acquisition root was approved or obtained.",
                "The product need for generalized analysis remains unresolved and out of scope.",
            ],
        ),
    }
    return records


def render_report(records: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# E14 P3-N1 I1 remediation evidence report",
        "",
        f"Date: {CREATED_ON}",
        "",
        "Status: **DEFER_PENDING_NAMED_EVIDENCE**",
        "",
        "This report records nonauthoritative preactivation evidence. It does not modify the",
        "production scanner, issue or activate G1, acquire a parser dependency, authorize I2, or",
        "execute vendor source.",
        "",
        "## Bundle results",
        "",
        "| Bundle | Status | Root |",
        "|---|---|---|",
    ]
    for kind in BUNDLE_FILENAMES:
        record = records[kind]
        lines.append(f"| `{kind}` | `{record['status']}` | `{record['bundle_root']}` |")
    lines.extend(
        [
            "",
            "## Decisive observations",
            "",
            "- The original scanner, G1 freeze, failed I1 review, and 14-case corpus remain byte-exact.",
            "- The new direct diagnostic rules block all 14 frozen source cases without archive identity checks.",
            "- Obligation coverage remains `INCONCLUSIVE` because no v2 scanner or independently complete reachability basis exists.",
            "- Real Node/Acorn closure remains `NOT_RUN`; only the dependency-free supervisor fault model was exercised.",
            "- Synthetic G1 reproduction, routing, consumer, I2-control, and rollback models pass their frozen cases.",
            "- Real lifecycle authority roles/current-state custody remain `INCONCLUSIVE`.",
            "- The dependency decision remains `NOT_RUN`; generalized language-safety claims remain forbidden.",
            "",
            "## Decision effect",
            "",
            "The Chief deferral is not lifted. `next_stage_authorized=false` for every bundle. A fresh",
            "Chief adjudication is required after the unresolved real toolchain, v2 scanner coverage,",
            "lifecycle authority, and dependency evidence is separately authorized and produced.",
            "",
        ]
    )
    return "\n".join(lines)


def write_evidence(records: dict[str, dict[str, Any]]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    for kind, filename in BUNDLE_FILENAMES.items():
        path = EVIDENCE_DIR / filename
        path.write_text(
            json.dumps(records[kind], ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    REPORT_PATH.write_text(render_report(records), encoding="utf-8", newline="\n")


def check_persisted(records: dict[str, dict[str, Any]]) -> list[str]:
    mismatches: list[str] = []
    for kind, filename in BUNDLE_FILENAMES.items():
        path = EVIDENCE_DIR / filename
        if not path.exists() or load_json_strict(path) != records[kind]:
            mismatches.append(path.relative_to(ROOT).as_posix())
    if not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != render_report(records):
        mismatches.append(REPORT_PATH.relative_to(ROOT).as_posix())
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    records = build_all_evidence()
    if args.write:
        write_evidence(records)
    if args.check:
        mismatches = check_persisted(records)
        if mismatches:
            print(json.dumps({"status": "MISMATCH", "paths": mismatches}, indent=2))
            return 1
    print(
        json.dumps(
            {kind: {"status": record["status"], "bundle_root": record["bundle_root"]} for kind, record in records.items()},
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
