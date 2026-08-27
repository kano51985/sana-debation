# E14 C1a ER-A3-MIN contract design

Date: 2026-08-27

Status: **APPROVED FOR CONTRACT IMPLEMENTATION ONLY**

This design turns the unresolved `ER-A3-MIN` evidence shape into a machine-checkable, read-only
contract. It does not provide the missing A1 or H1 semantics, identify an authority, create an
evidence package, approve Candidate A, assess compatibility, or authorize C1a acquisition.

## Context and decision

The read-only source investigation found four decisive conditions:

1. The current C1a architecture is a specification-only, operationally blocked document.
2. `AcquisitionManifestV1` and `AcquisitionReceiptV1` are prose obligations, not exact schemas.
3. No current reader implements those record contracts.
4. `A1` is overloaded by unrelated historical acquisition and debate-axis meanings, while `H1`
   has no repository definition. Guessing either meaning would manufacture semantics.

Three approaches were considered:

- wait for an unspecified external package, which is safe but supplies no stable admission
  interface;
- infer A1/H1 from nearby names, which is rejected because name proximity is not evidence; and
- define a contract that future sources must satisfy without generating or interpreting the
  missing semantics.

The third approach is selected. It provides useful structure while keeping
`ER_A3_MIN_SOURCE_GAP` as the current state.

## Artifacts and boundary

The contract consists of:

- `schemas/e14-c1a-er-a3-min-v1.schema.json`, the closed package shape;
- `src/e14_c1a_er_a3_min.py`, a pure raw-byte validator and schema/reader parity checker; and
- `tests/test_e14_c1a_er_a3_min.py`, positive, negative, purity, and schema-parity tests.

No package instance is created in this tranche. In particular, the implementation must not fill
`canonical_field_id`, legal-domain values, meanings, source spans, source-accountability claims,
or reader behavior on behalf of a future source.

The validator performs no filesystem, network, clock, environment, logging, persistence, Git, or
authority operation. A successful result means only that supplied bytes satisfy this contract and
that their declared field schema and reader interpretation agree structurally.

## Package model

The top-level package is exact and versioned:

```text
schema = sana.e14.c1a.er-a3-min.v1
profile = C1A_ER_A3_MIN_READ_ONLY_V1
candidate = A
source_spec
anchors[A1, H1]
canonical_profile
compatibility = UNASSESSED
authority_effect = NONE
next_stage_authorized = false
limitations
```

`source_spec` identifies the proposed source specification by repository-relative path, SHA-256,
declared version, and `SPECIFICATION_ONLY` status. Those declarations are content fields; the pure
validator cannot prove that the path exists, that the digest is current, or that an external
authority endorses it.

There must be exactly one A1 anchor and one H1 anchor. The aliases are lookup labels only. Each
anchor must explicitly supply:

- a collision-free `canonical_field_id`;
- `semantic_class = VERIFIED_FACT | PRESCRIPTIVE_PREFERENCE | MIXED`;
- an accountable source identity and one or more exact source spans;
- an exact field schema with wire name, version, JSON type, requirement, legal domain, and
  no-default behavior; and
- a reader interpretation naming the same field, schema version, JSON type, legal domain, and an
  explicit unknown-input behavior.

The contract does not decide which semantic class or legal domain is correct. It only prohibits
omission and mismatch.

## Legal-domain representation

Each anchor uses exactly one domain form:

- `STRING_ENUM` with one or more unique string values;
- `INTEGER_RANGE` with inclusive safe-integer minimum and maximum;
- `BOOLEAN`; or
- `OBJECT_SCHEMA_REF` with a versioned, digest-bound schema reference.

The validator normalizes each form into an immutable comparison tuple. The field schema and reader
must produce identical tuples. It does not interpret what a value means beyond the supplied
source-bound textual meaning.

## Reader parity and typed failures

The validator checks in this order:

1. raw byte limit, BOM, UTF-8, JSON syntax, duplicate keys, and top-level type;
2. exact top-level fields and fixed discriminators;
3. exact A1/H1 membership with no duplicate or extra alias;
4. source-reference and source-span shapes;
5. field-schema and reader-contract shapes; and
6. same-field, same-version, same-type, same-requiredness, same-domain parity.

Typed failures are stable:

```text
ER_A3_RAW_TOO_LARGE
ER_A3_JSON_BOM
ER_A3_JSON_INVALID_UTF8
ER_A3_JSON_INVALID
ER_A3_JSON_DUPLICATE_KEY
ER_A3_PACKAGE_FIELD_SET
ER_A3_SCHEMA_UNSUPPORTED
ER_A3_PROFILE_UNSUPPORTED
ER_A3_CANDIDATE_UNSUPPORTED
ER_A3_PACKAGE_INVALID
ER_A3_ANCHOR_SET_INVALID
ER_A3_SOURCE_INVALID
ER_A3_FIELD_SCHEMA_INVALID
ER_A3_READER_CONTRACT_INVALID
ER_A3_SCHEMA_READER_MISMATCH
```

Diagnostics may identify a JSON Pointer, but no error changes a gate or produces a fallback value.

## Successful-result semantics

A successful `VerifiedERA3MinPackageV1` is nominal and immutable. It establishes only:

```text
package_shape = VALID
declared_schema_reader_parity = MATCHED
source_truth = NOT_PROVEN_BY_VALIDATOR
source_authority = NOT_PROVEN_BY_VALIDATOR
compatibility = UNASSESSED
authority_effect = NONE
next_stage_authorized = false
```

It is not a `TEAM_RECOMMENDATION`, semantic ratification, evidence of ownership, G0 receipt,
acquisition capability, implementation input, or operational record.

## Testing and stopping rule

Tests must cover exact valid shapes for every legal-domain form; missing/extra fields; alias
collision; duplicate JSON names; invalid source spans and digests; schema/reader version, type,
requiredness, wire-name, and domain mismatches; unsupported discriminators; immutability; raw-size
limits; and absence of filesystem/network/clock calls.

After schema, validator, and tests pass, this tranche stops. The next state is
`ER_A3_MIN_CONTRACT_READY_SOURCE_INSTANCE_ABSENT`. Populating a real package requires a separately
identified source and must not be inferred from this contract.
