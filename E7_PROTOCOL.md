# E7 Normative Protocol Package

Status: **draft evidence contract; not installed or offered**  
Protocol pairs: `fixed-three-v1/schema-1`, `adaptive-axes-v1/schema-1`  
Normative keywords: **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are binding as written.

## 1. Scope and authority

This contract defines deterministic selection, artifact representation, transitions, duplicate
handling, terminal reconciliation, and Chief handoff. The executable reference is
`src/protocol.py`; JSON wire contracts are in `schemas/`. If prose, schema, and executable
semantics disagree, conformance fails as `PROTOCOL_SPEC_CONFLICT`. No implementation may choose a
preferred interpretation.

Publishing a behavioral change requires a new `protocol_id`. Publishing a representation change
requires a new `schema_version`. Draft P0–P3 revisions are pre-publication history, not compatible
wire versions.

## 2. Protocol resolver

The resolver runs once before manifest creation. Its result is immutable and is copied into every
artifact.

### 2.1 Recognized signals

- Exact structured or inline `protocol=fixed-three-v1` is a fixed signal.
- Exact structured or inline `protocol=adaptive-axes-v1` is an adaptive signal.
- Literal `three-round`, `three round`, `3-round`, `3 round`, `三轮`, or `三轮辩论` is a fixed
  signal.
- An unrecognized explicit `protocol=` token is an unknown signal.
- Absence of all signals is unqualified.

### 2.2 Resolution table

| Fixed signal | Adaptive signal | Unknown signal | Result |
|---|---|---|---|
| no | no | no | `fixed-three-v1` |
| yes | no | no | `fixed-three-v1` |
| no | yes | no | `adaptive-axes-v1` |
| yes | yes | no | `PROTOCOL_SELECTION_CONFLICT` |
| any | any | yes | `UNKNOWN_PROTOCOL` |

`PROTOCOL_SELECTION_CONFLICT` and `UNKNOWN_PROTOCOL` map to `PROTOCOL_INVALID` before substantive
dispatch. The manifest MUST NOT override the resolver. A mismatch is
`PROTOCOL_MANIFEST_MISMATCH → PROTOCOL_INVALID`. Literal three-round semantics remain fixed even if
the unqualified default changes in a future, separately governed selector version.

## 3. Capability acknowledgement

Before P0 or any candidate artifact is exposed, Root, Proposing TL, Peer TL, and Chief Architect
MUST acknowledge the exact `(protocol_id, schema_version)` with `supported=true`. Missing or
mismatched acknowledgement is `CAPABILITY_MISMATCH → PROTOCOL_INVALID`. A static mismatch MUST NOT
be retried without an observed capability change. A readiness acknowledgement contains no
candidate, rebuttal, verdict, or preference.

## 4. Canonical artifacts

Every stored or routed artifact uses the envelope in
`schemas/artifact-envelope.schema.json`.

Canonical JSON:

1. UTF-8 encoding;
2. object keys sorted lexically;
3. array order preserved;
4. explicit nulls preserved;
5. no insignificant whitespace;
6. non-finite numbers forbidden;
7. `artifact_hash` omitted while calculating SHA-256.

`previous_artifact_hash` MUST equal the prior envelope hash in sequence. Unknown fields, enums,
versions, protocols, or transitions fail closed unless the exact schema version defines an
extension point. Hash or chain mismatch is never correctable by rewriting history.

## 5. Fixed protocol

`fixed-three-v1/schema-1` preserves the current literal promise:

```text
RESOLVED → CORE_ACKED → P0_VALID
→ ROUND_1_CLOSED → ROUND_2_CLOSED → ROUND_3_CLOSED
→ CHIEF_DECIDED → COMPLETE
```

Exactly three complete round records are required. Every record MUST contain the mechanism,
rebuttal, realistic failure trace/counterexample, falsifier, itemized Proposing responses, proposal
diff/risk update, Peer closing assessment, verdict, and evidence/risk IDs. Missing fields make the
round invalid. Fixed artifacts MUST NOT be synthesized from adaptive inspections or empty cycles.

## 6. Adaptive protocol

`adaptive-axes-v1/schema-1` preserves three frozen attack axes but routes zero through three
substantive cycles.

```text
RESOLVED → CORE_ACKED → P0_VALID → ATTACK_MAP_VALID
→ {CYCLE_OPEN → CYCLE_CLOSED} 0..3
→ TERMINAL_RECONCILING
→ [CYCLE_OPEN only when cycles_used < 3] | TERMINAL_VALID
→ CHIEF_SCAN_FROZEN → CHIEF_RECONCILED_AND_DECIDED → COMPLETE
```

Any nonterminal state MAY fail as `PROTOCOL_INVALID` or `CORE_ROLE_FAILED`. Unknown, skipped,
reversed, or duplicated transitions fail closed. A fourth substantive cycle is forbidden.

### 6.1 Atomic inspection

Before the first rebuttal is routed, Peer MUST inspect A1–A3 against the same P0 snapshot. Every
axis produces either:

- `MATERIAL_CHALLENGE(issue_id)`; or
- `NO_MATERIAL_OBJECTION` with proposal reference, inspected mechanism, concern tested, evidence and
  risk IDs, reason it is non-material, and a reopen condition.

Silence, timeout, omitted axis, malformed output, or unsupported confidence is never
`NO_MATERIAL_OBJECTION`.

### 6.2 Materiality

A concern is material when it can do at least one of the following:

- violate a named invariant;
- require a behavioral, interface, migration, rollback, or failure-handling change;
- change a named risk state; or
- require named decision-relevant evidence.

If required structured effects are unknown, the result is `MATERIALITY_INDETERMINATE`; it MUST be
routed while budget remains or retained open at the ceiling. Generic caution, confidence,
seniority, preference, or restatement is not material.

### 6.3 Duplicate and new-issue equivalence

Duplicate suppression is fail-closed. Exact structured equality is necessary but not sufficient.
The comparison key includes:

- axis and mechanism;
- affected invariants and behaviors;
- risks and evidence requests;
- failure signature: precondition class, event class, observable-failure class;
- falsifier identity.

A later concern is `DUPLICATE` only when it cites one canonical predecessor, its structured effect
key is identical, every intervening proposal diff is listed and reviewed, and dependency impact is
explicitly `NONE`.

Any different effect key or `DIRECT`/`TRANSITIVE` proposal impact is `NEW_ISSUE`.
Missing predecessor, missing reviewed diff, malformed failure signature, or unknown dependency is
`EQUIVALENCE_INDETERMINATE`; it MUST NOT be closed as duplicate. Valid duplicates consume no
cycle. The original and classification remain in the audit.

### 6.4 Substantive cycle

The deterministic scheduler orders named invariant violations first, then frozen axis order, then
issue creation order. A routed cycle MUST satisfy the same complete-record contract as fixed-three
and MUST identify before/after proposal references. Proposing TL answers each challenged item as
`accepted`, `rejected with evidence`, or `unresolved`. Peer closes with `accepted`, `modified`,
`rejected`, or `unresolved`.

### 6.5 Terminal Peer reconciliation

Before Chief handoff, Peer MUST bind A1–A3 to the exact terminal proposal reference/hash. Each
record lists every intervening diff, semantic dependency, direct/transitive/none impact, evidence,
risks, and one outcome:

- `TERMINAL_EQUIVALENT`;
- `TERMINAL_REINSPECTED_NO_MATERIAL`;
- `TERMINAL_MATERIAL_CHALLENGE`; or
- `OPEN_BUDGET_EXHAUSTED`.

Unchanged axis text is not proof of semantic equivalence. New material findings re-enter routing
when fewer than three cycles were used. At three cycles, they remain visible as
`OPEN_BUDGET_EXHAUSTED`; no fourth response or verdict is fabricated. Any mutation after
reconciliation invalidates all terminal records. Proposal mismatch or twice-malformed required
output is `PROTOCOL_INVALID`.

### 6.6 Two-stage Chief

The fresh Chief uses the same thread for two explicitly separated stages.

Stage 1 receives only the frozen frame, validated evidence, invariants/axes, and terminal proposal.
It MUST NOT receive the AttackMap, issue labels, prior proposals, cycles, Peer reconciliation, risk
register, routing result, or preferences. It freezes a version-bound terminal scan.

Stage 2 receives the complete valid record. Every Stage-1 concern is reconciled as exactly one of:

- `CONFIRMED_OPEN`;
- `RESOLVED_BY_RECORD`;
- `SUPERSEDED_BY_STRONGER_ISSUE`; or
- `INVALIDATED_BY_EVIDENCE`.

Stage 1 is not a fourth cycle: it cannot mutate the proposal, receive a Proposing response, or
issue disposition. Only after Stage 2 may Chief choose the existing binding disposition.

## 7. Retry and typed failures

One focused correction MAY be requested for a malformed known artifact. The original invalid event
remains audited. Unknown protocol/schema/state, capability mismatch, hash mismatch, or selector
conflict is not transient and MUST NOT be retried without a changed external fact.

Required typed outcomes include:

- `PROTOCOL_INVALID` with a stable reason;
- `CORE_ROLE_FAILED`;
- `MATERIALITY_INDETERMINATE`;
- `EQUIVALENCE_INDETERMINATE`;
- `DUPLICATE`;
- `NEW_ISSUE`;
- `OPEN_BUDGET_EXHAUSTED`;
- `TELEMETRY_UNAVAILABLE`.

No unavailable telemetry may be reported as zero. Manager-observed packet size MUST NOT be called
effective model context.

## 8. Compatibility and rollback

- Unqualified selection remains fixed during this evidence phase.
- Literal three-round selection remains fixed permanently.
- Adaptive requires exact opt-in and matching capability acknowledgements.
- Legacy consumers fail closed on adaptive artifacts and never synthesize three rounds.
- Rollback disables adaptive selection or restores the fixed unqualified default. Published
  adaptive artifacts remain readable under their immutable protocol/schema pair.
- Default migration is a separate governance decision and is outside this evidence package.

## 9. Conformance gates

Conformance requires:

1. JSON Schema validation for fixed and adaptive successful artifacts;
2. resolver and transition golden traces for fixed, adaptive 0/1/3 cycles, conflicts, unknowns,
   malformed records, capability mismatch, retries, legacy handling, defer, and rollback;
3. T1–T4 terminal reconciliation tests;
4. duplicate/new/indeterminate classifier tests, including a revision-created second-order issue;
5. deterministic canonical hash and chain tests;
6. the separate E6 matched behavioral evaluation.

Passing structural conformance does not prove behavioral non-inferiority. E6 remains a distinct
Chief gate.
