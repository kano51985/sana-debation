# Sana adaptive-round evidence package

This package implements the evidence requested by the Chief Architect after the debate over
fixed-three versus adaptive routed cycles. It is deliberately separate from the installed skill.

## Contents

- `E7_PROTOCOL.md` — normative resolver, state, artifact, duplicate, terminal and Chief contract.
- `schemas/` — JSON Schema 2020-12 contracts for envelopes and fixed/adaptive runs.
- `src/protocol.py` — executable fail-closed reference semantics.
- `fixtures/golden_traces.json` — resolver and 0/1/3-cycle transition traces.
- `tests/test_protocol.py` — E7 and T1–T4 tests.
- `eval/e6_cases.jsonl` — six seeded failure families in short/noisy variants.
- `eval/build_e6_prompt.py` — creates label-free worker prompts without gold issue IDs.
- `eval/e6_run_output.schema.json` and `eval/e6_blind_grade.schema.json` — separate worker and blind-grader contracts.
- `eval/grade_e6.py` — deterministic matched-result grader.
- `eval/live-pilot/DIAGNOSTIC.md` — excluded-attempt record and recovered pilot diagnostics.
- `eval/live-pilot/PILOT_REPORT.md` — valid matched `F2-short` live-pilot audit and interpretation.
- `eval/live-pilot/f2_short_pilot_results.jsonl` — unblinded two-record partial E6 input.
- `eval/live-pilot/f2_short_partial_grade.json` — deterministic partial grade; intentionally `HARNESS_ONLY` because 22 records are missing.
- `eval/live-pilot/TRANCHE2_REPORT.md` — three-case matched result, clean-case failure, execution audit, and protocol direction.
- `eval/live-pilot/matched_results_3_cases.jsonl` — six unblinded live result records.
- `eval/live-pilot/matched_3_cases_partial_grade.json` — deterministic three-case partial grade.
- `eval/live-pilot/P4_RERUN_REPORT.md` — P4 closed-world provenance clean-case rerun and migration boundary.
- `eval/live-pilot/p4_clean_results.jsonl` — four unblinded P4 clean-run summaries.
- `eval/live-pilot/p4_clean_grade_summary.json` — frozen blind-grade acceptance and cost summary.
- `eval/live-pilot/p4_session_audits.json` — observable parent/child thread IDs, timing, tokens, and routing-call counts.
- `eval/live-pilot/P4_DEFECT_PRESERVATION_REPORT.md` — failed P4 F2-noisy detection gate and causal diagnosis.
- `eval/live-pilot/p4_defect_grade_summary.json` — frozen defect-grade acceptance result and cost.
- `eval/live-pilot/p4_defect_session_audit.json` — F2-noisy P4 host audit and non-fatal host warnings.
- `eval/live-pilot/P5_DESIGN_DEBATE_RAW.md` — complete three-round P5 design debate and Chief disposition.
- `eval/live-pilot/P5_DESIGN_DEBATE_AUDIT.json` — persisted parent/child IDs, readiness evidence, timing, and retry correction.
- `eval/live-pilot/P5_IMPLEMENTATION_REPORT.md` — P5 deterministic/live evidence, excluded attempts, fresh-Chief re-adjudication, and remaining boundary.
- `eval/live-pilot/P5_EVIDENCE_REVIEW_PACKET.md` — frozen eleven-package PASS/PARTIAL/NOT PROVIDED matrix submitted to the fresh Chief.
- `src/p5_protocol.py` and `schemas/adaptive-axes-v2.schema.json` — separate P5 reference semantics and canonical V2 schema; legacy behavior remains unchanged.
- `fixtures/p5_adversarial_traces.json` — 18 P5 adversarial and positive-control traces.
- `docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-p3-n1-control-closure-debate.md` — auditable three-round N1 decision record and Chief disposition.
- `docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-n1-i0-hash-envelope-correction-debate.md` — fresh three-round correction of the unissued hash envelope and I0 boundary.
- `docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-p3-n1-control-closure-spec.md` — approved A2-only N1 lifecycle, closure, authority, outcome, and rollback contract.
- `docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-p3-n1-implementation-plan.md` — staged tool-first implementation and evidence plan; it grants no operational authority.
- `schemas/e14-a2-n1-lifecycle-v2.schema.json` — corrected strict seven-kind N1 lifecycle artifact schema; draft v1 is retired and rejected.
- `tools/e14_n1_precode_audit.py` and `evidence/e14-n1-v2-precode-cap-report-v1.json` — reproducible schema-shape headroom audit.
- `evidence/e14-n1-draft-v1-retirement-v1.json` — file-level v1 retirement and no-issued-root inventory.
- `src/e14_n1_artifacts.py` — pure nominal route, bounded raw-byte parser, restricted canonical encoder, root verifier, and explicit use evaluation.
- `tests/test_e14_n1_artifacts.py` — independent root/canonical oracle, schema-parity, boundary, failure, anti-forgery, revocation, and purity tests.
- `docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-n1-i0-implementation-report.md` — I0 evidence and remaining authority boundary.
- `tools/e14_n1_dataflow_audit.py` and `fixtures/e14_n1_scanner_dataflow_cases_v1.json` — read-only I1 source/callback audit and 14 adversarial cases.
- `evidence/n1/` — I1 nonexecution policy, trusted-callback manifest, and reproducible `I1_FAIL_STOP` review.
- `tests/test_e14_n1_scanner_dataflow.py` — scanner-hash, callback, attack-family, purity, and evidence-reproduction tests.
- `docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-n1-i1-scanner-dataflow-report.md` — I1 result and remediation boundary.
- `fixtures/e14_n1_static_cases_v1.json` — 35 nonauthoritative routing, closure, replay, output, finalization, and rollback scenarios.
- `tests/test_e14_n1_static_fixtures.py` — test-only schema and static-fixture conformance oracle; not an N1 runtime component.
- `fixtures/e6_synthetic_results.jsonl` — intentionally synthetic failing data used only to test the grader.
- `eval/operator_comprehension.md` — blinded operator instrument.
- `EVIDENCE_STATUS.md` — authoritative gate status and limitations.

## Run structural evidence

```powershell
cd C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence
python -m unittest discover -s tests -v
```

Expected: 148 tests, all passing.

## Run the E6 grader harness

```powershell
python eval\grade_e6.py --cases eval\e6_cases.jsonl --results fixtures\e6_synthetic_results.jsonl
```

Expected status: `HARNESS_ONLY`. Synthetic results can never satisfy E6.

## What is and is not proven

The package proves that the proposed deterministic resolver, schemas, state transitions, hash
rules, duplicate classifier, retry ceiling, and terminal reconciliation have an executable,
locally consistent specification for the included golden traces. T1–T4 pass.

Three valid matched pairs prove that the host can execute separately instructed fresh core threads.
Adaptive found both seeded critical issues and reduced cycle count on the clean case, but it still
fabricated three unsupported blockers there; fixed fabricated eight. The current adaptive protocol
therefore does **not** satisfy behavioral non-inferiority. It also does not prove cognitive
independence, anchoring removal, or operator comprehension. See `EVIDENCE_STATUS.md` for the revised
gate and stopping condition.

The opt-in P4 `closed-world-provenance-v1` repair subsequently passed F3-short and F3-noisy in both
arms with zero unsupported material findings. Adaptive used zero substantive cycles while fixed
used six across the pair, but all runs still used three real core threads. This is clean-case
evidence only. The subsequent F2-noisy defect-preservation rerun failed because the improved P0
silently repaired the baseline without retaining resolved findings; P4 must not be installed as-is.
