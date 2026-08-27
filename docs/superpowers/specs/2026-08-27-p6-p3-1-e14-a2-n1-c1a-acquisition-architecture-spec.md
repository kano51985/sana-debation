# E14 N1 C1a acquisition architecture specification

Date: 2026-08-27

Disposition: **APPROVED — SPECIFICATION ONLY / OPERATIONALLY BLOCKED**

This document freezes the written architecture for a future C1a acquisition pass. It does not
instantiate an acquisition manifest, receipt, capability, transaction, fixture, candidate, or
status record. It authorizes no network request, file acquisition, source opening for acquisition,
qualification, execution, implementation, commit, or push.

## Decision audit

- mode: `real-subagents/comparative`;
- startup: `core-two-phase-v1`, serial PREPARE in
  `Chief Architect -> Peer TL -> Proposing TL` order;
- Chief Architect: `/root/c1a_supply_chief`, readiness-only until the three rounds closed;
- Peer TL: `/root/c1a_supply_peer`, readiness-only until P0 and X0 routing;
- Proposing TL: `/root/c1a_supply_proposer`, activated only after all three core readiness receipts;
- Alternative Architect: `/root/c1a_supply_alternative`, created after core COMMIT with
  `P0_NOT_PROVIDED` and a distinct reproducibility/custody search contract;
- Proposer and Alternative independently converged on the same candidate family;
- Peer classified X0 as `converged_variant`, not a materially distinct architecture;
- all roles used fresh, separately instructed threads; this proves execution and instruction
  separation only, not cognitive independence; and
- Chief Architect disposition: **approve**, limited to this one written specification.

| Round | Attack axis | Peer disposition | Binding result |
|---|---|---|---|
| 1 | supply-chain identity, TCB, provenance | `accepted` after P1 | Restrict Node and Acorn claims to observed bytes; bind Node import to one handle; distinguish active TCB, suppliers, and deferred execution TCB; define TOFU and staging-to-CAS semantics. |
| 2 | state machine, crash, HTTP, durability | `modified` then incorporated in P2.1 | Freeze canonical pre-I/O intent; define namespace, body, retry, receipt, marker, and durability rules; make crash recovery read-only; reject non-NFC rather than normalizing it. |
| 3 | qualification handoff, portability, governance | `modified` then incorporated in P3.1 | Require exact stage capabilities and isolated work roots; leave license policy unauthorized; keep status evidence abstract; preserve the spec-only boundary. |

## Frozen evidence ledger

- `E-C1A-01`: D0a is terminal `CONSUMED`, `authority_effect=NONE`, and
  `next_stage_authorized=false`.
- `E-C1A-02`: global G0 remains `ISSUER_NOT_ESTABLISHED`.
- `E-C1A-03`: the admitted sequence remains
  `G0 -> D0a -> C1a acquisition -> C1a qualification -> D0b -> C0 -> C1b -> Chief B`.
- `E-C1A-04`: the local Node executable reports version `24.19.0`, has size `92,825,416`, and
  SHA-256 `3602F2BB1A10F2CBAB4C36886218A33C1AB3DB87290E73B033C46C77147D0237`.
- `E-C1A-05`: the [official Node v24.19.0 checksum list](https://nodejs.org/download/release/v24.19.0/SHASUMS256.txt)
  contains that digest for `win-x64/node.exe`. This is checksum correspondence, not publisher,
  build, install, custody, trust, safety, or authority proof.
- `E-C1A-06`: a portable Node v24.19.0 Windows x64 distribution exists, but it is not selected
  and is not an automatic fallback.
- `E-C1A-07`: Acorn is absent from the inspected bundled dependency tree.
- `E-C1A-08`: [external official package metadata](https://www.npmjs.com/package/acorn/v/8.18.0)
  describes Acorn `8.18.0`, MIT licensing, zero runtime dependencies, and
  `dist/acorn.js` / `dist/acorn.mjs`. Those claims are not bound to any future observed archive
  bytes.
- `E-C1A-09`: no trusted locally observed Acorn archive size or digest exists. Third-party search
  integrity is inadmissible.
- `E-C1A-10`: no real Node/Acorn qualification or execution has run.
- `E-C1A-11`: the D0a record remains untracked and unchanged; its immutable identifier is recorded
  as `ABSENT_NOT_PROVIDED`. The stipulated repository base is
  `8095b073b2622d770d15a3f32501efdffca54a26`.
- `E-C1A-12`: the target Windows/architecture/native DLL/search closure, exact runner bytes,
  options, entry model, and executable corpus remain unresolved.

## D1 architecture decision

### Selected candidate

Candidate A is the frozen written design:

1. perform a local by-value acquisition/import of the preexisting Node executable whose observed
   bytes must match `E-C1A-04` and the stipulated checksum entry;
2. acquire exactly one opaque response body for the requested Acorn URL;
3. place both role objects into a create-new, content-addressed quarantine transaction without
   extracting, loading, compiling, evaluating, or executing either object; and
4. issue no authority through the resulting custody records.

The local Node copy is an acquisition/import operation. The accurate identity claim is only:

> a preexisting executable whose transaction-time bytes match the stipulated Node 24.19.0
> checksum entry

Installed-bundle lineage, publisher/build provenance, trust, safety, portability, and execution
authority remain unverified.

The future registry response may be described only as:

> the byte sequence observed in response to the requested URL, identified by its locally observed
> digest

Its status is `OBSERVED_CUSTODY_IDENTITY_ONLY`. It must not be called a qualified or authenticated
Acorn 8.18.0 release.

### Nonselected candidates

- Candidate B, a separately acquired portable Node distribution plus Acorn, is a reconsideration
  option only after an explicit D1 reopening.
- Candidate C retains the JavaScript validation gap and is likewise a reconsideration option only.
- No mismatch, endpoint failure, policy failure, or qualification failure silently activates B or C.

### Binding clause index

The following clause IDs are normative and control the detailed sections below:

- `BA-01`: Candidate A is the selected written architecture; B and C require explicit D1
  reopening and are never automatic fallbacks.
- `BA-02`: Node and Acorn claims are limited to their stated observed-byte identities; provenance,
  authenticity, trust, safety, portability, licensing, and authority are not inferred.
- `BA-03`: `AcquisitionManifestV1` contains immutable pre-I/O intent; handle, filesystem,
  transport, byte, digest, size, and seal observations belong only in later records.
- `BA-04`: all records use the frozen canonical profile and fail closed on unknown or incompatible
  schema semantics.
- `BA-05`: the acquisition TCB, untrusted inputs, and later qualification/execution TCBs are
  distinct and explicitly enumerated.
- `BA-06`: local Node import is same-handle, no-follow, pre/post observed, exact-size/hash, and by
  value.
- `BA-07`: transactions and CAS objects use create-new, staging, bounded hash/flush, no-replace
  commit, reopen/rehash, no-adoption, and explicit collision/concurrency rules.
- `BA-08`: only the exact receipt/marker/tree binding graph followed by full post-seal verification
  is handoff-admissible; internal hashes prove consistency only.
- `BA-09`: the frozen HTTP profile permits one exact bounded request and treats all transport data
  as observations rather than provenance.
- `BA-10`: crashes never authorize abandoned-root mutation or resume; `STRONG_COMMIT_V1` remains
  evidence-blocked and has no silent downgrade.
- `BA-11`: acquisition closes two opaque role objects only and permits no inspection,
  materialization, installation, evaluation, or execution.
- `BA-12`: acquisition completion and receipts grant no authority and cannot authorize a successor
  stage.
- `BA-13`: qualification requires an exact external capability, separate create-new work root,
  read-only custody verification, and by-value materialization.
- `BA-14`: static qualification and dynamic execution have distinct receipts, authorities, target
  closure, runner, environment, and evidence requirements.
- `BA-15`: license policy is proposed but unauthorized; status, rollback, transfer, retention, GC,
  and deletion remain separately governed abstractions/actions.
- `BA-16`: D0a and the stage sequence remain unchanged and non-authorizing; this specification
  instantiates no operational object.

## Trust and authority model

### Active acquisition TCB

The active acquisition trusted computing base includes:

- OS kernel file-handle, path-resolution, storage, atomicity, and durability behavior;
- ACL creation, enforcement, observation, and sealing;
- SHA-256, byte counting, bounded streaming, and byte comparison;
- HTTP client, TLS implementation, resolver, socket stack, and platform trust store;
- enforcement of exact URL, redirect, proxy, authentication, cookie, compression, retry, framing,
  header, deadline, and byte-cap policy;
- canonical record serialization; and
- transaction, crash, completion, and handoff verification logic.

The mutable local cache, local source bytes before observation, registry endpoint, response bytes,
and external package/license/version assertions are untrusted suppliers or inputs. Node, Acorn,
the runner, module loader, candidate bytes, and fixture bytes belong to later qualification or
execution TCBs and are not active during acquisition.

A hostile process with the same SID or administrative authority remains inside the acquisition
TCB unless a separately established OS identity, sandbox, or VM boundary proves otherwise.

### Authority rules

- Manifest, object, digest, receipt, path, `COMPLETE`, filename, package coordinate, and checksum
  correspondence grant no authority.
- A record field `authority_effect="NONE"` means that the record itself grants, mints, or delegates
  no authority. It does not claim that the recorded operation lacked prior external authority.
- Every operational stage requires a separately issued and validated external capability binding
  that stage's exact inputs and procedure.
- A receipt may inform a future issuer. It can never substitute for the next-stage capability.

## Normative record model

This section defines schemas and constraints only. It does not instantiate a record.

### Canonical profile

- Encoding is UTF-8 JSON under RFC 8785 JCS.
- Every string is validated as NFC before serialization. Non-NFC input is rejected and never
  normalized or rewritten.
- Duplicate keys, comments, BOM, floats, exponent forms, `NaN`, infinities, and negative zero are
  prohibited.
- JSON numeric values are schema-bounded integers. Precision-sensitive or out-of-range values use
  canonical decimal strings.
- Digests are lowercase hexadecimal SHA-256 values.
- Every schema/profile version and required feature set is explicit. Unknown or missing required
  semantics fail closed.
- There is no silent upgrade, downgrade, default substitution, normalization, or lossy conversion.
  An adapter creates a new derived record binding the source digest, adapter identity/version,
  procedure, and loss report.

### `AcquisitionManifestV1`

The manifest is immutable preflight intent. It contains no `manifest_sha256` or other self-digest.
Before any transaction, source, or network I/O, the future authorized process must independently
select the transaction ID, attempt ID, exact absolute root locator, expected store/volume policy,
and canonical manifest bytes.

The schema must bind at least:

```text
schema/profile/required_features
decision = D1 / candidate = A
transaction_id / attempt_id / maximum_attempts = 1
canonical absolute root locator
expected custody-store, volume, ACL, retention, and durability profiles
lineage state and stipulated base commit
authority and stage restrictions
exact Node source locator, expected size, and expected digest
requested package coordinate and exact registry URL
network, namespace, cap, deadline, and transformation policy
fact classifications and unresolved facts
qualification and execution prohibitions
```

The exact root and IDs must not derive from the manifest digest. Canonical path text is only a
locator and comparison value; handle-derived volume and file identities are authoritative.

The future process must freeze canonical bytes in memory, create the predetermined root with
create-new semantics, write and flush the exact bytes, reopen and rehash/recompare them, and only
then open a source or initiate a network operation.

### Fact classes

Normative fact classes are:

```text
POLICY
STIPULATED
EXTERNALLY_ASSERTED
HANDLE_OBSERVED
BYTE_OBSERVED
QUALIFICATION_DERIVED
UNRESOLVED
```

Acorn name, version, license, dependency, and entry-file claims remain
`EXTERNALLY_ASSERTED` until a later digest-bound qualification. Actual archive size and digest are
`NOT_YET_OBSERVED` in preflight and may become `BYTE_OBSERVED` only through an authorized
acquisition. A first observation creates custody identity only.

### `AcquisitionReceiptV1`

The receipt schema must bind:

```text
schema/profile/required_features
manifest_sha256
transaction_id / attempt_id
two exact role observations
role-to-object digest and size references
unique_object_count and role_count
retained-handle source and destination observations
bounded transport/TLS observations
policy outcome and intended seal policy
authorizing external capability digest and validation result
stage = C1a_ACQUISITION_CUSTODY
qualified = false
promotion_authorized = false
execution_authorized = false
discovery_authorized = false
authority_effect = NONE
```

The receipt must not bind a completion-marker digest. It proves internal custody-record
consistency only, never authenticity, provenance, licensing, safety, qualification, or authority.

### `AcquisitionCompletionV1`

The `COMPLETE` marker schema must bind:

```text
schema/profile/required_features
manifest_sha256
receipt_sha256
transaction_id / attempt_id
completion_format_version
required_acl_descriptor_sha256
```

This graph is acyclic: objects and manifest precede the receipt; the marker binds the receipt; the
receipt does not bind the marker. `COMPLETE` means only
`ACQUISITION_TRANSACTION_COMPLETE_ONLY` and is necessary but insufficient for handoff.

## Normative acquisition state machine

No state below exists operationally until separate authority and every before-acquisition gate pass.

```text
PREFLIGHT_FROZEN
  -> MANIFEST_PERSISTED_VERIFIED
  -> LOCAL_ROLE_STAGING
  -> LOCAL_ROLE_COMMITTED_UNCLAIMED
  -> NETWORK_ROLE_STAGING
  -> NETWORK_ROLE_COMMITTED_UNCLAIMED
  -> RECEIPT_PERSISTED_VERIFIED
  -> COMPLETE_PERSISTED
  -> ACL_SEALED
  -> FULL_GRAPH_REOPEN_VERIFIED
```

Only `FULL_GRAPH_REOPEN_VERIFIED` is handoff-admissible. A `COMPLETE` marker without exact
namespace, binding, object, identity, ACL, and selected-durability verification is invalid.

The exact valid success tree is:

```text
AcquisitionManifestV1.json
objects/
  sha256/
    <one-or-two lowercase SHA-256 object names>
AcquisitionReceiptV1.json
COMPLETE
```

No staging file, diagnostic journal, unexpected stream, file, directory, alias, link, reparse
point, or other namespace entry may remain.

### Namespace and CAS rules

- Use a unique create-new transaction root and hold an exclusive cooperative transaction lock and
  exclusive handles where the platform permits.
- Generate fixed ASCII components from protocol labels and lowercase hexadecimal values only.
- Reject rooted, drive-relative, UNC, device, ADS, separator, dot-segment, reserved-name,
  trailing-dot/space, Unicode-confusable, and case-folding aliases.
- Resolve descendants handle-relative to a verified root handle where supported.
- Require regular, single-unnamed-stream, non-reparse, link-count-one files on the frozen volume.
- Treat an unexpected preexisting digest object as an invariant failure; never adopt it.
- Stage outside the committed object namespace. Enforce bounds while streaming and hashing, flush,
  derive the digest, and atomically move same-volume with no replacement to
  `objects/sha256/<digest>`.
- Reopen the committed object, verify handle identity, size, and digest, and flush the final object.
- Before receipt issuance, an object is transaction-private `COMMITTED_UNCLAIMED` and is not
  handoff-visible.
- If both roles have the same digest, require equal lengths and full byte equality before allowing
  two role references to one object. Different bytes under one digest are terminal
  `HASH_COLLISION`.

### Local Node import

- Open the frozen local source exactly once with no-follow/reparse-aware semantics and sharing that
  permits reads but denies write/delete where supported.
- From the same handle, record final normalized path, volume ID, file ID, type, attributes/reparse
  state, link count, size, timestamps, stream inventory, owner, and DACL observations.
- Require a regular, non-reparse file and stream exclusively from that handle.
- Enforce exact size `92,825,416` and expected digest
  `3602F2BB1A10F2CBAB4C36886218A33C1AB3DB87290E73B033C46C77147D0237`.
- Re-query the same handle after EOF. Any identity, type, size, timestamp, link, reparse, stream, or
  security-state change is terminal.
- Copy by value; hardlinks are prohibited. A successful checksum comparison does not upgrade the
  source's provenance claims.

### HTTP acquisition profile

The only proposed URL is:

```text
https://registry.npmjs.org/acorn/-/acorn-8.18.0.tgz
```

The HTTP profile is:

- a fresh client and connection context;
- one logical DNS resolution, retaining no more than eight returned addresses and selecting only
  the first eligible address in resolver-return order;
- exactly one TCP connection, one TLS handshake, and one GET emission;
- no alternate-address attempt, redirect, retry, resume/range, proxy, authentication/default
  credentials, cookies, cache, connection reuse, automatic decompression, Alt-Svc, or TLS 0-RTT;
- SNI and hostname verification for exactly `registry.npmjs.org`;
- reject every 3xx response without following it; require status `200`;
- request `Accept-Encoding: identity` and require `Content-Encoding` absent or exactly `identity`;
- define custody bytes as the message body after transfer-framing removal and before content
  transformation;
- allow a missing `Content-Length`; if present, require one canonical nonnegative value within the
  cap and exact equality with observed body bytes;
- reject trailers;
- limit headers to 64 entries, 8 KiB per field, and 32 KiB aggregate;
- record only bounded allowlisted transport observations; never persist cookies, credentials,
  environment values, or unrestricted headers;
- cap the body at `4,194,304` bytes before writing an overflow byte, with a read buffer no larger
  than 64 KiB; and
- use monotonic deadlines of 10 seconds DNS, 10 seconds TCP, 15 seconds TLS, 15 seconds response
  headers, 15 seconds body idle, and 120 seconds total.

OS packet retransmission inside the one TCP operation is transport behavior. A repeated DNS
resolution, alternate address, new connection, repeated TLS handshake, or repeated HTTP emission
is a forbidden new application attempt. Remote endpoint, DNS, ALPN, TLS, certificate-chain, and
trust-store data are observations only and do not prove directness, publisher identity, or
provenance.

### Crash and durability rules

- A caught failure may allow only the original live transaction to write and flush `FAILURE`
  before applying a read-only seal.
- A crash creates implicit incompleteness through the absence of a valid `COMPLETE` graph.
- A later recovery process may inspect an abandoned root read-only. It may not append, mark, seal,
  repair, delete, resume, adopt, or synthesize success in that root.
- `INCOMPLETE` is a verifier outcome, not a recovery-created file.
- A retry requires new external authority, a new immutable manifest, attempt ID, and create-new root.

The selected design requirement is:

```text
durability_profile = STRONG_COMMIT_V1
profile_status = BLOCKED_PENDING_EVIDENCE
```

It requires staging flush, same-volume atomic no-replace commit, final-name reopen/verify/flush,
equivalent receipt persistence, `COMPLETE` last, supported directory/volume metadata durability,
exact ACL sealing, and full graph reopen verification. No API success is itself a durability proof.

`REHASH_REQUIRED_CUSTODY_V1` is an unselected alternative. It makes no power-loss durability claim
and would require full graph revalidation at every handoff. Selecting it requires a separate
issuer-authorized policy decision and capability update; it is never an automatic downgrade.

## Acquisition and qualification separation

The acquisition byte closure contains exactly two opaque role objects plus their records. It is
not an execution closure. Acquisition prohibits archive parsing or extraction, installation,
package-manager or lifecycle actions, import, evaluation, compilation, execution, runner creation,
fixture creation, and candidate creation.

A future `QualificationCapabilityV1` must bind at least:

```text
manifest_sha256
acquisition_receipt_sha256
node_role_sha256
registry_object_role_sha256
qualification_schema_version
qualification_profile_id
qualification_procedure_sha256
allowed_operations
expiry/status semantics
```

Qualification must use a separate create-new work root, open custody read-only, verify the complete
acquisition graph, and copy by value before any materialization. It must never inspect, extract,
install, or execute inside the custody root.

Static archive inspection/extraction requires its own authorized scope and a bounded hostile-archive
parser/extractor. Dynamic Node execution requires a separate execution capability. Static work
produces `QualificationReceiptV1`; a dynamic run produces `ExecutionReceiptV1`. Both bind the exact
external capability digest and validation result, and neither authorizes a successor stage.

Before dynamic execution, the evidence must bind:

- exact target OS family, release/build, architecture, execution policy, native dependencies, and
  loader/DLL search closure;
- exact archive format, member inventory, package identity/version, dependencies, entry files,
  license/NOTICE, companion objects, and archive-safety results;
- exact runner digest, Node digest, flags/options, working directory, module-resolution rules,
  environment allowlist, fixtures, candidates, inputs, and expected output schema; and
- no ambient module resolution, package installation, or network access.

## Governance, custody, update, and rollback

The proposed license policy is:

```text
proposed_policy = UNKNOWN_LICENSE_CUSTODY_ALLOWED_V1
selection_status = UNAUTHORIZED_PENDING_ISSUER
```

No license-custody policy is currently selected. An issuer choice of
`KNOWN_LICENSE_BEFORE_CUSTODY_V1` blocks Candidate A until independently digest-bound license
evidence exists. Under the proposed quarantine policy, observed objects remain
`LICENSE_UNVERIFIED`; promotion, redistribution, and dynamic execution remain prohibited pending
digest-bound clearance.

- Every new endpoint observation, version, URL, object, policy, or procedure creates a new manifest
  and receipt; historical records are immutable.
- Endpoint byte drift is a new object, never an edit or a stable `latest` alias.
- Qualification, promotion, revocation, retention, rollback, and disposal status require an
  abstract digest-keyed status-evidence interface. Its implementation, issuer, authentication,
  append-only behavior, persistence, and availability remain unselected evidence requirements.
- Rollback requires new authority naming an exact previously qualified digest/receipt set and a
  current revocation and policy check.
- Relocation requires a separately authorized by-value transfer, complete rehash and namespace
  verification, and `CustodyTransferReceiptV1` lineage. A path change is not transfer evidence.
- Garbage collection or deletion requires separate destructive authority, exact targets, live
  reference checks, and a declared recovery policy. Retention expiry alone deletes nothing.
- Paths are non-authoritative locators. Store identifier, volume, retention class, and durability
  profile are frozen policy inputs; digest-bound receipts preserve identity.

## Lineage and compatibility

The D0a lineage remains:

```text
d0a_state = CONSUMED
d0a_identifier = ABSENT_NOT_PROVIDED
d0a_tracked = false
d0a_authority_effect = NONE
base_head = 8095b073b2622d770d15a3f32501efdffca54a26
```

This specification does not repair, sign, replace, or operationalize D0a. Future conformance
fixtures must be test-only and rejected by operational readers. Capability negotiation must occur
before authority issuance and bind exact schema, profile, durability class, algorithms, and
required features.

## Trace matrix

| Trace | Round / issue | Binding correction | Residual risk |
|---|---|---|---|
| `TR-R1-01` | checksum/provenance overclaim | Restrict Node claim to observed byte correspondence | `RK-01` |
| `TR-R1-02` | TCB conflation | Separate acquisition TCB, suppliers, and execution TCB | `RK-02`, `RK-04` |
| `TR-R1-03` | local-source TOCTOU | One-handle stream with pre/post identity observations | `RK-02` |
| `TR-R1-04` | Acorn TOFU | Custody-only digest identity pending qualification | `RK-01`, `RK-05` |
| `TR-R1-05` | CAS staging/collision/concurrency | Create-new, staging, no-replace, reopen, no adoption | `RK-02` |
| `TR-R1-06` | unbound license/closure | Leave policy issuer-selected; defer digest-bound closure | `RK-05`, `RK-06` |
| `TR-R2-01` | canonical manifest | JCS, NFC rejection, bounded numbers, no self-digest | `RK-08` |
| `TR-R2-02` | path escape/aliases | Handle-relative fixed namespace and exhaustive rejection | `RK-02` |
| `TR-R2-03` | CAS ownership/concurrency | Private unclaimed objects, locks, explicit same-SID boundary | `RK-02`, `RK-04` |
| `TR-R2-04` | power-loss durability | Strong profile selected but evidence-blocked | `RK-02`, `RK-07` |
| `TR-R2-05` | HTTP body semantics | Exact framing/transformation boundary and strict limits | `RK-03` |
| `TR-R2-06` | proxy/TLS overclaim | Transport observations only | `RK-01`, `RK-03` |
| `TR-R2-07` | cyclic record graph | Receipt precedes and is bound by marker | `RK-07`, `RK-08` |
| `TR-R2-08` | journal/failure/seal | Exact success tree and marker-last semantics | `RK-07` |
| `TR-R2-09` | timeout/cap/retry | One application attempt and monotonic bounds | `RK-03` |
| `TR-R2-10` | recovery mutation/Unicode normalization | Read-only recovery; validate and reject non-NFC | `RK-07`, `RK-08` |
| `TR-R3-01` | authority confusion | Custody-only completion and external stage capabilities | `RK-06` |
| `TR-R3-02` | broad qualification label | Bind exact digests and procedure | `RK-06`, `RK-09` |
| `TR-R3-03` | shared work roots | Separate root and by-value materialization | `RK-02`, `RK-05` |
| `TR-R3-04` | target portability | Require exact target and native/search closure | `RK-05` |
| `TR-R3-05` | notices/companion artifacts | Require digest-bound runtime/legal closure | `RK-05` |
| `TR-R3-06` | Acorn identity | Separate URL observation from package qualification | `RK-01`, `RK-05` |
| `TR-R3-07` | license selection | Keep proposed policy unauthorized | `RK-05`, `RK-06` |
| `TR-R3-08` | mutable status/revocation | Immutable receipts and abstract status interface | `RK-06` |
| `TR-R3-09` | D0a lineage | Preserve untracked, absent-ID, non-authorizing state | `RK-06` |
| `TR-R3-10` | schema evolution | Exact fail-closed versions and derived adapters | `RK-08` |
| `TR-R3-11` | custody transfer | Separately authorized transfer receipt | `RK-02`, `RK-06` |
| `TR-R3-12` | proportional durability | Strong target blocked; weaker profile unselected | `RK-02`, `RK-07` |
| `TR-R3-13` | ledger/platform expansion | Abstract interface only; no platform instantiated | `RK-06` |

## Evidence gates

All gates in a phase are conjunctive. A later gate cannot repair or waive an earlier gate.

### Before acquisition

- `EG-A01`: establish G0 issuer and a validated stage-scoped external acquisition capability.
- `EG-A02`: issuer freezes and authorizes license-custody, store/retention, and durability policy.
- `EG-A03`: canonical schema/profile/capability conformance passes.
- `EG-A04`: establish Windows no-follow, handle-relative, no-replace, ACL, directory-durability,
  and volume-durability primitive mappings.
- `EG-A05`: establish canonical manifest, receipt, and marker byte/hash vectors.
- `EG-A06`: exhaustive crash and power-fault state tests pass.
- `EG-A07`: HTTP/wire traces prove exact no-retry, proxy, decompression, timeout, header, framing,
  and body-cap rules.
- `EG-A08`: namespace and handoff mutation tests pass.
- `EG-A09`: establish the same-SID and external-integrity boundary.
- `EG-A10`: transaction-time Node same-handle identity and digest meet frozen policy.
- `EG-A11`: operational readers reject design fixtures and discovery-by-path/marker.
- `EG-A12`: evidence the selected status interface's implementation, authentication, issuer
  binding, append-only semantics, and persistence.

### Before qualification

- `EG-Q01`: issue and validate an exact-digest `QualificationCapabilityV1`.
- `EG-Q02`: read-only reopen/rehash of the acquisition graph and current revocation/policy check pass.
- `EG-Q03`: establish bounded hostile-archive parsing/extraction and a no-network create-new work root.
- `EG-Q04`: establish target OS/build/architecture/policy and native DLL/search closure.
- `EG-Q05`: establish digest-bound package identity, inventory, dependencies, entries,
  license/NOTICE, companion closure, and archive safety.
- `EG-Q06`: establish the exact historical D0a lineage without changing it.

### Before dynamic execution

- `EG-X01`: issue and validate a separate exact execution capability.
- `EG-X02`: bind exact materialized digests, runner, options/flags, module resolution, and fixtures.
- `EG-X03`: establish compatibility results for the intended workload.
- `EG-X04`: establish hermetic execution closure, sandbox, resource, network, input, and output controls.
- `EG-X05`: validate current license, revocation, and promotion policy.

## Risk register

| Risk | Description | Current treatment |
|---|---|---|
| `RK-01` | Custody/checksum identity mistaken for provenance or release identity | Restrict claims; require digest-bound qualification |
| `RK-02` | Filesystem, namespace, ACL, atomicity, or durability semantics unavailable | Block on platform evidence |
| `RK-03` | HTTP stack cannot expose or enforce frozen wire profile | Block on wire evidence |
| `RK-04` | Same-SID/admin interference | Declare inside TCB or require stronger boundary |
| `RK-05` | Package, legal, target, or native closure insufficient | Qualification gate and possible D1 reopening |
| `RK-06` | Issuer, authority, status, revocation, transfer, and retention unestablished | Keep interfaces abstract and stages unauthorized |
| `RK-07` | Crash/power-loss violates strong commit | Block on fault evidence; no silent downgrade |
| `RK-08` | Canonical record interoperability fails | Canonical vectors and fail-closed readers |
| `RK-09` | Runner, fixture, resolution, or hermetic closure unresolved | Separate execution gates |

## Candidate-A falsifiers

- `FAL-A-01`: stable same-handle Node mismatch or unavailability.
- `FAL-A-02`: policy requires authenticated Node provenance or independently pinned Acorn
  integrity before acquisition.
- `FAL-A-03`: the platform cannot enforce the namespace, ACL, selected durability, or wire invariants.
- `FAL-A-04`: concrete runtime, redistribution, license/NOTICE, companion, or native closure is
  insufficient.
- `FAL-A-05`: an authorized issuer selects known-license-before-custody policy.

A falsifier reopens D1. It never activates Candidate B or C automatically.

## Current terminal boundary

This specification is the only artifact authorized by the Chief disposition. Its creation does not
advance C1a, satisfy an evidence gate, select a license policy operationally, instantiate a status
platform, or establish G0.

Prohibited under this disposition:

- acquisition, download, registry request, source opening for acquisition, operational hashing,
  staging, CAS mutation, extraction, installation, compilation, evaluation, execution, or evidence
  gathering;
- creation of an operational manifest, receipt, marker, capability, fixture, candidate, status
  record, transfer record, rollback record, or GC/deletion action;
- implementation, tests that exercise operational acquisition, deployment, unrelated workspace
  mutation, commit, or push;
- provenance, authenticity, qualification, safety, promotion, execution-readiness, or stage-authority
  claims; and
- fallback, durability downgrade, abandoned-root mutation, implicit conversion, adoption, relocation,
  or deletion.

The next operational step remains blocked by `EG-A01` through `EG-A12`. Any further written or
evidence tranche requires a separately bounded decision.
