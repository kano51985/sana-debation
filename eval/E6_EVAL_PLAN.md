# E6 Matched Behavioral Evaluation

Status: **designed; live execution not satisfied in the current agent tree**

## Objective

Compare `fixed-three-v1` and `adaptive-axes-v1` on identical seeded decisions without treating
lower token use or fewer cycles as success when correctness, traceability, or adversarial depth
regresses.

The dataset is `e6_cases.jsonl`: six failure families, each in short and deliberately noisy form.
Five families contain a revision-created critical issue; one is a clean additive change that tests
whether either protocol fabricates disagreement.

## Required execution topology

Each protocol/case run requires a new top-level run with:

- the same model family, reasoning setting, tools, neutral evidence, and output limits;
- three fresh real core threads;
- no conversation history from this design debate;
- protocol selection frozen before P0;
- protocol identity hidden from human graders;
- complete audit artifacts retained.

Both arms use the same closed-world worker budget: P0 700 words, Peer challenge/inspection 450,
Proposing response 350, Peer closing 250, and Chief 700. A ceiling never permits omission of a
required trace, falsifier, diff, reconciliation, or disposition. Main and subagent reasoning effort
must be explicitly frozen rather than inherited from ambient user configuration.

Fixed and adaptive order is randomized within each case. Reusing the Proposing, Peer, or Chief
threads from the design debate is forbidden because their context exposes the adaptive hypothesis
and expected failure seeds.

The current task already consumed its static thread identities. Existing agents are therefore not
valid E6 workers, and a fresh Chief cannot be created here. Live E6 must run in new Codex tasks or an
equivalent fresh Responses API harness. This limitation is recorded rather than bypassed.

## Result record

One JSONL record per `(case_id, protocol_id)`:

```json
{
  "case_id": "F1-short",
  "protocol_id": "fixed-three-v1",
  "evidence_kind": "live-real-subagents",
  "detected_issue_ids": ["CRIT-F1-STALE-COVERAGE"],
  "false_no_material_issue_ids": [],
  "false_duplicate_issue_ids": [],
  "unsupported_material_finding_refs": [],
  "audit_valid": true,
  "failure_trace_specificity": 1.0,
  "input_tokens": null,
  "output_tokens": null,
  "elapsed_ms": null,
  "retries": 0
}
```

Unavailable telemetry is `null`, not zero. `failure_trace_specificity` is graded from a frozen
rubric: 1 only when precondition, event, observable failure, affected mechanism, and falsifier are
all concrete and case-linked; 0.5 when exactly one element is generic; 0 otherwise.

For seeded clean cases, `unsupported_material_finding_refs` is required for live records. A fresh
protocol-blinded supplemental grader lists terminal findings that elevate an unsupplied assumption
into a material open risk, blocking evidence gate, or disposition reason despite the closed-world
no-effect contract. Specificity alone cannot make such a finding supported.

## Blinding

Before human grading, replace protocol IDs and run IDs with randomized A/B labels. The mapping is
sealed until issue extraction, trace-specificity grading, and audit-validity grading are frozen.
Graders receive the case contract and terminal artifacts, not the generation prompts or protocol
name.

The live worker prompt is produced by `build_e6_prompt.py`. It removes all seeded and critical
issue IDs plus `grading_notes`; the worker emits neutral finding references under
`e6_run_output.schema.json`. A separate grader, seeing only a randomized run alias, public case
contract, frozen gold rubric, and terminal output, emits `e6_blind_grade.schema.json`. Only after
that grade is frozen may the sealed mapping restore `protocol_id` and feed `grade_e6.py`. A worker
that directly reports gold IDs is contaminated and invalid.

## Gate

`grade_e6.py` enforces:

- every case has one live result for each protocol;
- adaptive has zero seeded critical misses;
- adaptive has zero false `NO_MATERIAL_OBJECTION` or `DUPLICATE` closures;
- adaptive has zero unsupported material findings on seeded clean cases;
- every adaptive audit is structurally valid;
- adaptive post-revision discovery and trace specificity are not below fixed;
- cost, elapsed time, retries, and telemetry availability are reported but never compensate for a
  correctness failure.

Any invariant-affecting miss fails E6 and requires protocol revision plus a complete rerun. Passing
this finite seeded suite does not prove universal non-inferiority or cognitive independence.

## Commands

```powershell
python eval/grade_e6.py --cases eval/e6_cases.jsonl --results <live-results.jsonl>
```

The included synthetic results exercise the grader only:

```powershell
python eval/grade_e6.py --cases eval/e6_cases.jsonl --results fixtures/e6_synthetic_results.jsonl
```

Their expected status is `HARNESS_ONLY`, never `PASS`.
