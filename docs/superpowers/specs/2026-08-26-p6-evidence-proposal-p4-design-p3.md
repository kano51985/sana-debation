# P6 evidence proposal P4/P3: admissibility-gated minimum slice

Date: 2026-08-26

Status: successor specification mechanically incorporating the accepted P1-P3 debate clauses. The
Chief disposition is `approve with required changes` for this written architecture only. This document
does not authorize EA0, probe construction, probe execution, L2 implementation, or production use.

Naming note: `P4` is the fourth proposal revision of the P6 evidence design. `/P3` identifies the final
document candidate produced by the later three-round specification review. Neither name refers to the
repository's earlier product, protocol, or evaluation phase named P4.

## Decision

Use an admissibility-gated minimum evidence slice, but separate written approval, L0 feasibility,
probe construction, probe execution, fresh-Chief review, L2 planning, and L2 implementation into
distinct authorization gates.

The prior files remain immutable historical inputs:

- `2026-08-26-p6-shadow-authority-evidence-design.md`;
- `2026-08-26-p6-evidence-proposal-p4-design.md`;
- `2026-08-26-p6-evidence-proposal-p4-ne1-ne5-acquisition-plan.md`.

This successor resolves the accepted debate findings without modifying those files.

## Binding admissibility classifications

| Evidence gap | Classification | Maximum local effect |
|---|---|---|
| Compatibility and independent legacy round trip | `LOCAL_SHADOW_NARROWS_ONLY` | Narrows local contract/serialization uncertainty; does not prove deployed compatibility. |
| Authoritative route inventory | `REAL_INTEGRATION_REQUIRED` | No local P4 result closes it. |
| Real runtime authority behavior | `REAL_INTEGRATION_REQUIRED` | A local mechanism test has no closing effect. |
| Actual authority receipt | `REAL_INTEGRATION_REQUIRED` | A local executed-process record is not an actual authority receipt. |
| Issued replay | `LOCAL_SHADOW_NARROWS_ONLY` | At most `RUN_LOCAL_REPLAY_TESTED`. |
| Live lineage | `LOCAL_SHADOW_NARROWS_ONLY` | Narrows local logic; does not prove live or non-forkable lineage. |
| Clean monetary cost | `EXTERNAL_EVIDENCE_REQUIRED` | Raw resources may be measured; price requires an authoritative external source. |
| Existing F2/F3 extraction | `ALREADY_SUFFICIENT_FOR_BOUNDED_SCOPE` | Existing numeric token, turn, and summed-duration claims need no P4 rerun. |

No component, report, compiler, or Chief limitation may contradict this table.

## Invariants

- **I1 — Mutation boundary:** installed skills, Codex/plugin/MCP configuration, production consumers,
  production authority, external services, and unrelated user data remain unchanged.
- **I2 — Classification, identity, and closure:** an unclassified item, unresolved final object,
  unmatched edge, unreserved run root, unarmed required control, unverifiable actual image/module,
  detected source drift, or unavailable required monitor blocks before key or input publication. A
  detect-and-quarantine control may support only its exact bounded claim; it cannot support a
  prevent-before-input claim.
- **I3 — Authority and publication separation:** non-authority results never become decisive. `NON_P5`
  receives no envelope, payload file, inherited artifact handle, key, or authorized process start. No
  child receives key or input until authorization, root reservation, controls, final object, actual
  image, and required modules have been verified.
- **I4 — Historical compatibility:** v1-v7 raw bytes and existing canonical hashes are immutable.
- **I5 — Ambiguous delivery:** ambiguity produces `INCONCLUSIVE`; recovery never silently resends.
- **I6 — Claim boundary:** local evidence never implies installed, global, production, OS-isolated,
  host-nonforkable, organizationally identified, cognitively independent, or priced evidence.
- **I7 — Secret and corpus custody:** private keys, holdout, oracle, and sibling data are absent from
  consumer inputs and final evidence except for approved synthetic canaries.
- **I8 — Decision ownership:** evidence never becomes approval; fresh Chief and user gates remain
  mandatory.

## Authorization sequence

```text
written-spec approval
(authorizes no L0, construction, L1 execution, or L2)
        |
        v
EA0: exact bounded L0 authorization
        |
        v
sealed L0 packet + AcquisitionFeasibilityPacket
        |
        +---- stop condition --------------------------+
        |                                               |
        v                                               v
retained EarlyStopReport                  feasible named acquisition
+ dependent INCONCLUSIVE NEs                    |                |
                                                | existing       | construction
                                                | byte-complete  | required
                                                v                v
                                         ExistingProbeBundle  EA1-CONSTRUCT
                                                                 |
                                                                 v
                                                        SealedProbeBuildPacket
                                                |                |
                                                +-------+--------+
                                                        v
                                                  EA1-EXECUTE
                                                        |
                                                        v
                                      full chain + execution-identity checks
                                                        |
                                                        v
                                      sealed raw results + NEReports
                                                        |
                                                        v
                                               fresh Chief review
                                              |                   |
                                              | stop/defer        | named permission
                                              v                   v
                                      retain and stop       L2 implementation plan
                                                                  |
                                                                  v
                                                     separate user authorization
```

EA0 binds exact L0 contracts, source roots, output operations, tools, numeric caps, retention, expiry,
and prohibitions. L0 emits a sealed packet and an `AcquisitionFeasibilityPacket`.

The feasibility packet is mandatory before construction or execution. It binds the exact
`QualifiedCorpus`, provenance gaps, NE2 L0 capability survey, per-NE maximum decision effect, required
primitives and tools, smaller alternatives, bounded estimates, dependency graph, and stop result.

`EA1-CONSTRUCT` authorizes only exact admitted probe-tool build actions. It authorizes no NE execution
and produces no NE `PASS`.

`EA1-EXECUTE` binds EA0, the exact L0 packet, the exact feasibility packet, either an exact existing
bundle or exact sealed build packet, and all contracts, executable bytes, dependencies, tools, oracle,
expected outcomes, reason codes, caps, network policy, and retention rules. Placeholder hashes, future
paths, version ranges, package names, or unbuilt source trees are invalid.

No stage implies or authorizes the next.

## Architecture

### 1. Admission plane

The admission plane owns the binding gap classification and claim-effect matrix. Before construction it
produces an `AcquisitionFeasibilityPacket`. Every proposed tool has a `ProbeToolAdmissionRecord` with:

- exact NE question and falsifier;
- maximum decision effect;
- smallest interface and operation set;
- no-code, existing-tool, one-shot, and constructed alternatives;
- evidence explaining why smaller alternatives are insufficient;
- exact construction inputs and outputs;
- numeric construction caps;
- prohibited P4 boundaries;
- dependencies, stop conditions, retention, and promotion state.

Tool admission fails when the host primitive is unsupported, all possible results leave named gaps
unchanged, a smaller method suffices, construction cannot be numerically bounded, a prohibited P4
component would be implemented, or the maximum claim exceeds the binding admissibility class.

### 2. Scope and execution-identity plane

The declared slice scope contains only one current shadow worker, one legacy-contract worker, and one
`NON_P5` denial endpoint. It uses bounded scope, snapshot, attestation, coverage, absolute/final-object,
dependency, observer, and sink contracts.

A checked path or source hash is not execution identity. Every subprocess follows this monotonic state
machine:

```text
CHAIN_VERIFIED
  -> RUN_ROOT_ATOMICALLY_RESERVED
  -> HARD_CONTROLS_ARMED
  -> EXECUTABLE_FINAL_OBJECT_BOUND
  -> CHILD_CREATED_NONRUNNING
  -> ACTUAL_IMAGE_INITIAL_MODULES_VERIFIED
  -> KEY_INPUT_PUBLISHED
  -> RUNNING
```

Each transition is content-root bound to its predecessor, tool/control hashes, final identities, cap
state, and event-loss state. Skipped, reordered, repeated, reconstructed, or contradictory transitions
invalidate the attempt.

The run root uses fail-if-exists under the authorized parent. Its final identity is retained or
rechecked before publication. Existing paths, collisions, reparse traversal, replacement, identity
ambiguity, or directory reuse stop the attempt.

Required controls expose positive arm acknowledgement before child execution. If a control attaches
after process creation, the child remains nonrunning and input-blind until attachment and
acknowledgement. Unsupported ordering blocks the dependent claim.

The executable/interpreter is resolved to a final-object tuple: final path, volume/filesystem identity,
stable object ID where available, content hash, alias/reparse resolution, and the retained handle, lock,
or equivalent binding through process creation. A requested path and prelaunch hash are insufficient.

The child is created suspended or under an equivalent non-executing guarantee. OS-derived evidence must
verify the actual main image/interpreter and required initial modules. Late loads remain monitored for
the process lifetime. No key, payload, artifact handle, or input path is visible before
`KEY_INPUT_PUBLISHED`.

Every required edge is exactly one of:

- `PREVENT_BEFORE_KEY_INPUT`;
- `DETECT_AND_QUARANTINE_BEFORE_TERMINAL`;
- `UNSUPPORTED_FOR_STRONG_CLOSURE`.

Unsupported capability blocks dependent evidence as `INCONCLUSIVE`. Detection after publication cannot
upgrade a preventive claim.

### 3. Evidence plane

The later seven-case slice remains limited to:

1. one current shadow worker;
2. one independently implemented, provenance-qualified `legacy-contract worker`;
3. one structurally discovered `NON_P5` denial endpoint;
4. a byte-frozen, provenance-qualified v1-v7 corpus;
5. separate control sidecar and unchanged raw bytes;
6. child-generated per-run receipt keys;
7. one clean and one `FAULT_TEST_ONLY` lineage;
8. one forbidden synthetic canary and one safe positive control.

The legacy-contract worker is not a deployed consumer. Its structural separation does not prove
cognitive independence. Current local acceptance and legacy validation affect no Chief or production
authority.

Evidence acquisition before L2 may build only the smallest admitted acquisition utility:

- synthetic host-control/execution-identity canary launcher;
- frozen-contract legacy validator;
- standalone canonicalizer/verifier;
- bounded synthetic canary scanner;
- result sealer/compiler adapter.

Those utilities are evidence tools, not P4 implementation components.

### 4. Replay plane

The eventual minimum slice uses only the mechanism required for one ambiguous-recovery case and one
cooperative two-run replay case: framed canonical records, durable intent, atomic receipt publication,
no-resend recovery, immutable local namespace, predecessor/checkpoint/unresolved commitment,
history-scoped identities, and one successor reservation.

Acquisition tooling may not implement this replay plane. Replay implementation is L2 work after fresh
Chief and user authorization. The strongest later local claim remains `RUN_LOCAL_REPLAY_TESTED`; hidden
fork absence remains unproved.

### 5. Verification plane

Public-data verification checks the complete authorization/content-root chain, raw and canonical hashes,
tool and oracle roots, expected and actual reasons, caps, network mode, controls, execution identity,
event loss, canaries, and report completeness. It cannot sign worker receipts, omit adverse roots,
reconstruct a missing seal, relabel an outcome, widen a claim, calculate unsupported money, or issue
approval.

## Minimum seven-case boundary

| Case | Required gate | Maximum local effect |
|---|---|---|
| Compatibility | Qualified NE1 corpus plus actual L2 conformance | Narrows local compatibility only |
| Receipts | NE3 pass plus actual-path rerun | Local executed-process record only; authority-receipt gap unchanged |
| Pre-serialization denial | NE2 pass for full absence claim | Local gate/closure behavior only |
| Ambiguous recovery | Actual L2 journal/recovery conformance | Local no-resend behavior; host loss unproved |
| Cross-run replay | Actual L2 predecessor/checkpoint conformance | `RUN_LOCAL_REPLAY_TESTED`; nonforkability unproved |
| DLP pair | NE5 method pass plus actual output-channel rerun | Bounded leak detection only |
| Resource evidence | Complete per-case ledger | Burden evidence only; price unavailable |

A blocked case still emits `INCONCLUSIVE/BLOCKED_DEPENDENCY`; it is not replaced. No additional route,
worker, lineage, crash case, dashboard, or ecosystem adapter is admitted automatically.

## Contract inventory

The architecture requires these responsibilities before their applicable stage:

- `AdmissibilityMatrix` and `DecisionEffectMatrix`;
- `ComponentAdmissionRecord` for later scope expansion;
- `EA0AuthorizationManifest`;
- `L0ProbeContract`;
- `SealedL0Packet`;
- `AcquisitionFeasibilityPacket`;
- `ProbeToolAdmissionRecord`;
- `ExistingProbeBundle`;
- `EA1ConstructAuthorization`;
- `SealedProbeBuildPacket`;
- `EA1ExecuteAuthorization`;
- `L1RunManifest`;
- `ProbeContract` and `ProbeCodeDisposition`;
- `ExecutionIdentityContract`;
- `RunRootReservation`;
- `ControlArmRecord`;
- `LaunchBindingRecord` and `LoadedObjectRecord`;
- `ScopePolicy`, `DiscoverySnapshot`, `OwnerAttestation`, and `CoverageContract`;
- `CorpusManifest` and canonical `VectorOracleManifest`;
- `GateDecision`, eventual L2 `ControlSidecar`, and eventual L2 `ConsumerReceipt`;
- `JournalFrame` and `LineageCheckpoint` only at L2;
- `ProbeRunReport`, `NEReport`, `EarlyStopReport`, and `VerificationReport`;
- `ProbePromotionRecord` for any executable reuse.

Logical IDs, filenames, authorization IDs, version labels, or matching summaries do not substitute for
content roots.

## Outcome and decision-effect algebra

Every NE has exactly one evidence outcome:

- `PASS`;
- `FAIL`;
- `INCONCLUSIVE`.

It separately records one decision effect:

- `CLOSES_NAMED_GAP`;
- `NARROWS_NAMED_GAP`;
- `LEAVES_NAMED_GAP_UNCHANGED`;
- `INVALIDATES_NAMED_CLAIM`;
- `STOP_DECISION_GATE_NON_ADVANCEMENT`.

`STOP_DECISION_GATE_NON_ADVANCEMENT` is not a fourth outcome. A valid NE4 measurement packet may be
`PASS` while its decision effect requires stop.

Missing authorization or evidence, blocked dependency, unsealed ancestor, unavailable observation, or
chain mismatch is `INCONCLUSIVE`. An expected-negative supports `PASS` only when its exact authorized
reason occurs, positive controls pass, and the complete chain verifies.

The later slice retains independent integrity, coverage, replay, decision-effect, and cost dimensions.
No aggregate `EVIDENCE_COMPLETE`, approval boolean, or compiler-generated authorization is permitted.

## Typed stop and failure behavior

- **Authorization/chain block:** missing or mismatched content root, permission, cap, tool, oracle,
  expected outcome, reason code, network mode, retention rule, or seal.
- **Feasibility block:** unsupported host primitive, unavailable provenance, no possible decision
  advancement, smaller sufficient method, unbounded construction, or prohibited component boundary.
- **Construction block:** absent, incomplete, cap-stopped, invalid, or unsealed build packet.
- **Execution identity inconclusive:** final-object binding, actual image/module comparison, root identity,
  control order, or loss accounting is unavailable.
- **Execution identity invalid:** substituted image/module, reparse/replacement drift, accepted root
  collision, premature child/key/input, or forged/missing control acknowledgement.
- **Integrity invalid:** changed historical hash, canonical divergence, invalid signature, missed positive
  control, forbidden canary leak, unexpected negative acceptance, or trimmed Chief handoff.
- **Run inconclusive:** ambiguous input visibility, missing terminal result, torn state, unresolved
  predecessor, or recovery ambiguity.
- **Decision non-advancement:** valid evidence changes no named admissible gap.

A prelaunch mismatch returns exactly:

```text
execution_state = NOT_STARTED
outcome = INCONCLUSIVE
reason_code = PRELAUNCH_CHAIN_MISMATCH
decision_effect = LEAVES_NAMED_GAP_UNCHANGED
```

Feasibility and construction stops produce retained `EarlyStopReport` records and dependent
`BLOCKED_FEASIBILITY`, `BLOCKED_CONSTRUCTION`, or `BLOCKED_DEPENDENCY` reports. No adverse result is
repaired by deletion, substitution, automatic tool construction, scope widening, or silent rerun.

## Probe reuse and promotion

The following non-executable artifacts may be reused by exact root: specifications, schemas, contracts,
vectors, expected outcomes, canary definitions, reason codes, capability matrices, raw evidence,
reports, risks, and limitations.

Probe executables are `NOT_ADMITTED_TO_L2` by default. They are retained for audit and may not be
silently discarded, copied, imported, renamed, or promoted.

Executable promotion requires a `ProbePromotionRecord`, fresh Chief review, and user-authorized L2
plan. It binds exact source/binary roots, target component, semantic differences, trust and dependency
review, migration/rollback, retained tests, and actual-path reruns. Even unchanged promoted bytes rerun
all applicable L2 vectors, canaries, execution-identity, failure, and resource cases.

## Explicitly prohibited acquisition components

EA1-CONSTRUCT may not build, retain, or execute an implementation of:

- P4 `ControlSidecar` or `ConsumerReceipt`;
- consumer receipt signer, authority registry, issuer, or gate;
- replay journal;
- lineage, checkpoint, history-head, reservation, or recovery engine;
- retained seven-case slice runner;
- production or installed integration;
- plugin, MCP, external service, or authority adapter.

Crossing a prohibited boundary requires a separate `ComponentAdmissionRecord`, fresh Chief disposition,
and user authorization before construction.

## Resource and observability boundary

Every stage has per-action and aggregate non-negative integer caps. A prohibited dimension has cap `0`;
it is not omitted. Required dimensions include source/read/output objects and bytes, temporary objects,
processes, concurrency, tool/build invocations, wall/CPU time, working set, stdout/stderr, monitor
events/buffers, and explicitly authorized loopback sockets/bytes.

Default network mode is `NONE`. `LOOPBACK_SYNTHETIC_ONLY` requires an explicit separate authorization
and caps. External network, DNS, model calls, privilege elevation, credentials, installed configuration,
plugins, MCPs, and production routes remain prohibited.

Existing F2/F3 usage is prior evidence, not P4 burden. Cached input remains a subset of input and summed
turn duration is not wall time. Missing measurement is `UNAVAILABLE`, never zero. Monetary cost remains
`COST_UNAVAILABLE` without an authoritative price source and rate mapping.

## Risk register

| Risk | P3 treatment | Status |
|---|---|---|
| R1 scope/executable omission | Slice contract plus feasibility/NE2 gates | Needs evidence |
| R2 shadow substituted for integration | Binding classifications and immutable chain; real gaps unchanged | Actual integration missing |
| R3 hostile same-user substitution | Explicitly outside claim | Unproved |
| R4 ambiguous recovery | Later bounded L2 no-resend case | Needs evidence |
| R5 physical host loss | Explicitly outside claim | Unproved |
| R6 corpus provenance | QualifiedCorpus/NE1 gate | Needs evidence |
| R7 legacy independence overclaim | Structural naming and claim cap | Needs evidence |
| R8 DLP interpreted as isolation | Leak detection separated from containment | Containment unproved |
| R9 authoritative pricing | `COST_UNAVAILABLE` | External evidence required |
| R10 Windows alias/reparse escape | Final-object binding, rechecks, canaries | Needs NE2 evidence |
| R11 excessive mechanism burden | Feasibility, smallest-method analysis, construction caps | Needs measurement |
| R12 monitor/event-loss blind spot | Pre-child arming, sequence/loss accounting | Needs NE2 evidence |
| R13 hidden history fork | Local claim cap | Nonforkability unproved |
| R14 canonical divergence | Vector oracle and differential gate | Needs NE3 evidence |
| R15 decision non-advancement | Stop before construction and bind all results | Open until fresh Chief |
| R20 authorization/cap drift | Complete content-root chain | Execution unproved |
| R22 trimmed corpus relabeled complete | QualifiedCorpus inseparable from sealed root | Needs NE1 evidence |
| R25 chain/execution substitution | Chain extends through actual execution identity | Execution unproved |
| R26 L0 output mutation | Sole create-new/append-only root and caps | Filesystem enforcement unproved |
| R27 incomplete Chief handoff | Complete raw/ancestor packet required | Packet implementation unproved |
| R28 check-to-execute substitution | Retained final-object binding and actual-image checks | Needs NE2 evidence |
| R29 controls armed late/unsupported | Ordered nonrunning launch and publication delay | Needs NE2 evidence |
| R30 preauthorization construction | Separate construct/execute authorizations; no placeholders | Contractually mitigated |
| R31 acquisition becomes shadow implementation | Per-tool minimum admission and prohibited components | Open until feasibility review |
| R32 probe/L2 semantic drift | Reuse immutable semantics; gated executable promotion and rerun | Open until L2 |
| R33 cost without decision effect | Preconstruction effect analysis, caps, and mandatory stop | Needs feasibility evidence |

## Gates before L2 implementation

The P4 slice cannot enter implementation until:

1. the user approves this successor specification and its matching acquisition-plan successor; that
   approval authorizes no acquisition;
2. EA0 authorizes exact bounded L0 acquisition;
3. L0 produces a sealed packet and feasibility packet;
4. the feasibility packet does not require stop;
5. every required tool is an exact sealed existing bundle or an EA1-CONSTRUCT-authorized sealed build;
6. EA1-EXECUTE binds the complete exact chain and bytes;
7. every execution passes authorization, root, control-order, identity, cap, and loss checks;
8. all NE outcomes and independent decision effects remain unchanged in the Chief packet;
9. fresh Chief issues an implementation-permitting disposition for the same seven cases;
10. a detailed L2 plan freezes schemas, reasons, caps, components, verification, promotion, reruns, and
    rollback;
11. the user separately authorizes L2.

The Chief may permit a reduced claim only while preserving adverse outcomes, affected cases,
limitations, and risks. The Chief cannot relabel evidence, omit chain artifacts, expand corpus or
closure, convert local evidence to real integration, add components/cases, authorize construction
retrospectively, or promote probe code automatically.

## Rollback and retention

Rollback is gate-local stop, quarantine, and retention, not installed-system reversal. Every retry has
a new run/attempt ID and `supersedes` link. Failed, incomplete, blocked, cap-stopped, and inconclusive
records remain. Private keys are never retained. Synthetic plaintext canary cleanup requires a
separately authorized post-seal retention action and deletion tombstone; manifests, errors, caps, and
terminal state remain.

## Deferred work

Comprehensive ecosystem discovery, every report/grader/extractor path, arbitrary runtime tracing,
multi-consumer/multi-lineage systems, exhaustive crash/fork/epoch/key suites, dashboards, OS/network
containment, physical host-loss testing, trusted monotonic anchors, authoritative price discovery, and
all installed/production integration remain outside P4/P3.

## Accepted-clause conformance map

| Accepted clause | Applied section |
|---|---|
| P1-E1-1 | Authorization sequence |
| P1-E1-2 | Contract inventory |
| P1-E1-3 | Outcome and decision-effect algebra |
| P1-E1-4 | Gates before L2 implementation |
| P1-E1-5 | Risk register R2/R15/R20/R22/R25-R27 |
| P2-E1-1 | Invariants I2/I3 |
| P2-E1-2 | Scope and execution-identity plane |
| P2-E1-3 | Contract inventory |
| P2-E1-4 | Typed stop and failure behavior |
| P2-E1-5 | Risk register R10/R12/R25/R28/R29 |
| P3-E1-1 | Authorization sequence |
| P3-E1-2 | Admission plane |
| P3-E1-3 | Contract inventory |
| P3-E1-4 | Explicitly prohibited acquisition components |
| P3-E1-5 | Gates before L2 implementation |
| P3-E1-6 | Probe reuse and promotion |
| P3-E1-7 | Risk register R11/R15/R30-R33 |

## Self-review

- The current document authorizes no EA0, build, execution, L2, or production action.
- The immutable chain binds L0 packet content, feasibility, exact tool bytes, execution, raw results,
  NE reports, and Chief handoff.
- L0 writes are create-new/content-addressed or declared append-only; no overwrite/delete/reuse.
- Three-valued evidence outcome is separate from decision effect.
- Hash verification is not treated as execution identity.
- Unsupported Windows controls block dependent claims instead of being inferred.
- Acquisition cannot implement P4 receipts, authority, replay, lineage, recovery, or the slice runner.
- Probe executables cannot enter L2 without review, authorization, and actual-path reruns.
- DLP, local keys, local history, usage, and separate instructions are not overstated.
- Real integration gaps remain real-integration requirements.

