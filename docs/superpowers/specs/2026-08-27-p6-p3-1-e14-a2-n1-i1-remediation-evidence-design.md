# E14 P3-N1 I1 remediation evidence design

Date: 2026-08-27

Status: approved for evidence construction; production remediation, G1 issuance, activation, and I2 remain unauthorized.

Decision source: three-round `sana-debation` review with Proposing TL, Peer TL, and Chief Architect.
Chief disposition: `defer pending named evidence`.

## 1. Purpose and authorization boundary

I1 stopped because the frozen source analyzers rejected only 5 of 14 required alias, reflection,
dynamic-code, callback, native-load, subprocess, and output-reentry cases. The production scanner
itself remained read-only and did not execute the fixture bytes. The failed scanner, schema, G1
freeze, and I1 evidence remain immutable.

This phase may add only specifications, non-production evidence tooling, synthetic fixtures, tests,
and `authority_effect=NONE` evidence records needed to answer the Chief's nine named evidence
requests. It must not:

- modify `src/e14_admission.py` or its existing schema;
- acquire or install Node, Acorn, another parser, or a native dependency;
- issue `G1FreezeV2`, a lifecycle event, or an I2 authorization;
- register a production consumer or change routing;
- build or pull an image, execute vendor source, or begin I2; or
- rewrite any v1 evidence or repair a failed evidence identity in place.

Producing a conforming evidence bundle proves only the proposition named by that bundle. No bundle,
test PASS, report PASS, hash, review signature, or future G1 candidate grants operational authority.

## 2. Binding architectural decision

The selected architecture is hybrid and exact-scope:

1. Exact archive identity is the only package acceptance mechanism. It proves that the role-bound
   npm and wheel bytes equal the frozen A2 pair; it does not prove vendor-language safety.
2. The production prescan remains standard-library-only, read-only, and unable to launch diagnostic
   tooling. A future version may verify a frozen diagnostic envelope but may not create one.
3. Python AST and a pinned Node/Acorn toolchain are offline diagnostic evidence builders. Their
   findings can veto a future freeze, but success cannot authorize or establish semantic
   completeness.
4. Scanner noninterpretation is a separate, exact-hash property defined by a closed obligation
   matrix rather than by a generalized source-language absence claim.
5. v1 is immutable `HISTORICAL_ONLY` and nonroutable for the successor qualification path. A future
   v2 family must use new domains, schemas, hashes, candidate identities, and a new G1 freeze.
6. Every prescan claim maps only to `RECORD_EVIDENCE`. I2 requires a separate, current, revocable,
   single-use authorization after every preactivation gate passes.

General JavaScript or Python safety analysis is explicitly out of scope. Scope expansion requires a
new architecture decision and a new freeze domain.

## 3. Claims and prohibited interpretations

The evidence design recognizes only these future claim meanings:

| Claim | Exact meaning |
|---|---|
| `EXACT_A2_IDENTITY_MATCH_V2` | Exact role-bound raw archives, physical structures, inventories, metadata, and source roots equal the frozen A2 pair. |
| `DIAGNOSTIC_TOOL_COMPLETED_V1` | The bound offline tool completed under the recorded policy and emitted the recorded findings. Completeness is not asserted. |
| `I1_SCANNER_NONINTERPRETATION_REVIEWED_V2` | For one exact scanner hash and entry model, the reviewed obligation set found no path by which A1/vendor-derived data selects or becomes a denied effect before return. |
| `A2_PRESCAN_PASS_V2` | Exact identity and exact-scanner noninterpretation evidence both passed. This is evidence eligibility only. |

The following claims and equivalents are forbidden:

```text
ABSENT_BY_CONSERVATIVE_SCAN
ABSENT_BY_AST_SCAN
GENERAL_JS_SAFE
GENERAL_PYTHON_SAFE
NO_RUNTIME_CALLBACKS
VENDOR_RUNTIME_SAFE
OPERATION_AUTHORIZED
```

The frozen Node `object.toJSON()` site is recorded as
`VENDOR_RUNTIME_CALLBACK/PRESENT_RUNTIME_DISPATCH`. It is neither invoked by this phase nor
classified as absent or safe. Any later runtime-input or reachability decision is a separate gate.

## 4. Nine evidence bundles

Every bundle is strict UTF-8 JSON with a closed schema, duplicate-key rejection, a versioned domain,
stable file hashes, explicit limitations, and `authority_effect=NONE`. A bundle may reference only
immutable roots, never a mutable path such as `latest`.

### 4.1 `ObligationCoverageBundleV1`

Purpose: establish the exact scanner-noninterpretation obligation universe without treating the
diagnostic generator's own output as complete by definition.

It binds:

- exact scanner hash and supported entry points;
- mechanically enumerated reachable scanner functions and callsites;
- every A1/vendor-derived ingress;
- parser callback, callable-valued expression, import, native-load, subprocess, deserializer,
  write-target, and output-consumption edges;
- a separately implemented conservative detector inventory;
- reviewer-curated source spans and exact set comparisons;
- one matrix row for every obligation;
- direct results for all unchanged 14 negative fixtures;
- exact-source reachability notes, including `toJSON()`; and
- custody and consumer-evidence roots.

Each matrix row contains:

```text
scanner_hash, entry_point, reachable_function, ingress_id,
edge_id, denied_effect, disposition, evidence_location, reviewer
```

Allowed dispositions are `PASS`, `FAIL`, and `INCONCLUSIVE`. Missing, extra, duplicate, unresolved,
unsupported, or dynamically selected rows block. The fixed denied effects are:

```text
VENDOR_BYTES_EXECUTED
NETWORK_EFFECT
PROCESS_LAUNCH
FILESYSTEM_WRITE
RUNTIME_SELECTED_CALLBACK
DYNAMIC_IMPORT_OR_CODE
DESERIALIZER_FACTORY_SELECTION
NATIVE_LOAD_TARGET_SELECTION
OUTPUT_REENTRY_BEFORE_RETURN
```

The 14-case test route invokes the diagnostic rules directly and performs no archive-identity check.
All 14 must produce their exact blocking family. This proves regression coverage for those cases
only.

### 4.2 `HermeticDiagnosticBundleV1`

Purpose: demonstrate that an offline diagnostic success is produced by the exact declared
toolchain, under bounded failure semantics, rather than by an unmanifested runtime or partial output.

Its future `DiagnosticBuildEnvelopeV1` binds:

```text
schema, session_id, source_roots,
toolchain_closure_root, startup_policy_root, parser_options_root,
callback_policy_root, generator_root, independent_detector_root,
logical_caps, observed_usage, loaded_object_root,
finding_root, obligation_universe_root,
child_result, supervisor_result, fault_policy_root, result_root
```

The closure includes exact CPython and Node executables, standard-library and Acorn/analyzer bytes,
loader/native dependencies, absolute module paths, startup flags, environment allowlist, filesystem
read allowlist, and observed loaded objects. `NODE_OPTIONS`, preloads, custom loaders, mutable module
search, network, subprocesses, writes, parser plugins, and unmanifested modules are forbidden.

Source byte and line limits apply before child start. Token, AST node/depth, edge, worklist,
callback-invocation, finding, and output limits apply during processing. CPU, memory, descriptor,
filesystem, and wall limits are supervisor backstops and never substitute for deterministic logical
limits.

Only the supervisor may emit a success envelope after clean child exit, complete output validation,
closure verification, cap checks, source/result-root recomputation, and session binding:

```text
INIT
 -> CLOSURE_VERIFIED
 -> CHILD_STARTED_UNDER_LIMITS
 -> CHILD_COMPLETE
 -> OUTPUT_VALIDATED
 -> ROOTS_RECOMPUTED
 -> SUCCESS_ENVELOPE_EMITTED
```

Every exception, signal, nonzero exit, timeout, OOM, quota event, malformed or partial output,
closure drift, stale session, preload, resolution mismatch, or validator disagreement ends in
`ABORTED_NO_ENVELOPE`. There is no recovery, reuse, retry, or fallback under the same session.

This evidence phase may specify and test a dependency-free supervisor model and synthetic fault
protocol. It may not acquire Node/Acorn. Real toolchain-closure evidence remains `NOT_RUN` until a
separate dependency-acquisition authorization exists.

### 4.3 `FreezeReproductionBundleV1`

Purpose: prove that two independent implementations derive the same future G1 candidate root from
the same sealed inputs.

This phase defines the canonical `G1FreezeV2` commitment model, domain separation, role ordering,
and independent test oracle. It uses synthetic roots only. The model commits directly to:

- candidate and exact A2 scope;
- npm-role and wheel-role archive/member/source roots;
- scanner, schema, and policy roots;
- diagnostic envelope;
- I1 obligation, diagnostic, and fault-evidence roots;
- dependency budget;
- consumer policy and conformance;
- lifecycle policy; and
- issuer role/identity and predecessor.

No real G1 root is issued by this bundle. A later candidate is eligible only if production and
independent oracles reproduce identical canonical bytes and roots.

### 4.4 `LifecycleAuthorityBundleV1`

Purpose: specify and test monotonic candidate state without confusing an internally consistent
history with a fresh view of current authority.

The synthetic lifecycle is:

```text
CANDIDATE -> ACTIVE -> DISABLED
                  \-> REVOKED
CANDIDATE -> REJECTED
v1         -> HISTORICAL_ONLY
```

Every event binds candidate root, prior event root, monotonic epoch, transition, reason, issuer
role, and revocation snapshot. `REVOKED`, `REJECTED`, and `HISTORICAL_ONLY` are terminal. `DISABLED`
can resume only through a new candidate and G1.

Tests must include stale active-event replay after revocation, forked histories, skipped epochs,
wrong predecessor, unauthorized role, missing current-state evidence, and stale revocation snapshot.
The bundle may prove state-machine behavior with synthetic role IDs, but it must report real issuer,
activator, disabler, revoker, storage, durability, and current-view ownership as `UNRESOLVED` until
separately evidenced.

### 4.5 `RoutingCompatibilityBundleV1`

Purpose: prove atomic selection and mutual rejection across version and freeze families.

`RouteKeyV2` is the indivisible tuple:

```text
selector, media_type, profile_kind, request_schema,
scanner_hash, scanner_policy_root,
npm_archive_hash, wheel_archive_hash,
diagnostic_envelope_root, g1_root,
activation_event_root, activation_epoch
```

The corpus covers missing and unknown selectors, v1/v2 cross-version inputs, stale scanners and
policies, mixed freeze components, npm/wheel role swaps, incomplete tuples, disabled/revoked events,
unknown claims, and attempted downward negotiation. Every case must fail closed; v1 is never invoked.

### 4.6 `ConsumerConformanceBundleV1`

Purpose: prevent a syntactically valid evidence report from becoming operational authority through a
legacy adapter or incomplete consumer inventory.

`ConsumerPolicyV1` contains a closed inventory of routers, report readers, automations, and other
consumers plus an exact claim-to-action allowlist. Identity, diagnostic completion, review, test
PASS, and prescan PASS map only to `RECORD_EVIDENCE`. Unknown consumer, claim, version, or action
blocks. Tests must prove there is no path from any evidence claim to qualification, admission,
execution, I2 issuance, build, pull, or vendor execution.

This bundle records repository consumers discovered by `rg`-based inventory. Absence outside the
repository remains an explicit limitation rather than a universal consumer claim.

### 4.7 `I2AuthorizationControlBundleV1`

Purpose: demonstrate that I2 cannot be inferred from I1 success and that its authorization is exact,
single-use, current, and revocable.

The test-only `I2SourceOnlyAuthorizationV1` binds active G1 root, activation event and epoch, exact
package roles, exact source-only operation and request, subject, issuer role, validity, nonce, and
revocation epoch. Tests cover missing authorization, wrong binding, expiry, revocation, nonce replay,
cache reuse, queued work, and in-flight safe-stop behavior. The fixtures contain no live identity,
root, credential, or permission and cannot authorize I2.

### 4.8 `RollbackBundleV1`

Purpose: prove that disable or revoke makes v2 unusable while preserving evidence and never
reactivating v1.

Tests cover route-cache invalidation, queued and unstarted authorization invalidation, in-flight
prescan result discard, I2 safe-stop, nonauthoritative in-flight output, inability-to-prove-stop,
repeated disable/revoke, stale event replay, and v1 fallback attempts. Roll forward always requires a
new candidate, session, roots, run ID, and fresh I1 result.

### 4.9 `DependencyApprovalBundleV1`

Purpose: record the exact-scope dependency and TCB decision without acquiring the dependency.

`ExactScopeDependencyBudgetV1` records A2-only scope, proposed CPython/Node/Acorn closure, acquisition
requirements, parser options/callback surface, TCB justification, logical and OS caps, approved and
prohibited dependency classes, and the ban on general-language claims. During this evidence-only
phase its approval status is `PENDING_SEPARATE_ACQUISITION_AUTHORIZATION`; it cannot be represented
as approved.

## 5. Failure namespaces and precedence

Offline builder failures produce no freeze-eligible artifact and use `DB_*` codes:

```text
DB_TOOLCHAIN_CLOSURE_MISMATCH
DB_STARTUP_POLICY_VIOLATION
DB_PRELOAD_OR_RESOLUTION_DRIFT
DB_SOURCE_CAP
DB_PARSE_FAILED
DB_UNKNOWN_SYNTAX_OR_NODE
DB_UNRESOLVED_EDGE
DB_CALLBACK_POLICY_VIOLATION
DB_LOGICAL_CAP
DB_CHILD_CRASH
DB_TIMEOUT
DB_OOM_OR_OS_KILL
DB_OUTPUT_PARTIAL
DB_OUTPUT_MALFORMED
DB_SESSION_STALE
DB_SUPERVISOR_ABORTED
DB_GENERATOR_DETECTOR_MISMATCH
```

Future production envelope verification uses a separate namespace:

```text
N1_DIAGNOSTIC_ENVELOPE_HASH_MISMATCH
N1_DIAGNOSTIC_ENVELOPE_SCHEMA
N1_DIAGNOSTIC_ENVELOPE_SOURCE_BINDING
N1_DIAGNOSTIC_ENVELOPE_POLICY_BINDING
N1_DIAGNOSTIC_ENVELOPE_NOT_SUCCESS
N1_DIAGNOSTIC_ENVELOPE_ROOT_MISMATCH
```

Routing, governance, and I2 controls require stable distinct wire failures for historical-only,
disabled, revoked, incomplete route, route mismatch, cross-version, package-role mismatch,
component-set mismatch, G1 binding/state, unlisted consumer, forbidden claim/action, and I2
missing/binding/expired/revoked/replay. Exact spellings are frozen by their evidence schemas before a
future G1 candidate; no generic alias or fallback is permitted.

Precedence is route/schema, exact component set, lifecycle freshness, consumer/action policy, then
the separate I2 authorization. Offline diagnostic failures never appear as if production performed
parsing; production reports only envelope-binding failures.

## 6. Planned repository layout

Evidence implementation after this design is reviewed is limited to:

```text
schemas/e14-n1-i1-remediation-evidence-v1.schema.json
fixtures/e14_n1_i1_remediation_cases_v1.json
tools/e14_n1_i1_evidence.py
tests/test_e14_n1_i1_evidence.py
evidence/n1/remediation/obligation-coverage-v1.json
evidence/n1/remediation/hermetic-diagnostic-v1.json
evidence/n1/remediation/freeze-reproduction-v1.json
evidence/n1/remediation/lifecycle-authority-v1.json
evidence/n1/remediation/routing-compatibility-v1.json
evidence/n1/remediation/consumer-conformance-v1.json
evidence/n1/remediation/i2-authorization-control-v1.json
evidence/n1/remediation/rollback-v1.json
evidence/n1/remediation/dependency-approval-v1.json
docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-n1-i1-remediation-evidence-report.md
```

The implementation uses only the Python standard library and synthetic inputs. It reads production
files to inventory and hash them but never writes them. It does not add a v2 production scanner,
production report schema, lifecycle service, authorization issuer, or parser dependency.

## 7. Implementation sequence and fail-stop checkpoints

1. Freeze the closed evidence schema, canonical hashing rules, synthetic case corpus, and typed
   failure taxonomy.
2. Implement pure data models and independent canonical-root oracle for synthetic G1 and lifecycle
   records.
3. Implement read-only repository inventory, scanner AST/callsite inventory, consumer inventory,
   obligation matrix comparison, and direct 14-case diagnostic contract checks.
4. Implement the dependency-free supervisor state model and complete abnormal-termination fault
   corpus. Real Node/Acorn execution remains `NOT_RUN`.
5. Implement route, lifecycle, consumer, I2 authorization, revocation, cache, queue, and rollback
   models over synthetic roots.
6. Generate all nine evidence records deterministically and validate them against the closed schema.
7. Run focused tests, the complete repository suite, deterministic regeneration, immutable-v1 hash
   checks, and production-source diff checks.
8. Publish one evidence report that states each bundle as `PASS`, `FAIL`, `INCONCLUSIVE`, or
   `NOT_RUN`; any non-PASS required gate keeps the Chief disposition deferred and I2 blocked.

An unexpected accepted negative case, changed v1 hash, production source change, schema validation
failure, nondeterministic regeneration, missing consumer, unresolved obligation, or fault path that
leaves a valid envelope immediately stops the stage. Repair requires a new evidence-run identity;
the failed record remains immutable.

## 8. Verification and exit criteria

The evidence construction phase exits only when:

- every planned evidence file is schema-valid and deterministically reproducible;
- all 14 unchanged negative cases are evaluated directly and produce exact blocking outcomes;
- production scanner and original G1 hashes remain exactly unchanged;
- the scanner audit finds no production execution, process, network, write, native/deserializer, or
  vendor-selected callback sink;
- all synthetic abnormal supervisor paths yield no success envelope;
- all cross-version, mixed-root, downgrade, stale-event, consumer-overreach, replay, cache, queue,
  in-flight, and rollback cases fail closed;
- independent canonicalization reproduces the same synthetic G1 roots;
- the complete repository test suite passes; and
- the final report accurately preserves every unresolved or not-run external dependency and
  governance item.

The expected result of this authorized phase is not necessarily nine PASS records. Because real
Node/Acorn acquisition and lifecycle authority ownership are outside the current authorization,
their bundles may validly remain `NOT_RUN` or `INCONCLUSIVE`. Such a result is useful evidence but
does not lift the Chief's deferral.

## 9. Rollback and observability

Before merge, rollback removes only the new evidence schema, fixtures, tool, tests, generated
records, and report. It never changes v1 artifacts. After merge, correction is additive: a failed or
superseded evidence run remains and a new version/run is created.

Every generated record includes schema, run ID, created date, input and tool hashes, deterministic
root, status, authority effect, limitations, typed failure where applicable, and `next_stage_authorized=false`.
The report records bundle roots, tests, production immutability checks, unresolved evidence, and the
exact resubmission boundary.

## 10. Resubmission boundary

After evidence generation, the unchanged P3 architecture and all generated bundle roots return to a
fresh Chief adjudication. Only `approve` or `approve with required changes` may permit a later,
separately approved production-scanner version and G1-candidate phase. Evidence generation itself
does not authorize that transition.
