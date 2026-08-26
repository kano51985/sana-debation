# P4 closed-world provenance clean-case rerun

Date: 2026-08-25  
Result: **PASS for the bounded clean-case regression; not yet approved for skill migration**

## Outcome

`closed-world-provenance-v1` removed the observed clean-case false-positive behavior in all four
fresh runs. Both short and noisy F3 variants produced empty terminal findings, a Chief `APPROVE`,
and protocol-blinded grades with zero unsupported material findings.

This establishes a candidate repair for the measured clean-case defect. It does not establish that
P4 preserves detection of supplied, post-revision defects, so it is not sufficient to change the
installed skill or claim behavioral non-inferiority.

## Matched results

| Case | Protocol | Cycles | Terminal findings | Chief | Worker tokens | Elapsed |
|---|---|---:|---:|---|---:|---:|
| F3-short | adaptive | 0 | 0 | APPROVE | 40,155 | 199.127 s |
| F3-short | fixed | 3 | 0 | APPROVE | 81,436 | 296.088 s |
| F3-noisy | fixed | 3 | 0 | APPROVE | 54,822 | 373.257 s |
| F3-noisy | adaptive | 0 | 0 | APPROVE | 49,128 | 172.801 s |

Across the two matched cases, adaptive used 89,283 worker tokens and 371.928 seconds; fixed used
136,258 tokens and 669.345 seconds. Adaptive therefore used 46,975 fewer worker tokens (34.5%),
297.417 fewer elapsed seconds (44.4%), and zero rather than six substantive cycles. Zero cycles did
not omit the core roles: it retained Proposing TL, Peer TL initial/terminal inspection, and the
Chief blind terminal scan plus full-record reconciliation.

On the directly comparable F3-short legacy run, P4 changed adaptive from three unsupported
findings / DEFER / one cycle to zero / APPROVE / zero cycles. Fixed changed from eight unsupported
findings / DEFER to zero / APPROVE while remaining at three cycles. F3-noisy is a new noise-
robustness regression and has no legacy matched baseline.

## Blind grading

Aliases were sealed until all four grades were frozen:

| Blind alias | Unsealed run | Unsupported findings | Closed-world disposition | Audit |
|---|---|---:|---|---|
| RUN-R4K2 | F3-short adaptive | 0 | consistent | valid |
| RUN-M7Q9 | F3-short fixed | 0 | consistent | valid |
| RUN-T5B1 | F3-noisy fixed | 0 | consistent | valid |
| RUN-Y8C6 | F3-noisy adaptive | 0 | consistent | valid |

Each grader was a fresh single-agent session with multi-agent execution, plugins, browsing, and
workspace inspection disabled. The four graders used 58,941 tokens. Worker plus grader cost for
this P4 tranche was 284,482 tokens; cumulative evidence-production cost is 887,526 tokens.

## Execution audit

All four worker sessions used exactly three distinct core subagent threads, all created with
`fork_turns=none`. Peer and Chief first returned readiness-only messages before their permitted
exposure. Fixed used one complete-record Chief handoff after round 3. Adaptive used a blind Chief
terminal scan followed by full-record reconciliation. No optional role was added.

One audit-parser limitation was found: it recognized `READY*` but not a one-line natural-language
equivalent such as “Ready; I’ll wait” or “remain blinded.” The parser now accepts only short,
explicit wait/blind acknowledgements and rejects verdict/substantive markers; the added regression
test and the full suite pass.

These facts prove observable thread and prompt separation. They do not prove cognitive
independence.

## What P4 changed

Every causal precondition must be classified as exactly one of `SUPPLIED_FACT`,
`VERIFIED_EVIDENCE`, or `HYPOTHETICAL`. Only the first two may create a material challenge,
consume an adaptive cycle, remain open, enter terminal findings, require evidence or changes, or
affect the Chief disposition. A hypothetical can remain only as a non-blocking limitation.

The prompt generator keeps `legacy-v1` as its default, so prior runs remain reproducible. P4 is an
explicit opt-in contract in the evidence package.

## Remaining gate and authorization boundary

The next minimum gate was executed as `F2-noisy / adaptive`. It failed: the blind grader detected
neither the initial issue nor `CRIT-F2-SECOND-ORDER`. The run silently repaired the baseline in P0
but did not retain resolved detection provenance in terminal findings. See
`P4_DEFECT_PRESERVATION_REPORT.md`.

Do not modify the installed skill, change its default, or request a new binding Chief disposition.
P4 now has positive clean-case evidence and negative defect-preservation evidence; a separately
approved P5 repair is required.
