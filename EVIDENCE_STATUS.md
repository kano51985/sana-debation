# Evidence Status

Generated under user authorization for evidence production only. The installed
`C:\Users\Administrator\.codex\skills\sana-debation` files were not modified.

## Gate summary

| Gate | Status | Evidence |
|---|---|---|
| T1–T4 terminal reconciliation | **PASS** | Four named executable tests pass. |
| E7 deterministic core | **PASS** | Resolver, schemas, state machines, canonical hashes, capabilities, retry limits, legacy rejection, duplicate/new/indeterminate rules and golden traces pass. |
| E7 operator comprehension | **NOT RUN** | Instrument prepared; no human respondents. |
| E7 independent consumer conformance | **PARTIAL** | Reference implementation and JSON Schema agree locally; no second independent implementation was available. |
| E6 grader/dataset | **PASS AFTER MEASUREMENT REPAIR (harness only)** | Label-free workers and protocol-blinded graders detect critical misses. A discovered clean-case omission was repaired with a supplemental unsupported-finding schema and deterministic gate; synthetic records still cannot report behavioral PASS. |
| E6 live fixed-vs-adaptive evaluation | **PARTIAL 3/12; P4 DEFECT-PRESERVATION FAILED** | P4 passed four fresh F3 clean arms, then missed both gold issues on a fresh F2-noisy adaptive rerun. The repaired P0 lost resolved detection provenance and treated missing handler detail as enough to avoid a structural finding. |
| P5 design Chief disposition | **DEFER PENDING NAMED EVIDENCE** | A fresh real-subagent three-round debate accepted revised A+B as coherent P3 and rejected grader inference, but requires F2/F3, adversarial review, schema/consumer authority, projection, grader, epoch rollback, and cost evidence before approval. |
| P5 bounded implementation/live gates | **PASS** | 67 tests and 18 adversarial traces pass; F2 detects both gold issues at specificity 1.0; F3 short/noisy remain zero-cycle and clean. |
| P5 fresh evidence re-adjudication | **DEFER PENDING NAMED EVIDENCE** | Behavioral/reference gates pass, but real authority-route inventory, runtime enforcement, legacy round-trip, actual receipts/replay, live lineage canary, and end-to-end cost remain incomplete. |

## Automated result

Command:

```powershell
python -m unittest discover -s tests -v
```

Result: **67 tests passed, 0 failed**.

Coverage includes:

- fixed exact-three success and skipped-round failure;
- adaptive zero/one/three-cycle success and fourth-cycle failure;
- selector default, English/Chinese literal fixed selection, adaptive opt-in, conflict and unknown;
- canonical hash stability, tamper detection and hash chaining;
- unknown schema/field failure;
- capability mismatch and one-correction retry ceiling;
- legacy fixed consumer rejection of adaptive artifacts;
- complete-cycle schema enforcement, including required falsifier;
- exact A1/A2/A3 semantic coverage;
- duplicate, new issue, transitive issue and indeterminate equivalence;
- T1 cycle-three transitive finding retained open;
- T2 unchanged axis terminal equivalence;
- T3 below-ceiling material finding requeued;
- T4 malformed or mismatched terminal reconciliation invalidated;
- E6 grader completeness and fail-detection behavior.
- E6 worker prompts exclude gold issue IDs and grading notes; fixed/adaptive contracts remain distinct.
- E6 blind-grader prompts redact protocol and original run ID.
- structured-output schemas avoid unsupported `uniqueItems`, while the deterministic grader rejects duplicate issue IDs explicitly.
- seeded clean cases require protocol-blinded unsupported-finding grading.
- persisted session audits verify three distinct fresh core threads and bounded readiness variants.
- the P4 materiality contract is versioned, keeps legacy generation stable by default, prevents
  hypothetical-only blockers, and permits a zero-cycle adaptive clean result.
- session audits accept tightly bounded natural-language wait/blind acknowledgements without
  accepting verdict-bearing readiness messages.
- P5 captures literal B0, admits deltas before exclusion, preserves stable resolved findings,
  supports candidate-free supplied/verified Peer discoveries, and fails closed on missing links or
  zero-cycle reconciliation of routed findings.
- P5 adversarial fixtures reject generic, copied, unsupported, and already-fixed closure,
  unjustified batching, projection loss, authority bypass, stale epochs, missing acknowledgements,
  receipt mismatch, and future historical interpretation.
- P5 blind graders redact both protocol and materiality-contract IDs.

## E6 harness result

Synthetic grader check status: `HARNESS_ONLY`.

The synthetic fixture intentionally hides `CRIT-F2-SECOND-ORDER` from adaptive in both short and
noisy variants. The grader reports two critical misses, two false duplicate closures, lower
post-revision discovery, and lower trace specificity. This demonstrates that cost/token savings do
not override correctness. It is not evidence about real model behavior.

## Live pilot result

The CLI environment was repaired by updating the globally installed Codex CLI from `0.147.0` to
`0.149.1`; the existing incompatible model cache was refreshed rather than deleted. Earlier failed
and prompt-ambiguous attempts remain excluded in `eval/live-pilot/DIAGNOSTIC.md`.

A later three-case matched tranche completed with three fresh real subagent threads per arm and
protocol-blinded grading. Adaptive detected both seeded critical issues while fixed missed the
noisy post-revision issue. Adaptive also used one rather than three cycles on `F3-short`, but both
protocols fabricated unsupported material blockers on that clean case. See
`eval/live-pilot/TRANCHE2_REPORT.md` and `eval/live-pilot/matched_results_3_cases.jsonl`.

The clean-case failure falsifies the current adaptive non-inferiority gate even though nine pairs
remain. More sampling is paused until precondition provenance and closed-world materiality rules are
revised and the two F3 cases pass. Cognitive independence remains unproven.

The P4 rerun now satisfies that bounded repair gate: both protocols passed F3-short and F3-noisy,
and adaptive used zero substantive cycles while retaining all three real core threads and the Chief
blind scan. Across the two cases adaptive used 34.5% fewer worker tokens and 44.4% less elapsed time
than fixed. See `eval/live-pilot/P4_RERUN_REPORT.md`.

This does not erase the legacy result or complete E6. The required F2-noisy defect-preservation run
was executed and failed: zero terminal findings, neither gold issue detected, specificity 0.0. See
`eval/live-pilot/P4_DEFECT_PRESERVATION_REPORT.md`.

## Remaining authorization boundary

No skill update, offering, rollout, default change, or claim of behavioral non-inferiority is
authorized by these partial results. P4 must not become an installed default. A separately approved
P5 must preserve baseline-to-P0 resolved finding provenance and recognize supplied behavioral
change as non-equivalence before repeating the F2/F3 gates. Only after broader E6 and the
operator/consumer portions of E7 are complete should a new fresh Chief issue the binding
disposition.

The P5 design debate has now produced that fresh Chief disposition, but it is `defer pending named
evidence`, not implementation approval. The unchanged P3 and full evidence list are in
`eval/live-pilot/P5_DESIGN_DEBATE_RAW.md`; observable thread IDs and retry corrections are in
`eval/live-pilot/P5_DESIGN_DEBATE_AUDIT.json`.

The authorized P5 evidence tranche subsequently passed its bounded F2/F3 and deterministic gates.
The new fresh Chief still deferred installation/offer because production authority and cost evidence
remain missing. See `eval/live-pilot/P5_IMPLEMENTATION_REPORT.md` and
`eval/live-pilot/P5_EVIDENCE_REVIEW_PACKET.md`.

## E14 acquisition and admission status

The corrected A1 runner v3 completed against a new immutable root. G1 passed after recomputing all
inventory hashes, npm SRI/SHA-1, PyPI wheel SHA-256/size, package identities, RFC/errata identities,
runtime identity, response counts, and caps. The successful root is `e14/vendor-acquisition-v2`;
the earlier `vendor-acquisition-v1` failure remains retained and `INCONCLUSIVE`. See
`docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a1-g1-pass-review.md`.

A fresh three-thread A2 architecture debate then closed all three rounds as `modified`, but the
Chief disposition is `defer pending named evidence`. The final P3 requires evidence for the
production physical archive scanner, source-level runtime dependency closure, and an externally
measured process-start network/child isolation envelope with an independently measured terminal
finalizer. No A2 runner or `e14/vendor-admission-v1` root has been created, and G2/B0/F0/R0 remain
unauthorized. See
`docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-admission-design-debate.md`.
