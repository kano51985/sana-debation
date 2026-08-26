# P3-N1 implementation and evidence plan

Date: 2026-08-27

Status: plan only. No implementation or operational step is authorized by this file.

## Objective

Implement the approved `P3_N1_CONTROL_CLOSURE_V1` as tool-owned, testable components while keeping
`sana-debation` limited to architecture-decision orchestration. Legacy strict G7/G8/G9 must remain
byte- and behavior-compatible.

## Stage D0 — document and static fixtures

Deliverables in the current authorized phase:

- control-closure debate record;
- normative specification and hash domain;
- unified lifecycle JSON Schema;
- nonauthoritative static scenario corpus;
- test-only read-only fixture oracle; and
- repository status/index updates.

Exit conditions:

- schema passes Draft 2020-12 self-validation;
- every lifecycle artifact kind has a schema-valid test example;
- fixture scenarios cover routing, roles, closure, preparation, replay, predecessor, output identity,
  candidate authority, finalizer, outcomes, revocation, and rollback;
- all repository tests pass; and
- no `src/` N1 implementation, image, container, ledger, live root, signature, or terminal exists.

Completion of D0 authorizes no later stage.

The original unissued lifecycle draft was corrected before I0 because its root did not bind the
schema, profile, or top-level fixture classification. Lifecycle-v2 removes the ambiguous wrapper
fields, binds all four semantic commitment members, and retires v1 without migration. The
correction debate, cap report, and retirement manifest are mandatory I0 pre-code evidence.

## Stage I0 — pure artifact and routing library

Status: source-only I0 implementation complete. Pre-code gates and local verification pass. No live
artifact, root, authority, persistence, network, process, or operational route is authorized.

Proposed files:

```text
src/e14_n1_artifacts.py
tests/test_e14_n1_artifacts.py
```

Implement a single-pass bounded raw-byte parser, duplicate-key rejection, the restricted
RFC-8785-equivalent `N1-V2-CANON` encoder, typed-root verification, nominal artifact-kind dispatch,
exact route/media checks, and explicit-time/revocation use evaluation. The library must be pure and
side-effect free: no Docker, filesystem reads or mutation, network, environment, clock, keys,
ledger, cache, registry, or process launch.

Required tests include independently computed canonical byte/root vectors, Unicode and escape
equivalence, unknown fields, wrong schema/profile/kind/media, duplicate keys, invalid UTF-8,
surrogates, forbidden number forms and arrays, every cap boundary, deterministic failures, removed
fixture fields, mutual v1 rejection, validity/revocation inputs, purity traps, and no fallback.

## Future stage I1 — scanner dataflow qualification

Proposed evidence artifacts:

```text
evidence/n1/scanner-data-nonexecution-policy-v1.json
evidence/n1/scanner-dataflow-review-v1.json
evidence/n1/trusted-callback-manifest-v1.json
fixtures/e14_n1_scanner_dataflow_cases_v1.json
```

Review the exact production scanner hash. Enumerate every parser callback and every path by which
A1 bytes can affect control flow. Add alias/reflection, dynamic code, deserializer callback,
native-load, subprocess, and output-reentry negative fixtures. Vendor code remains AST/text data.

This stage must stop if a dynamic input-to-execution path exists; it may not repair the scanner
silently inside an evidence run.

## Future stage I2 — dedicated image and OCI closure tooling

Proposed files:

```text
container/e14-n1/Dockerfile
container/e14-n1/normative-final-view-manifest.json
tools/e14_n1_oci_verify.py
fixtures/e14_n1_oci_cases_v1.json
tests/test_e14_n1_oci_verify.py
```

The first separately authorized action is source-only construction of a deterministic image recipe
and normative manifest. Building or pulling the image is a later authorization.

The OCI verifier must run outside the candidate image and reconstruct descriptors, layers,
whiteouts, links, modes, ownership, and the merged root. It must validate the final mounted view,
loader/bootstrap configuration, constructors, NSS/gconv/locale, explicit late loads, embedded
interpreter inventory, prohibited bytecode/archive sources, and exact platform tuple.

Negative fixtures cover invalid whiteouts, opaque replacement, link escape, mount shadow, preload,
audit, loader cache/config, environment injection, late load, `.pyc`, zipimport, frozen-inventory
drift, tool substitution, and platform drift.

## Future stage I3 — local ledger and output reservation

Proposed files:

```text
src/e14_n1_ledger.py
src/e14_n1_output_reservation.py
tests/test_e14_n1_ledger.py
tests/test_e14_n1_output_reservation.py
```

Use a local single-writer ledger with atomic compare-and-set and create-new output objects. Do not
introduce a distributed database, registry, lease service, or network coordinator.

Qualification evidence must bind implementation, schema, storage identity, access rules,
consistency, durability, and recovery. Fault tests cover replay, competing writers, stale head,
fork, truncation, crash before/after append, recovery, lease replay, pathname swap, concurrent
attachment, and immutable-object mismatch.

## Future stage I4 — controller and safe preparation

Proposed files:

```text
tools/e14_n1_controller.py
tests/test_e14_n1_controller.py
```

The controller may reserve output and prepare one stopped container. Before G8 it must not start
PID1, execute guest code, or invoke an unqualified OCI hook/plugin/helper. The immutable prepared
configuration and container identity are inputs to G8. Only the qualified controller retains start
capability.

Authorization failure destroys the stopped container, invalidates the lease, and creates no
terminal. If Docker Desktop cannot evidence no-execution preparation and exclusive start, N1 is
unavailable rather than weakened.

## Future stage I5 — G8 verifier and one-run authorization

Proposed files:

```text
src/e14_n1_authorization.py
tests/test_e14_n1_authorization.py
```

Implement exact issuer-policy/qualification binding, role scope, validity, revocation, fresh nonce,
request and input roots, prepared container, launch/mount/environment, output lease, controller,
finalizer, platform, sequence, predecessor, and single-use checks. The artifact must not bind a
future candidate.

Tests cover role confusion, expiry, nonce replay, predecessor mismatch, revoked qualification,
wrong prepared container, output reservation substitution, and concurrent authorization.

## Future stage I6 — candidate assembly and G9 finalizer

Proposed files:

```text
tools/e14_n1_finalizer.py
tests/test_e14_n1_finalizer.py
```

The external controller assembles one nonauthoritative candidate after the container closes. The
prebound external finalizer verifies all actual identities and evidence, rechecks revocation, then
CAS-updates exactly one terminal.

Tests cover missing/replayed/conflicting/stale candidate, guest PASS, output rebinding, attachment
drift, finalizer drift, evidence timeout, scanner PASS, determinate scanner DENY, infrastructure
BLOCK, CAS crash/recovery, and exactly-one-final under concurrency.

## Future stage I7 — end-to-end qualification packet

Assemble immutable roots for:

- issuer policy and role scopes;
- dedicated image/final-view equality;
- scanner dual closure;
- OCI/loader/platform negative suites;
- safe preparation and exclusive start;
- output reservation and local ledger;
- G8 replay/single-use behavior;
- candidate and G9 finalization behavior; and
- consumer, revocation, and rollback conformance.

The packet remains evidence only. A fresh architecture/owner review must decide whether evidence is
sufficient to issue a real qualification. It cannot create that qualification itself.

## Future stage O0 — separately authorized operation

Operational work is intentionally outside this plan's authority. It would require exact approval
of image, tools, policies, role identities, platform tuple, caps, A1/vendor roots, output object,
nonce, G8 artifact, and finalizer. No earlier implementation or test result implies O0.

## Verification commands for D0

```powershell
python -m unittest tests.test_e14_n1_static_fixtures -v
python -m unittest discover -s tests -v
```

The skill package should also continue to pass the installed skill validator, but D0 intentionally
does not modify `SKILL.md` or the installed skill.

## Rollback

D0 rollback is removal of only the new document/schema/fixture/test files and index entries before
merge. Later N1 rollback is selector disablement or qualification revocation; it never modifies
legacy behavior or reclassifies existing artifacts.
