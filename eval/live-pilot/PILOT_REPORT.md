# F2-short matched live pilot

Date: 2026-08-25  
Status: **VALID MATCHED PILOT — E6 remains incomplete**

This pilot completed one of the twelve required matched cases. It is real behavioral evidence for
`F2-short`, but it is not an E6 pass and cannot establish general non-inferiority.

## Frozen execution conditions

- Parent and all core agents: `gpt-5.6-sol`, reasoning effort `medium`.
- Closed-world, read-only execution with plugins disabled.
- Three distinct core threads per run, all started with `fork_turns=none`.
- Peer and Chief received readiness-only contracts before their permitted exposure stage.
- Common P0, challenge, response, closing, and Chief output ceilings.
- No observed model-sampling retry in either included run. Background model-list refresh timeouts
  were not counted as sampling retries.

Separate prompts and fresh threads establish separately instructed, separately executed roles. They
do not prove cognitive independence; the model family and workspace substrate were shared.

## Blinding and unblinding

The two worker artifacts were independently graded in fresh single-agent sessions with protocol
names and original run IDs redacted. The alias mapping was not used until both schema-valid grades
were frozen:

- `RUN-Q7M2` → `adaptive-axes-v1`
- `RUN-B4K9` → `fixed-three-v1`

Both graders detected `I-F2-DUPLICATE` and `CRIT-F2-SECOND-ORDER`, reported no false no-material or
duplicate closure, accepted the host audit, and assigned trace specificity `1.0`.

## Matched result

| Measure | Fixed three | Adaptive axes |
|---|---:|---:|
| Completed cycles | 3 | 3 |
| Terminal findings | 4 | 5 |
| Chief disposition | `DEFER` | `APPROVE_WITH_REQUIRED_CHANGES` |
| Initial gold issue detected | yes | yes |
| Post-revision critical issue detected | yes | yes |
| False closures | 0 | 0 |
| Trace specificity | 1.0 | 1.0 |
| Audit valid | yes | yes |
| Original run elapsed | 532,655 ms | 622,501 ms |
| Original run total tokens | 94,198 | 62,835 |

For this one pair, adaptive used 31,363 fewer run tokens (33.3% below fixed) but took 89,846 ms
longer (16.9% above fixed) and did not stop before the three-cycle ceiling. Cost and time therefore
point in different directions, and neither compensates for correctness.

The original matched debates consumed 157,033 tokens in total. A fixed-run format-only correction
consumed another 37,006 tokens, and the two blind graders consumed 32,283 tokens (16,469 adaptive
alias; 15,814 fixed alias), for 226,322 tokens across included debate, correction, and grading
work. Invalid earlier infrastructure attempts and the excluded ambiguous fixed run are not included
in these totals. The CLI exposed total tokens rather than a reliable input/output split, so the
result JSONL records those two telemetry fields as `null`.

## Execution audit

Adaptive parent session: `01a03829-2d90-7413-ab01-37845926bcef`

- Proposing TL: `01a03829-d764-7a91-9125-99ec55fc2542`
- Peer TL: `01a0382a-02a3-7890-b260-0d792fb39de6`
- Chief Architect: `01a0382a-1a65-7970-a7ec-8587f816f5df`
- Collaboration calls observed: 3 spawn, 10 follow-up, 11 wait.

Fixed parent session: `01a03840-dc3e-7703-a6b2-56812ad22476`

- Proposing TL: `01a03841-699f-7501-a7cf-c9e3eef9c6cb`
- Peer TL: `01a03841-8411-7b51-8e0d-9ab272436028`
- Chief Architect: `01a03841-9a37-7a12-9caa-da5b3c88cc0f`
- Collaboration calls observed: 3 spawn, 11 follow-up, 14 wait.

The fixed worker originally used `TERMINAL_RECONCILIATION` for a Chief-only finding because the
shared output schema had no fixed Chief stage. The schema was additively extended with
`CHIEF_DECISION`; one same-session format correction changed only that field. No finding content,
status, or disposition changed.

## Interpretation and next gate

This pilot rejects the claim that the revised adaptive protocol is merely roleplay: both included
runs have auditable real subagent threads. It does not show that adaptive routing is better. On
`F2-short`, both protocols found the seeded second-order issue and both used three cycles; their
different Chief dispositions are not themselves a correctness score.

Full E6 still requires the remaining eleven matched cases and fresh blinded grading. Because this
single pair plus grading already consumed substantial time and tokens, expanding to all 24 worker
runs should be an explicit budget decision. A lower-risk next tranche would add the clean case and
one noisy revision-created case before authorizing the full suite.
