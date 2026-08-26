# P6 evidence proposal P4/P3.1: acyclic authorization binding successor

Date: 2026-08-26

Status: additive written-spec successor approved by the fresh Chief Architect for document architecture
only. This document creates no authorization object, selects no operational root or cap, and authorizes
no EA0, L0, EA1-CONSTRUCT, EA1-EXECUTE, L2, signing infrastructure, network action, or production
mutation.

## Controlling predecessors

This successor depends on, but does not modify or reinterpret:

| Artifact | SHA-256 |
|---|---|
| P4/P3 design | 9D72EF54012348523FB11D21728E9C827D106F9B73D8E6B17B57AF01367C90A2 |
| P4/P3 NE1-NE5 acquisition plan | 71801CBE28254FC71D8C2CEBE0B47740330CD6B165C5232FD032717BB8D390DA |
| P4/P3 conformance record | 0DC996D7CD9C815E5F4BA2DDCCA2B03EEE04A3A1CACDE4AF123C34C9C0E5B561 |

The predecessor P3 documents and all v1-v7 bytes and hashes remain immutable.

## Decision

Replace each cyclic one-phase authorization content graph with:

    non-authorizing intent
        -> exact intermediate contracts and manifests
        -> final authorization content root
        -> native approval of that exact final root
        -> complete verification and single-use local claim
        -> bounded stage action

The content hash identifies exact semantic bytes. It does not itself grant authority. The already
established user or authority channel must approve the exact final root, stage, and scope before a
final object can activate.

## P3.1-01 — Scope and precedence

P3.1 controls only:

- successor authorization phase ordering;
- canonical successor content roots;
- intent, intermediate, and final content references;
- exact-root activation;
- authorization-graph closure;
- single-use local claim semantics directly required to prevent replay;
- subordinate successor failure detail.

P3 continues to control every other gate, cap, root-isolation rule, network prohibition, retention
rule, outcome, decision effect, launch control, no-resend rule, and no-automatic-next-stage rule.

Legacy P3 artifacts remain P3-only. They are never rewritten, rehashed, upgraded, downgraded, mixed
with a P3.1 execution graph, or treated as P3.1 objects.

## Invariants

- I1 — Acyclicity: every P3.1 content-root graph is finite, acyclic, and computable in topological
  order. No payload directly or transitively contains its own root.
- I2 — Activation: an intent, contract, manifest, content hash, filename, ID, summary, document
  approval, or debate approval grants no operational authority.
- I3 — Direction: every intermediate binds its exact intent root and only already-existing
  ancestors. It never binds the later final root.
- I4 — Completeness: a final binds its intent and the exact ordered complete set of typed
  intermediate roots. Indirection or reconstruction cannot substitute for those roots.
- I5 — Canonical identity: the canonical payload, root profile, graph order, and collision behavior
  are versioned and non-self-referential.
- I6 — Additive compatibility: predecessor P3 and v1-v7 bytes and hashes remain unchanged.
- I7 — Fail closed: graph, approval, capability, claim, or fence uncertainty stops before effects
  and preserves the inherited three-valued evidence algebra.
- I8 — Audit closure: downstream evidence binds the activated final, intent, complete ancestors,
  native approval reference, claim, and effect state without widening authority.

## P3.1-02 — Canonical core root

The mandatory profile is p6.p3_1.content-envelope.v1:

    {
      "envelope_schema": "p6.p3_1.content-envelope.v1",
      "payload": { ...all semantic fields... },
      "content_root": {
        "profile": "sha256-jcs-p31",
        "digest": "<64 lowercase hexadecimal characters>"
      }
    }

Root computation is:

    canonical_payload_bytes = RFC8785-JCS(payload)
    content_digest = SHA-256(canonical_payload_bytes)
    content_root = "sha256-jcs-p31:" + lowercase_hex(content_digest)

Inputs use strict UTF-8 JSON:

- no byte-order mark;
- no duplicate member names;
- no invalid Unicode;
- no non-I-JSON or non-finite number;
- schema-constrained UTC timestamp strings;
- lowercase fixed-length hexadecimal digests.

The payload contains every semantic permission, prohibition, stage, root, operation, tool, cap,
network, retention, expiry, binding, and scope field. The derived content root is outside the payload.
The payload may not contain its own content root, a later final root, a signature, a witness-envelope
hash, or another self-dependent value.

## P3.1-03 — Unsigned mandatory core

The mandatory core payload declares:

    authorization_proof_profile = NATIVE_EXACT_ROOT_APPROVAL
    signature_profile = NONE

Under this profile, signer, signature, key-root, quorum, and trust-policy fields are prohibited. A
valid content hash proves content identity only.

## P3.1-04 — Conditional signed-witness profile

A signed-witness profile is inactive unless E13 establishes a pre-existing authorization-signing
governance and E10 proves deterministic witness behavior.

An activated profile must use the algorithm, signature input, authoritative keys, quorum, policy
lifecycle, rotation, revocation, and native receipt semantics established by E13. No algorithm is
inferred from NE3 or another evidence-tool contract.

P3.1 and evidence acquisition may not create or emulate an issuer, key, signer, registry, quorum, or
trust policy. When the signed profile is inactive, witness fields are absent.

## P3.1-05 — Intent and final roles

| Object | P3.1 role | Operational grant |
|---|---|---|
| EA0AuthorizationIntent | Non-authorizing EA0 intent | Never |
| L0ProbeContract | Intermediate binding the EA0 intent | Never |
| EA0AuthorizationManifest | Final EA0 content object | Only after native exact-root activation |
| EA1ExecuteAuthorizationIntent | Non-authorizing EA1 intent | Never |
| ProbeContract | Intermediate binding the EA1 intent | Never |
| L1RunManifest | Intermediate binding intent and exact contracts | Never |
| EA1ExecuteAuthorization | Final EA1 content object | Only after native exact-root activation |

The established final role names remain. The new intent schemas are version-distinct. A role name or
FINAL label alone grants nothing.

## Binding plan

Every intent declares an ordered binding plan. Each row contains at least:

- a unique slot;
- required artifact kind;
- topological rank or predecessor rule;
- required cardinality;
- stage and scope relation.

The binding plan fixes structure and order, but a slot never substitutes for a content root.

### P3.1-06 — Intermediate binding

Every intermediate:

- binds the exact intent content root;
- identifies its exact slot and kind;
- contains all semantic fields in its canonical payload;
- binds only lower-rank, already-existing intermediate roots;
- contains no direct or transitive reference to the later final.

### P3.1-07 — Exact final binding

Every final:

- binds the exact intent content root;
- contains the exact ordered complete array of slot, kind, and content root;
- matches the intent plan one-for-one;
- contains no missing, duplicate, additional, reordered, mistyped, or substituted object;
- cannot add a root, operation, tool, permission, network mode, cap, retention rule, or later-stage
  authority absent from the intent.

If mechanically complete binding cannot be decided, finalization fails closed.

## P3.1-08 — EA0 content DAG

    P3 and P3.1 specification roots plus exact policy leaves
        -> EA0AuthorizationIntent
        -> exact L0ProbeContract roots
        -> EA0AuthorizationManifest final content root
        -> native approval of exact final root
        -> full verification and single-use local claim
        -> L0
        -> SealedL0Packet and AcquisitionFeasibilityPacket

EA0AuthorizationIntent contains every semantic item that P3 assigns to EA0, including exact approved
specification roots, source-read roots and exclusions, source snapshot rules, sole output root,
permitted operations, tools, numeric caps, retention, issue and expiry, and prohibitions.

Every P3.1 L0ProbeContract binds EA0AuthorizationIntent.content_root and never the later
EA0AuthorizationManifest root. The final manifest binds the intent and the exact ordered complete
contract and intermediate roots.

## P3.1-09 — EA1-EXECUTE content DAG

    exact EA0 and L0 ancestors, feasibility packet, tool bundle, and execution leaves
        -> EA1ExecuteAuthorizationIntent
        -> exact ProbeContract roots
        -> exact L1RunManifest roots
        -> EA1ExecuteAuthorization final content root
        -> native approval of exact final root
        -> full verification and single-use per-run local claim
        -> L1 execution
        -> raw results and NEReports

EA1ExecuteAuthorizationIntent contains every semantic item that P3 assigns to EA1-EXECUTE, including
the exact L0 and feasibility packets, exact existing or sealed build packet, executable bytes,
dependencies, tools, oracle, expected outcomes, reason codes, caps, executable permissions, network
mode, retention, and ordered execution slots.

Every P3.1 ProbeContract binds the EA1 intent root. Every L1RunManifest binds the intent and its exact
ordered ProbeContract roots. Neither binds the later final. The final repeats the intent and every
exact ordered complete contract and manifest root.

## P3.1-10 — EA1-CONSTRUCT classification

EA1-CONSTRUCT remains governed by P3 unless an E8 inspection finds the same reverse-reference pattern.
If found, an additive construct intent is inserted before the affected intermediates and the existing
final construct authorization binds their exact roots. This phase rule grants no construction
permission and does not reopen the P4 architecture.

## P3.1-11 — Native exact-root activation

A completed final content object enters FINALIZED_NOT_AUTHORIZED. It enters ACTIVATED_FINAL only when
the pre-existing user or authority channel supplies verifiable native provenance for:

- the exact final content root;
- the exact stage;
- the exact scope or scope root;
- the authority-channel or profile identity;
- the native approval event or receipt identity, when exposed;
- native issue, expiry, revocation, or one-time scope semantics, when defined.

The verifier uses the channel native mechanism. P3.1 does not define, create, emulate, or locally
self-assert that channel.

Approval of an intent, document, draft, filename, logical ID, summary, earlier root, or different root
is invalid. Missing verifiable exact-root approval produces subordinate detail
AUTH_APPROVAL_ROOT_UNAVAILABLE and stops before effects.

The approval that authorized this document revision and debate is not operational activation and does
not approve any future intent, final root, stage, scope, root path, or cap.

## P3.1-12 — Required capability negotiation

Every P3.1 final payload declares the exact ordered required capabilities, including:

- p6.p3_1.core-content-dag.v1;
- sha256-jcs-p31;
- native-exact-root-approval with an exact profile ID;
- exact graph-order profile;
- exact local reservation and fencing profile;
- a signed-witness profile only when separately activated.

The executor verifies every capability before activation. It rejects:

- implicit P3-to-P3.1 conversion;
- P3.1-to-P3 downgrade;
- mixed legacy and successor graphs;
- fallback between proof profiles;
- filename, ID, or summary approval as a substitute for exact-root approval;
- treating an intent as a final;
- dispatch to an unverified legacy consumer.

## P3.1-13 — Graph verification

Define each semantic dependency edge as dependency to dependent. A conforming verifier:

1. strictly parses the final content envelope;
2. recomputes and compares its typed root;
3. loads the intent and every dependency by exact typed root;
4. recomputes every root and verifies each artifact role and schema;
5. rejects final backreferences from intermediates;
6. rejects duplicate roots that resolve to different bytes, kinds, or schemas;
7. verifies the binding plan one-for-one;
8. verifies non-widening, stage, scope, permissions, tools, caps, network, retention, and expiry;
9. computes canonical topological order;
10. validates native exact-root activation;
11. reapplies every inherited P3 prelaunch gate;
12. pins the verified canonical bytes and required object identities until the first effect.

Canonical ordering uses Kahn iteration:

- initialize the ready set with un-emitted vertices having no un-emitted dependencies;
- choose the minimum ready vertex by UTF-8 root profile, raw digest bytes, then UTF-8 artifact kind;
- emit it and remove its outgoing edges;
- repeat until empty;
- remaining vertices with an empty ready set are a cycle.

Identical references to the same canonical bytes and typed root are one vertex. A shared root resolving
to different bytes, kind, or schema is a hard collision. The verifier never selects one conflicting
candidate.

## P3.1-14 — Single-use local claim

EA0 is single-use per intent and exact sole output-run root. Each EA1 run slot is single-use per intent,
execution nonce, and exact run root. Multiple EA1 slots require distinct nonces, roots, and result
chains.

All finals for the same intent and run slot compete for the same claim because claim identity excludes
the final root.

The linearization point is the inherited local atomic reservation:

- EA0 atomically creates its exact new sole output-run root with fail-if-exists semantics;
- EA1 uses RUN_ROOT_ATOMICALLY_RESERVED for the exact declared run root.

An existing, colliding, ambiguous, stale, or consumed root is never deleted, emptied, renamed away,
reclaimed, taken over, or reused.

The winner create-new seals a downstream claim record that identifies the intent, slot, nonce, exact
requested and actual root identity, selected final content root, native approval reference, controller
or tool root, nonrenewable hard deadline, and available inherited fence mechanism.

## P3.1-15 — Fence boundary

Every effect remains inside an already available enforcement boundary:

- inherited fail-if-exists root reservation;
- retained local root handle, lock, object identity, and recheck;
- inherited P3 nonrunning-child, hard-control, final-object, actual-image, and launch-order mechanisms;
- target-native create-new, append-only, one-way publication, duplicate rejection, or fencing.

A check followed by an unfenced target operation is insufficient. If the inherited or target-native
mechanism cannot prevent a competing, duplicate, expired, or stale controller from crossing the
effect boundary, the capability is UNSUPPORTED_FOR_STRONG_CLOSURE and the stage does not begin.

P3.1 authorizes no authority registry, signer, key service, distributed lease, network coordinator, or
new fencing platform.

## P3.1-16 — Crash and retry

Root reservation is irreversible.

- A crash after reservation but before a complete claim leaves an uncertain consumed root.
- Loss before a proven first effect is retained as INCONCLUSIVE and is not resumed.
- Ambiguity before, during, or after an effect remains INCONCLUSIVE under inherited P3 no-resend rules.
- A restarted process cannot reconstruct executable authority from a claim or audit record.
- No claimed root, final, nonce, effect, or result chain is retried, resent, deleted, or reused.

Any later attempt requires a separately approved new intent, nonce, absent root, complete contracts and
manifests, and final authorization.

## P3.1-17 — Output closure

Every downstream sealed packet, raw result, and NEReport binds:

- the exact activated final content root;
- the exact intent content root;
- the canonical ordered complete ancestor-root list;
- the native exact-root approval reference;
- the claim and reserved-root identity;
- applicable effect ordinals and states;
- terminal ownership, loss, and uncertainty state.

When a conditional signed-witness profile is active, outputs additionally bind the exact witness and
policy snapshot roots required by that profile.

These roots record authority and consumption. They do not grant or widen either.

## P3.1-18 — Failure algebra

New graph, binding, canonicalization, approval, capability, schema, collision, claim, fence, witness,
and effect-ambiguity codes are subordinate detail only.

Every prelaunch failure retains the inherited top-level tuple:

    execution_state = NOT_STARTED
    outcome = INCONCLUSIVE
    reason_code = PRELAUNCH_CHAIN_MISMATCH
    decision_effect = LEAVES_NAMED_GAP_UNCHANGED

Post-effect uncertainty retains the inherited P3 INCONCLUSIVE and no-resend semantics. No successor
detail creates a fourth outcome, replaces a top-level reason, authorizes automatic retry, or implies a
next stage.

Exact subordinate code spellings beyond AUTH_APPROVAL_ROOT_UNAVAILABLE are fixed and tested through
E14 before an executable successor object can exist.

## Evidence gates

| Gate | Required before | Minimum purpose |
|---|---|---|
| E14 successor compatibility and root-carriage corpus | Producing or accepting an executable P3.1 schema or object | Canonical bytes, role mapping, capability negotiation, root carriage, no fallback, unchanged top-level tuple |
| E13 authorization-governance provenance | Activating any P3.1 final | Native channel owner, exact-root carriage, receipt, scope, time, revocation, verifier |
| E11 concurrent consumption and fencing conformance | EA0 or EA1 execution | Atomic claim, retained fence, crash, pause, collision, stale-worker exclusion |
| E10 signed-witness conformance | Activating a signed-witness profile only | Envelope equivocation, signature-set normalization, witness interoperability |
| E8 construct-cycle inspection | Changing P3.1 EA1-CONSTRUCT only | Determine whether the same reverse-reference pattern exists |

None of these evidence packets exists in this document-only action.

## Risk register

| Risk | Failure condition | Mitigation | Status |
|---|---|---|---|
| R1 cyclic binding | Intermediate and final roots depend on each other | Intent-only intermediate references and cycle rejection | Structurally mitigated |
| R2 canonical divergence | Implementations derive different successor bytes or roots | One strict profile and E14 corpus | Needs E14 |
| R3 incomplete binding plan | Applicable object is omitted from a supposedly complete final | Typed slots and refuse undecidable completeness | Needs E14 |
| R4 object drift | Verified bytes or identities change before effect | Retained handles and inherited rechecks | Needs E11 |
| R5 activation provenance | Native channel cannot prove exact final root | Fail closed | Needs E13 |
| R6 semantic approval error | Authority approves exact but unsafe content | Independent governance review | Open |
| R7 multiple finals or replay | One intent or run executes more than once | Shared local atomic claim and no takeover | Needs E11 |
| R8 hidden construct cycle | EA1-CONSTRUCT has an undiscovered reverse reference | E8 same-pattern inspection | Conditional |
| R9 legacy confusion | Intent or successor final is treated as a legacy object | Versioned roles and capability rejection | Needs E14 |
| R10 closure burden | Verification exceeds later approved caps | No action until exact caps cover preflight | Open |
| R11 witness retention | Conditional proof or policy snapshot is unavailable | Retain exact witness closure | Conditional E10 |
| R12 proof normalization | Signed-profile implementations disagree | Deterministic profile and corpus | Conditional E10 |
| R13 double execution | Same or competing final crosses effects twice | Single-use atomic claim | Needs E11 |
| R14 check-to-effect gap | Paused or stale controller acts after check | Continuous inherited or target-native fence | Needs E11 |
| R15 unproven cryptographic governance | Mandatory signing invents unsupported authority | Unsigned mandatory core | Signed profile needs E13 |
| R16 authority-construction conflict | Acquisition creates issuer, keys, or registry | Explicit prohibition | Structurally mitigated |
| R17 schema and name incompatibility | Legacy consumer misclassifies successor objects | Preserve final roles; distinct intents; no fallback | Needs E14 |
| R18 outcome-tuple drift | Detail code becomes a new top-level outcome or reason | Strict subordination | Needs E14 |

## Rejected and deferred choices

- Excluding a semantic backreference from the hash is rejected because it weakens exact binding.
- Mandatory Ed25519 or locally created signing governance is rejected.
- A distributed registry, lease, or fencing platform is rejected for this bounded scope.
- Legacy reinterpretation, upgrade, downgrade, and profile fallback are prohibited.
- Exact operational roots, caps, authority receipts, executable schema bytes, and targets are deferred.
- EA1-CONSTRUCT changes are deferred until E8 is applicable.

## Rollback and observability

Rollback is fail-closed non-activation: withhold successor executable artifacts and leave P3 and v1-v7
unchanged. Downgrade or legacy reinterpretation is not rollback.

Within inherited P3 caps and retention, later observability exposes typed roots, graph verification,
capability result, native approval reference, claim and reservation state, retained fence state, effect
ordinal and state, and the inherited top-level outcome tuple. Uncertain effects remain visible as
INCONCLUSIVE and never trigger retry.

## P3.1-19 — Current authority boundary

This written successor authorizes no intent creation, final manifest creation, root or cap selection,
acquisition, probe construction, execution, signing infrastructure, network action, L2 action, or
production mutation.

A future operational proposal requires a new exact authorization boundary after its applicable evidence
gates. No approval in the current debate or document-writing action can be reused for that purpose.

## Self-review

- The final-to-intermediate and intermediate-to-final content cycle is absent.
- All semantic fields are inside the canonical payload; the derived root is outside it.
- The mandatory core does not invent signing governance.
- Final role names are preserved while intent roles are distinct.
- Native approval is an external control-flow edge, never a content backreference.
- Existing P3 caps, network, outcomes, root isolation, and no-next-stage rules remain controlling.
- Single-use local claims reuse inherited reservation rather than a new coordination platform.
- New failures remain subordinate to the inherited tuple.
- E13, E14, and E11 remain blocking gates; E10 is conditional.
- No operational object or action is authorized.
