# P6 fail-closed shadow authority evidence design

Date: 2026-08-26

Status: user-approved section design; pending final whole-spec approval before implementation.

Scope: local evidence package only. The installed `sana-debation` skill, Codex runtime, enabled
plugins, MCP configuration, production consumers, and production authority remain unchanged.

## Decision

Build a local, auditable, fail-closed shadow authority evidence system based on hybrid discovery and
owner attestation. The system must bind every claim to a deterministic discovery snapshot, classify
every discovered route, execute current and independent legacy consumers, collect signed receipts,
exercise epoch and lineage failure paths, and compile real local telemetry.

This design does not claim that a local shadow run proves production isolation, organization-level
identity, global machine inventory completeness, or cognitive independence between agents. It
proves only the behavior of the declared implementation inside the hashed, owner-attested scan scope.

## Context and evidence gap

P5 established the protocol behavior and passed its package tests and native worker evaluations, but
the fresh Chief adjudication remained `defer pending named evidence`. The remaining gap is not another
architecture debate. It is evidence that the authority boundary is complete, compatible, fail-closed,
receipt-bearing, replay-safe, lineage-safe, and operationally measurable.

The installed skill is instruction-only. It does not register an authority consumer. The currently
observed P5 producer, grader, extractor, report, and manual-review paths reside in this evidence
package. Enabled generic plugins and the `node_repl` MCP are not P5 consumers, but excluding them
silently would recreate the inventory-omission problem. They therefore remain discovered,
owner-attested `NON_P5` routes and must be denied before artifact serialization.

## Goals

- Produce a deterministic discovery snapshot over an explicitly bounded local scope.
- Require owner attestation for every discovered item and fail closed on omissions or drift.
- Separate successful validation from authority to make a decisive decision.
- Generate real, verifiable receipts from isolated current and legacy consumer processes.
- Preserve every historical v1-v7 payload byte and canonical hash.
- Demonstrate rollback, replay, gap, merge, split, and collision rejection.
- Demonstrate recovery from durable state without silently retrying ambiguous dispatches.
- Detect forbidden data propagation with negative canaries and a working positive control.
- Report real token, latency, turn, and interaction telemetry with source provenance.
- Produce one Chief-facing evidence bundle whose limitations are machine-readable.

## Non-goals

- Modifying `C:\Users\Administrator\.codex\skills\sana-debation`.
- Registering a real Codex, plugin, MCP, gateway, database, or production consumer.
- Sending model, gateway, application, or internet requests.
- Granting production authorization or changing a P5 artifact's production disposition.
- Claiming physical-host failure proof from a process-kill simulation.
- Claiming OS security isolation when all processes run under the same unrestricted user identity.
- Inferring monetary cost from a similar public model when an authoritative price is unavailable.
- Using separate prompts or threads as proof of cognitive independence.

## Trust and claim boundary

The evidence system has five distinct trust roles:

1. **Discovery scanner** enumerates the approved scope but does not classify authority.
2. **Owner attestor** classifies the complete snapshot and signs that classification.
3. **Shadow issuer/gate** creates test artifacts and enforces dispatch policy.
4. **Consumers** validate artifacts and independently sign their own receipts.
5. **Evidence compiler** verifies public signatures and compiles evidence but cannot sign consumer
   receipts.

All keys are test-only. Their signatures prove which isolated test process held a run key; they do not
prove organization-level identity. A same-user local operator could replace code or keys before a run,
which is why the run manifest binds source hashes, public keys, commands, scope, and output hashes.

## Approved discovery scope

The scanner reads only structural data required for inventory and provenance:

- this evidence-package root, excluding caches and generated private material;
- installed `sana-debation/SKILL.md`, `agents/openai.yaml`, and its referenced protocol contracts;
- enabled plugin manifests and their declared skill/MCP/app entry points;
- `config.toml` section and key names for enabled plugins and MCP server names, never secret values;
- the route declarations and executable entry points introduced by the P6 shadow package;
- sanitized telemetry metadata from the named Codex SQLite databases and named rollout files.

Session text, prompt bodies unrelated to the named P5 runs, credential values, browser state, and
arbitrary user files are outside the scan. The snapshot records the inclusion rules, exclusion rules,
scanner version/hash, root identifiers, relative paths, file hashes, manifest-declared capabilities,
and a deterministic Merkle root.

The claim is therefore: "there are no unclassified routes inside this exact snapshot and scope." It is
not: "there are no unknown routes anywhere on the host."

## Initial route classes

Discovery supplies candidates; owner attestation supplies the binding classification. The initial
expected classes are:

- `P5_AUTHORITY`: only an explicitly designated shadow decisive consumer, if one is declared.
- `P5_NON_AUTHORITY`: producer formatting, defect grader, clean grader, audit/extractor, independent
  legacy verifier, evidence compiler, report generation, and manual-review projections.
- `NON_P5`: enabled generic plugins, plugin-provided capabilities, and `node_repl` MCP when they have no
  declared P5 artifact contract.

The expected list is not accepted as the inventory. Every discovered item must appear exactly once in
the signed attestation. Duplicate classifications, missing items, unknown item IDs, or a changed
snapshot hash block the run.

## Architecture and data flow

```text
bounded read-only discovery
        |
        v
discovery snapshot + Merkle root
        |
        v
complete owner attestation
        |
        v
fail-closed shadow registry
        |
        v
test artifact issuer/gate
        |
        +----> current consumer ----> signed receipt
        +----> legacy consumer -----> signed receipt
        +----> negative routes -----> gate-signed denial
                                      |
                                      v
                         append-only hash-chained journal
                                      |
                                      v
                     evidence compiler + local telemetry
                                      |
                                      v
                            Chief evidence bundle
```

No consumer receives a direct filesystem path to the full evidence package. The controller prepares a
per-attempt input directory and starts a consumer with only its envelope, public trust material, and an
anonymous pipe carrying its ephemeral private key. Receipt output is written to a per-attempt spool.

## Registry state machine

Every discovered route begins in `DISCOVERED_UNCLASSIFIED` and may transition through a complete,
snapshot-bound owner attestation to exactly one of:

- `ATTESTED_AUTHORITY`;
- `ATTESTED_NON_AUTHORITY`;
- `ATTESTED_NON_P5`.

Any source hash, manifest declaration, classification, owner key, scope, or expiration change moves
the route or registry to `DRIFTED`, `EXPIRED`, or `REVOKED`. Those states, and any unclassified state,
block the whole run.

An `ATTESTED_NON_AUTHORITY` route may validate compatibility or audit data, but its receipt is always
non-decisive. An `ATTESTED_NON_P5` route is rejected before payload serialization. The journal records
a gate-signed denial containing the route ID, policy hash, reason code, and attempted artifact ID; the
route receives no artifact bytes.

## Artifact lifecycle

The only successful lifecycle is:

```text
PREPARED
  -> ISSUE_JOURNALED
  -> DISPATCH_AUTHORIZED
  -> DISPATCH_JOURNALED
  -> RECEIPT_RECEIVED
  -> RECEIPT_VERIFIED
  -> CLOSED
```

Any unexpected transition, process exit, signature error, receipt mismatch, journal failure, registry
drift, or recovery ambiguity transitions the attempt to `QUARANTINED` and the run to
`RUN_INCONCLUSIVE`.

The issuer must durably append and `fsync` the issue and dispatch-intent records before making input
available to a consumer. Every journaled dispatch must have one unique terminal outcome. A missing
terminal outcome is not repaired by another consumer's success.

There is no silent retry. A deliberate rerun uses a new attempt ID and retains the prior attempt's
terminal or ambiguous state. An ambiguous prior attempt keeps the original run inconclusive.

## Canonical encoding and signatures

P6 control records use `canonical-json-v1`:

- UTF-8 without a byte-order mark;
- Unicode strings normalized to NFC;
- object keys ordered lexicographically by Unicode code point;
- no insignificant whitespace;
- integers and booleans are permitted; floating-point values are forbidden;
- duplicate keys, NaN, Infinity, and invalid Unicode are rejected.

Historical artifact payloads are opaque bytes for hashing and compatibility. They are not parsed and
re-serialized before their existing canonical hash is checked.

Ed25519 keys are separated by role: owner, issuer/gate, current consumer, and legacy consumer. Public
keys and key IDs are pinned in the run manifest. Consumer private keys are generated per run, passed
over inherited anonymous pipes, and never written to the evidence bundle. The evidence compiler holds
public keys only.

The journal uses SHA-256 hash chaining. Signatures establish record origin inside the test run; the
chain establishes ordering and tamper evidence. Neither substitutes for an external timestamp or a
production trust anchor.

## Artifact envelope

The signed outer envelope contains at least:

- `schema_version` and `canonicalization_version`;
- `artifact_id` and `run_id`;
- `epoch`, `lineage_root_id`, and nullable `parent_artifact_id`;
- byte-exact `payload_hash` and declared historical payload version;
- `registry_snapshot_hash` and `authority_policy_hash`;
- intended `route_id` and `consumer_id`;
- `issuer_key_id` and signature.

The envelope is additive. It does not alter the historical payload. A route mismatch is rejected before
consumer parsing.

## Receipts and gate denials

A consumer receipt binds:

- `receipt_version`, `receipt_id`, `artifact_id`, and artifact hash;
- `run_id`, `attempt_id`, `route_id`, and `consumer_id`;
- observed epoch, lineage root, and parent ID;
- validator version and validator source hash;
- registry snapshot and authority-policy hashes;
- `result`, stable `reason_code`, and boolean `decisive`;
- consumer key ID and Ed25519 signature.

Missing, duplicate, malformed, mismatched, stale, or incorrectly signed receipts fail closed. A valid
non-authority receipt proves execution and validation only; it can never grant authority.

For a denied `NON_P5`, unclassified, stale, or revoked route, the gate produces a signed denial record
instead of inventing a consumer receipt. Evidence must distinguish "not delivered" from "delivered and
rejected."

## Epoch and replay policy

Each lineage has a bootstrap epoch pinned in the manifest and two durable views: the issuer ledger and
the consumer's high-water record. Successful advancement is exactly `E -> E+1`.

- Exact replay of a previously observed artifact becomes `DUPLICATE_REPLAY`, non-decisive.
- A different artifact hash at an existing epoch becomes `EPOCH_CONFLICT`.
- Any lower epoch becomes `EPOCH_ROLLBACK`.
- Any unproved forward gap becomes `EPOCH_GAP`.
- A consumer high-water mark inconsistent with the issuer ledger makes the run inconclusive.

Recovery may inspect durable records but cannot infer acceptance from a process exit code. A signed,
verified receipt is required.

## Lineage policy

P6 uses a deliberately linear lineage:

- genesis has no parent;
- every later artifact has exactly one existing parent;
- a parent may have only one accepted child;
- `(lineage_root_id, epoch)` maps to exactly one artifact hash;
- artifact IDs are globally unique inside the run.

Merge, split, reused artifact ID, reused epoch with another hash, missing parent, and cross-lineage
parent references are adversarial canaries and must be rejected. Branching is not added implicitly; it
would require a new policy version and fresh adjudication.

## Historical compatibility matrix

The fixture corpus contains byte-frozen v1-v7 examples with expected raw SHA-256, existing canonical
hash, parse result, and semantic result. Two implementations evaluate every fixture:

1. the current consumer;
2. an independent legacy consumer in a separate process and source tree.

The legacy consumer may use only the frozen public contract and standard parsing/crypto dependencies.
It must not import the current producer, current consumer, shared parser, or shared normalization code.
Its source hash, command, minimal environment-key names, exit code, public key, and signed receipt are
recorded.

For every v1-v7 fixture, both paths must prove that the original bytes and canonical hash are unchanged.
The current consumer may interpret the additive envelope. The legacy path must either ignore it by
contract or explicitly accept the wrapper while preserving the inner historical bytes. Any migration
or silent rewrite is a failure.

## Failure injection and recovery

The deterministic failure matrix includes termination:

- before issue journaling;
- after durable issue, before dispatch intent;
- after durable dispatch intent, before consumer input becomes visible;
- after consumer input, before receipt creation;
- after receipt signing, before controller journal ingestion;
- during journal append and with a deliberately truncated tail;
- during evidence compilation.

It also injects artifact, signature, receipt, registry, key, epoch, and lineage corruption. A new
recovery process starts with no predecessor memory and reconstructs state from the durable journal and
receipt spool. It must quarantine ambiguous work and must not resend an artifact automatically.

Hard process termination plus clean-process recovery proves memory-independent recovery. It does not
prove physical host power-loss durability. Unless a separately approved VM or host test is executed,
the host-failure evidence field remains `UNPROVEN` and the overall package cannot state that named
evidence is complete.

## Isolation and data-loss prevention

Harness isolation requires:

- a unique per-consumer working directory;
- a minimal allowlisted environment;
- read-only envelope and public trust inputs;
- a private-key anonymous pipe unique to that process;
- a writable receipt spool unique to that attempt;
- no mounted holdout, oracle, sibling-consumer, report, or aggregate-result directory;
- no inherited standard input other than the defined key channel;
- captured and bounded stdout/stderr.

Unique forbidden canaries are placed in the holdout, oracle, key-source, sibling, and prohibited-result
locations. Receipts, journal records, stdout/stderr, temporary outputs, and the final bundle are scanned
for forbidden canaries. A separate synthetic positive-control output intentionally contains a safe
canary and must be detected; this prevents a nonfunctional scanner from reporting a false zero.

Same-user directory separation is harness isolation, not an OS security boundary. OS isolation requires
a separately approved low-privilege identity or sandbox, filesystem ACL proof, and network-deny proof.
If those controls are unavailable, `os_isolation` and `network_isolation` remain `UNPROVEN`, and the
evidence bundle remains incomplete for production-security claims.

## Telemetry provenance

Telemetry extraction reads numeric fields only and emits a sanitized derivative with source database
or rollout hash and query/extractor hash. It does not copy conversation content.

The already recovered native-run totals are:

| Run | Input | Output | Cached input | Reasoning output | Total | Turns | Sum of turn duration |
|---|---:|---:|---:|---:|---:|---:|---:|
| F2 | 181,713 | 14,340 | 148,224 | 9,648 | 196,053 | 9 | 424,246 ms |
| F3-short | 110,140 | 1,120 | 102,912 | 588 | 111,260 | 6 | 63,478 ms |
| F3-noisy | 110,106 | 1,304 | 103,936 | 735 | 111,410 | 6 | 97,736 ms |

`input` includes cached input as reported by the source usage record; cached input is shown as a
subset, not added again. Sum-of-turn duration is not mislabeled as end-to-end wall time. Rollout TTFT
and per-agent usage remain available as lower-level evidence.

Monetary cost requires an authoritative price snapshot binding provider/model identity, effective
date, input/output/cache/reasoning treatment, currency, and source hash. Without that snapshot, cost is
`COST_UNAVAILABLE`, never zero and never inferred from a similarly named public model.

## Evidence bundle

The final bundle contains no private keys and includes:

- scope and exclusion declaration;
- discovery snapshot, Merkle root, and scanner hash;
- complete owner attestation and owner public key;
- compiled registry and state transitions;
- source, command, environment-key-name, schema, and policy hashes;
- signed envelopes, receipts, and gate denials;
- journal segments, chain root, and recovery report;
- v1-v7 compatibility matrix and independent round-trip results;
- failure-injection matrix with expected and actual stable outcomes;
- epoch, replay, lineage, collision, and DLP canary results;
- sanitized telemetry with provenance;
- limitation ledger and overall evidence status.

The compiler must be deterministic except for explicitly declared run IDs, keys, and timing fields.
Recompiling the same immutable run inputs produces the same content manifest and evidence status.

## Chief evidence mapping

| Named evidence | P6 proof | Fail-closed condition |
|---|---|---|
| Owner-attested authoritative inventory | snapshot + Merkle root + complete attestation | omission, duplicate, drift, or expiry |
| Canonical/legacy compatibility | frozen v1-v7 bytes + independent consumer receipts | any byte/hash/semantic mismatch |
| Runtime behavior for every route | current/legacy dispatches and gate-signed pre-serialization denials | route without a unique terminal record |
| Actual receipts | per-consumer Ed25519 receipts from executed processes | absent, forged, duplicate, or mismatched receipt |
| Real issued-artifact epoch replay | durable issuer/consumer ledgers and replay injections | rollback, conflict, gap, or ledger divergence |
| Lineage/collision/canary | deterministic adversarial matrix and DLP positive control | any unexpected acceptance or missed positive control |
| Clean-path operational envelope | native SQLite/rollout telemetry and interaction journal | missing provenance or unavailable required price |

## Acceptance states

The overall status is one of:

- `EVIDENCE_COMPLETE`: every named local requirement passes and no required external claim is pending;
- `EVIDENCE_INCOMPLETE`: valid local evidence exists, but one or more named claims are unproved;
- `EVIDENCE_INVALID`: evidence integrity, provenance, or expected fail-closed behavior failed.

`EVIDENCE_COMPLETE` requires all of the following:

1. zero unclassified, expired, revoked, or drifted items in the attested scan scope;
2. unchanged v1-v7 bytes and canonical hashes in both implementations;
3. one expected runtime terminal outcome for every discovered route;
4. valid, unique receipts or gate denials for every attempted dispatch;
5. all failure injections fail closed with zero unresolved dispatches;
6. all epoch and lineage adversarial cases are rejected with the expected reason;
7. zero forbidden-canary leaks and a detected DLP positive control;
8. telemetry traces to immutable local source hashes;
9. every Chief-required cost or security-isolation field is proved rather than inferred.

If physical-host failure, OS/network isolation, or authoritative pricing remains required but unproved,
the correct result is `EVIDENCE_INCOMPLETE`. The package must not reinterpret a partial evidence pass as
a Chief approval.

## Implementation sequencing constraint

Implementation, when separately approved, should proceed in evidence-risk order:

1. freeze schemas, canonical encoding, reason codes, and acceptance tests;
2. implement bounded discovery and complete attestation validation;
3. implement registry, journal, issuer/gate, and deterministic recovery;
4. implement independent current and legacy consumer processes and receipts;
5. add compatibility, failure, epoch, lineage, and DLP matrices;
6. add sanitized telemetry extraction and evidence compilation;
7. execute the local shadow run and submit the unchanged design plus evidence to a fresh Chief.

No step may modify the installed skill or production configuration. Discovery must run again immediately
before the evidence run; a changed snapshot invalidates earlier attestation.

## Self-review

- The design distinguishes inventory discovery from owner authority classification.
- Generic plugins and `node_repl` are visible, classified `NON_P5`, and denied before serialization.
- Validation success is separate from decisive authority.
- Gate denials are not misrepresented as consumer receipts.
- Historical payload bytes and canonical hashes remain unchanged behind an additive envelope.
- Current and legacy consumers do not share application parsing code or private keys; use of the same
  reviewed cryptographic library is permitted and does not count as parser coupling.
- Cryptographic process identity is not overstated as organizational or cognitive independence.
- Process-kill recovery is not overstated as physical-host power-loss proof.
- Same-user working directories are not overstated as OS isolation.
- Cached tokens are disclosed as a subset of input and are not double-counted.
- Missing authoritative pricing becomes `COST_UNAVAILABLE`, not a fabricated estimate.
- Any missing named evidence produces `EVIDENCE_INCOMPLETE`, never implicit approval.
- Installed skill, production systems, network services, and external consumers remain unchanged.
