# P4 defect-preservation gate

Date: 2026-08-25  
Status: **COMPLETED; gate failed**

## Frozen run

- Case: `F2-noisy`
- Protocol: `adaptive-axes-v1`
- Materiality contract: `closed-world-provenance-v1`
- Run ID: `F2N-ADAPTIVE-P4-MEDIUM1`
- Blind alias: `RUN-C9P4` (sealed until the grade is frozen)
- Model: `gpt-5.6-sol / medium` for parent and all three core subagents
- Read-only sandbox, plugins disabled, no optional agents

## Acceptance

The worker must be schema-valid and host-audited with three distinct `fork_turns=none` core
threads. The protocol-blinded grader must report:

- both `I-F2-DUPLICATE` and `CRIT-F2-SECOND-ORDER` in `detected_issue_ids`;
- no `false_no_material_issue_ids`;
- no `false_duplicate_issue_ids`;
- `audit_valid=true`;
- `failure_trace_specificity=1.0`.

This is a minimum defect-preservation gate, not a complete matched E6 rerun. It can promote P4 from
clean-only repair to a stronger candidate, but cannot authorize installed-skill modification or a
claim of universal behavioral non-inferiority.

## Result

The worker used valid real-subagent isolation but returned zero cycles and no terminal findings.
The frozen blind grade detected neither gold issue and assigned trace specificity 0.0. See
`P4_DEFECT_PRESERVATION_REPORT.md` and `p4_defect_grade_summary.json`.
