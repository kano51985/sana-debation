# Tranche 2 frozen plan

Date: 2026-08-25  
Status: **COMPLETED; stopped on decisive adaptive clean-case failure**

## Scope correction

The prior recommendation incorrectly described `F6-short` as the clean additive case. Inspection
of the frozen dataset showed that `F6-short` contains the critical rollback-unreadability seed. The
actual clean, no-gold-issue case is `F3-short`. The authorized objective was to test fabricated
disagreement and adaptive early stopping, so this tranche uses `F3-short` plus the separately named
`F2-noisy`. No worker run had started when the correction was made.

## Frozen order

1. `F3-short / adaptive-axes-v1`
2. `F3-short / fixed-three-v1`
3. `F2-noisy / fixed-three-v1`
4. `F2-noisy / adaptive-axes-v1`

The cross-over ordering balances simple clock-order effects. Protocol/run aliases remain sealed
until all four blind grades are frozen.

## Frozen conditions

- model: `gpt-5.6-sol`
- parent reasoning: `medium`
- default subagent model/reasoning: `gpt-5.6-sol / medium`
- sandbox: read-only
- plugins: disabled
- subagent ceiling: three
- three fresh core threads required; no optional agents
- label-free closed-world worker packet
- protocol-name-blinded fresh single-agent grader per artifact
- no model-sampling retry unless the protocol's one focused format-correction rule applies

The installed skill remains unchanged. This tranche evaluates behavior only.
