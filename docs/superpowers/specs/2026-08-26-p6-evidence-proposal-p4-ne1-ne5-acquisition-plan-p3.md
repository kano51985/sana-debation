# P6 evidence proposal P4/P3: NE1-NE5 acquisition plan

Date: 2026-08-26

Status: successor acquisition specification mechanically incorporating the accepted P1-P3 debate
clauses. This document authorizes no L0 acquisition, probe construction, probe execution, L2
implementation, network/model call, or external mutation.

## Objective

Produce a bounded and immutable packet for:

- **NE1:** corpus and worker provenance;
- **NE2:** Windows closure capability;
- **NE3:** canonicalization differential behavior;
- **NE4:** burden and decision advancement;
- **NE5:** positive/negative control validity.

Every NE ends as `PASS`, `FAIL`, or `INCONCLUSIVE` and separately records its decision effect. Missing,
ambiguous, blocked, cap-stopped, or unsupported evidence never passes. The unchanged complete packet
goes to a fresh Chief before any seven-case L2 implementation plan.

## Authorization boundary

The current authorization covers this written document only. Evidence acquisition has three separately
authorized stages.

### EA0 — L0 acquisition authorization

EA0 binds:

- hashes of the approved P3 design and acquisition specifications;
- every exact `L0ProbeContract`;
- exact source-read roots and exclusions;
- source-snapshot algorithm;
- one sole output root under the authorized `outputs` tree;
- permitted output operations;
- acquisition/hashing/inspection tool identities and hashes;
- per-action and aggregate numeric caps;
- retention, terminal-seal, issue/expiry, and prohibition rules.

EA0 authorizes no probe source creation, compilation, L1 canary, subprocess evidence run, key creation,
monitor activation, socket creation, or L2 action.

The sole L0 output root permits only:

- creation of a new, previously absent run directory;
- create-new immutable evidence objects at unique or content-addressed paths;
- append-only writes to predeclared length-framed ledgers;
- predeclared one-way publication of a unique temporary object to an absent final path.

L0 forbids overwrite, truncation, replacement, deletion during acquisition, reuse of an existing run
directory, and writing outside the sole root.

EA0 numeric caps use non-negative integers for source files/bytes, output objects/total/per-object
bytes, append operations/bytes, temporary objects/bytes, processes/concurrency, wall and CPU time,
working set, stdout/stderr, and tool invocations. A prohibited dimension has cap `0`; it is not omitted.

### EA1-CONSTRUCT — optional probe construction authorization

EA1-CONSTRUCT exists only when the sealed feasibility packet proves that no byte-complete existing tool
or smaller method answers a named admissible falsifier.

It binds:

- EA0 and the exact sealed L0 packet;
- exact `AcquisitionFeasibilityPacket`;
- every approved `ProbeToolAdmissionRecord`;
- source and build-output roots;
- exact toolchain and dependency inputs;
- permitted source kinds and maximum file count;
- executable allowlist;
- numeric construction caps;
- network mode, retention, and prohibited P4 boundaries.

EA1-CONSTRUCT authorizes build activity only. It cannot produce an NE `PASS` or run an NE evidence case.

### EA1-EXECUTE — L1 probe execution authorization

EA1-EXECUTE binds:

- EA0;
- exact sealed L0 packet and source snapshot;
- exact `AcquisitionFeasibilityPacket`;
- exact `ExistingProbeBundle` or `SealedProbeBuildPacket`;
- every exact L1 `ProbeContract` and `L1RunManifest`;
- every executable, dependency, tool, oracle, expected outcome, reason code, cap, executable permission,
  network mode, and retention rule.

No placeholder, future filename, unbuilt tree, version range, package name, or logical tool ID satisfies
an exact executable root. EA1-EXECUTE is issued only after all executable bytes exist and are sealed.

The default network mode is `NONE`. `LOOPBACK_SYNTHETIC_ONLY` requires explicit authorization and
numeric socket, byte, process, and wall-time caps. External network, DNS, listeners, model calls,
privilege elevation, credentials, installed configuration, plugins, MCPs, and production routes remain
prohibited.

No stage inherits unstated permission or implies the next stage.

## Evidence action levels

- **L0 — source-read-only, output-create-bounded:** inspect approved existing sources without mutating
  them; write only EA0-permitted immutable objects and append-only records.
- **L1C — bounded probe construction:** build only admitted probe-only utilities under EA1-CONSTRUCT.
- **L1E — bounded probe execution:** run exact sealed utilities under EA1-EXECUTE and retain results.
- **L2 — retained seven-case implementation:** forbidden until a later fresh Chief and user-authorized
  implementation plan.

L1C/L1E artifacts are evidence tooling. They are not automatically reusable implementation.

## Immutable acquisition chain

```text
EA0
 -> exact L0ProbeContracts
 -> sealed L0 packet + L0PacketRoot
 -> AcquisitionFeasibilityPacket
 -> exact ExistingProbeBundle
       or EA1-CONSTRUCT -> SealedProbeBuildPacket
 -> EA1-EXECUTE
 -> exact L1 contracts/manifests
 -> sealed raw-result roots
 -> NEReports
 -> unchanged fresh-Chief packet
```

### L0ProbeContract

Every L0 action binds EA0, its NE question, exact read roots/exclusions, sole output root, permitted
operations, snapshot rules, tool hashes, expected artifact kinds, numeric caps, terminal seal, and stable
failure/inconclusive reasons.

### SealedL0Packet

The packet records EA0, ordered L0 contract hashes, exact source snapshot, source IDs and hashes, command
and tool hashes, `QualifiedCorpus`, `CorpusGapReport`, capability/provenance roots, every evidence-object
hash, cap ledger, stdout/stderr sizes, exit states, errors/exclusions/unmatched sources, local-clock
times, terminal state, and content root.

Allowed terminal states are `SEALED`, `INCOMPLETE`, `CAP_STOPPED`, and `INVALID`. Only `SEALED` may
advance. The compiler cannot reconstruct or replace a missing seal.

## Acquisition feasibility packet

After L0 and before any construction, the compiler emits an `AcquisitionFeasibilityPacket` containing:

- EA0 and sealed L0 roots;
- `QualifiedCorpus` and provenance-gap roots;
- NE2 L0 host-capability and privilege survey;
- available native and pre-existing tools with provenance;
- for every NE: question/falsifier, binding admissibility class, maximum effect, required primitive,
  required interface/tool, dependencies, no-code alternative, existing-tool alternative, one-shot
  adapter alternative, constructed-tool alternative, smallest method, bounded estimate, and stop rule;
- aggregate construction estimate/caps;
- prohibited-component analysis;
- feasibility outcome and content root.

Allowed outcomes:

- `PROCEED_WITH_EXISTING_BUNDLE`;
- `PROCEED_TO_BOUNDED_CONSTRUCTION`;
- `STOP_CAPABILITY_UNSUPPORTED`;
- `STOP_NO_DECISION_ADVANCEMENT`;
- `STOP_SMALLER_METHOD_REQUIRED`;
- `STOP_CONSTRUCTION_UNBOUNDED`;
- `INCONCLUSIVE`.

Construction requires at least one named gap that may permissibly narrow or close, an exact falsifier
not answered by a smaller method, and complete numeric construction caps. Stop outcomes authorize no
construction or execution.

## Probe construction protocol

Every proposed utility has a separate `ProbeToolAdmissionRecord`. Bundle-level justification cannot
conceal an unnecessary component.

Permitted families are limited to the smallest admitted form of:

- synthetic host-control/execution-identity canary launcher;
- frozen-contract legacy validator;
- standalone canonicalizer/verifier;
- bounded synthetic canary scanner;
- result sealer/compiler adapter.

EA1-CONSTRUCT prohibits implementations of:

- P4 sidecar or consumer receipt;
- consumer receipt signer, authority registry, issuer, or gate;
- replay journal;
- lineage, checkpoint, history, reservation, or recovery engine;
- retained seven-case runner;
- production/installed integration;
- plugin, MCP, external-service, or authority adapter.

Construction caps cover source files/bytes read and created, generated binaries/objects/bytes,
dependencies, build processes/concurrency/invocations, wall/CPU time, working set, stdout/stderr,
temporary files/bytes, and final packet bytes. Network/package-download caps default to `0`.

Build tests are limited to compilation integrity, startup, frozen interface shape, and synthetic
self-tests. They cannot count as an NE evidence run or produce NE `PASS`.

`SealedProbeBuildPacket` binds EA1-CONSTRUCT, all admission records, created source/binary/dependency,
commands/configuration/toolchain, build/test results, cap ledger, errors/warnings,
prohibited-boundary inspection, terminal state, and content root. Only terminal state `SEALED` may
advance; `INCOMPLETE`, `CAP_STOPPED`, and `INVALID` block execution.

## Exact-tool availability

Before EA1-EXECUTE, every required executable is exactly one of:

- `EXISTING_BYTE_COMPLETE`;
- `CONSTRUCTED_AND_SEALED`;
- `UNAVAILABLE`;
- `INVALID`.

Existing completeness requires source/binary, dependencies, provenance, command, configuration,
capability, and content roots. Unavailable or invalid tools block dependent probes. Rebuild, dependency,
configuration, or binary changes require a new build packet and new execution authorization.

## L1 prelaunch chain verification

Before any L1 process, synthetic write, key, monitor, or socket:

1. recompute EA0 and every L0 contract;
2. recompute the sealed L0 root and require terminal `SEALED`;
3. recompute the approved source snapshot and reject drift;
4. verify the feasibility packet and selected tool branch;
5. verify EA1-EXECUTE binds the exact ancestor chain and tool bytes;
6. recompute every L1 contract, manifest, tool, oracle, expected result, reason table, cap, permission,
   network mode, and retention rule;
7. require the L1 output root to be absent before atomic reservation.

Any missing or mismatched item produces exactly:

```text
execution_state = NOT_STARTED
outcome = INCONCLUSIVE
reason_code = PRELAUNCH_CHAIN_MISMATCH
decision_effect = LEAVES_NAMED_GAP_UNCHANGED
```

No L1 side effect follows this result.

## Bound execution launch protocol

Passing prelaunch reaches only `CHAIN_VERIFIED`. Every L1 subprocess then follows:

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

Each transition is appended to the attempt record with predecessor, controller/tool hash, cap state,
control/loss state, and transition evidence. Missing, repeated, reordered, reconstructed, or
contradictory transitions prevent progression.

### Run-root reservation

Create a new root fail-if-exists under the authorized parent. Record parent identity, requested name,
atomic result, created final identity, alias/reparse result, strongest retained handle/lock/equivalent,
and identity rechecks before publication. Collision, existing path, reparse traversal, replacement,
identity ambiguity, or unsupported required recheck stops; no directory is emptied or reused.

### Hard-control arming

Before child execution, all required prevention, observation, job, loader, network, IPC, sink, cap, and
event-loss controls match approved hashes and expose positive arm acknowledgement. Configuration alone
is not acknowledgement. Controls that attach after creation require a nonrunning, input-blind child. If
that ordering cannot be guaranteed, the capability is unsupported.

### Final-object binding

Resolve executable/interpreter through the OS and record requested/final path, filesystem/volume
identity, stable object ID where available, content hash, alias/hard-link/symbolic-link/junction/reparse
resolution, retained object binding, and the mechanism tying the verified object to process creation.
A path string and preliminary hash are insufficient.

### Nonrunning child and actual image

Create the child suspended or equivalently non-executing, associated with all controls. Record OS
process identity, flags, parent, assigned controls, and nonrunning evidence. OS-derived evidence must
verify actual main image/interpreter and required initial modules. Command text, requested path, source
imports, or worker self-report cannot establish identity. Unavailable module/loss coverage makes the
dependent probe `INCONCLUSIVE`.

### Key/input publication and running

Only after all earlier states succeed may key, synthetic payload, input path, or handle be journaled and
published. Publication binds child, root, control-arm root, actual image/modules, cap ledger, and
attempt. Application execution begins only after publication is durably recorded. Late loads,
descendants, IPC, sockets, reads/sinks, control termination, cap breaches, and event loss remain
monitored until terminal reconciliation.

## Edge-control contract

Every required edge is exactly:

- `PREVENT_BEFORE_KEY_INPUT`;
- `DETECT_AND_QUARANTINE_BEFORE_TERMINAL`;
- `UNSUPPORTED_FOR_STRONG_CLOSURE`.

Executable substitution, root collision, control arming, actual-image identity, and publication order
are preventive obligations. Detect-after-publication cannot upgrade them. Detect/quarantine is allowed
only with the exact frozen event, loss accounting, quarantine action, and terminal reason. Unsupported
capability blocks every dependent claim.

## Raw results and NE reports

Every subprocess raw result binds:

- EA1-EXECUTE, L0, feasibility, and exact run manifest roots;
- source/dependency/command/input/tool/oracle roots;
- authorization and cap roots;
- `ExecutionIdentityContract`;
- ordered launch ledger;
- root reservation and rechecks;
- control configuration and arm acknowledgements/order;
- final-object tuple and binding;
- child/nonrunning evidence;
- actual main image and initial/late modules;
- key/input publication point;
- edge sequence, caps at every transition, monitor sequence/drop/loss;
- quarantine, terminal result, timing, stdout/stderr, limitations, and content root.

A requested-path hash without actual-image evidence cannot support a subprocess pass.

Every `NEReport` binds the complete ancestor chain, all applicable run/raw roots including failed,
inconclusive, blocked, cap-stopped, and expected-negative cases, compiler hashes, execution state,
exactly one outcome, separate decision effect, limits, and residual risks.

## Outcome and decision-effect algebra

Every NE has exactly one outcome: `PASS`, `FAIL`, or `INCONCLUSIVE`.

It independently records one decision effect:

- `CLOSES_NAMED_GAP`;
- `NARROWS_NAMED_GAP`;
- `LEAVES_NAMED_GAP_UNCHANGED`;
- `INVALIDATES_NAMED_CLAIM`;
- `STOP_DECISION_GATE_NON_ADVANCEMENT`.

Outcome describes evidence validity/completeness. Decision effect describes gate impact.
`STOP_DECISION_GATE_NON_ADVANCEMENT` is not a fourth outcome. Missing authorization/evidence, blocked
dependency, unsealed ancestor, chain mismatch, or unavailable observation cannot pass.

An expected-negative supports `PASS` only on its exact authorized fail-closed reason, successful
positive controls, and verified chain.

## NE1 — Corpus and worker provenance

### Question

Can every v1-v7 compatibility claim be traced to byte-frozen inspectable material, and can a
legacy-contract validator be structurally separate from current application parsing without claiming
cognitive or deployed independence?

### L0

Inventory candidate schemas, fixtures, generators, expected hashes, and compatibility tests. Record
version/contract source, path, length/SHA-256, existing canonical hash and establishing code/test,
inspectable derivation, semantic expectation, and complete/incomplete provenance. The package is not a
Git repository; no commit provenance is invented.

L0 produces `QualifiedCorpus` plus `CorpusGapReport`. Missing provenance remains explicit.

### Admitted L1 method

Only when feasibility permits, build or use a probe-only validator from a frozen public contract packet.
It may not import current producer/consumer/shared parser/normalization code. It receives unchanged raw
bytes and emits a generic probe validation record, not a P4 sidecar, consumer receipt, gate, journal,
lineage, history, or recovery artifact.

Synthetic canaries demonstrate that private-key, holdout, oracle, sibling-worker, and aggregate-result
locations are absent from its manifest and outputs.

### Outcome

`PASS` requires complete provenance for the claimed QualifiedCorpus, stable bytes/hashes, prohibited
dependency absence, and no synthetic secret exposure. Changed bytes/hashes, prohibited import, or leak
is `FAIL`. Missing provenance/separation/custody is `INCONCLUSIVE` and cannot preserve a v1-v7
completeness claim.

Maximum claim: structural source separation and local compatibility for the exact QualifiedCorpus.

## NE2 — Windows closure capability

### Question and capability matrix

Can the authorized Windows environment observe or deny each required operation and detect monitor loss?
For loads, descendants, handles, IPC, sockets, reads/sinks, outputs, aliases/hard links/symlinks/junctions,
reparse, replacement, and monitor loss, record observation, denial, final-object identification, loss
detection, privilege, mechanism, controls, and limitations.

### L0 feasibility

Identify available non-admin mechanisms, current identity/filesystem/path semantics, unavailable
primitives, and the proposed final-object tuple. A source-only import graph or worker self-report cannot
prove OS-observed closure.

### Authorized canaries

Every canary freezes its edge class, state transition, reason, caps, and evidence before execution:

1. `RUN_ROOT_COLLISION`;
2. `POST_VERIFY_EXECUTABLE_REPLACEMENT`;
3. `REPARSE_RETARGET_BEFORE_CREATE`;
4. `CONTROL_ARMING_GAP`;
5. `ACTUAL_IMAGE_MISMATCH`;
6. `UNDECLARED_INITIAL_MODULE`;
7. `LATE_MODULE_LOAD`;
8. `CAP_BEFORE_PUBLICATION`;
9. `MONITOR_TERMINATION_OR_LOSS`;
10. omitted helper;
11. undeclared descendant or IPC;
12. loopback-only socket only when explicitly authorized;
13. undeclared file sink.

### Outcome and dependencies

`PASS` for strong closure requires every necessary edge observed or denied, every positive control
detected, no unexplained loss, and every canary's exact result. Unexpected exposure, silent unmatched
edge, alias substitution, or missed positive control is `FAIL`. Unobservable/undenied required edges or
ambiguous loss are `INCONCLUSIVE`.

If required NE2 capability is not PASS, any subprocess-dependent NE1/NE3/NE5 probe does not launch and
records `BLOCKED_DEPENDENCY + INCONCLUSIVE + exact NE2 reference + LEAVES_NAMED_GAP_UNCHANGED`.

NE2 evidence remains mechanism/privilege/filesystem/runtime/host bounded and never proves OS isolation.

## NE3 — Canonicalization differential

### Question and freeze

Do independently implemented adapters produce identical canonical bytes/domain-separated preimages and
typed rejections? Before execution freeze canonical JSON bytes, NFC, ordering, integer range, null/empty,
duplicate/float/NaN/invalid Unicode/unknown/oversize rejection, framing, domain tags, and Ed25519
encoding. Historical payloads remain raw bytes under NE1 rules.

### Vector oracle and execution

`VectorOracleManifest` is pre-authorized and cannot be generated by either candidate adapter. Use two
standalone probe-only canonicalizer/verifier adapters; they may share a reviewed crypto library but not
application record-builders or private keys. Vectors cover multilingual normalization/order, integer
boundaries, empty values, alternate syntax, malformed encodings, duplicate/forbidden numeric forms,
unknown/oversize fields, cross-domain replay, predecessor/checkpoint/key-transition/artifact records,
and truncated frames.

The maximum acquisition claim is `CANONICAL_CONTRACT_DIFFERENTIAL_TESTED`, not future L2 equivalence.
Actual L2 issuer, worker, history, and verifier paths rerun the same vectors later.

### Outcome

Byte-identical valid results, exact invalid rejection, and cross-domain rejection are required for
`PASS`. Any divergence or invalid acceptance is `FAIL`. Incomplete oracle/vector/implementation paths
are `INCONCLUSIVE`.

## NE4 — Burden and decision advancement

### Existing evidence separation

Prior native totals remain a separate derivative:

| Run | Input | Output | Cached-input subset | Reasoning | Total | Turns | Summed turn duration |
|---|---:|---:|---:|---:|---:|---:|---:|
| F2 | 181,713 | 14,340 | 148,224 | 9,648 | 196,053 | 9 | 424,246 ms |
| F3-short | 110,140 | 1,120 | 102,912 | 588 | 111,260 | 6 | 63,478 ms |
| F3-noisy | 110,106 | 1,304 | 103,936 | 735 | 111,410 | 6 | 97,736 ms |

Cached input is a subset, not an addition. Summed turn duration is not wall time. These values are not
P4 acquisition or L2 cost.

### Measurements

Hash source telemetry and numeric-only extraction logic. For every authorized action record wall/CPU,
working set where available, process/attempt count, files/bytes, input/output/journal/spool/receipt/
stdout/stderr/final bytes, verification time, cap consumption, and first breach. Missing fields are
`UNAVAILABLE`, never zero. Ambiguous delivery has no retry.

Every case maps:

`gap -> admissibility -> artifact -> result -> close/narrow/unchanged/invalid -> residual risk`.

Real-integration gaps remain unchanged. Cost is `COST_UNAVAILABLE` without authoritative provider,
model, date, rates, and mapping.

### Outcome

Complete credible capped measurement is `PASS`; cap bypass, false zero, mixed totals, or unsupported
money is `FAIL`; unavailable required measurement/provenance is `INCONCLUSIVE`. A valid `PASS` may still
have `STOP_DECISION_GATE_NON_ADVANCEMENT` and require stop.

## NE5 — Positive/negative control validity

### Question and method

Can a standalone scanner distinguish real absence from observation failure, and can fault cases remain
isolated? During acquisition, validate only a standalone scanner/configuration against a fixed synthetic
tree. Do not implement or invoke P4 worker, receipt, journal, lineage, history, or recovery.

Generate unique synthetic canaries for holdout, oracle, sibling key, aggregate results, forbidden env,
and safe positive output. Values contain no user or real secret data.

Clean, positive, deliberate-leak, and expected-negative runs have different roots/IDs/manifests/terminal
states. A poisoned fault result cannot become clean. Expected negatives pass only on exact reasons.

### Outcome

Detect safe positive and deliberate leak, show zero forbidden canaries in clean outputs, and prove run
separation for `PASS`. Missed detection or clean leak is `FAIL`. Unobservable channels or ambiguous
separation are `INCONCLUSIVE`. Maximum claim is `CONTROL_METHOD_VALIDATED`, never OS/network containment
or actual L2 DLP success. Actual output channels rerun after L2.

## Execution order and dependencies

```text
EA0/L0 corpus + capability + effect inventory
        |
        v
AcquisitionFeasibilityPacket
        |
        +-- early stop -> retained dependent INCONCLUSIVE reports
        |
        +-- exact existing bundle
        |          or
        +-- EA1-CONSTRUCT -> sealed build
                            |
                            v
                        EA1-EXECUTE
                            |
          +-----------------+------------------+
          v                 v                  v
        NE2             NE1/NE3           NE4/NE5
   capability gates    as dependencies     measurement/control
          \                 |                  /
           +----------------+-----------------+
                            v
                    immutable combined packet
                            |
                            v
                       fresh Chief
```

NE1 corpus identity precedes NE3 historical vectors. NE2 capability gates every subprocess-dependent
probe. NE4 caps and measures all stages, including blocked/stop results. NE5 accompanies the methods it
validates.

## Early-stop reports

Feasibility stop yields dependent:

```text
execution_state = BLOCKED_FEASIBILITY
outcome = INCONCLUSIVE
decision_effect = LEAVES_NAMED_GAP_UNCHANGED
```

Construction absent/incomplete/cap-stopped/invalid/prohibited yields `BLOCKED_CONSTRUCTION` with the
same outcome/effect. Unsupported NE2 execution binding yields `BLOCKED_DEPENDENCY`.

Stop before construction for unsupported capability, unavailable required corpus/provenance, all
results unchanged, smaller sufficient method, missing construction caps, or prohibited P4 component.
Stop before execution for missing/unsealed exact tools, incomplete binding, unsupported P2 launch
capability, or cap excess.

Early stop is retained and is not repaired by new tools, broader scope, replacement corpus, wider caps,
or automatic retry.

## Combined packet and Chief gate

The packet contains every authorization, L0 contract and sealed root, feasibility packet, tool-admission
record, existing/build bundle, execution contract/manifest, raw/adverse/blocked result, NE outcome/effect,
cross-link, invariant/risk mapping, limitation, and no-mutation statement.

The compiler preserves the chain and cannot omit adverse roots, reconstruct seals, change outcomes,
expand claims, or approve. Chief receives the chain unchanged.

Chief cannot relabel `FAIL/INCONCLUSIVE`, omit or excuse chain artifacts, expand QualifiedCorpus,
upgrade closure, convert local to real integration, add components/cases, authorize construction
retrospectively, or promote code automatically. Reduced claims retain original adverse outcomes,
affected cases, limitations, and risks.

## Reuse and promotion

Exact non-executable specifications, schemas, contracts, vectors, expected results, canaries, reasons,
capability matrices, raw evidence, reports, risks, and limitations may be reused by root.

Executable probes remain `NOT_ADMITTED_TO_L2`. Promotion requires exact source/binary roots, target,
semantic/security/trust/dependency review, tests, rollback, fresh Chief, and user-authorized L2 plan.
Acquisition outcomes do not become L2 outcomes. All relevant contracts, vectors, canaries,
execution-identity, failure, and resource cases rerun against actual L2 paths.

The required `ProbePromotionRecord` binds the exact probe source/binary roots, target L2 component,
component-admission effect, semantic differences, security and trust-boundary review,
dependency/toolchain review, retained and added tests, rollback, fresh-Chief disposition, and the
user-authorized L2 plan. It cannot import an acquisition outcome as an L2 outcome.

## Risks

- **R2:** local chain integrity never changes real-integration classifications.
- **R10:** final-object binding/rechecks/canaries gate alias and reparse claims.
- **R11:** mechanism burden requires feasibility, smallest-method analysis, construction caps, and NE4.
- **R12:** pre-child arming and sequence/loss accounting gate monitoring claims.
- **R15:** stop before construction when no named gap can change; bind every adverse/early-stop root.
- **R20:** authorization/cap drift is blocked by the full content-root chain.
- **R22:** QualifiedCorpus cannot be trimmed while retaining completeness.
- **R25:** document chain extends through actual execution identity and raw results.
- **R26:** L0 output uses sole create-new/append-only root and caps.
- **R27:** Chief packet contains complete ancestors/raw results, not summaries alone.
- **R28:** check-to-execute substitution requires final-object/actual-image evidence and canaries.
- **R29:** late/unsupported controls require ordered nonrunning launch and delayed publication.
- **R30:** construction and execution authorizations are separate; placeholders are forbidden.
- **R31:** per-tool admission and prohibited-component checks prevent shadow implementation growth.
- **R32:** immutable semantics may be reused; executable promotion is gated and rerun.
- **R33:** feasibility effect/cost analysis stops non-advancing construction.

## Stop rules

- Stop before L0 without exact EA0 and numeric caps.
- Stop before construction on a feasibility stop.
- Stop at first construction or execution cap breach.
- Stop execution without exact sealed tool bytes and EA1-EXECUTE.
- Stop dependent subprocess evidence when NE2 capability is not PASS.
- Stop compatibility on NE1 failure/inconclusive provenance.
- Stop canonical integrity on NE3 failure/incompleteness.
- Stop expansion when NE4 reports no advancement.
- Stop DLP claims on NE5 failure/inconclusive coverage.
- Preserve every adverse record; do not delete or silently rerun it.
- Never widen filesystem, process, network, system, or production scope automatically.

## Accepted-clause conformance map

| Accepted clause | Applied section |
|---|---|
| P1-E2-1 | Authorization boundary; Evidence action levels |
| P1-E2-2 | Immutable chain; L0 packet; prelaunch; raw reports |
| P1-E2-3 | Outcome and decision-effect algebra |
| P1-E2-4 | Combined packet and Chief gate |
| P1-E2-5 | Risks R2/R15/R20/R22/R25-R27 |
| P2-E2-1 | Bound execution launch protocol |
| P2-E2-2 | Edge-control contract |
| P2-E2-3 | NE2 canaries |
| P2-E2-4 | Raw results and NE reports |
| P2-E2-5 | NE2 dependencies and execution order |
| P2-E2-6 | Risks R10/R12/R25/R28/R29 |
| P3-E2-1 | Authorization boundary |
| P3-E2-2 | Acquisition feasibility packet |
| P3-E2-3 | Probe construction protocol |
| P3-E2-4 | Exact-tool availability |
| P3-E2-5 | Early-stop reports |
| P3-E2-6 | Reuse and promotion |
| P3-E2-7 | Risks R11/R15/R30-R33 |

## Self-review

- Current approval covers only this document; EA0/L1C/L1E/L2 remain unauthorized.
- EA0, feasibility, construction, and execution are separate content-rooted gates.
- No placeholder or future executable can satisfy EA1-EXECUTE.
- Probe construction cannot implement P4 sidecar, receipt, authority, replay, lineage, recovery, or L2.
- Three-valued outcomes remain separate from decision effects.
- Hash verification does not substitute for actual execution identity.
- Unsupported Windows capability blocks dependent probes rather than upgrading closure.
- NE1/NE3/NE5 validate acquisition methods, not future L2 paths; actual L2 reruns remain mandatory.
- DLP remains leak detection, local history remains forkable, and usage remains unpriced.
- Early stop is a valid retained result and never triggers automatic expansion.
