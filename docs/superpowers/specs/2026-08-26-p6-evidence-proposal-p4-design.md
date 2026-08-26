# P6 evidence proposal P4: admissibility-gated minimum slice

Date: 2026-08-26

Status: written design for whole-spec user review. Implementation and evidence spikes are not
authorized by this document.

Naming note: `P4` here is the fourth proposal revision produced by the P6 specification review. It
is not the repository's earlier product, protocol, or evaluation phase named P4.

## Decision

Replace direct implementation of the comprehensive P6 shadow-authority design with an
admissibility-gated minimum evidence slice.

The prior P6 specification remains an immutable historical baseline. Its mechanisms are retained as
constraints where they protect a named invariant, but they are not all admitted for implementation.
The Chief disposition is `defer pending named evidence`, with checkpoint outcome
`REVISE_SLICE_TO_NAMED_EVIDENCE`.

The next authorized architectural unit is therefore P4 plus an NE1-NE5 acquisition plan. Any local
probe, source addition, consumer implementation, runtime dispatch, configuration change, or production
integration requires a later, explicit authorization.

## Why P4 exists

The reviewed P6 design correctly limited its claims, but it would have created a scanner, registry,
closure monitor, signing system, journal, recovery engine, history service, two consumers, and broad
adversarial matrices before proving that those outputs were admissible to the original decision gate.

Three routed review rounds required these corrections:

1. A top-level worker hash is not an executable or artifact-flow closure. Any stronger claim requires
   dependency, spawn, IPC, sink, final-object, and event-loss evidence.
2. A run-local signature and hash chain cannot prove one unique history. Local replay evidence must be
   capped at `RUN_LOCAL_REPLAY_TESTED` unless an external non-forkable anchor exists.
3. A complete local shadow platform may still leave every actual-integration requirement unchanged.
   Admissibility and decision effect must be established before expanding the mechanism.

P4 preserves the fail-closed corrections while reducing speculative implementation.

## Binding scope classifications

The Chief classified the unresolved evidence as follows:

| Evidence gap | Classification | Maximum effect of P4 |
|---|---|---|
| Compatibility and independent legacy round trip | `LOCAL_SHADOW_NARROWS_ONLY` | Narrows local contract and serialization uncertainty; does not prove deployed compatibility. |
| Authoritative route inventory | `REAL_INTEGRATION_REQUIRED` | P4 cannot close it. |
| Real runtime authority behavior | `REAL_INTEGRATION_REQUIRED` | P4 may test a mechanism but has no closing effect. |
| Actual authority receipt | `REAL_INTEGRATION_REQUIRED` | A P4 receipt is a local executed-process receipt only. |
| Issued replay | `LOCAL_SHADOW_NARROWS_ONLY` | Supports only `RUN_LOCAL_REPLAY_TESTED`. |
| Live lineage | `LOCAL_SHADOW_NARROWS_ONLY` | Narrows local lineage logic; does not prove a live or non-forkable lineage. |
| Clean monetary cost | `EXTERNAL_EVIDENCE_REQUIRED` | Raw usage and resources may be reported; price remains unavailable without an authoritative source. |
| Existing F2/F3 extraction | `ALREADY_SUFFICIENT_FOR_BOUNDED_SCOPE` | Existing numeric token, turn, and summed-duration claims need no P4 rerun. |

No P4 component may emit a status that contradicts this table.

## Invariants

- **I1 — Mutation boundary:** installed skills, Codex/plugin/MCP configuration, production consumers,
  production authority, and external services remain unchanged.
- **I2 — Classification and closure:** an unclassified item, unresolved final object, unmatched edge,
  or unavailable required monitor blocks before artifact creation or delivery.
- **I3 — Authority separation:** non-authority results never become decisive; `NON_P5` receives no
  envelope, payload file, inherited artifact handle, or process start.
- **I4 — Historical compatibility:** v1-v7 raw bytes and existing canonical hashes are immutable.
- **I5 — Ambiguous delivery:** ambiguity produces `INCONCLUSIVE`; recovery never silently resends.
- **I6 — Claim boundary:** local evidence never implies installed, global, production, OS-isolated,
  host-nonforkable, organizationally identified, or priced evidence.
- **I7 — Secret and corpus custody:** consumer private keys, holdout, oracle, and sibling data are not
  present in consumer inputs or final evidence.
- **I8 — Decision ownership:** technical evidence never becomes an approval; a fresh Chief owns every
  disposition and expansion decision.

## Authorization sequence

```text
P4 design + NE1-NE5 acquisition plan
               |
               v
user review of written specifications
               |
               v
separate authorization for bounded evidence acquisition only
               |
               v
NE1-NE5 packet with PASS / FAIL / INCONCLUSIVE per item
               |
               v
fresh Chief re-review
       |                         |
       | defer/stop              | explicit slice approval
       v                         v
retain evidence and stop     implementation plan for minimum slice
                                   |
                                   v
                           separate implementation authorization
```

Evidence acquisition is not slice implementation. Slice implementation is not production
integration. Neither authorization implies the next.

## Five-plane architecture

### 1. Admission plane

The admission plane owns a machine-readable gap classification and claim-effect matrix. Every proposed
component and output claim identifies:

- the evidence gap it addresses;
- the Chief admissibility class;
- the minimum falsifier it enables;
- whether a passing result closes, narrows, or leaves the gap unchanged;
- new trust boundaries and failure modes;
- resource burden, rollback boundary, and stop condition.

An extension beyond the minimum slice requires a `ComponentAdmissionRecord`. It is rejected unless a
fresh Chief has already confirmed that the preceding slice narrowed a named gap and that no smaller
extension can answer the residual question.

### 2. Scope plane

The scope plane is limited to two workers and one denial endpoint. It compiles:

- a bounded `ScopePolicy`;
- a deterministic `DiscoverySnapshot`;
- complete owner attestation over that snapshot;
- one `CoverageContract` per worker and denial endpoint;
- absolute paths, resolved final-object identity, dependency hashes, and allowed edges;
- a closure preflight result before any artifact is created.

The scope plane may report `DECLARED_SLICE_COMPLETE`. It may report
`EXECUTABLE_SLICE_CLOSURE_COMPLETE` only if NE2 proves that every required load, descendant, IPC,
network, sink, and alias/reparse condition is observed or denied without silent event loss. Otherwise
the stronger status is unavailable, not inferred.

### 3. Evidence plane

The evidence plane contains only:

1. one designated current shadow worker;
2. one independently sourced `legacy-contract worker`;
3. one structurally discovered `NON_P5` endpoint used only for pre-serialization denial;
4. a provenance-complete, byte-frozen v1-v7 corpus;
5. a separate control sidecar and unmodified raw payload;
6. child-generated, per-run receipt keys;
7. one clean lineage and one explicitly isolated `FAULT_TEST_ONLY` lineage;
8. one forbidden DLP canary and one safe positive control.

The legacy-contract worker is never described as an existing deployed consumer. The current worker may
emit local `SHADOW_ACCEPTED`; the legacy worker emits `VALIDATION_ONLY`; neither affects a Chief or
production disposition.

### 4. Replay plane

The replay plane uses the minimum mechanism needed for one ambiguous-recovery case and one cooperative
two-run replay case:

- length-framed, canonical, hash-chained journal records;
- durable issue and dispatch intent before input publication;
- temporary receipt, flush, and atomic spool publication;
- recovery from durable state without predecessor memory and without resend;
- one immutable local namespace and genesis-derived lineage identity;
- predecessor manifest/checkpoint/unresolved-attempt commitment;
- history-scoped logical payload and artifact identity;
- a minimal cooperative history head and one successor reservation.

This plane detects presented local reset, replay, or divergence cases. It cannot prove that a same-user
operator did not copy, roll back, hide, or replace the complete history. Its strongest status is
`RUN_LOCAL_REPLAY_TESTED`.

### 5. Verification plane

An independent, public-key-only verification path checks:

- raw and canonical hashes;
- sidecar and receipt signatures;
- receipt-to-attempt and receipt-to-closure binding;
- journal framing, ordering, and terminal reconciliation;
- predecessor and checkpoint continuity;
- canonicalization differential vectors;
- DLP negative and positive controls;
- source and evidence-manifest hashes;
- raw runtime, storage, and usage telemetry.

It cannot sign consumer receipts, issue approval, calculate unsupported money, or upgrade a limitation.

## Minimum slice cases

The slice is exactly seven executable cases:

1. **Compatibility:** every provenance-qualified v1-v7 fixture retains its raw SHA-256 and existing
   canonical hash in both workers.
2. **Receipts:** one current and one legacy-contract receipt are generated by executed child processes,
   independently signed, uniquely bound, and semantically consistent.
3. **Pre-serialization denial:** the selected `NON_P5` endpoint receives no envelope, payload, inherited
   artifact handle, or process start.
4. **Ambiguous recovery:** termination after input visibility but before terminal receipt ingestion
   yields `RUN_INCONCLUSIVE`; clean-process recovery performs no resend.
5. **Cross-run replay:** the second run commits the first predecessor/checkpoint/key-transition roots and
   rejects reissue with the frozen replay failure.
6. **DLP pair:** forbidden canaries are absent from outputs and a safe positive control is detected.
7. **Resource evidence:** wall time, process CPU where available, peak working set where available,
   scanned bytes, journal bytes, receipt bytes, bundle size, and stdout/stderr volume are reported with
   provenance. Monetary cost remains `COST_UNAVAILABLE` without authoritative pricing.

No additional route, worker, lineage, crash window, dashboard, or ecosystem adapter is admitted in the
first slice.

## Minimum contracts

P4 freezes the following contract responsibilities but does not authorize their implementation:

- `AdmissibilityMatrix`: gap classification and permitted decision effect.
- `ComponentAdmissionRecord`: justification and stop boundary for any later extension.
- `ScopePolicy`: roots, exclusions, eligible kinds, path rules, monitor requirements, and resource caps.
- `DiscoverySnapshot`: deterministic items, kinds, hashes, scanner hashes, exclusions, and root hash.
- `OwnerAttestation`: exact one-to-one classification bound to policy and snapshot.
- `CoverageContract`: worker objects, final identities, dependencies, allowed edges, observers, and sinks.
- `CorpusManifest`: v1-v7 provenance, raw hash, existing canonical hash, and expected interpretation.
- `RunInputManifest`: all pre-run inputs, public keys, code hashes, limits, and predecessor commitments.
- `GateDecision`: metadata-only authorization or denial before serialization.
- `ControlSidecar`: run, attempt, route, payload hash, lineage, policy, and issuer signature.
- `ConsumerReceipt`: sidecar/raw/canonical hashes, worker identity, closure root, result, authority effect,
  and child signature.
- `JournalFrame`: length, sequence, previous hash, typed body, and frame hash.
- `LineageCheckpoint`: predecessor, issuer/consumer, artifact, unresolved-attempt, and terminal roots.
- `VerificationReport`: independent results, limitations, and stable evidence references.
- `DecisionEffectMatrix`: actual result mapped to close, narrow, unchanged, or invalid for each gap.

Inputs and outputs use separate manifests. Historical payloads remain opaque raw bytes; they are never
re-serialized into the control sidecar.

## Typed stop and failure behavior

The following classes are sufficient at design level:

- **Admission block:** missing or invalid admissibility, component, corpus, scope, resource, or
  authorization record.
- **Pre-serialization denial:** unclassified, `NON_P5`, mismatched, drifted, unresolved final object,
  unavailable required monitor, or unmatched closure.
- **Integrity invalid:** changed historical hash, canonicalization divergence, invalid signature,
  receipt mismatch, missed positive control, forbidden canary leak, or unexpected negative acceptance.
- **Run inconclusive:** ambiguous input visibility, missing terminal receipt, torn journal/spool state,
  unresolved predecessor, or recovery ambiguity.
- **Decision non-advancement:** every technical case passes but no named evidence gap closes or narrows.

Stable implementation reason codes must be frozen before any executable evidence run. A failed or
inconclusive run is retained; ambiguity is never repaired by deleting history or retrying silently.

## Status model

P4 outputs independent dimensions:

- `integrity_status`: `VALID | INVALID | INCONCLUSIVE`;
- `coverage_status`: `DECLARED_SLICE_COMPLETE | EXECUTABLE_SLICE_CLOSURE_COMPLETE | INCOMPLETE`;
- `replay_status`: `RUN_LOCAL_REPLAY_TESTED | REPLAY_EVIDENCE_INCOMPLETE | REPLAY_EVIDENCE_INVALID`;
- `decision_effect`: `CHIEF_REQUIRED | STOP_DECISION_GATE_NON_ADVANCEMENT`;
- `cost_status`: authoritative amount or `COST_UNAVAILABLE`.

Mandatory limitations remain explicit when applicable:

- `PRODUCTION_ROUTE_UNPROVEN`;
- `PRODUCTION_RUNTIME_UNPROVEN`;
- `PRODUCTION_RECEIPT_UNPROVEN`;
- `NONFORKABLE_HISTORY_UNPROVEN`;
- `OS_ISOLATION_UNPROVEN`;
- `NETWORK_ISOLATION_UNPROVEN`;
- `HOST_LOSS_UNPROVEN`;
- `ORGANIZATIONAL_IDENTITY_UNPROVEN`.

No aggregate `EVIDENCE_COMPLETE` or approval boolean is permitted.

## Resource and observability boundary

The evidence-acquisition authorization must provide numeric probe limits before any probe starts. The
slice implementation authorization must later freeze independent numeric limits for file count, input
bytes, payload bytes, processes, runtime, stdout/stderr, journal, spool, and bundle size. Absence of a
required numeric limit is a pre-run admission block.

Existing F2/F3 token totals remain prior-run evidence and are not added to P4 harness resource totals.
P4 must label summed turn duration separately from wall time and cached input as a subset of input.

## Risks and disposition

| Risk | P4 treatment | Status before evidence |
|---|---|---|
| R1 scope/executable closure omission | Slice-sized contract and NE2 gate | Needs evidence |
| R2 shadow substituted for integration | Binding admissibility table and hard claim caps | Controlled; actual integration still missing |
| R3 hostile same-user substitution | Explicitly outside claim | Unproved |
| R4 ambiguous local recovery | One durable no-resend case | Needs evidence |
| R5 physical host loss | Explicitly outside claim | Unproved |
| R6 corpus provenance | NE1 hard gate | Needs evidence |
| R7 legacy independence overclaim | Rename and narrow effect | Needs provenance evidence |
| R8 DLP interpreted as OS isolation | Separate leak detection from containment | Containment unproved |
| R9 authoritative pricing | `COST_UNAVAILABLE` | External evidence required |
| R10 Windows alias/reparse escape | NE2 final-object and canary gate | Needs evidence |
| R11 excessive mechanism burden | Seven-case cap and NE4 measurement | Needs measurement |
| R12 monitoring blind spot/event loss | NE2 monitor capability gate | Needs evidence |
| R13 cross-run hidden fork | Claim capped to local presented history | Non-forkability unproved |
| R14 canonicalization divergence | NE3 differential gate | Needs evidence |
| R15 decision-gate non-advancement | DecisionEffectMatrix and mandatory stop | Open until fresh Chief review |

## Deferred work

The following are not part of the minimum slice:

- comprehensive installed/plugin/MCP ecosystem inventory adapters;
- execution of every package, report, grader, or extractor path;
- generalized arbitrary-runtime dependency tracing;
- multi-consumer, multi-lineage, merge/split, or exhaustive epoch matrices;
- exhaustive crash-window, history-fork, CAS-stress, or key-transition suites;
- dashboards and generalized evidence services;
- OS/network sandbox claims, physical host-loss tests, or trusted monotonic anchors;
- authoritative price discovery or inferred cost;
- any installed, configured, deployed, or production integration.

These items require their own `ComponentAdmissionRecord`, evidence relevance, and authorization.

## Gates before implementation

The P4 slice must not enter implementation until all conditions hold:

1. the user approves this written specification and the NE1-NE5 acquisition plan;
2. a separate authorization permits bounded evidence acquisition;
3. NE1-NE5 each reports a traceable `PASS`, or a fresh Chief explicitly accepts a named limitation;
4. the fresh Chief chooses an implementation-permitting disposition and names the allowed slice;
5. a detailed implementation plan freezes schemas, reason codes, numeric resource caps, file boundaries,
   verification commands, and rollback behavior;
6. the user separately authorizes that implementation plan.

Failure at any gate retains the evidence and stops. It never widens scope automatically.

## Self-review

- P4 is unambiguously a proposal revision, not the repository's earlier P4 protocol or evaluation.
- The architecture starts with evidence admissibility and does not assume shadow evidence closes actual
  integration gaps.
- The seven cases are bounded and each maps to a named gap or invariant.
- The stronger closure status is unavailable unless NE2 proves the required monitor capability.
- Local signatures and history do not claim organization identity or hidden-fork absence.
- The legacy-contract worker is not called a deployed consumer.
- DLP leak detection is not called OS/network containment.
- Existing native telemetry is not mixed with P4 harness telemetry.
- Missing pricing remains `COST_UNAVAILABLE`.
- Numeric caps are a mandatory authorization input, not an unstated default.
- No implementation, probe, production mutation, or decision authority is implied by this document.

