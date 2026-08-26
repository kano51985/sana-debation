# P6 P3.1 E14 read-only fixture plan

Date: 2026-08-26

Status: planning artifact only. It defines a future 48-case static corpus. No listed path, byte
fixture, expected root, schema, validator, or result packet is created or authorized by this plan.

## Purpose

Turn the E14 matrix-first design into a bounded, inspectable fixture-construction contract while
preserving the P3.1 non-activation boundary.

## Controlling design

The controlling E14 design is:

    2026-08-26-p6-p3-1-e14-compatibility-root-carriage-design.md

Its reviewed SHA-256 is:

    74F96D292B7D3B1E85E3EA0847ACB9DB39798930D9D15ADE65AFEE125B2DF2F8

The P3.1 predecessor roots remain:

- design: B6DBE2702C6CBB0CA69E3BAF2F595DB8E4D57ADA8BC23B810DFF109955EC6E20;
- acquisition amendment: C3ECEB8CB3E47EADA03A85F3479EA7EED9D668C507F53231225349BB1933D5DA;
- conformance record: 3CAE47A62B2B5DD4A3BED7108CB61E827F511439D1643E813311CBA6544F48FA.

## Current non-action boundary

This plan does not authorize:

- creating the planned directory tree;
- copying RFC examples into files;
- generating malformed byte sequences;
- computing golden canonical bytes or roots;
- implementing or running either verification path;
- selecting packages or downloading dependencies;
- producing a native approval reference;
- creating any operational authorization-shaped object;
- EA0, L0, EA1, E10, E11, E13, L2, or production work.

## Planned future corpus topology

The following names are reservations in the plan, not existing paths:

    e14-corpus/
      corpus-manifest.json
      clause-coverage.json
      detail-code-registry.json
      cases/
        <case-id>/
          case.json
          input.bin
          expected.json
      standards/
        source-index.json
      verifier-a/
        identity.json
      verifier-b/
        identity.json
      results/
        <case-id>-a.json
        <case-id>-b.json
      e14-result.json

Every future path is relative to one new absent corpus root. No symlink, junction, reparse point, or
external include is permitted.

## Planned manifest responsibilities

### corpus-manifest.json

Would bind:

- exact controlling specification roots;
- exact external-source identifiers and retrieval provenance;
- all 48 ordered case roots;
- clause-coverage root;
- detail-code-registry root;
- verifier identity roots;
- result schema version;
- no-authority declaration;
- retention and numeric caps;
- terminal state and corpus content root.

### case.json

Would contain only the descriptive E14CaseManifest fields. It never contains a native approval receipt.

### input.bin

Would preserve exact raw bytes. Text display is derivative only. Malformed cases remain byte files and
are never rewritten through a text editor or parser.

### expected.json

Would contain exact expected parse, canonicalization, root, role, graph, capability, activation,
detail-code, inherited-tuple, and output-closure results.

### e14-result.json

Would contain complete per-case comparison roots and E14 PASS, FAIL, or INCONCLUSIVE. It grants no
authority.

## Planned case catalog

All 48 cases are mandatory. Each negative case has one primary causal distinction.

### JCS and I-JSON: 12 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| JCS-01 | Object properties arrive in noncanonical order | Accept; recursively sort by raw UTF-16 code units |
| JCS-02 | Objects occur inside arrays | Accept; sort object properties and preserve array element order |
| JCS-03 | Control characters, quote, and backslash require exact escaping | Accept; emit JCS string form |
| JCS-04 | Representative integer, decimal, and exponent forms | Accept only within I-JSON/JCS number domain; emit canonical number bytes |
| JCS-05 | Canonically equivalent-looking composed and decomposed Unicode strings | Accept as distinct unchanged strings with distinct roots |
| JCS-06 | Nested objects, arrays, literals, and strings are combined | Accept; emit one exact whitespace-free canonical byte sequence |
| JCS-07 | Duplicate object member name | Reject with AUTH_CANONICAL_IJSON_INVALID |
| JCS-08 | UTF-8 byte-order mark precedes JSON | Reject with AUTH_CANONICAL_UTF8_INVALID |
| JCS-09 | Invalid UTF-8 byte sequence | Reject with AUTH_CANONICAL_UTF8_INVALID |
| JCS-10 | Lone surrogate or invalid Unicode scalar condition | Reject with AUTH_CANONICAL_JCS_INVALID |
| JCS-11 | Number cannot be represented within the required I-JSON/JCS domain | Reject with AUTH_CANONICAL_IJSON_INVALID |
| JCS-12 | Negative-zero input covered by verified RFC 8785 errata | Reject with AUTH_CANONICAL_JCS_INVALID |

### Envelope and typed root: 4 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| ENV-01 | Whitespace and member order differ but semantic payload is identical | Same canonical payload bytes and content root |
| ENV-02 | One semantic payload field changes | Different content root |
| ENV-03 | Payload contains its own content_root or another self-root field | Reject with AUTH_SELF_REFERENCE_FORBIDDEN |
| ENV-04 | Envelope digest differs from recomputed payload digest | Reject with AUTH_CONTENT_ROOT_MISMATCH |

### Role mapping: 4 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| ROL-01 | EA0AuthorizationIntent has grants_execution false | Accept role; remain non-authorizing |
| ROL-02 | EA0AuthorizationManifest binds intent and complete contracts | Accept final role; remain FINALIZED_NOT_AUTHORIZED |
| ROL-03 | EA1ExecuteAuthorizationIntent and final authorization use distinct schemas | Accept exact roles; intent remains non-authorizing |
| ROL-04 | EA0AuthorizationIntent is presented as an EA0AuthorizationManifest | Reject with AUTH_ROLE_MISMATCH |

### Binding and graph closure: 10 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| GRF-01 | Minimal valid EA0 intent, two contracts, and final | Accept exact DAG and canonical order; no activation |
| GRF-02 | Minimal valid EA1 intent, contracts, manifests, and final | Accept exact DAG and canonical order; no activation |
| GRF-03 | Object references its own typed root | Reject with AUTH_GRAPH_CYCLE |
| GRF-04 | Two intermediates form an indirect cycle | Reject with AUTH_GRAPH_CYCLE |
| GRF-05 | Intermediate contains a reference to the later final | Reject with AUTH_FINAL_BACKREFERENCE_FORBIDDEN |
| GRF-06 | One required binding slot is absent | Reject with AUTH_BINDING_SLOT_MISSING |
| GRF-07 | A binding slot occurs twice | Reject with AUTH_BINDING_SLOT_DUPLICATE |
| GRF-08 | Final reverses two otherwise valid binding slots relative to the intent plan | Reject with AUTH_BINDING_SET_MISMATCH |
| GRF-09 | Same typed root resolves to two different canonical byte sequences | Reject with AUTH_ROOT_COLLISION |
| GRF-10 | Multiple vertices are simultaneously ready and one root is referenced repeatedly | Emit exact Kahn order; deduplicate identical exact references only |

### Capability, schema, and fallback: 6 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| CAP-01 | Exact required core capabilities are supported | Capability check passes; activation still unavailable |
| CAP-02 | Required capability is omitted | Reject with AUTH_CAPABILITY_MISSING |
| CAP-03 | Required capability is unknown or unsupported | Reject with AUTH_CAPABILITY_UNSUPPORTED |
| CAP-04 | Legacy P3 and P3.1 nodes are mixed | Reject with AUTH_SCHEMA_MIXED |
| CAP-05 | Consumer implicitly upconverts a legacy P3 object into a P3.1 role | Reject with AUTH_UPCONVERSION_FORBIDDEN |
| CAP-06 | Signed profile falls back to unsigned or another profile | Reject with AUTH_PROFILE_FALLBACK_FORBIDDEN |

### Native approval-root carriage: 4 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| APR-01 | Native approval provenance is absent | FINALIZED_NOT_AUTHORIZED plus AUTH_APPROVAL_ROOT_UNAVAILABLE |
| APR-02 | Approval reference carries a different final root | Reject with AUTH_APPROVAL_ROOT_MISMATCH |
| APR-03 | Approval reference carries the correct root but wrong stage | Reject with AUTH_APPROVAL_STAGE_MISMATCH |
| APR-04 | Approval reference carries the correct root and stage but wrong scope | Reject with AUTH_APPROVAL_SCOPE_MISMATCH |

No APR case expects ACTIVATED_FINAL. A syntactically correct test reference remains non-native and
non-authorizing.

### Output closure and carriage: 4 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| CLS-01 | Core-profile result carries final, intent, ordered ancestors, approval reference, claim, and effect state | Accept schema carriage only; no operational acceptance |
| CLS-02 | One mandatory ancestor root is absent | Reject with AUTH_CLOSURE_INCOMPLETE |
| CLS-03 | Ancestor array is complete but not in canonical order | Reject with AUTH_CLOSURE_ORDER_MISMATCH |
| CLS-04 | Unsigned core-profile result incorrectly includes signed-witness fields | Reject with AUTH_SCHEMA_MIXED |

### Failure algebra: 2 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| ALG-01 | Representative graph, schema, capability, or approval detail is present | Top-level tuple remains NOT_STARTED, INCONCLUSIVE, PRELAUNCH_CHAIN_MISMATCH, LEAVES_NAMED_GAP_UNCHANGED |
| ALG-02 | AUTH_FENCE_UNSUPPORTED is encoded in an inert prelaunch result | Detail remains subordinate to the inherited prelaunch tuple and grants no retry |

ALG-02 proves field placement and enumeration only. E11 remains required for behavior.

### Metamorphic checks: 2 cases

| ID | Causal distinction | Expected result |
|---|---|---|
| MET-01 | Only input whitespace and object-member order change | Canonical bytes and root stay identical |
| MET-02 | One authorization-semantic value changes while display remains similar | Root changes and every dependent binding becomes mismatched |

## Coverage summary

| Family | Case count |
|---|---:|
| JCS and I-JSON | 12 |
| Envelope and typed root | 4 |
| Role mapping | 4 |
| Binding and graph closure | 10 |
| Capability, schema, and fallback | 6 |
| Native approval-root carriage | 4 |
| Output closure | 4 |
| Failure algebra | 2 |
| Metamorphic checks | 2 |
| Total | 48 |

The total is a fixed baseline, not a score denominator that permits failures.

## Oracle construction plan

Future authorization would require:

1. Freeze exact local specification hashes and primary RFC references.
2. Create ClauseCoverageMatrix before fixture bytes.
3. Construct each input independently from its expected-result record.
4. Anchor JCS cases to RFC text, RFC examples where applicable, and verified errata.
5. Derive P3.1 graph expectations from small hand-auditable DAGs.
6. Have a second review path recompute canonical bytes, roots, and Kahn order without using the
   system-under-test implementation.
7. Freeze expected bytes and roots before running either compatibility verifier.
8. Seal every discrepancy rather than editing the oracle after observing actual output.

If an expectation changes, the old corpus is retained and the reason, evidence, review, and new corpus
root are recorded. Silent golden-file update is prohibited.

## Verification-path plan

Two future paths are required:

- Path A: reference-oriented canonicalization and graph verification.
- Path B: separately implemented compatibility path.

The plan does not select languages, packages, or executables. Future admission must show:

- distinct source roots;
- distinct decisive canonicalizer and graph-order implementations;
- exact dependency roots;
- no dynamic dependency download;
- network NONE;
- raw output separation;
- reproducible command and configuration roots.

Shared operating system or JSON parser is disclosed. It limits independence claims but does not
automatically invalidate the comparison if decisive canonicalization and graph logic remain separate.

## Planned detail-code registry validation

The future detail-code-registry.json must:

- contain exactly the approved E14 design vocabulary;
- assign each code to one category;
- mark whether E14 checks encoding only or behavior;
- map every prelaunch code to the inherited top-level tuple;
- map claim and fence behavior to E11;
- prohibit aliases, case variants, unknown fallbacks, and display-only substitutions;
- have an immutable content root.

A verifier must reject an unknown detail code rather than treat it as a known successful state.

## Planned result comparison

For every case, compare:

- raw input root;
- parse status;
- canonical bytes and length;
- content root profile and digest;
- artifact kind and schema;
- exact graph vertex and edge set;
- canonical vertex order;
- binding-plan status;
- capability status;
- activation state;
- subordinate detail;
- inherited tuple;
- output-closure arrays and list roots;
- authority_effect.

All differences are retained.

## E14 result decision

PASS requires:

- all 48 cases present and individually passing;
- complete clause coverage;
- immutable input and oracle provenance;
- dual-path agreement with the accepted oracle;
- exact detail-code registry agreement;
- no unsafe acceptance;
- no ACTIVATED_FINAL;
- no top-level tuple drift;
- complete raw comparison roots.

FAIL occurs on any deterministic mismatch, unsafe acceptance, forbidden fallback, missing closure,
tuple drift, or activation.

INCONCLUSIVE occurs when a mandatory artifact, primary source, oracle, verifier path, dependency
identity, or observation is unavailable or ambiguous.

No outcome authorizes E13, E11, EA0, EA1, or L2.

## Planned custody

Future fixtures are:

- synthetic only;
- immutable after sealing;
- stored under one new absent corpus root;
- free of real credentials, approval receipts, user data, holdout, or production paths;
- never mounted into an operational run root;
- never accepted from a symbolic or reparse traversal;
- never overwritten, deleted, or silently regenerated.

Malformed byte fixtures are displayed only through escaped summaries. The raw bytes remain the
authority for the test input.

## Proposed future size boundary

The exact later authorization must set numeric caps. The planning ceiling is:

- exactly 48 case directories;
- at most one raw input and one expected-result object per case, plus bounded comparison records;
- at most 160 total corpus and result objects;
- at most 2 MiB total sealed corpus bytes before raw verifier logs;
- network and package downloads equal zero;
- no concurrency above the separately approved verifier-path count.

These are planning ceilings, not current authority or final runtime caps.

## Planned review gates

Before fixture creation:

- user approves the exact fixture root, file plan, tools, caps, and prohibitions;
- primary-standard references and errata are frozen;
- no E13 or operational authority is included.

Before verifier execution:

- every input and expectation root exists and is sealed;
- verifier identities and dependencies are exact;
- network is NONE;
- output root is absent;
- numeric caps are approved.

Before E14 PASS:

- all raw results and discrepancies are retained;
- every case maps back to the coverage matrix;
- no oracle was updated after actual output without a new retained corpus version;
- a reviewer confirms that PASS grants no operational authority.

## Stop rules

- Stop if a fixture needs real authority provenance.
- Stop if a positive activation expectation appears.
- Stop if one case contains multiple unrelated causal mutations.
- Stop if the system under test generated its own only oracle.
- Stop if either verifier path is unavailable.
- Stop if a case or raw discrepancy would be omitted.
- Stop if a proposed fix changes P3.1 instead of recording a failing case.
- Stop if future actions exceed exact approved file, byte, process, time, or network caps.

## Rollback

Before fixture creation, rollback is deletion of no files because none exist.

After a future sealed corpus exists, rollback means withholding it from execution and retaining its
content roots. It never means modifying a golden expectation, deleting a failure, activating a final,
or falling back to legacy semantics.

## Current completion condition

This plan is complete when:

- the 48 case contracts are present in this document;
- the count sums exactly to 48;
- no case expects native activation;
- every case has one causal distinction and exact expected category;
- the later file topology, oracle separation, decision rule, custody, and stop rules are explicit;
- no fixture or executable artifact has been created.

## Self-review

- Case count is 48.
- Each family count is explicit.
- No case expects ACTIVATED_FINAL.
- RFC-derived cases preserve strings without Unicode normalization.
- Negative zero is a rejection case.
- Claim and fence cases validate schema placement only and remain E11-gated.
- Every E14 failure remains non-authorizing.
- No future path or cap is treated as current authority.
