# E14 C1a consumer-intent v1 design

Status: **APPROVED FOR PLANNING; NOT IMPLEMENTED**

This design defines one concrete, read-only consumer use for the ER-A3-MIN v2 atomic profile. It
does not implement the consumer, publish a source instance, perform semantic admission, issue a
team recommendation, freeze Candidate A, satisfy G0, or authorize acquisition or execution.

## Decision

Create `C1A_DESIGN_RECOMMENDATION_CONSUMER.v1`, a pure design-plane consumer-intent admission
boundary. Its sole product use is to establish whether a complete, version-matched consumer intent
is eligible for a later non-ratifying Candidate A recommendation workflow.

The consumer is not an acquisition planner, calibration component, runtime adapter, source-instance
registry, recommendation issuer, or governance authority. The `sana-v3` calibration and archive
admission modules are outside this design.

## Invariants

1. The only consumer is `C1A_DESIGN_RECOMMENDATION_CONSUMER.v1`.
2. The only use is `DESIGN_PLANE_RECOMMENDATION_ONLY`.
3. The only candidate is `A`.
4. The only accepted profile binding is
   `C1A_CANDIDATE_A_PREFERENCE_PROFILE` version `1`.
5. The requested effect is `CONSUMER_INTENT_ADMISSION_ONLY`.
6. A successful result is `C1A_CONSUMER_INTENT_ADMITTED_NON_AUTHORIZING`.
7. Every non-success path is `STRICT_STOP` with a typed reason.
8. There are no defaults, coercions, aliases, partial results, compatibility fallback, version
   negotiation, or automatic continuation.
9. Successful intent admission does not require or create a registered ER-A3-MIN source instance.
10. Successful intent admission is not semantic admission, recommendation, ratification, freeze,
    G0, gate movement, operational authority, or permission to access a network or filesystem.
11. The existing v1 retirement and v2 profile contract remain unchanged.
12. Any future source-instance or semantic-admission phase requires a separate decision and cannot
    infer authorization from this result.

## Input contract

The future closed input schema is `sana.e14.c1a.consumer-intent.v1`:

```json
{
  "schema": "sana.e14.c1a.consumer-intent.v1",
  "consumer_id": "C1A_DESIGN_RECOMMENDATION_CONSUMER.v1",
  "use": "DESIGN_PLANE_RECOMMENDATION_ONLY",
  "candidate": "A",
  "profile_binding": {
    "profile_id": "C1A_CANDIDATE_A_PREFERENCE_PROFILE",
    "profile_version": 1
  },
  "requested_effect": "CONSUMER_INTENT_ADMISSION_ONLY",
  "authority_effect": "NONE",
  "next_stage_authorized": false
}
```

All fields are required exactly once. Unknown fields, duplicate JSON names, nulls, wrong JSON
types, alternate case or whitespace, unknown consumer/use/candidate/profile/version/effect, and
truthy next-stage values reject. No field has a default.

The record contains no requester identity, owner, mandate, approval receipt, source instance,
recommendation value, runtime path, credential, endpoint, or gate identifier. This prevents the
intent contract from becoming a local authority-minting mechanism.

## Processing model

The planned public API is:

```text
admit_consumer_intent(intent_raw_bytes, profile_raw_bytes)
  -> AdmittedConsumerIntentV1
  | StrictStop
```

Processing is ordered and fail-closed:

1. Bound the two raw byte strings before parsing.
2. Parse the intent under strict UTF-8 JSON rules, rejecting a BOM, duplicate keys, malformed input,
   forbidden numeric forms, and trailing data.
3. Validate the complete closed intent record and its exact constants.
4. Parse `profile_raw_bytes` through the existing
   `parse_candidate_a_preference_profile` reader.
5. Compare the admitted profile's complete ID/version to `profile_binding`.
6. Construct one nominal, immutable `AdmittedConsumerIntentV1` only after both complete inputs pass.
7. Return no partially validated intent or profile data on failure.

The profile input used by tests is the existing `CONFORMANCE_FIXTURE_NON_NORMATIVE` specimen. It
does not become a registered source instance. The consumer must not call
`resolve_registered_source_instance` and must not interpret `None` as permission to synthesize one.

## Success result

The sealed success result contains only:

```text
status = C1A_CONSUMER_INTENT_ADMITTED_NON_AUTHORIZING
consumer_id = C1A_DESIGN_RECOMMENDATION_CONSUMER.v1
use = DESIGN_PLANE_RECOMMENDATION_ONLY
candidate = A
profile_id = C1A_CANDIDATE_A_PREFERENCE_PROFILE
profile_version = 1
preference_class = PRODUCT_DESIGN_PREFERENCE
compatibility = UNASSESSED
recommendation_effect = NONE
ratification_effect = NONE
freeze_effect = NONE
consumer_intent_effect = ADMITTED_ONLY
semantic_admission_effect = NONE
authority_effect = NONE
next_stage_authorized = false
```

The status means only that a concrete consumer/use contract exists and matches the v2 profile
shape. It does not mean that Candidate A is correct, preferred, recommended, admitted, frozen, or
ready to run.

## Failure model

The implementation plan may refine diagnostic pointers, but it must preserve this closed reason
set:

- `C1A_INTENT_RAW_TOO_LARGE`
- `C1A_INTENT_JSON_INVALID`
- `C1A_INTENT_JSON_DUPLICATE_KEY`
- `C1A_INTENT_FIELD_SET_INVALID`
- `C1A_INTENT_CONSUMER_UNSUPPORTED`
- `C1A_INTENT_USE_UNSUPPORTED`
- `C1A_INTENT_CANDIDATE_UNSUPPORTED`
- `C1A_INTENT_PROFILE_BINDING_UNSUPPORTED`
- `C1A_INTENT_EFFECT_ESCALATION`
- `C1A_INTENT_PROFILE_INVALID`
- `C1A_INTENT_PROFILE_BINDING_MISMATCH`

Every failure has terminal status `STRICT_STOP`, authority effect `NONE`, and
`next_stage_authorized=false`. There is no retry, fallback, default, mutation, or automatic request
for missing evidence.

## Planned implementation boundary

Implementation planning is limited to:

- `schemas/e14-c1a-consumer-intent-v1.schema.json`;
- `src/e14_c1a_consumer_intent.py`;
- `fixtures/e14_c1a_consumer_intent_v1_cases.json`;
- `tests/test_e14_c1a_consumer_intent.py`; and
- direct README and evidence-status updates.

The implementation must remain pure: no filesystem reads, network access, clock, environment,
database, subprocess, persistence, registry mutation, application import, or `sana-v3` dependency.
It may import only the existing v2 profile reader from this evidence package.

No existing v1 or v2 contract bytes may be changed. The version registry's registered-instance
inventories must remain empty.

## Test strategy

One shared raw-byte corpus must be evaluated by JSON Schema and the reference reader. It includes:

- one exact positive intent/profile pair;
- missing, extra, duplicate, null, wrong-type, wrong-case, and whitespace-altered fields;
- unsupported consumer, use, candidate, requested effect, profile ID, and profile version;
- profile-binding mismatch after each input is independently valid;
- malformed, BOM-prefixed, invalid UTF-8, oversized, floating-point, and non-object input;
- nominal-result anti-forgery and immutability;
- no partial result after either input fails;
- filesystem, network, clock, environment, database, and subprocess traps;
- unchanged v1 digests and v2 reader behavior;
- empty registered-source-instance inventories before and after every case; and
- absence of imports or calls into `sana-v3`, acquisition, calibration, admission, or runtime code.

The current 179-test suite remains the regression baseline.

## Alternatives rejected

### Acquisition-planner consumer

Rejected because translating the profile into network or execution actions would cross G0 and
operational gates. It would also make a design preference appear to authorize acquisition.

### Calibration-system consumer

Rejected because model-review calibration, provider billing, and crash settlement are a different
semantic domain. Shared words such as candidate or admission do not establish compatibility.

### External consumer wait

Safe but unnecessarily inert after the requester approved a concrete design-plane recommendation
use. It remains the fallback if this design is withdrawn.

## Rollback and next boundary

Rollback removes only the future consumer-intent schema, module, fixture, tests, and direct status
documentation. The ER-A3-MIN v1 retirement and v2 design contract remain unchanged; the source
instance inventory remains empty.

After a future implementation passes its focused and full regression tests, work stops at:

```text
C1A_CONSUMER_INTENT_ADMITTED_NON_AUTHORIZING
ER_A3_MIN_REGISTERED_SOURCE_INSTANCE_ABSENT
SEMANTIC_ADMISSION_NOT_RUN
```

The next possible phase would be a separate source-instance and same-version semantic-admission
decision. It is not authorized by this design or by successful consumer-intent validation.
