# Tranche 2 matched behavioral report

Date: 2026-08-25  
Status: **STOPPED ON DECISIVE ADAPTIVE GATE FAILURE**

## Outcome

Three of twelve matched cases are now complete: `F2-short`, `F2-noisy`, and `F3-short`.
All six worker runs used three fresh real core subagent threads and passed the observable isolation
audit. This proves separately instructed, separately executed roles for these runs, not cognitive
independence.

Adaptive found both seeded post-revision critical issues; fixed found one of two. However, both
protocols fabricated material blockers on the seeded clean case. Adaptive produced three
unsupported findings in one cycle; fixed produced eight in three rounds. The adaptive gate
`adaptive_zero_unsupported_material_findings` is therefore false. Remaining cases were not started
because more sampling cannot erase a valid clean-case failure; the protocol must change first.

## Scope correction

The initial tranche recommendation mistakenly called `F6-short` the clean case. Dataset inspection
before dispatch showed that `F6-short` contains a rollback-unreadability seed; `F3-short` is the
actual clean additive case. The run set was corrected to `F3-short + F2-noisy` before any tranche-2
worker launched.

## Unblinded results

| Case | Protocol | Cycles | Findings | Critical detection | Unsupported clean findings | Disposition | Tokens | Elapsed | Sampling retries |
|---|---|---:|---:|---|---:|---|---:|---:|---:|
| F2-short | fixed | 3 | 4 | yes | n/a | `DEFER` | 94,198 | 532,655 ms | 0 |
| F2-short | adaptive | 3 | 5 | yes | n/a | `APPROVE_WITH_REQUIRED_CHANGES` | 62,835 | 622,501 ms | 0 |
| F3-short | fixed | 3 | 8 | n/a | 8 | `DEFER` | 86,958 | 488,184 ms | 2 |
| F3-short | adaptive | 1 | 3 | n/a | 3 | `DEFER` | 71,142 | 309,278 ms | 0 |
| F2-noisy | fixed | 3 | 4 | **miss** | n/a | `APPROVE_WITH_REQUIRED_CHANGES` | 63,977 | 489,784 ms | 0 |
| F2-noisy | adaptive | 3 | 6 | yes | n/a | `APPROVE_WITH_REQUIRED_CHANGES` | 59,170 | 456,301 ms | 0 |

Across the three cases, adaptive used 7 cycles versus fixed's 9, 193,147 worker tokens versus
245,133, and 1,388,080 ms versus 1,510,623 ms. This is 21.2% fewer worker tokens and 8.1% less
elapsed time, but the elapsed comparison is confounded by two websocket sampling retries in the
fixed F3 run. Cost savings do not cure the clean-case correctness failure.

Tranche 2 alone consumed 281,247 worker tokens, 63,802 ordinary blind-grader tokens, and 31,673
clean-case supplemental grader tokens: 376,722 total. Including the earlier matched pair, its blind
grades, and the fixed format-only correction, the included evaluation work totals 603,044 tokens.

## Blinding

The alias mapping was held until each relevant grade was frozen:

- `RUN-L8V3` → `F3-short / adaptive-axes-v1`
- `RUN-H2C7` → `F3-short / fixed-three-v1`
- `RUN-N5R1` → `F2-noisy / fixed-three-v1`
- `RUN-X9D4` → `F2-noisy / adaptive-axes-v1`

Ordinary blind grading found:

- `RUN-N5R1`: initial issue only; the P1 handler change was not bound to a changed observable
  effect, so `CRIT-F2-SECOND-ORDER` was missed and specificity was 0.0.
- `RUN-X9D4`: both issues detected with specificity 1.0.
- Both F3 graders noted that the artifacts raised speculative material objections despite the
  clean contract, but the original schema could not encode a false positive.

The clean-case requirement was already frozen in the dataset (`expected zero material issues` and
`should not fabricate disagreement`). A supplemental protocol-blinded schema repaired that
measurement omission without changing or rerunning the worker artifacts. It classified all three
adaptive findings and all eight fixed findings as unsupported, with both dispositions inconsistent
with the closed world.

## Execution audit

| Run | Parent | Proposing TL | Peer TL | Chief Architect | Calls (spawn/follow-up/wait) |
|---|---|---|---|---|---|
| F3 adaptive | `01a038be-7176-73c3-8086-16cb9d67b282` | `01a038be-e467-7f51-8f95-2ff4531b16e3` | `01a038bf-0002-7231-8287-a005a709b58c` | `01a038bf-1de9-7631-83af-ab27d6e01df8` | 3 / 6 / 8 |
| F3 fixed | `01a038c4-01d0-7612-9086-dccddcfd89e8` | `01a038c4-7fa5-7d52-b05a-887120c32c85` | `01a038c4-9aed-7bf1-b88d-6b759051e656` | `01a038c4-b35c-7b62-aa57-58c3b32c7066` | 3 / 11 / 14 |
| F2 noisy fixed | `01a038cc-61c7-7bd1-aa73-2f697ae647a6` | `01a038cd-0015-7a51-bfcc-2c3e00bee36e` | `01a038cd-199a-7403-a8dc-82ba0b092e87` | `01a038cd-3757-7433-91d9-41be075d6df0` | 3 / 10 / 12 |
| F2 noisy adaptive | `01a038d4-3b50-7b42-b041-032b6400eae3` | `01a038d4-abaf-7eb1-966a-48a56c36754a` | `01a038d4-c4e3-7762-9c22-6f012e8e8b99` | `01a038d4-db9b-7840-91ca-a5c8beffb32b` | 3 / 10 / 14 |

Every run had three distinct core thread IDs, all spawned with `fork_turns=none`. Peer and Chief
first returned bounded readiness messages. Fixed Chief received one complete-record handoff after
round three; adaptive Chief returned a blind terminal scan before full-record reconciliation.

## Root cause and protocol direction

The observed failure is not fake subagents. It is a decision-frame discipline defect shared by
both protocols: P0 and Peer may introduce hypothetical implementation details absent from the
closed-world frame; the Chief contract then converts missing evidence for those self-created
preconditions into mandatory deferral.

The next protocol revision should require every blocking failure trace to label precondition
provenance as `SUPPLIED_FACT`, `VERIFIED_EVIDENCE`, or `HYPOTHETICAL`. A hypothetical precondition
may become a non-blocking implementation note, but cannot create a material objection, consume an
adaptive cycle, or force Chief deferral unless it exposes a named non-negotiable invariant that the
frozen frame actually makes uncertain. P0 must not manufacture new invariants from optional best
practices.

After that revision, rerun only `F3-short` and `F3-noisy` first. The acceptance condition is zero
unsupported material findings and a disposition consistent with the closed world. Only then resume
the remaining defect families. The installed `sana-debation` skill has not been modified.
