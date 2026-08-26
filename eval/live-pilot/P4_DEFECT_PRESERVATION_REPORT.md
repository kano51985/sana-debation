# P4 defect-preservation gate

Date: 2026-08-25  
Result: **FAIL — clean-case repair does not yet preserve auditable defect detection**

## Frozen result

The fresh `F2-noisy / adaptive-axes-v1 / closed-world-provenance-v1` worker completed with three
real core subagent threads, but returned zero cycles, zero terminal findings, and Chief `APPROVE`.
The protocol-blinded grader then detected neither the seeded initial issue nor the critical
post-revision issue.

| Measure | Result | Acceptance |
|---|---|---|
| Initial issue `I-F2-DUPLICATE` | miss | detected |
| Critical `CRIT-F2-SECOND-ORDER` | miss | detected |
| False no-material closures | 0 | 0 |
| False duplicate closures | 0 | 0 |
| Trace specificity | 0.0 | 1.0 |
| Host audit | valid | valid |

The sealed alias `RUN-C9P4` was unblinded only after the grade froze. Worker cost was 42,505 tokens
and 289.318 seconds; the grader used 14,972 tokens. This gate added 57,477 tokens, bringing total
evidence-production cost to 945,003 tokens.

## Failure mechanism

The failure is more specific than “P4 ignored every revision.” The Proposing TL silently replaced
the supplied baseline rule — concerns sharing an axis and mechanism ID are duplicates — with a
stronger P0 that also compared a normalized failure contract and treated deduplication as
revision-local. It then correctly applied the supplied P1 change as `REVISION_DELTA` with a new
digest/canonical ID.

That repair never became a resolved terminal finding. Peer and Chief inspected the already-repaired
P0, saw no remaining material issue, and the final artifact lost the provenance that the baseline
and post-revision defects had been found and fixed. The blind grader correctly treats a missing
terminal finding as a miss; it cannot infer detection merely because the final proposal is better.

P4 also made a second semantic mistake: it treated the absence of exact handler severity and
remediation details as a reason not to retain a material finding. Exact severity may remain unknown,
but the supplied fact that handler behavior changed is already sufficient to falsify semantic
equivalence under an unchanged mechanism ID.

## Execution audit

- Parent: `01a03906-9cdb-7ca1-bae0-5d9406a035bf`
- Proposing TL: `01a03907-03ff-7a80-938e-dbfa2dba3825`
- Peer TL: `01a03907-1c56-7b31-8a37-fe77c1ebb918`
- Chief Architect: `01a03907-2e70-7d93-b3c0-6fe55f0df67a`
- all three core threads were distinct and used `fork_turns=none`
- Peer and Chief returned readiness before permitted exposure
- adaptive Chief blind scan preceded full-record reconciliation
- no role retry or role failure was observed
- two model-list refresh timeouts and analytics-delivery failures were observed; the process still
  completed with exit code 0 and a valid terminal artifact

This proves observable execution and prompt separation, not cognitive independence.

## Decision boundary

P4 as written must not be installed. Its clean-case success remains valid, but the combined evidence
shows an overcorrection: it suppresses synthetic hypothetical blockers while allowing preemptive P0
repair and missing implementation detail to erase auditable detection of supplied structural
changes.

Any P5 repair must preserve a baseline-to-P0 issue ledger, treat supplied decision-relevant behavior
change as non-equivalence even when severity details are missing, and retain preemptively resolved
findings in the terminal artifact. A new implementation and rerun require separate approval.
