# P4 clean-case rerun plan

Date: 2026-08-25  
Status: **COMPLETED; bounded clean-case regression passed**

## Change under test

Worker prompts opt into `closed-world-provenance-v1`; legacy prompt generation remains the default
for reproducibility. Each causal precondition is classified as `SUPPLIED_FACT`,
`VERIFIED_EVIDENCE`, or `HYPOTHETICAL`.

Only supplied or verified preconditions may create a material challenge, adaptive cycle, terminal
finding, evidence requirement, required change, or Chief defer/reject effect. Hypotheticals may
appear only as non-blocking limitations. P0 may not invent topology, consumers, capacity, privacy,
schema composition, or invariants and then treat missing evidence for them as a blocker.

## Frozen order

1. `F3-short / adaptive-axes-v1`
2. `F3-short / fixed-three-v1`
3. `F3-noisy / fixed-three-v1`
4. `F3-noisy / adaptive-axes-v1`

Protocol aliases remain sealed until the four clean blind grades are frozen.

## Frozen execution conditions

- `gpt-5.6-sol / medium` for parent and all subagents
- three fresh `fork_turns=none` core threads; no optional agents
- read-only sandbox; plugins disabled; closed-world packets
- unchanged worker output schema and output ceilings
- clean-case protocol-blinded grader
- fixed must complete three no-material rounds; adaptive should route zero cycles when no
  supplied/verified conflict exists

## Acceptance

Both F3 variants must have:

- zero `unsupported_material_finding_refs` in both arms;
- `disposition_consistent_with_closed_world=true`;
- valid three-thread host audit;
- fixed `cycles_used=3` and adaptive `cycles_used=0`;
- empty terminal findings unless a blind grader identifies a supplied/verified causal conflict.

The installed skill remains unchanged during this rerun.

## Frozen result

All four runs met the acceptance criteria. Adaptive routed zero cycles on both clean cases; fixed
completed three no-material rounds on both. All terminal finding arrays were empty, all Chief
dispositions were `APPROVE`, and all four protocol-blinded clean graders reported zero unsupported
material findings with valid host audits.

See `P4_RERUN_REPORT.md`, `p4_clean_results.jsonl`, and `p4_clean_grade_summary.json`. P4 remains a
candidate until a supplied-fact defect-preservation rerun demonstrates that the stricter provenance
rule does not suppress genuine post-revision findings.
