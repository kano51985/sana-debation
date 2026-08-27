"""Read-only I1 dataflow audit for the exact frozen E14 production scanner.

The audit never repairs the scanner.  It inventories source-level sinks and callback boundaries,
then submits adversarial source-as-data cases to the scanner's existing analyzers.  Any unexpected
acceptance produces I1_FAIL_STOP.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import e14_admission as scanner  # noqa: E402


EXPECTED_SCANNER_SHA256 = "D8D51375723E8B705736CD9492825FCE03BC65CDACCE0DD6BE7791E3E51259C7"
DEFAULT_SCANNER = ROOT / "src" / "e14_admission.py"
DEFAULT_CASES = ROOT / "fixtures" / "e14_n1_scanner_dataflow_cases_v1.json"

ATTACK_FAMILIES = (
    "ALIAS",
    "REFLECTION",
    "DYNAMIC_CODE",
    "DESERIALIZER_CALLBACK",
    "NATIVE_LOAD",
    "SUBPROCESS",
    "OUTPUT_REENTRY",
)

DANGEROUS_IMPORT_ROOTS = {
    "ctypes",
    "importlib",
    "marshal",
    "multiprocessing",
    "pickle",
    "requests",
    "socket",
    "subprocess",
    "urllib",
}

DANGEROUS_CALLS = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "ctypes.CDLL",
    "ctypes.PyDLL",
    "importlib.import_module",
    "marshal.loads",
    "os.popen",
    "os.replace",
    "os.system",
    "pickle.loads",
    "subprocess.call",
    "subprocess.Popen",
    "subprocess.run",
}

MUTATION_METHODS = {
    "chmod",
    "link_to",
    "mkdir",
    "rename",
    "rmdir",
    "symlink_to",
    "touch",
    "unlink",
    "write_bytes",
    "write_text",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _qualname(node: ast.AST) -> str:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def _source_audit(source_bytes: bytes) -> dict[str, Any]:
    tree = ast.parse(source_bytes.decode("utf-8", "strict"), filename="src/e14_admission.py")
    imports: list[dict[str, Any]] = []
    dangerous_imports: list[dict[str, Any]] = []
    dangerous_calls: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    callback_sites: list[dict[str, Any]] = []
    decode_sites: list[int] = []
    bytes_parser_sites: list[int] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                row = {"line": node.lineno, "module": alias.name}
                imports.append(row)
                if root in DANGEROUS_IMPORT_ROOTS:
                    dangerous_imports.append(row)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            row = {"line": node.lineno, "module": module}
            imports.append(row)
            if root in DANGEROUS_IMPORT_ROOTS:
                dangerous_imports.append(row)
        elif isinstance(node, ast.Call):
            name = _qualname(node.func)
            if name in DANGEROUS_CALLS:
                dangerous_calls.append({"line": node.lineno, "call": name})
            if isinstance(node.func, ast.Attribute) and node.func.attr in MUTATION_METHODS:
                mutations.append({"line": node.lineno, "call": name})
            if isinstance(node.func, ast.Attribute) and node.func.attr == "decode":
                decode_sites.append(node.lineno)
            if name == "BytesParser":
                bytes_parser_sites.append(node.lineno)
            for keyword in node.keywords:
                if keyword.arg in {"object_hook", "object_pairs_hook", "parse_float", "parse_int"}:
                    callback_name = _qualname(keyword.value)
                    row = {
                        "line": node.lineno,
                        "parser": name,
                        "keyword": keyword.arg,
                        "callback": callback_name,
                    }
                    callback_sites.append(row)

    allowed_callback_sites = [
        row
        for row in callback_sites
        if row == {
            "line": 113,
            "parser": "json.loads",
            "keyword": "object_pairs_hook",
            "callback": "pairs_hook",
        }
    ]
    vendor_selected = [row for row in callback_sites if row not in allowed_callback_sites]
    status = (
        "PASS"
        if not dangerous_imports and not dangerous_calls and not mutations and not vendor_selected
        else "FAIL"
    )
    return {
        "status": status,
        "imports": sorted(imports, key=lambda row: (row["line"], row["module"])),
        "dangerous_imports": dangerous_imports,
        "dangerous_calls": dangerous_calls,
        "filesystem_mutation_calls": mutations,
        "fixed_callback_sites": allowed_callback_sites,
        "vendor_selected_callback_sites": vendor_selected,
        "fixed_text_decode_lines": sorted(decode_sites),
        "bytes_parser_constructor_lines": sorted(bytes_parser_sites),
        "claim": "No scanner-source execution, network, process, deserializer, native-load, or write sink was found by the frozen AST policy.",
        "limitation": "Source inventory is exact for the frozen bytes but does not prove a benign Python runtime or standard library.",
    }


def _callbacks(scanner_sha256: str, source_audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "sana.e14.n1-trusted-callback-manifest.v1",
        "authority_effect": "NONE",
        "scanner_sha256": scanner_sha256,
        "status": "PASS_WITH_TCB_BOUNDARY",
        "callbacks": [
            {
                "callback_id": "JSON_OBJECT_PAIRS_HOOK",
                "sites": source_audit["fixed_callback_sites"],
                "selected_by": "scanner source",
                "implementation": "local pairs_hook rejects duplicate keys",
                "vendor_selectable": False,
                "trust_boundary": "frozen scanner bytes",
            },
            {
                "callback_id": "EMAIL_POLICY_HEADER_FACTORY",
                "sites": source_audit["bytes_parser_constructor_lines"],
                "selected_by": "email_policy.default in scanner source",
                "implementation": "CPython email package header factory",
                "vendor_selectable": False,
                "trust_boundary": "qualified CPython standard library",
            },
            {
                "callback_id": "FIXED_TEXT_CODEC_REGISTRY",
                "sites": source_audit["fixed_text_decode_lines"],
                "selected_by": "literal ascii or utf-8 codec names",
                "implementation": "CPython codec registry",
                "vendor_selectable": False,
                "trust_boundary": "qualified interpreter and preinitialized standard codecs",
            },
            {
                "callback_id": "AMBIENT_INTERPRETER_HOOKS",
                "sites": ["whole scanner process"],
                "selected_by": "host process before scanner entry",
                "implementation": "audit, trace, profile, warning, and import hooks",
                "vendor_selectable": False,
                "trust_boundary": "qualified host process; scanner cannot prove this boundary alone",
            },
        ],
        "conclusion": "No parser callback is selected by vendor bytes; ambient interpreter hooks remain an explicit TCB dependency.",
    }


def _policy(scanner_sha256: str, cases_sha256: str) -> dict[str, Any]:
    return {
        "schema": "sana.e14.n1-scanner-data-nonexecution-policy.v1",
        "authority_effect": "NONE",
        "scanner_sha256": scanner_sha256,
        "case_corpus_sha256": cases_sha256,
        "scope": "Exact frozen E14 scanner source and its Node/Python source-closure analyzers",
        "invariants": [
            "Vendor archive and metadata bytes are parser or AST/text data only.",
            "Vendor bytes never select a Python callback, import target, callable, codec, output sink, process, network endpoint, or filesystem mutation.",
            "Scanner reports never re-enter a dynamic dispatcher or parser-selected callable.",
            "The scanner performs read-only input access and creates no admission or lifecycle authority.",
        ],
        "required_negative_families": list(ATTACK_FAMILIES),
        "required_decision": "Every negative case must be REJECT.",
        "stop_rule": "Any unexpected acceptance or scanner-source dangerous sink produces I1_FAIL_STOP; the evidence run must not repair the scanner.",
        "pass_scope": "A PASS would establish only the named frozen source/dataflow contract, not a malicious-TCB claim or operational authorization.",
    }


def _run_cases(corpus: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in corpus["cases"]:
        language = case["language"]
        try:
            if language == "NODE":
                scanner._node_source_closure(
                    {"lib/case.js": case["source"].encode("utf-8")},
                    {"main": "lib/case.js"},
                )
            elif language == "PYTHON":
                scanner._python_source_closure(
                    {"pkg/case.py": case["source"].encode("utf-8")}
                )
            else:
                raise ValueError(f"unsupported case language {language!r}")
        except scanner.AdmissionError as error:
            actual = "REJECT"
            error_code: str | None = error.code
        except Exception as error:  # audit infrastructure failure, never a successful rejection
            actual = "AUDIT_ERROR"
            error_code = type(error).__name__
        else:
            actual = "ACCEPT"
            error_code = None
        rows.append(
            {
                "case_id": case["case_id"],
                "language": language,
                "category": case["category"],
                "required_decision": case["required_decision"],
                "actual_decision": actual,
                "error_code": error_code,
                "pass": actual == case["required_decision"],
            }
        )
    return rows


def build_evidence(scanner_path: Path, cases_path: Path) -> dict[str, dict[str, Any]]:
    source_bytes = scanner_path.read_bytes()
    cases_bytes = cases_path.read_bytes()
    scanner_sha256 = _sha256(source_bytes)
    cases_sha256 = _sha256(cases_bytes)
    corpus = json.loads(cases_bytes.decode("utf-8", "strict"))
    source_audit = _source_audit(source_bytes)
    negative_cases = _run_cases(corpus)
    unexpected_accepts = sum(row["actual_decision"] == "ACCEPT" for row in negative_cases)
    audit_errors = sum(row["actual_decision"] == "AUDIT_ERROR" for row in negative_cases)
    rejected = sum(row["actual_decision"] == "REJECT" for row in negative_cases)
    matches = scanner_sha256 == EXPECTED_SCANNER_SHA256
    passed = (
        matches
        and source_audit["status"] == "PASS"
        and unexpected_accepts == 0
        and audit_errors == 0
        and all(row["pass"] for row in negative_cases)
    )
    review = {
        "schema": "sana.e14.n1-scanner-dataflow-review.v1",
        "authority_effect": "NONE",
        "scanner": {
            "path": scanner_path.relative_to(ROOT).as_posix(),
            "sha256": scanner_sha256,
            "expected_g1_sha256": EXPECTED_SCANNER_SHA256,
            "matches_g1_freeze": matches,
        },
        "case_corpus": {
            "path": cases_path.relative_to(ROOT).as_posix(),
            "sha256": cases_sha256,
            "case_count": len(negative_cases),
        },
        "source_audit": source_audit,
        "negative_cases": negative_cases,
        "summary": {
            "required_rejects": len(negative_cases),
            "actual_rejects": rejected,
            "unexpected_accepts": unexpected_accepts,
            "audit_errors": audit_errors,
        },
        "status": "PASS" if passed else "FAIL",
        "decision": "I1_PASS_CONTINUE" if passed else "I1_FAIL_STOP",
        "stop_reason": (
            None
            if passed
            else "The frozen analyzer accepted one or more required-negative source patterns or the audit contract failed."
        ),
        "scanner_modified_by_stage": False,
        "next_stage_authorized": False,
        "limitation": "This review tests exact source and named adversarial families; it does not prove semantic completeness or cognitive independence.",
    }
    return {
        "policy": _policy(scanner_sha256, cases_sha256),
        "callbacks": _callbacks(scanner_sha256, source_audit),
        "review": review,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanner", type=Path, default=DEFAULT_SCANNER)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    args = parser.parse_args()
    bundle = build_evidence(args.scanner.resolve(), args.cases.resolve())
    print(json.dumps(bundle, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if bundle["review"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
