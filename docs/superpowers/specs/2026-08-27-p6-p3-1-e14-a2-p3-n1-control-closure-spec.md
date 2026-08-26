# P3-N1 G7 control-closure specification

Date: 2026-08-27

Status: design approved; document and static-fixture phase only.

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

## 2. Canonical envelope and hash domain

Every future N1 artifact uses strict UTF-8 JSON, no BOM, no duplicate keys, no comments, and no
trailing data. The payload is canonicalized with RFC 8785 JCS.

```text
payload_bytes = RFC8785-JCS(payload)
digest        = SHA-256(
                  UTF8("sana.e14.n1.lifecycle-artifact.v1\n")
                  || UTF8(artifact_kind)
                  || 0x00
                  || payload_bytes
                )
content_root  = "sha256-jcs-e14-n1-v1:" || lowercase_hex(digest)
```

The root is outside the payload. The payload cannot contain its own root or a later artifact root.
Every reference is an exact typed root, never a path, filename, logical ID, summary, or reconstructed
equivalent. The candidate schema is
`schemas/e14-a2-n1-lifecycle-v1.schema.json`.

Static artifact examples may use `fixture_only=true` only for nonauthorizing kinds. The schema
rejects fixture-only G8 or terminal authority. The behavioral corpus is a separate scenario format,
not a lifecycle artifact. Operational consumers must reject every `fixture_only=true` object.

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
