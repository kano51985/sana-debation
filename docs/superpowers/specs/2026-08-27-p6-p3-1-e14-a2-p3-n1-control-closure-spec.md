# P3-N1 G7 control-closure specification

Date: 2026-08-27

Status: v2 design approved with pre-code gates; no operational authority.

Profile: `P3_N1_CONTROL_CLOSURE_V1`

This specification records the Chief Architect's approved additive A2-only alternative to strict
G7. It does not weaken, rename, or reinterpret legacy G7/G8/G9. It defines a control-closure claim,
not universal observation of every CPython module event.

No object in this document is an authorization. No image, container, output reservation, ledger,
qualification, G8 authorization, G9 terminal, or admission root is created by this phase.

## 1. Decision and precedence

1. Legacy strict G7/G8/G9 remains unchanged and remains the default when the N1 selector is absent.
2. N1 is selected only by exact `profile_kind=P3_N1_CONTROL_CLOSURE_V1` and applies only to A2.
3. N1 and legacy artifacts mutually reject. Conversion, fallback, downgrade, upconversion, resume,
   and reinterpretation are prohibited.
4. The current `sha256:c459db0b82f43b3b8fe0fb7b5d12d902c449764e9f1260c8483ce459514b9e89`
   image is ineligible. N1 requires a dedicated image whose final mounted
   view equals a finite normative manifest exactly.
5. N1 treats the approved image, interpreter, embedded modules, standard library, native runtime,
   scanner, verifier, controller, local ledger, authorization verifier, and finalizer as explicit
   TCB. It makes no claim against malicious approved TCB.
6. Guest module lists and guest PASS claims are diagnostic only.

## 2. Lifecycle-v2 envelope and hash domain

Every future N1 artifact uses strict UTF-8 JSON, no BOM, no duplicate keys, no comments, and no
trailing data. The exact operational envelope contains five members and no others:

```json
{
  "schema": "sana.e14.n1.lifecycle-artifact.v2",
  "artifact_kind": "<allowed N1 kind>",
  "profile_kind": "P3_N1_CONTROL_CLOSURE_V1",
  "content_root": "sha256-jcs-e14-n1-v2:<64 lowercase hex>",
  "payload": {}
}
```

`fixture_only` and top-level `authority_effect` are forbidden. Kind-specific `authority_effect`
inside `payload` is the only content effect field and does not itself grant authority.

The exact four-member commitment and typed root are:

```text
commitment = {
  "schema":        "sana.e14.n1.lifecycle-artifact.v2",
  "artifact_kind": artifact_kind,
  "profile_kind":  "P3_N1_CONTROL_CLOSURE_V1",
  "payload":       payload
}

commitment_bytes = N1-V2-CANON(commitment)
digest = SHA-256(
           UTF8("sana.e14.n1.lifecycle-artifact.v2\n")
           || commitment_bytes
         )
content_root = "sha256-jcs-e14-n1-v2:" || lowercase_hex(digest)
```

The root is outside the commitment and payload. The commitment is constructed from exactly the four
named parsed values; implementations must not copy the envelope and generically delete the root.
Every reference is an exact typed root, never a path, filename, logical ID, summary, or reconstructed
equivalent. The normative schema is `schemas/e14-a2-n1-lifecycle-v2.schema.json`. Draft v1 is
unissued, retired, and never accepted, translated, stripped, or re-rooted.

### 2.1 Restricted canonical input profile

`N1-V2-CANON` is not a general JCS implementation. It accepts a strict subset whose output is
byte-for-byte identical to RFC 8785 for every accepted value:

- decoded object names are ASCII and at most 160 characters;
- string values preserve valid Unicode without normalization and are limited to 1,024 Unicode
  scalars and 4,096 UTF-8 bytes;
- lone surrogates are rejected and valid surrogate pairs are accepted;
- number tokens are minimal safe integers matching `0|-?[1-9][0-9]{0,15}` in the inclusive range
  `-9007199254740991..9007199254740991`;
- decimal points, exponents, `-0`, and out-of-range integers are rejected; and
- arrays are forbidden because lifecycle-v2 has no array-valued field.

Any future non-ASCII key or noninteger numeric support requires a new schema, domain, and typed-root
version. It cannot be introduced by relaxing v2.

### 2.2 Bounded raw parsing

The v2 safety limits are 262,144 raw bytes, depth 12, 4,096 total value nodes, 2,048 total object
members, and 128 members in one object. The root object has depth 1; each value including an object,
string, number, boolean, or null counts as one node; property names are not nodes; every syntactic
pair counts as a member, including a duplicate before rejection. Limits are enforced left-to-right
during tokenization. A `[` fails immediately.

Raw offsets are zero-based octet positions. Key limits are measured after unescaping in ASCII
characters. String limits are measured after unescaping in Unicode scalars and UTF-8 bytes. The
pre-code headroom report must prove every schema-valid artifact fits and that parser safety limits
have at least two times the schema-derived maximum.

### 2.3 Nominal routes and pure APIs

Lifecycle verification requires exact selector
`N1_LIFECYCLE_ARTIFACT_V2` and media type
`application/vnd.sana.e14.n1-lifecycle-artifact-v2+json`. Scenario fixtures use a separate selector,
media type, schema, API, and result type. No generic normalizer, wrapper, field stripper, default, or
v1 upconverter is permitted.

`verify_content(raw_bytes, explicit_route)` returns content-only
`VerifiedLifecycleArtifactV2` or a typed failure. `evaluate_use(verified, now_utc, revocation)`
receives explicit immutable time and revocation inputs. Neither API reads a clock, filesystem,
network, environment, cache, registry, or mutable global, and neither grants authority.

The processing order is route/media, raw-size check, bounded strict parsing, exact envelope,
kind-specific payload, commitment encoding, and root comparison. Route failures precede parsing;
raw failures return the earliest byte offset; semantic failures return a stable JSON Pointer where
available.

The behavioral corpus is a separate nonartifact format. It contains no lifecycle root and cannot
be converted to an operational artifact by any public I0 API.

### 2.4 Frozen verification failures

I0 exposes only these content-verification failure codes:

```text
N1_ROUTE_SELECTOR_MISSING
N1_ROUTE_SELECTOR_UNSUPPORTED
N1_ROUTE_MEDIA_TYPE_MISMATCH
N1_RAW_TOO_LARGE
N1_JSON_BOM
N1_JSON_INVALID_UTF8
N1_JSON_SYNTAX
N1_JSON_TRAILING_DATA
N1_JSON_ARRAY_FORBIDDEN
N1_JSON_DUPLICATE_KEY
N1_JSON_DEPTH_LIMIT
N1_JSON_NODE_LIMIT
N1_JSON_MEMBER_LIMIT
N1_JSON_OBJECT_MEMBER_LIMIT
N1_JSON_KEY_NON_ASCII
N1_JSON_KEY_TOO_LONG
N1_JSON_STRING_SCALAR_LIMIT
N1_JSON_STRING_UTF8_LIMIT
N1_JSON_SURROGATE_INVALID
N1_JSON_NUMBER_FORBIDDEN
N1_JSON_INTEGER_RANGE
N1_ENVELOPE_FIELD_SET
N1_SCHEMA_UNSUPPORTED
N1_PROFILE_KIND_MISMATCH
N1_ARTIFACT_KIND_UNSUPPORTED
N1_PAYLOAD_INVALID
N1_CONTENT_ROOT_FORMAT
N1_CONTENT_ROOT_MISMATCH
```

Precedence is: missing/unsupported selector, media mismatch, raw-size, BOM, the first raw parser
failure encountered left-to-right, exact envelope field set, schema, profile, artifact kind,
kind-specific payload, root format, then root equality. Parser failures carry the zero-based octet
offset of the first decisive byte. Semantic failures carry the first deterministic JSON Pointer;
the root object uses the empty pointer. Limit failures also carry the frozen limit and the first
observed value that exceeds it. Failure details are diagnostics only and are not stable protocol
inputs.

`evaluate_use` returns exactly `N1_USE_VALID`, `N1_USE_NOT_YET_VALID`, `N1_USE_EXPIRED`,
`N1_USE_REVOKED`, or `N1_USE_INVALID_INTERVAL`. It checks explicit root revocation, policy epoch,
interval consistency, not-before, and half-open expiry in that order after validating the supplied
canonical UTC time. These are content-use diagnostics only; even `N1_USE_VALID` grants no role,
signature, start, finalization, or admission authority.

## 3. Authority separation

`N1_ISSUER_POLICY_ROOT` binds:

- exact profile/schema/kind and `scope=A2`;
- permitted environment and platform tuple;
- qualification, preparation, authorization, run, and finalization evidence predicates;
- maximum qualification and authorization validity;
- revocation authority and epoch rules;
- compatibility and no-conversion rules; and
- separately scoped role/key identifiers.

The following roles are non-interchangeable:

| Role | May do | Must not do |
|---|---|---|
| Policy issuer | Publish the exact N1 rule | Qualify a profile, start or finalize a run |
| Qualification issuer | Issue `N1_PROFILE_QUALIFIED` | Start a container or emit a terminal |
| G8 authorizer | Authorize one exact prepared run | Qualify a profile or finalize |
| Controller | Exercise one exact G8 authorization | Create policy, qualification, or terminal authority |
| G9 finalizer | Verify and emit the sole final outcome | Start the guest or trust a guest terminal |

Role identity, key scope, validity, and revocation are qualification predicates. A successful
hash check grants no authority.

## 4. Normative lifecycle

```text
N1 policy published
  -> N1_PROFILE_QUALIFIED
  -> N1_OUTPUT_RESERVED
  -> N1_CONTAINER_PREPARED
  -> G8_N1_RUN_AUTHORIZED
  -> N1_RUNNING
  -> N1_RUN_CLOSED
  -> N1_RUN_EVIDENCE_CANDIDATE
  -> G9_N1_FINALIZER
  -> N1_FINAL_PASS | N1_FINAL_DENY | N1_INDETERMINATE_BLOCK
```

No artifact binds a future result. Every transition is monotonic and exact-root bound.

### 4.1 `N1_PROFILE_QUALIFIED`

This is N1's pre-G8 G7 acceptance artifact. It has `authority_effect=NONE` and binds:

- issuer-policy root, validity, qualification issuer, and revocation epoch;
- dedicated image and normative final-view manifest;
- interpreter, embedded/frozen inventory, stdlib and native closure;
- scanner, static callback manifest, data-nonexecution policy, review, and negative tests;
- OCI verifier, controller, authorization verifier, finalizer, and local ledger;
- loader/bootstrap/late-load closure and adversarial fixture roots;
- exact platform TCB tuple; and
- consumer-routing, blocker, revocation, and rollback conformance roots.

Qualification authorizes use of the profile as a prerequisite only. It cannot start a run.

### 4.2 `N1_OUTPUT_RESERVED`

The controller atomically creates a private empty output object. The record binds:

- immutable object identity;
- domain-separated empty initial inventory root;
- authenticated exclusive single-use lease;
- creation event; and
- empty attachment-history root.

A replaceable pathname and an emptiness check are insufficient. If object identity, exclusive
attachment, or lease semantics cannot be evidenced on the selected platform, N1 is unavailable.

### 4.3 `N1_CONTAINER_PREPARED`

A stopped container may be created before G8 only when qualification proves that preparation:

- executes no guest code;
- executes no unqualified OCI hook, runtime plugin, initializer, or helper;
- binds immutable image, container, command, environment, mounts, platform, and output identity;
- grants exclusive start capability to the qualified controller; and
- cannot be attached to or started through another route.

Failure to obtain G8 destroys the stopped container, invalidates its output lease, and emits no
completion-like terminal.

### 4.4 `G8_N1_RUN_AUTHORIZED`

This is the sole start authority. It binds only facts available before execution:

- current issuer-policy and qualification roots;
- fresh, unique, single-use and, where prepositioning matters, unpredictable run nonce;
- request, exact A1/vendor roots, and G1-G6 evidence roots;
- stopped container ID and immutable inspected configuration;
- exact launch, final-mount, environment, platform, controller, and finalizer roots;
- output reservation, immutable object, lease, and empty initial root;
- issuance, not-before, expiry, run sequence, and predecessor final-record root; and
- `single_use=true`.

It never binds a future evidence candidate. Authorization failure invalidates the prepared resources
without terminal emission.

### 4.5 `N1_RUN_EVIDENCE_CANDIDATE`

After PID1 closes, the external controller may produce one nonauthoritative candidate binding:

- authorization, qualification, request, input, and nonce;
- actual container, launch, environment, and mount identities;
- start/stop/exit observations;
- external network `0B/0B` evidence;
- PID1, `pids.max=1`, and child-denial evidence;
- resource and timeout evidence;
- output identity, complete attachment history, initial root, and final Merkle root; and
- runner evidence and controller evidence roots.

The candidate is never named G7 PASS, never consumed directly, and never mapped to legacy G7.

### 4.6 `G9_N1_FINALIZER`

The prebound external finalizer is the only terminal issuer. It atomically compares and sets the
local ledger head after verifying:

- nonce single use, authorization validity, and exact predecessor;
- current qualification, issuer policy, validity, and revocation state;
- candidate uniqueness, freshness, exact run binding, and closed-container identity;
- exact output identity, exclusive attachment history, and final inventory root;
- controller, finalizer, platform, and all external envelope evidence; and
- absence of contradictory, missing, or guest-authoritative claims.

Retry requires a new nonce, reservation, container, authorization, sequence, and predecessor. A run
is never silently resumed or reused.

## 5. Dual closure claim

Both predicates are mandatory and independently evidenced.

### 5.1 `EXECUTABLE_STORE_CLOSURE`

Every code-bearing object in the final mounted view is exactly present in the normative manifest
and classified as approved TCB. The claim covers:

- ELF interpreter, dependencies, RPATH/RUNPATH, constructors, and explicit late loading;
- loader environment, cache, configuration, preload, and audit surfaces;
- NSS, gconv, locale, extension modules, and permitted `dlopen` targets;
- scripts, Python source, bytecode, executable archives, tool mounts, and bootstrap helpers; and
- builtin/frozen CPython payload through an interpreter build-inventory root.

N1-v1 normatively excludes unneeded shells, package managers, compilers, `.pyc`, zipimport, eggs,
wheels as executable sources, preload/audit objects, and unrelated application code.

### 5.2 `INPUT_NONINTERPRETATION_CLOSURE`

No A1-derived value may select or construct a callable, code object, import target, deserialization
factory, native path, subprocess, or executable output. Vendor Python is parsed only as AST data and
vendor JavaScript only as text. Parser callbacks are statically named, hash-bound TCB callables.

The exact scanner first verifies sealed A1/archive hashes. Input and output are outside every
execution/search path, and output cannot re-enter execution before PID1 exits. Required evidence
includes alias, reflection, dynamic code, deserializer callback, native-load, subprocess, and
output-reentry negative families.

`semantic_completeness=false` remains a separate blocker. Control closure cannot promote incomplete
vendor semantic attestation.

## 6. Dedicated image and final-view equality

`DEDICATED_MINIMAL_ADMISSION` is mechanically defined as:

```text
canonical_final_mounted_view_manifest == normative_admission_manifest
```

The manifest lists every entry by normalized path, kind, code/data/config class, mode, owner, size,
and content hash. There may be no extra, missing, unclassified, shadowed, or substituted entry.

A frozen verifier outside the candidate image reconstructs OCI descriptor, manifest, config,
layers, ordering, whiteouts, opaque directories, replacements, symlinks/hardlinks, ownership,
modes, and merged-rootfs identity. It rejects traversal, duplicate ambiguity, invalid whiteouts,
link escape, special files, case/canonicalization collisions, and mount shadowing.

Acceptance applies after exact input/output/tool mounts. All code-bearing tool mounts are
content-addressed. Input and output mounts are absent from interpreter, loader, import, and native
search paths.

The exact TCB tuple includes host OS build, virtualization backend, Docker Desktop, engine,
containerd, runc, Linux kernel, architecture, cgroup mode, security options, seccomp policy,
OCI verifier, controller, ledger, authorization verifier, and finalizer. Tuple drift invalidates
qualification.

## 7. Local ledger and output ownership

A local single-writer compare-and-set ledger is sufficient. No distributed registry, lease service,
or control plane is introduced. The ledger is TCB and qualification binds:

- implementation and schema roots;
- storage identity and access authority;
- consistency, durability, and recovery semantics;
- append/CAS and predecessor rules; and
- replay, fork, crash, truncation, stale-head, and recovery fault-test roots.

The output object has exactly one qualified controller attachment during the run. The finalizer must
verify creation, lease, every attachment, immutable object identity, empty initial root, and final
inventory root. Any unexplained attachment or namespace substitution blocks.

## 8. Outcome algebra

| Outcome | Required meaning |
|---|---|
| `N1_FINAL_PASS` | Complete valid evidence and accepted frozen-scanner result |
| `N1_FINAL_DENY` | Complete valid evidence proving a determinate frozen-scanner policy rejection |
| `N1_INDETERMINATE_BLOCK` | Missing, conflicting, replayed, stale, revoked, timed-out, drifted, infrastructure, or uncertain evidence |
| `N1_UNAVAILABLE` | A required qualification or pre-run platform capability is absent |
| `NO_TERMINAL_STOP` | A prestart authorization/preparation failure; no completion-like artifact is emitted |

Infrastructure uncertainty never becomes determinate DENY. Before blocker-consumer conformance,
blocked conditions produce an external operational error and no completion-like terminal.

The following are representative typed detail codes:

```text
N1_QUALIFICATION_MISSING
N1_QUALIFICATION_EXPIRED
N1_QUALIFICATION_REVOKED
N1_QUALIFICATION_BINDING_MISMATCH
N1_ROLE_SCOPE_MISMATCH
N1_PREPARATION_EXECUTION_DETECTED
N1_EXCLUSIVE_START_UNPROVEN
N1_AUTH_NONCE_REPLAY
N1_AUTH_EXPIRED
N1_PREDECESSOR_MISMATCH
N1_OUTPUT_RESERVATION_NOT_EXCLUSIVE
N1_OUTPUT_INITIAL_ROOT_NONEMPTY
N1_OUTPUT_IDENTITY_CHANGED
N1_OUTPUT_CONCURRENT_ATTACHMENT
N1_CONTAINER_ID_MISMATCH
N1_CANDIDATE_MISSING
N1_CANDIDATE_REPLAY
N1_CANDIDATE_CONFLICT
N1_EVIDENCE_TIMEOUT
N1_FINAL_STATE_CAS_FAILED
N1_FINALIZER_IDENTITY_MISMATCH
N1_REVOCATION_CHECK_UNAVAILABLE
N1_PROFILE_KIND_MISMATCH
N1_LEGACY_MAPPING_FORBIDDEN
N1_GUEST_AUTHORITY_CLAIM
N1_FALLBACK_FORBIDDEN
```

## 9. Consumer routing and rollback

Consumers first match an exact `(profile_kind, schema, artifact_kind)` allowlist. Legacy consumers
reject every N1 artifact. N1 consumers reject legacy/missing-kind artifacts, candidates, unknown
schemas, and ambiguous blockers. No candidate is an admission terminal.

Rollback disables the N1 selector or revokes its qualification. New runs cannot authorize;
in-flight runs block at finalization. Existing artifacts remain immutable and never become
legacy-valid. Roll-forward requires a new qualification version and wholly new run identities.

## 10. Static fixture contract

`fixtures/e14_n1_static_cases_v1.json` is a nonauthoritative scenario corpus. Its identifiers are
placeholders, it contains no content roots, keys, signatures, credentials, filesystem targets, or
live authorization. Cases cover:

- strict/N1 routing and mutual rejection;
- issuer-role separation;
- qualification and exact-manifest failures;
- unsafe preparation and nonexclusive start;
- nonce replay, predecessor mismatch, and CAS failure;
- output swap, concurrent attachment, and stale candidate replay;
- finalizer drift, revocation, guest authority, and unknown schema;
- PASS/DENY/BLOCK separation; and
- rollback with no fallback.

`tests/test_e14_n1_static_fixtures.py` is a test-only read-only conformance oracle. It is not an N1
controller, ledger, authorizer, finalizer, or production implementation.

## 11. Evidence gates before implementation or operation

1. Formal issuer policy, canonical schemas, role/key separation, validity, revocation, and routing.
2. Dedicated image and exact final-view equality.
3. OCI/whiteout/mount, loader/bootstrap/late-load, bytecode/archive, and platform adversarial suites.
4. Scanner dataflow review, callback manifest, and negative-test roots.
5. Safe stopped-container preparation and exclusive-start proof.
6. Atomic output identity, lease, attachment, swap, concurrency, and recovery tests.
7. G8 nonce, expiry, predecessor, prepared-container, and single-use tests.
8. Local CAS-ledger consistency, recovery, authority, and fault tests.
9. Candidate omission, rebinding, replay, conflict, timeout, and guest-authority tests.
10. G9 outcome, revocation, exactly-one-final, consumer-routing, and rollback conformance.

Any absent or contradictory gate keeps N1 unavailable or blocked. None can be satisfied by this
document or the static fixture corpus alone.

## 12. Observability and retained risks

Future evidence must immutably record lifecycle transition, typed roots, role identities, nonce,
qualification, predecessor/CAS state, container and output identities, attachment history,
revocation state, evidence completeness, and terminal reason. Guest traces stay diagnostic.

Residual risks are malicious accepted TCB, incomplete executable inventory, scanner data-to-control
edges, pre-CPython execution, late native loading, output rebinding, stale authorization, ledger
fork/corruption, finalizer drift, platform drift, and semantic-scope confusion. Every uncertainty
fails closed.

## 13. Current authority boundary

This specification and its static fixtures authorize no policy publication, key or role creation,
image build/pull, container preparation/start, scanner run, output reservation, ledger mutation,
qualification issuance, G8 authorization, A2 execution, candidate creation, G9 finalization,
admission root, terminal, deployment, or rollout.
