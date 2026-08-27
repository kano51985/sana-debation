# E14 N1 D0a task-local specification

Date: 2026-08-27

Final status: **`CONSUMED`**

This record contains one inert D0a pass. It is a current-task interpretation and terminal receipt,
not a global G0 success, actor appointment, durable policy successor, acquisition or execution
authorization, or later-stage gate.

## Decision audit

- mode: `real-subagents/core`;
- startup: `core-two-phase-v1`, serial PREPARE in
  `Chief Architect -> Peer TL -> Proposing TL` order;
- Chief Architect: `/root/g0_minimal_r3_chief`, readiness-only until final handoff;
- Peer TL: `/root/g0_minimal_r3_peer`, readiness-only until P0 routing;
- Proposing TL: `/root/g0_minimal_r3_proposer`, activated only after all three readiness receipts;
- all three threads were fresh and separately instructed; this demonstrates execution separation,
  not cognitive independence;
- optional roles: none; retries: none; startup or protocol failures: none; and
- Chief decision `CA-D1`: **APPROVE WITH REQUIRED CHANGES**, limited to one inert current-task D0a
  pass followed by a terminal receipt.

| Round | Axis | Peer verdict | Binding change |
|---|---|---|---|
| 1 | authorization legitimacy and role separation | `modified` | Removed self-asserted issuer admission and recorded circular bootstrap as a blocking risk. |
| 2 | least authority, sequencing, and proportionality | `modified` | Replaced unbounded antecedent-document regress with an explicit finite native/delegated authority model. |
| 3 | audit, revocation, compatibility, and rollback | `modified` | Narrowed the result to lower-assurance user-role provenance, visible-message revocation, and a task-local interpretation with no global precedence. |

## Task-local permission record

```yaml
record_type: g0.d0a-task-local.v3
record_relation: TASK_LOCAL_D0A_INTERPRETATION
chief_decision: CA-D1
scope: CURRENT_TASK_ONLY
repository_scope: C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence
base_commit: 8095b073b2622d770d15a3f32501efdffca54a26
stage: D0a
permission_status: CONSUMED
authority_effect: NONE
next_stage_authorized: false
global_precedence: NONE
cross_task: false
durable: false

permission_provenance:
  - E11
  - E12
  - E14
preserved_prior_records:
  - E2
  - E3

g0_global_status: ISSUER_NOT_ESTABLISHED
actor_appointment_status: UNESTABLISHED
durable_policy_successor_authorization: UNESTABLISHED

validation_mode: NON_INDEPENDENT_TASK_LOCAL_CHECK
revocation_basis: CURRENT_TASK_VISIBLE_MESSAGES_ONLY
revocation_observation: NO_REVOKE_VISIBLE_AS_OF_VALIDATION
ordering_assurance: RUNTIME_PRESENTATION_ONLY

integrity_claims:
  signature: false
  seal: false
  ordering_proof: false
  authority_proof: false

not_claimed:
  - stable_identity
  - legal_identity
  - cryptographic_signature
  - independent_custody
  - independent_review
  - cognitive_independence
  - durable_ordering
  - durable_revocation
```

The predecessor checksums below identify bytes only. They are not signatures, seals, ordering
proofs, or authority proofs.

| Predecessor | SHA-256 integrity checksum |
|---|---|
| E2 — G0 actor-and-authority record | `9341DCC667C62073A2C8EC469C4B16FD8B382595A7F9FC747DFBAEA90BEBBBA0` |
| E3 — I1 remediation next-stage debate | `62A3A3B473828F23575BDB7007A9D2730DDE84EB01A7C1E51D940C6858C84C40` |

## Preserved evidence and authority boundary

- E2 remains historically and globally controlling: `ISSUER_NOT_ESTABLISHED`,
  `authority_effect=NONE`, and `next_stage_authorized=false`.
- E3's later sequence remains unchanged:
  `G0 -> D0a -> C1a acquisition -> C1a qualification -> D0b -> C0 -> C1b -> Chief B`.
- E11 is the [official OpenAI request-scoped autonomy guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices).
  It supports requested in-scope local changes and non-destructive validation without repeated
  approval; it does not establish a legal identity, signature, custody relationship, or durable
  authority channel.
- E12 is the visible user-role instruction to continue and use self-debate for material decisions.
- E14 is the bounded inference that E11 and E12 permit this one safe, local, inert documentation
  pass. It does not authorize any external, destructive, costly, production, acquisition,
  execution, candidate, or materially expanded action.

## D0a questions

Every question remains open until a separately authorized later stage produces named evidence.
Writing the question does not authorize gathering that evidence.

| ID | Question | Blocking effect |
|---|---|---|
| `Q-D0A-01` | What exact Node executable version, absolute path, raw-byte SHA-256, distribution identity, license, and complete native/loader closure would C1a propose? | Blocks C1a qualification and any `ExecutionReceiptV1`. |
| `Q-D0A-02` | What exact Acorn package name, version, archive identity, archive size, registry integrity fields, license evidence, transitive dependency closure, and source-root calculation would C1a propose? | Blocks acquisition-manifest finalization; no digest may be guessed. |
| `Q-D0A-03` | What exact diagnostic runner bytes, entry point, arguments, parser options, callback configuration, and output schema would be bound before execution? | Blocks qualification; a description cannot substitute for runner bytes. |
| `Q-D0A-04` | Which environment variables, startup flags, loaders, preloads, plugins, module-resolution roots, writable locations, clocks, locales, and network surfaces must be absent or frozen? | Blocks any hermeticity claim. |
| `Q-D0A-05` | What independently derived actual entry model covers every path from raw fixture bytes through parsing, traversal, reporting, and return without importing or executing fixture or candidate source? | Blocks D0b and C0; the intended design cannot answer its own entry-model question. |
| `Q-D0A-06` | How will the existing 14 negative cases be identified by exact bytes and expected blocking family, and which positive controls demonstrate that the diagnostic does not reject all input indiscriminately? | Blocks qualification-result interpretation. |
| `Q-D0A-07` | How will aliasing, reflection, dynamic code, callbacks, native loading, subprocess access, and output-driven re-entry each receive a distinct observable diagnostic result? | Blocks any claim that I1's nine accepted attacks were remediated. |
| `Q-D0A-08` | How will the known `object.toJSON()` runtime-dispatch site be represented without claiming it is absent, unreachable, safe, or invoked before actual reachability evidence exists? | Blocks semantic-safety or completeness claims. |
| `Q-D0A-09` | Which CPU, wall-time, memory, process, file, output, stderr, recursion, AST-node, and input-byte caps bind the single offline run, and how are cap failures distinguished from diagnostic findings? | Blocks an exact execution receipt. |
| `Q-D0A-10` | Which crash, timeout, truncation, malformed-output, preload, resolution-drift, stale-root, and partial-write cases must produce typed `INCONCLUSIVE` evidence rather than PASS? | Blocks supervisor and failure-semantic qualification. |
| `Q-D0A-11` | What acquisition quarantine, no-install, no-lifecycle-script, no-auto-extract, redirect, size, inventory, and license checks are required before any Node/Acorn bytes become eligible for qualification? | Blocks C1a acquisition and admission. |
| `Q-D0A-12` | Which exact evidence artifacts, roots, limitations, and nonauthority labels must Chief B receive, and which missing fields force defer rather than inference? | Blocks evidence-frame completion and Chief B review. |

## D0a exclusions

The following are deliberately outside this pass:

- no network request, download, registry lookup, repository checkout, package acquisition, archive
  extraction, dependency resolution, installation, or lifecycle script;
- no Node, Acorn, parser, runner, fixture, candidate, or vendor-source import, compilation,
  evaluation, or execution;
- no creation or modification of executable runner, scanner, candidate, test, fixture bytes,
  schema, source code, production configuration, consumer, route, database, API, Redis, image, or
  container;
- no guessed archive digest, package closure, runtime hash, source root, license conclusion,
  reachability conclusion, semantic-completeness claim, or general language-safety claim;
- no global G0 PASS, actor appointment, role-separation claim, independent review, independent
  sealing, custody, signature, durable revocation, durable ordering, or canonical account identity;
- no reuse of the current task-local permission and no implication that completing D0a authorizes
  C1a, D0b, C0, C1b, G1, I2, Chief B, production, issuance, or another D0a pass; and
- no mutation, reinterpretation, deletion, or global supersession of E2, E3, the failed I1 record,
  the frozen scanner, G1-v1, or existing evidence bundles.

## Inert fixture specifications

These specifications define possible future evidence inputs and records. They do not create those
artifacts, approve their contents, or authorize their construction or execution.

### `F-D0A-01 — ExactToolchainIdentitySpec`

Required future fields:

- exact Node executable bytes, version output, absolute path, distribution source, license, loader
  and native-library closure;
- exact Acorn raw archive bytes, package/version, registry fields, size, SHA-256, inventory,
  dependency closure, license evidence, and admitted source root;
- exact diagnostic-runner bytes, entry point, arguments, parser options, callback policy, output
  schema, and integrity root; and
- explicit `identity_only=true`, `authority_effect=NONE`, and no safety/completeness conclusion.

Any missing object, identity mismatch, extra dependency, redirect drift, or unresolved license is a
typed non-PASS result. A package name or version never substitutes for byte identity.

### `F-D0A-02 — FrozenCorpusManifestSpec`

The future manifest must identify the existing 14 required-negative cases by stable case ID, exact
input-byte checksum, language, attack family, expected blocking family, and immutable source path.
It must also name positive controls that exercise ordinary safe syntax. The manifest cannot contain
gold conclusions derived from the candidate diagnostic, and this D0a pass creates no fixture bytes.

Required attack families are:

1. alias indirection;
2. reflection or computed member access;
3. dynamic-code construction or evaluation;
4. parser/runtime callback dispatch;
5. native or foreign-function loading;
6. process or subprocess creation; and
7. diagnostic-output-driven re-entry.

### `F-D0A-03 — ActualEntryModelObservationSpec`

The future entry-model record must be derived from the exact admitted runner and toolchain rather
than copied from the candidate design. It must enumerate:

- every executable entry point and argument;
- every read boundary and byte-to-AST transition;
- parser options and callbacks;
- traversal, visitor, reporter, serializer, and return paths;
- module resolution, loaders, preloads, native dependencies, child-process surfaces, and network
  surfaces; and
- the known `toJSON()` site with a typed reachability status.

Allowed reachability statuses are `OBSERVED_REACHABLE`, `OBSERVED_NOT_REACHED_UNDER_BOUND_INPUT`,
and `UNRESOLVED`. None means generally safe or unreachable.

### `F-D0A-04 — DiagnosticExpectationSpec`

Each future case expectation must bind one case ID to:

- an expected diagnostic family;
- a minimum decisive source span or event;
- permitted ancillary findings;
- forbidden PASS/general-safety conclusions;
- a typed result when parsing, caps, or supervisor integrity prevents diagnosis; and
- a falsifier that would demonstrate the expectation or diagnostic rule is wrong.

Diagnostic agreement on the frozen corpus may establish only exact-corpus behavior. It cannot
establish semantic completeness, general JavaScript/Python safety, candidate admissibility, G1, or
I2.

### `F-D0A-05 — HermeticRunContractSpec`

A future one-run `ExecutionReceiptV1` must bind the exact toolchain and corpus records plus:

- offline network state and read-only input mounts;
- empty or exact environment allowlist;
- prohibited preloads, custom loaders, plugins, package managers, fallbacks, and extra runs;
- process, time, memory, input, output, and file caps;
- create-new output semantics and captured stdout/stderr limits;
- supervisor identity and exact procedure; and
- fail-closed behavior for every mismatch, timeout, crash, truncated output, and resolution drift.

This specification is not an execution receipt and has no run capacity.

### `F-D0A-06 — QualificationResultSpec`

The future result packet must separate:

- acquisition/admission identity status;
- hermetic supervisor status;
- per-case diagnostic result;
- exact-corpus coverage summary;
- unresolved reachability and callback observations;
- resource-cap and crash outcomes;
- evidence limitations; and
- `authority_effect=NONE` plus `next_stage_authorized=false`.

Missing, malformed, mismatched, ambiguous, or partially written results are `INCONCLUSIVE`; they
cannot be repaired by rerunning under the same one-run receipt.

### `F-D0A-07 — CandidateEvidenceFrameManifestSpec`

Before D0b or C0, a future manifest must enumerate every admitted evidence object and its role,
checksum, provenance, assurance level, limitation, and applicable claim. It must explicitly list
absent evidence, including any missing independent entry model, lifecycle authority, consumer
inventory, or custody record. Evidence repetition, model agreement, or byte hashing cannot upgrade
an inference into authority or semantic truth.

## D0a completion conditions

This pass is complete because it records:

- twelve bounded questions with explicit blocking effects;
- an exact exclusion boundary that prevents acquisition, execution, candidate creation, or global
  governance claims;
- seven inert future-fixture specifications with typed limitations; and
- a terminal, non-reusable task-local receipt below.

It does not answer the questions, construct the fixtures, authorize C1a, or change the global G0
state.

## Terminal task-local receipt

```yaml
receipt_type: g0.d0a-task-local-terminal.v1
record_relation: TASK_LOCAL_D0A_INTERPRETATION
repository_scope: C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence
base_commit: 8095b073b2622d770d15a3f32501efdffca54a26
permission_final_status: CONSUMED
validation_result: PASS_WITH_DISCLOSED_TASK_LOCAL_ASSURANCE
validation_mode: NON_INDEPENDENT_TASK_LOCAL_CHECK
visible_revoke_or_override: false
outputs:
  - this Markdown record
question_count: 12
exclusion_boundary_recorded: true
fixture_specification_count: 7
evidence_ids:
  - E1
  - E2
  - E3
  - E4
  - E5
  - E6
  - E7
  - E8
  - E9
  - E10
  - E11
  - E12
  - E13
  - E14
risk_ids:
  - R1
  - R2
  - R3
  - R4
  - R5
  - R6
  - R7
  - R8
  - R9
  - R10
authority_effect: NONE
next_stage_authorized: false
global_precedence: NONE
cross_task: false
reusable: false
signature: false
seal: false
ordering_proof: false
authority_proof: false
```

The permission terminates with this receipt. The next stage remains unauthorized.
