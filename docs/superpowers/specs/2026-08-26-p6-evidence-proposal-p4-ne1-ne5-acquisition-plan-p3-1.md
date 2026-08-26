# P6 evidence proposal P4/P3.1: authorization-DAG acquisition amendment

Date: 2026-08-26

Status: document-only companion to the P3.1 design successor. It does not create a machine schema,
authorization object, approval receipt, root, cap, probe, process, or evidence run.

## Purpose

Apply the approved P3.1 authorization-DAG rules to the existing NE1-NE5 acquisition sequence while
preserving every other P3 acquisition boundary.

The controlling predecessor acquisition plan has SHA-256:

    71801CBE28254FC71D8C2CEBE0B47740330CD6B165C5232FD032717BB8D390DA

The matching P3 design has SHA-256:

    9D72EF54012348523FB11D21728E9C827D106F9B73D8E6B17B57AF01367C90A2

Both remain unchanged.

## Authorization boundary

Current approval covers only this written amendment. It does not authorize:

- E14 fixture or executable-schema creation;
- E13 authority-channel integration;
- an EA0 intent, contract, or final manifest;
- any source read for acquisition;
- any L0 output;
- any EA1 construction or execution;
- E10 or E11 conformance execution;
- a signing key, issuer, registry, trust policy, or receipt;
- network, model, plugin, MCP, configuration, service, L2, or production action.

## Gate sequence

    approved P3.1 written successor
        -> separately authorized E14 compatibility and root-carriage work
        -> validated E14 packet
        -> validated E13 native exact-root authority provenance
        -> separately authorized exact operational proposal
        -> EA0AuthorizationIntent
        -> exact L0ProbeContracts
        -> EA0AuthorizationManifest final root
        -> native approval of that exact root
        -> graph, capability, approval, and local-claim verification
        -> E11-conformant single-use L0
        -> sealed L0 and feasibility packets
        -> existing P3 construction or execution gates

No stage implies the next. E10 is inserted only when E13 activates a signed-witness profile. E8 is
inserted only before a proposed P3.1 change to EA1-CONSTRUCT.

## E14 successor compatibility packet

E14 is blocking before producing or accepting any executable P3.1 schema or object.

Its separately authorized corpus must freeze:

- strict UTF-8 and RFC 8785 JCS cases;
- duplicate-name, invalid-Unicode, number-domain, timestamp, and digest rejection cases;
- exact sha256-jcs-p31 root carriage;
- EA0 and EA1 intent/final role mapping;
- exact binding-plan order and completeness;
- mixed P3/P3.1 graph rejection;
- no implicit conversion, downgrade, or profile fallback;
- required-capability negotiation;
- exact-root native approval carriage;
- complete ancestor-root carriage in downstream result schemas;
- unchanged inherited prelaunch tuple;
- subordinate detail-field placement;
- collision, cycle, type, and role rejection;
- display-only legacy projection that grants no authority, if such a projection is needed.

E14 may not synthesize authority. A conformance fixture proves encoding and rejection behavior only.

## E13 native authority provenance

E13 is blocking before any P3.1 final can activate.

It must identify:

- the existing authority channel and accountable owner;
- how the channel carries the exact final content root;
- how stage and scope are bound;
- the native approval event or receipt identity;
- issue, expiry, revocation, or one-time semantics;
- the verifier and verification input;
- provenance retention and audit access;
- whether a signed profile exists;
- proof that acquisition does not create the authority channel or its keys, issuers, registry, or
  trust policy.

If the channel cannot verifiably approve the exact final root, P3.1 activation remains unavailable.

## EA0 object construction order

After E14 and E13, a separately authorized operational proposal may construct objects in this order:

1. Freeze the exact approved P3 and P3.1 specification roots.
2. Freeze exact read roots, exclusions, snapshot algorithm, sole absent output-run root, permitted
   operations, tools, numeric caps, network NONE, retention, issue and expiry, and prohibitions.
3. Construct EA0AuthorizationIntent with grants_execution false and an ordered binding plan.
4. Compute its canonical sha256-jcs-p31 root.
5. Construct each exact L0ProbeContract against the intent root and declared slot.
6. Verify that every contract contains no final-manifest reference.
7. Construct EA0AuthorizationManifest against the intent and exact ordered complete contract roots.
8. Compute the final manifest root.
9. Present that exact final root, stage, scope, roots, caps, expiry, and prohibitions through the
   established native approval channel.
10. Keep the final FINALIZED_NOT_AUTHORIZED until exact-root provenance is verified.
11. Recompute the complete graph and required capabilities.
12. Require E11-conformant local atomic consumption before L0.

Creating the intent or final content does not authorize L0.

## L0 contract rule

Every P3.1 L0ProbeContract binds:

- the exact EA0AuthorizationIntent content root;
- its exact slot and kind;
- exact NE question and falsifier;
- exact read roots and exclusions;
- sole output root;
- allowed create-new or append-only operations;
- source snapshot rules;
- exact tool roots;
- artifact kinds;
- non-negative integer caps;
- retention and terminal seal;
- stable failure and inconclusive semantics.

It may bind only already-existing ancestors. It must not contain the later
EA0AuthorizationManifest content root.

## EA0 final rule

EA0AuthorizationManifest binds:

- the exact EA0AuthorizationIntent content root;
- the exact ordered complete slot, kind, and root array for every L0 contract and required
  intermediate;
- exact count and canonical list root;
- the same or narrower stage, scope, roots, operations, tools, caps, network, retention, expiry, and
  prohibitions;
- required P3.1 capabilities;
- no-automatic-next-stage.

It cannot add or widen a semantic field absent from the intent. It is not active until native approval
of its exact content root is verified.

## L0 prelaunch

Before the sole L0 run-root reservation or any output effect:

1. Verify E14 applies to the exact profiles.
2. Recompute the final and intent roots.
3. Load and recompute every contract and ancestor by exact typed root.
4. Reject cycles, backreferences, collisions, mixed schemas, type mismatches, and incomplete binding.
5. Compute canonical Kahn order.
6. Verify exact required capabilities.
7. Verify the native approval references the exact final root, stage, and scope.
8. Verify issue, expiry, caps, network, retention, and prohibitions.
9. Reapply every P3 L0 precondition.
10. Atomically create the exact absent output-run root with fail-if-exists semantics.
11. Create-new the downstream claim record before any further stage effect.

Any failure before reservation writes nothing. A failure after irreversible reservation retains the
consumed or uncertain root and never reuses it.

## Single-use L0 claim

EA0 is single-use per intent and sole output-run root. Every final for the same intent competes for that
root.

The claim identity contains stage, intent root, run slot, execution nonce, authorized parent, and exact
requested root. It excludes the final root so another final cannot escape the collision domain.

The winning claim record identifies the selected final root, native approval reference, exact actual
root identity, controller and tool roots, nonrenewable hard deadline, and available inherited fence.
It is an audit record, not authority.

No existing or abandoned root is deleted, reclaimed, or taken over.

## L0 effect boundary

Every L0 output effect must be handle-relative or otherwise continuously protected by:

- the retained exact root identity and available exclusive handle or lock;
- create-new, append-only, or absent-final publication semantics already permitted by P3;
- the selected final and claim identity;
- exact next effect ordinal and action contract;
- cap and deadline checks;
- target-native duplicate or stale-operation rejection when needed.

If an allowed effect cannot remain in such an inherited or target-native boundary, it is unsupported
and L0 does not begin. This amendment authorizes no new controller or fencing service.

## L0 crash states

- Reservation without a complete claim leaves an uncertain, permanently consumed root.
- A complete claim with no proven effect remains INCONCLUSIVE and is not resumed.
- An effect prepared but not provably observed remains INCONCLUSIVE.
- A restarted process may inspect under separate read authority but cannot continue the old claim.
- No effect is resent and no old intent, final, nonce, or root is reused.

A retry is a new separately authorized chain.

## Sealed L0 packet additions

In addition to every inherited P3 field, the packet binds:

- EA0AuthorizationManifest exact activated root;
- EA0AuthorizationIntent exact root;
- canonical ordered complete ancestor roots;
- native exact-root approval reference;
- required capability result;
- claim and requested and actual root identity;
- ordered effect states;
- terminal ownership, loss, or uncertainty state.

Conditional witness and policy roots appear only if a signed profile was activated under E13 and E10.

## EA1-EXECUTE object order

After the inherited feasibility and tool gates:

1. Freeze exact EA0, L0, feasibility, tool, oracle, expected-result, cap, network, retention, and
   execution leaves.
2. Construct EA1ExecuteAuthorizationIntent with grants_execution false and exact run slots.
3. Construct each ProbeContract against the EA1 intent root.
4. Construct each L1RunManifest against the intent and exact ordered ProbeContract roots.
5. Verify no intermediate references the later final.
6. Construct EA1ExecuteAuthorization against the intent and every exact ordered complete intermediate
   root.
7. Obtain native approval of that exact final root, stage, scope, and run slots.
8. Verify the full graph and each required capability.
9. Require E11 before any run.
10. Atomically reserve each exact run root before its first effect.

Each run slot has a distinct nonce, root, and result chain. Reusing the final does not create another
attempt.

## EA1 prelaunch preservation

The P3 ordered execution-identity sequence remains controlling after P3.1 activation and claim:

    CHAIN_VERIFIED
      -> RUN_ROOT_ATOMICALLY_RESERVED
      -> HARD_CONTROLS_ARMED
      -> EXECUTABLE_FINAL_OBJECT_BOUND
      -> CHILD_CREATED_NONRUNNING
      -> ACTUAL_IMAGE_INITIAL_MODULES_VERIFIED
      -> KEY_INPUT_PUBLISHED
      -> RUNNING

P3.1 does not remove, reorder, or weaken any transition. Unsupported local or target-native fencing
prevents the run from starting.

## EA1-CONSTRUCT

No construct-phase object changes in this amendment. Before any future P3.1 construct change, E8 must
inspect the exact contracts for a reverse reference. Only the same intent/intermediate/final repair is
allowed, and it grants no construction permission.

## Failure and outcome preservation

All new successor details are subordinate.

Before launch, every graph, binding, approval, schema, capability, claim, or fence failure returns:

    execution_state = NOT_STARTED
    outcome = INCONCLUSIVE
    reason_code = PRELAUNCH_CHAIN_MISMATCH
    decision_effect = LEAVES_NAMED_GAP_UNCHANGED

AUTH_APPROVAL_ROOT_UNAVAILABLE is the one currently fixed successor detail name. E14 freezes all
remaining exact detail spellings and encodings before executable objects.

Post-effect ambiguity uses inherited P3 INCONCLUSIVE and no-resend semantics. A subordinate detail can
never become a new outcome, replace the top-level reason, or authorize retry.

## E11 execution gate

E11 is blocking before EA0 or EA1 execution. Its separately authorized conformance work must cover:

- two workers presenting the same final;
- two finals for the same intent and slot;
- pause after claim validation;
- root collision;
- crash before claim completion;
- crash after claim but before a proven effect;
- crash around an effect;
- stale-worker resumption;
- owner-loss takeover attempt;
- duplicate effect ordinal;
- unsupported target fencing.

For every permitted effect surface, at most one contender may cross. Any double effect, stale
continuation, root reuse, takeover, or silent retry falsifies the mechanism.

## NE1-NE5 preservation

The P3 NE1-NE5 questions, admissibility classes, maximum claims, dependencies, outcomes, decision
effects, early-stop behavior, and fresh-Chief gate remain unchanged.

P3.1 evidence can establish only authorization-graph and local-consumption conformance. It cannot
upgrade local evidence to deployed compatibility, real integration, actual authority receipt,
production isolation, nonforkable history, cognitive independence, or authoritative price.

## Combined packet and Chief handoff

A later combined packet includes the complete P3.1 activation and claim closure without replacing any
P3 artifact:

- predecessor and successor specification roots;
- intent, contract, manifest, and final roots;
- native approval provenance reference;
- capability and graph-verification results;
- local claim and effect state;
- every inherited L0, feasibility, construction, execution, raw, blocked, adverse, and NE root;
- unchanged outcome and decision effect;
- risks and limitations.

The compiler cannot activate, approve, omit adverse roots, reconstruct a missing seal, relabel an
outcome, widen a claim, or infer a missing authority channel.

## Stop rules

- Stop before executable successor objects without E14.
- Stop activation without E13 and native exact-root provenance.
- Stop execution without E11.
- Stop a signed profile without E10.
- Stop construct-phase modification without applicable E8 inspection.
- Stop on any graph cycle, backreference, collision, mixed schema, incomplete binding, unsupported
  capability, approval mismatch, root collision, lost fence, or uncertain effect.
- Preserve every adverse or uncertain root.
- Never widen roots, caps, process, network, system, or production scope automatically.

## Document-only next boundary

The next eligible work after this transcription is separately authorized E14 conformance design and
read-only fixture planning. This document does not authorize that work.

No operational manifest, root, cap, tool invocation, probe, or execution may be inferred from this
written amendment.

## Self-review

- EA0 and EA1 intermediates bind intents, not later finals.
- Final objects bind exact ordered complete intermediate roots.
- Exact-root native approval is required after final hashing.
- Hashing does not self-authorize.
- Mandatory signing governance is absent.
- Local claim and fencing reuse inherited mechanisms only.
- New failure details do not change the P3 evidence algebra.
- E14, E13, and E11 remain blocking in their declared order.
- P3 NE1-NE5 scope and claims remain unchanged.
- No current operational authority exists.
