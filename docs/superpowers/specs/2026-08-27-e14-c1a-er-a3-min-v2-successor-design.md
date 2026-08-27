# E14 C1a ER-A3-MIN v2 atomic successor design

Status: **DESIGN CONTRACT AVAILABLE; REGISTERED SOURCE INSTANCE ABSENT**

Disposition: `approve with required changes` from
`C1A-SEMANTIC-SUCCESSOR-2026-08-27-R1`.

This document defines one non-authorizing product-preference profile. It does not publish an
ER-A3-MIN source instance and it does not establish source truth, external authority,
compatibility, admission, G0, a recommendation, a freeze, or permission to acquire or execute
anything.

## Historical note (non-normative)

The ambiguous historical tokens `A1` and `H1` motivated creation of unambiguous vocabulary. V2
does not assign a meaning to either token and does not claim equivalence, recovery, migration, or
compatibility. Neither token is a v2 field, alias, selector, reader output, or registry key.

## Normative profile

The wire value is one closed structured profile:

```json
{
  "profile_id": "C1A_CANDIDATE_A_PREFERENCE_PROFILE",
  "profile_version": 1,
  "acquisition_topology": "LOCAL_NODE_BY_VALUE_PLUS_SINGLE_REMOTE_OPAQUE_BODY",
  "http_attempt_profile": "ONE_DNS_ONE_TCP_ONE_TLS_ONE_GET_IDENTITY_NO_RETRY"
}
```

The four fields form one indivisible variant. The two component values are not independently
canonical fields, version selectors, capabilities, defaults, or migration units. The exact
`profile_id` and `profile_version` pair is the only dispatch key. Any semantic change must mint a
new complete profile version that restates every component and returns a new sealed reader variant.

The profile is classified as `PRODUCT_DESIGN_PREFERENCE`. Its fixed result semantics are:

- custody: `OBSERVED_CUSTODY_ONLY`;
- serialization: `J1_SERIALIZATION_ONLY`;
- compatibility: `UNASSESSED`;
- authority effect: `NONE`; and
- next stage authorized: `false`.

The wire schema is
`schemas/e14-c1a-er-a3-min-v2.schema.json`. Every field is required exactly once. Defaults,
coercions, unknown properties, extensions, partial records, field-local versions, and independently
negotiated values are forbidden.

## Design basis, not authority evidence

The substantive design basis is the pre-existing approved C1a specification:

`docs/superpowers/specs/2026-08-27-p6-p3-1-e14-a2-n1-c1a-acquisition-architecture-spec.md`

Its exact byte length is `32777` and its SHA-256 is
`7089AD951DA97A4B5419F80DD2728C130ED1C4020E3196241FB7348FCF5A88DB`.
The lifecycle notice records four exact raw-byte ranges:

| Role | Lines | Byte range `[start,end)` | SHA-256 |
|---|---:|---:|---|
| Acquisition topology | 66–73 | `[4200,4714)` | `90825AFD9C5FBDC104760F8394731F11CEAB7A3AEA49381D6152728C56730D19` |
| Custody/use boundary | 75–89 | `[4715,5328)` | `6B61984B873CD03BC10C06EB80E1A46E144628648AD69B039012AC386FE38E81` |
| J1 serialization boundary | 172–186 | `[10040,10865)` | `CDD9CF0D73772335BB70BD1ECEB64C62162BCD501F23A7F4F777A8F337E748E2` |
| HTTP attempt profile | 349–384 | `[17081,19054)` | `AEE54A4F558C4997D063FD39ED4C0A17408DFDC860010BC59237A3A064AB16F1` |

These hashes identify bytes supporting the new product preference. They do not prove that the
document is externally authoritative or factually true. This successor document's own digest may
identify its schema revision only; it may never serve as independent evidence for the choice it
defines.

## Reader contract

`src/e14_c1a_er_a3_min_v2.py` parses a bounded UTF-8 JSON byte string, rejects a BOM, malformed JSON,
duplicate keys, the wrong field set, wrong types, unknown profile IDs or versions, and any component
value outside the one sealed tuple. J1 is used only as serialization discipline.

The reader validates the complete record before it invokes the private nominal constructor. The
only public success value is one immutable `CandidateAPreferenceProfileV1` containing both profile
components and all fixed non-effects. There is no public component parser, constructor, partial
result, optional/default path, independent version router, or field-level admission result.

If a future implementation cannot preserve validation-before-construction and a single sealed
result, it must replace the surface with one sealed `semantic_profile` value rather than expose
partial component semantics.

## V1 retirement and version resolution

V1's committed bytes remain immutable. The external lifecycle notice
`evidence/e14-c1a-er-a3-min-version-registry.json` locks the exact digests of the v1 design,
schema, validator, and baseline tests and classifies v1 as:

```text
lifecycle_status = RETIRED_UNISSUED
resolution = AUDIT_REPRODUCTION_ONLY
issuance = REJECT
admission = REJECT
migration = NONE
semantic_inference = NONE
```

V2 is `HISTORICAL_SUCCESSOR_ONLY`: an artifact-lineage successor, not a correction,
reinterpretation, migration target, or compatibility claim. Normal v1 use fails
`ER_A3_V1_RETIRED_UNISSUED`. The explicit audit route wraps the immutable v1 validator in a
non-admitting result. No v1-to-v2 converter, fallback, alias mapping, or compatibility adapter
exists.

Rollback removes v2 artifacts but retains the v1 digest lock and retirement. The resulting current
successor is `NONE`; rollback never reactivates v1.

## Conformance corpus and validator limit

`fixtures/e14_c1a_er_a3_min_v2_cases.json` is
`CONFORMANCE_FIXTURE_NON_NORMATIVE`. It has no registry, catalog, recommendation, freeze, authority,
or admission effect. Its one positive specimen and negative cases are fed as identical serialized
bytes to JSON Schema and the reader. The negative matrix covers missing, null, duplicate, unknown,
wrong-type, coercible, wrong-case, whitespace-altered, historical-token, unknown-version,
independent-version, mixed-value, and partial records.

Successful validation proves only profile shape and schema/reader accept-reject parity. It does not
prove design-source truth or authority, compatibility, recommendation, admission, freeze, G0, or
operational readiness.

## Registered-instance and authorization boundary

The registered source-instance inventory is empty. Technical readiness, hashes, and passing tests
are necessary but insufficient to publish an instance. A future instance requires both a concrete,
independently authorized consumer/use and a separate same-version semantic-admission decision. A
consumer request must not auto-create the instance.

This tranche ends after lifecycle metadata, v2 design/schema/reader, non-normative fixtures, tests,
and documentation. It authorizes no network, acquisition, execution, migration, compatibility
finding, recommendation, freeze, G0/gate action, downstream admission, commit-dependent operation,
or automatic follow-up.
