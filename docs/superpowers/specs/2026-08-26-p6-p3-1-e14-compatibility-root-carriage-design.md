# P6 P3.1 E14 compatibility and root-carriage design

Date: 2026-08-26

Status: approved design transcription only. This document specifies a future static conformance corpus
and result contract. It does not create fixture bytes, an executable schema, a validator, an
authorization object, an approval receipt, a root, a cap, or an operational action.

## Authority boundary

The current authorization covers only:

- this E14 design;
- a read-only fixture construction plan;
- document self-review and hashes.

It does not cover:

- creating the planned fixture files;
- compiling or running a canonicalizer, graph verifier, or compatibility runner;
- producing or accepting an executable P3.1 schema or object;
- locating or emulating the E13 authority channel;
- native exact-root approval;
- EA0, L0, EA1-CONSTRUCT, EA1-EXECUTE, E10, E11, L2, or production work;
- network, model, plugin, MCP, configuration, service, credential, or signing mutation.

Every future corpus artifact and tool requires a new exact authorization boundary.

## Controlling local sources

| Artifact | SHA-256 |
|---|---|
| P3.1 authorization-DAG design | B6DBE2702C6CBB0CA69E3BAF2F595DB8E4D57ADA8BC23B810DFF109955EC6E20 |
| P3.1 acquisition amendment | C3ECEB8CB3E47EADA03A85F3479EA7EED9D668C507F53231225349BB1933D5DA |
| P3.1 document conformance record | 3CAE47A62B2B5DD4A3BED7108CB61E827F511439D1643E813311CBA6544F48FA |

The predecessor P3 and P3.1 documents remain immutable.

## External normative references

- RFC 8785, JSON Canonicalization Scheme:
  https://www.rfc-editor.org/rfc/rfc8785.html
- RFC 7493, The I-JSON Message Format:
  https://www.rfc-editor.org/rfc/rfc7493.html
- Verified RFC 8785 errata:
  https://www.rfc-editor.org/errata/rfc8785

E14 treats the RFC text and verified errata as primary canonicalization evidence. Local prose may
narrow the application schema, but it cannot contradict those sources.

Relevant design consequences include:

- JCS uses I-JSON input constraints;
- duplicate member names are invalid;
- strings must remain unchanged and are not Unicode-normalized;
- lone surrogates and other invalid Unicode terminate canonicalization;
- object properties sort recursively by raw property-name UTF-16 code units;
- array element order remains unchanged while objects inside arrays are recursively sorted;
- canonical output contains no inter-token whitespace;
- number serialization follows the JCS/ECMAScript profile;
- the verified negative-zero erratum is represented by a rejection test.

## Decision

Use a matrix-first static golden corpus.

The corpus is organized by normative clause and causal mutation rather than statistical sampling. Its
baseline contains exactly 48 case contracts. The number 48 is a bounded coverage size, not a
generalization claim, confidence interval, or sample-size argument.

Every case is synthetic, inert, and non-authorizing. E14 never includes a positive native activation
case while E13 is absent.

## Alternatives considered

### Full golden authorization bundles first

Rejected as the primary approach. Full bundles are easy to execute later but can be mistaken for
operational authorization objects before schema, role, root, and approval boundaries are proven.

### Property-generated corpus first

Rejected as the primary oracle. It offers broad mutation coverage, but the generator can silently
become both the rule and the judge. Property generation may supplement the frozen corpus after the
baseline passes; it cannot replace named golden cases.

### Matrix-first static corpus

Selected. It is inspectable, clause-traceable, reproducible, and naturally fail-closed. Each case has
one named causal distinction and one exact expected result.

## E14 objective

E14 answers only:

Can two conforming verification paths consume the same frozen synthetic inputs and agree on strict
parsing, canonical bytes, typed content roots, role and graph semantics, capability handling, root
carriage, and inherited failure tuples?

E14 does not answer:

- whether a native authority channel exists;
- whether an approval is authentic;
- whether root reservation or fencing works under concurrency;
- whether any P3.1 object should activate;
- whether EA0 or an evidence claim should proceed.

Those questions remain gated by E13, E11, or a later Chief and user authorization.

## E14 invariants

- E14-I1 — Inert fixtures: every fixture has authority_effect = NONE.
- E14-I2 — No activation: every final-shaped case ends at FINALIZED_NOT_AUTHORIZED or an earlier
  rejection state.
- E14-I3 — Exact bytes: an input byte artifact is immutable and is never reconstructed from a display
  rendering.
- E14-I4 — Oracle separation: the system under test does not generate its own expected result.
- E14-I5 — One causal mutation: every negative case identifies one primary changed condition.
- E14-I6 — Complete traceability: every case maps to local clause IDs, external standard sections when
  applicable, expected detail, inherited top-level tuple, and affected risk.
- E14-I7 — No aggregate masking: every mandatory case passes individually; averages and majority votes
  are prohibited.
- E14-I8 — No authority synthesis: hashes, test wrappers, mock approval references, and display
  projections never activate a final.
- E14-I9 — Legacy preservation: predecessor bytes and hashes are read-only comparison inputs.
- E14-I10 — Three-valued gate: E14 itself reports PASS, FAIL, or INCONCLUSIVE and never grants the next
  stage.

## Architecture

    immutable local specifications plus RFC references
        -> ClauseCoverageMatrix
        -> E14CaseManifest with 48 named cases
        -> future inert input-byte fixtures
        -> GoldenExpectationManifest
        -> two verification paths
        -> per-case comparison records
        -> immutable E14ResultPacket
        -> document and evidence review

No arrow represents operational authority.

## Components

### ClauseCoverageMatrix

Maps each mandatory behavior to one or more case IDs:

- canonical UTF-8, I-JSON, and JCS;
- envelope and typed-root identity;
- P3.1 role mapping;
- binding-plan and graph closure;
- capability negotiation and no-fallback;
- native approval-root carriage without activation;
- downstream output closure;
- detail-code subordination;
- metamorphic stability and sensitivity.

A clause without a mandatory case blocks E14 sealing.

### E14CaseManifest

Each case contract contains:

- case_id;
- case_family;
- title and one causal distinction;
- controlling local clause IDs;
- external reference and limitation, when applicable;
- input artifact kind and future byte path;
- input provenance class;
- expected strict-parse result;
- expected canonical-byte root or explicit rejection;
- expected artifact role;
- expected graph result and canonical order;
- expected capability result;
- expected activation state;
- expected subordinate detail code;
- expected inherited top-level tuple;
- authority_effect = NONE;
- risk IDs;
- oracle method;
- mandatory or conditional status.

The manifest is descriptive until separately authorized fixture bytes exist.

### InertFixtureEnvelope

A future fixture wrapper is outside the candidate P3.1 payload and contains:

- fixture schema and case ID;
- raw input byte root;
- media type;
- provenance note;
- expected-result manifest root;
- test-only custody fields;
- authority_effect = NONE.

The wrapper is never supplied to an operational executor. It cannot be interpreted as a P3.1
authorization object.

Positive serialization fixtures may contain final-shaped synthetic payloads, but:

- they use synthetic non-filesystem identifiers;
- all resource dimensions are zero or non-operational placeholders defined by the fixture contract;
- they contain no native approval provenance;
- they are never placed in an authorized run root;
- expected activation remains FINALIZED_NOT_AUTHORIZED.

### GoldenExpectationManifest

Contains exact expected:

- parse acceptance or rejection;
- canonical bytes for accepted canonicalization cases;
- sha256-jcs-p31 root;
- role;
- ordered vertex list and closure root where applicable;
- capability status;
- activation state;
- subordinate detail;
- inherited tuple;
- output-closure field set;
- limitations.

Golden expectations are independently reviewed and are not produced solely by the verifier under test.

### DetailCodeRegistry

E14 freezes the minimal successor detail vocabulary. All entries are subordinate to the inherited P3
top-level tuple.

Canonical and root details:

- AUTH_CANONICAL_UTF8_INVALID
- AUTH_CANONICAL_JSON_INVALID
- AUTH_CANONICAL_IJSON_INVALID
- AUTH_CANONICAL_JCS_INVALID
- AUTH_CONTENT_ROOT_MISMATCH
- AUTH_SELF_REFERENCE_FORBIDDEN

Role, binding, and graph details:

- AUTH_ROLE_MISMATCH
- AUTH_INTENT_ATTEMPTED_EXECUTION
- AUTH_CONTRACT_INTENT_MISMATCH
- AUTH_BINDING_SLOT_MISSING
- AUTH_BINDING_SLOT_DUPLICATE
- AUTH_BINDING_SET_MISMATCH
- AUTH_FINAL_BACKREFERENCE_FORBIDDEN
- AUTH_GRAPH_CYCLE
- AUTH_ROOT_COLLISION
- AUTH_DEPENDENCY_TYPE_MISMATCH
- AUTH_GRAPH_NOT_TOPOLOGICAL

Capability and schema details:

- AUTH_CAPABILITY_MISSING
- AUTH_CAPABILITY_UNSUPPORTED
- AUTH_SCHEMA_MIXED
- AUTH_UPCONVERSION_FORBIDDEN
- AUTH_DOWNGRADE_FORBIDDEN
- AUTH_PROFILE_FALLBACK_FORBIDDEN

Approval and closure details:

- AUTH_APPROVAL_ROOT_UNAVAILABLE
- AUTH_APPROVAL_ROOT_MISMATCH
- AUTH_APPROVAL_STAGE_MISMATCH
- AUTH_APPROVAL_SCOPE_MISMATCH
- AUTH_CLOSURE_INCOMPLETE
- AUTH_CLOSURE_ORDER_MISMATCH

Claim and fence schema details, whose behavior remains E11-gated:

- AUTH_EXECUTION_ALREADY_CONSUMED
- AUTH_EXECUTION_COMPETING
- AUTH_CLAIM_ROOT_COLLISION
- AUTH_FENCE_UNSUPPORTED
- AUTH_FENCE_LOST
- AUTH_FENCE_EXPIRED
- AUTH_EFFECT_STATE_UNCERTAIN

E14 checks spelling, field placement, and inherited-tuple mapping. It does not claim to prove
concurrent claim or fence behavior.

### CompatibilityRunnerContract

This is an interface design, not executable code.

A future runner accepts only:

- the sealed E14 case manifest;
- exact input-byte fixtures;
- the exact golden expectation manifest;
- the detail-code registry;
- declared verifier identities and hashes;
- numeric resource caps;
- network NONE;
- a new absent output root.

It emits per-case raw comparison records and one result packet. It cannot open an authority channel,
activate a final, reserve an operational root, or dispatch EA0/EA1 work.

### E14ResultPacket

The packet records:

- controlling local specification roots;
- external standard and errata references;
- case-manifest and coverage-matrix roots;
- every input and golden-expectation root;
- verifier and dependency identities;
- raw results from both verification paths;
- every per-case expected and actual result;
- all differences and unavailable observations;
- DetailCodeRegistry root;
- PASS, FAIL, or INCONCLUSIVE;
- limitations and residual risks;
- no-authority and no-mutation declarations.

The packet is evidence for review only.

## Verification-path separation

Canonical bytes, content roots, and graph order require two separately implemented verification paths
that do not share the canonicalizer or graph-order implementation.

Observable separation must record:

- distinct source and dependency roots;
- distinct entry commands;
- whether parser or canonicalizer libraries are shared;
- distinct raw outputs;
- exact version and environment facts.

This proves implementation-path separation, not cognitive independence.

For a case directly reproduced from an RFC golden vector, the RFC vector is the primary oracle and
both paths are checked against it. For P3.1-specific graphs, expectations use small hand-auditable
graphs plus dual-path agreement. Agreement alone cannot upgrade an unsupported interpretation into a
fact; the clause trace remains controlling.

## Root and graph comparison

Comparison is byte-exact:

- canonical bytes compare as raw bytes;
- digest values compare as raw 32-byte values and typed display strings;
- property order never compares through locale-sensitive text sorting;
- graph vertices compare by typed root and exact canonical bytes;
- canonical graph order uses the P3.1 Kahn ready-set rule;
- output closure compares complete ordered arrays, not only their list root.

A display rendering or parsed semantic equivalence cannot substitute for exact bytes.

## Native approval carriage boundary

Because E13 is absent, E14 contains no successful activation oracle.

Approval cases test only:

- schema carriage of an exact candidate final root, stage, and scope;
- rejection when provenance is missing;
- rejection when root, stage, or scope mismatches;
- preservation of AUTH_APPROVAL_ROOT_UNAVAILABLE;
- preservation of FINALIZED_NOT_AUTHORIZED.

A mock, test, display, or syntactically well-formed approval reference is never considered native
provenance.

## Failure and result algebra

Every prelaunch successor failure case expects:

    execution_state = NOT_STARTED
    outcome = INCONCLUSIVE
    reason_code = PRELAUNCH_CHAIN_MISMATCH
    decision_effect = LEAVES_NAMED_GAP_UNCHANGED

The subordinate detail changes by case. It cannot replace a top-level field.

E14 outcome is separate:

- PASS: all 48 mandatory cases have complete provenance, both verification paths agree with the
  accepted oracle, no unsafe acceptance occurs, and every required field is carried exactly.
- FAIL: a deterministic mismatch, unsafe acceptance, forbidden fallback, missing mandatory closure
  field, top-level tuple drift, or unauthorized activation is observed.
- INCONCLUSIVE: a required fixture, oracle, verifier path, dependency identity, or observation is
  unavailable or ambiguous.

There is no partial PASS. A valid E14 PASS grants no activation or execution permission.

## Security and privacy boundary

All inputs are synthetic. The future corpus contains:

- no user conversation text;
- no real path outside a synthetic namespace;
- no credential, private key, holdout, oracle secret, or production identifier;
- no live approval receipt;
- no executable or script bytes;
- no symlink, junction, or external reference that resolves outside the future corpus root.

Display-only Unicode and malformed-byte vectors are bounded to the exact bytes required by their case.

## Resource and operability boundary

The design fixes 48 cases and forbids unbounded generation. A later fixture authorization must specify
numeric caps for:

- source files and bytes read;
- fixture and manifest objects and bytes created;
- verifier processes, invocations, and concurrency;
- wall and CPU time;
- memory, stdout, and stderr;
- temporary objects;
- final packet objects and bytes.

Default network is NONE. No package download or dynamic dependency resolution is implied.

## Risks

| Risk | Failure condition | Mitigation | Status |
|---|---|---|---|
| E14-R1 oracle circularity | One implementation generates both expected and actual outputs | Frozen external or hand-auditable oracle plus two paths | Open until fixtures |
| E14-R2 RFC misinterpretation | Local case contradicts JCS, I-JSON, or verified errata | Primary-source trace per case | Structurally mitigated |
| E14-R3 authority-shaped fixture misuse | Synthetic final is treated as operational | External fixture wrapper, no approval, no operational root | Needs future custody evidence |
| E14-R4 false completeness | Clause has no case or multiple behaviors are hidden in one case | Coverage matrix and one causal mutation | Open until corpus review |
| E14-R5 implementation monoculture | Two paths share decisive code | Dependency/source-root disclosure | Needs future evidence |
| E14-R6 detail-code drift | Runtime and fixtures use different spellings or placement | Frozen registry root | Needs future schema evidence |
| E14-R7 tuple drift | New detail replaces inherited failure fields | Mandatory algebra cases | Needs fixture execution |
| E14-R8 aggregate masking | Most cases pass while one mandatory case fails | No averaging or partial PASS | Mitigated by contract |
| E14-R9 E13 leakage | Mock approval becomes accepted activation | No positive activation case; E13 remains blocking | Mitigated by design |
| E14-R10 corpus overgrowth | Property generation expands scope indefinitely | Fixed 48-case baseline | Mitigated by design |

## Stop rules

- Stop document work if a case would require real authority provenance.
- Stop future fixture creation without exact separate authorization.
- Stop future E14 sealing if any mandatory clause lacks a case.
- Stop with FAIL on deterministic unsafe acceptance or tuple drift.
- Stop with INCONCLUSIVE when an oracle or independent path is missing.
- Never repair a failed case by deleting it, widening expected results, or changing P3.1.
- Never infer E13, E11, EA0, EA1, or L2 authority from E14.

## Acceptance boundary

This design is complete when:

- the 48-case catalog is specified in the companion plan;
- every P3.1 E14 requirement maps to at least one case;
- standards-derived behaviors name their primary references;
- exact detail vocabulary and result algebra are specified;
- fixture custody and no-authority rules are explicit;
- no fixture bytes or executable tools have been created.

The next step after this document is user review. Actual fixture generation remains separately
authorized work.

## Self-review

- Matrix-first scope is fixed and auditable.
- No positive activation case exists without E13.
- Unicode normalization is not introduced.
- Negative zero is included as a verified-errata rejection case.
- Oracle and system-under-test responsibilities are separated.
- Two implementation paths do not imply cognitive independence.
- Failure details remain subordinate to P3.
- E14 PASS remains non-authorizing.
- No current fixture, schema, runner, or operational object exists.
