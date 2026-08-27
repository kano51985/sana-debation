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
| E14 P3-N1 design and D0 fixtures | **DESIGN APPROVED; D0 PASS; V1 DRAFT RETIRED** | Chief approved the additive A2-only dedicated-image control-closure design. A fresh correction review replaced the unissued under-bound v1 envelope with v2; 35 nonauthoritative static cases pass locally. |
| E14 P3-N1 I0 pure verifier | **PASS (SOURCE ONLY)** | Lifecycle-v2 binds schema/kind/profile/payload. The bounded byte parser, restricted canonical encoder, nominal verifier, and explicit use evaluation pass 27 focused tests. Schema-derived maxima retain at least 2x headroom. No live N1 root or authority exists. |
| E14 P3-N1 I1 scanner dataflow | **FAIL — I1_FAIL_STOP** | Scanner hash still matches G1 and scanner source has no execution/network/process/write sink, but the existing analyzers accepted 9/14 required-negative alias, reflection, callback, native/process, and output-reentry cases. Scanner was not modified; I2 is not authorized. |

## Automated result

Command:

```powershell
python -m unittest discover -s tests -v
```

Result: **146 tests passed, 0 failed**.

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
- the P3-N1 lifecycle schema validates all seven artifact kinds and rejects fixture-carried authority,
  guest authority claims, and guest execution during preparation;
- 35 nonauthoritative N1 scenarios preserve strict routing, role separation, dual closure,
  no-guest preparation, nonce/predecessor single use, immutable output identity, candidate
  nonauthority, PASS/DENY/BLOCK separation, revocation, and no-fallback rollback.
- lifecycle-v2 uses nominal route/media types, rejects the retired draft without conversion,
  parses bounded raw bytes without a general JSON DOM parser, binds schema/kind/profile/payload,
  matches an independent restricted-canonical oracle, and evaluates only explicit time/revocation;
- parser boundary tests cover raw bytes, depth, object and total members, decoded key length,
  Unicode scalar/UTF-8 limits, duplicate decoded keys, invalid UTF-8/surrogates, forbidden arrays
  and number forms, deterministic offsets/pointers, immutable verified payloads, and ambient-I/O
  traps.
- I1 reproduces the exact G1 scanner hash, inventories fixed parser/codec/email and ambient runtime
  callback boundaries, and proves the scanner source itself has no execution, network, subprocess,
  native-deserializer, or filesystem-write sink;
- I1 also preserves a fail-closed negative result: only 5/14 source-closure attacks were rejected,
  so analyzer completeness is not established and the evidence cannot advance to I2.

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

The authorized G0-G7 evidence tranche has now frozen the production read-only scanner/schema,
passed 15 A1-PHYS and source/path tests, computed deterministic G3 roots, recorded the dependency,
hook, license, and source-closure decisions, and measured a Docker envelope. The envelope proves
G6 plus process-start network/child/resource/mount controls, but G7 remains
`PARTIAL_BLOCKING_EXTERNAL_MODULE_OBSERVATION` because loaded Python module origins are
guest-reported rather than externally observed. A fresh three-thread debate rejected identity-only
substitution and Chief deferred pending an accountable P3-owner `reaffirm`/`narrow`/`replace`
decision plus net-assurance evidence. G8/G9/A2 remain blocked; no admission root or completion-like
denial terminal was created. See
`docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-g7-observation-gap-debate.md`.

The P3 owner selected the narrow path. A second fresh-thread three-round debate closed all rounds as
`modified`, and the Chief approved `P3_N1_CONTROL_CLOSURE_V1` for design only. The current large
image is ineligible; a future N1 implementation requires a dedicated exact-manifest image, dual
executable-store/input-noninterpretation closure, separated policy/qualification/G8/controller/G9
roles, immutable output reservation, a qualified local CAS ledger, a nonauthoritative candidate,
and external finalization. The D0 document/schema/static-fixture phase is complete. It created no
N1 runtime component, qualification, authorization, admission root, or terminal. See
`docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-p3-n1-control-closure-debate.md` and
`docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-p3-n1-control-closure-spec.md`.

The current repository test result is **146 tests passed, 0 failed**.
