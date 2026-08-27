# Debate protocol

These are semantic contracts; Markdown is acceptable. Stable IDs and traceable relationships are
required.

## Decision frame

Freeze once before candidate dispatch:

- Decision and boundary
- Invariants I1...
- Constraints C1...
- Attack axes A1, A2, A3
- Uncertain assumptions U1...

Do not rename axes after seeing rebuttals.

## Routing manifest

Record:

- mode: `core`, `comparative`, `specialist-assisted`, or combined;
- reason and user-requested breadth, if any;
- optional role, bounded question, and possible decision effect;
- distinct prompt/tool/evidence/policy contract;
- allowed and withheld inputs;
- prompt mechanism: custom/developer profile or fresh-thread explicit contract;
- context labels such as `P0_NOT_PROVIDED` or `P0_EXPOSURE_REQUIRED`;
- thread-budget kind: active, lifetime/static, or unknown;
- startup protocol and state: `core-two-phase-v1` plus `PREPARING`, `PREPARED`, `RUNNING`,
  `WAITING_FOR_CORE_CAPACITY`, or `ABORTED_PARTIAL_EXPOSURE`;
- reserved Proposing TL, Peer TL, and Chief thread identifiers/status;
- one readiness receipt per prepared core role and the observed COMMIT point;
- optional job limit, retry limit, merge checkpoint, and fallback;
- skipped, failed, retried, blocking, or late optional work.

Default optional budget is one Alternative Architect plus one evidence/domain specialist. Reserve
all three core identities before optional dispatch or substantive exposure. When lifetime quota is
unknown, create all three with readiness-only contracts and wait for every receipt before activating
Proposing TL. If optional capacity is absent, emit `OPTIONAL_THREAD_BUDGET_UNAVAILABLE` and continue
core-only. Do not redispatch after a thread-limit rejection without an observed quota increase. Late
artifacts are audited but excluded after the merge checkpoint unless a predeclared
invariant-blocking evidence wait remains within its maximum.

## Core startup transaction

Every run uses `core-two-phase-v1` before P0.

```text
PREPARING
  -- all three fresh readiness receipts --> PREPARED
PREPARED
  -- activate Proposing TL with frozen substantive packet --> RUNNING
PREPARING
  -- core thread unavailable --> WAITING_FOR_CORE_CAPACITY
PREPARING or PREPARED
  -- substantive exposure before COMMIT --> ABORTED_PARTIAL_EXPOSURE
```

Readiness packets contain only role contract, protocol/schema tuple, and readiness request. A
readiness receipt identifies the role and created thread and confirms that no decision frame,
evidence ledger, candidate, rebuttal, verdict, or preference was provided. Manager intent, an active
slot count, or a successful first/second spawn is not a receipt for the missing role.

`WAITING_FOR_CORE_CAPACITY` is a non-running capacity state, not `CORE_ROLE_FAILED` and not a debate
result. The manager stops dispatch, reports the missing role and observed quota error, and performs
no blind retry. A later attempt requires an observed capacity/quota change and a new run with three
fresh roles. Partially prepared threads are never promoted or reused.

Any substantive exposure before all three readiness receipts is a protocol breach. Mark
`ABORTED_PARTIAL_EXPOSURE`, interrupt unfinished substantive work, exclude every exposed artifact,
and require a wholly fresh run. Never reconstruct PREPARED by deleting or hiding the exposure.

### DebateContinuationPacketV1

On `WAITING_FOR_CORE_CAPACITY` or `ABORTED_PARTIAL_EXPOSURE`, emit a compact continuation packet in
the response. Persist it only when file mutation is otherwise authorized. It contains:

- schema `sana.debate-continuation.v1` and startup protocol `core-two-phase-v1`;
- failed run ID and terminal startup state;
- SHA-256 identities for the frozen frame, evidence ledger, and routing manifest;
- each core role's `READY`, `THREAD_LIMIT_REACHED`, or `NOT_ATTEMPTED` status and observable thread
  identifier when one exists;
- every role that received substantive exposure;
- `substantive_artifacts_admissible=false`; and
- resume requirements: new run, three fresh core threads, revalidated frozen hashes, no partial-role
  reuse, and an observed capacity change before retry.

The packet is a handoff checksum, not a reservation, authority receipt, role output, P0, rebuttal,
or Chief decision. A resumed manager validates the hashes against current inputs, records the parent
run ID, then repeats PREPARE from zero. Hash drift requires a new frame rather than silent resume.

## Evidence ledger

Each entry contains ID, class (`verified fact`, `inference`, `product preference`, or `unresolved
risk`), claim, inspectable source, and limitations. Only verified facts receive factual-source
assertions. Repetition does not upgrade an inference.

## Candidate records

P0 and optional X0 include mechanisms, boundaries, data/control flow, contracts, typed failures,
invariants, compatibility/migration, rollback/observability, resource effects, risks, and evidence.

X0 additionally records its search contract and context-exposure label. It is called a `second
candidate`, not cognitively independent. Peer TL records one run-local classification:

- `CAUSAL_DIVERGENCE_OBSERVED` with a mutually exclusive decisive commitment and different failure
  implication;
- `ALT_DIVERSITY_UNPROVEN`;
- `ALT_ISOMORPHIC`.

Surface component differences alone do not establish causal divergence.

## Proposal versions

Use P0, P1, and so on. Every revision includes the changed mechanism and a diff from the prior
version. A prose promise without behavioral or contract change is not a new version.

## Specialist artifacts

Evidence Scout artifacts propose sourced ledger entries with limitations. Domain Specialist
artifacts state scope, applicable invariants, mechanisms, counterexamples, evidence uncertainty,
and required gates. Specialists never mutate candidates or choose verdicts. Any artifact affecting
the debate is routed unchanged to both core debaters and included in the Chief packet.

## Round record

Each of three records contains round/axis, proposal version, mechanism, rebuttal, failure trace,
falsifier, itemized Proposing TL responses, diff/risk update, Peer closing assessment, verdict, and
evidence/risk IDs. Reject a packet missing a counterexample, falsifier, response status, or traceable
outcome. A round closes only after Peer verification.

## Risk register

Each risk contains ID/origin, failure condition, affected invariant, impact, evidence/uncertainty,
detection, mitigation, rollback, and status (`open`, `mitigated`, `accepted by named product
preference`, or `needs evidence`). Do not invent numeric likelihoods. A risk is mitigated only by a
current mechanism or cited evidence.

## Chief decision gate

The fresh Chief receives no preferred outcome and chooses exactly one disposition. Include a trace
matrix:

`Decisive issue | Evidence/artifact IDs | Round/verdict | Proposal change | Residual risk | Decision effect`

Approve only when no unresolved risk can violate an invariant. Use required changes for a viable
architecture with explicit pre-implementation gates, reject for structural contradiction, and defer
when named evidence is necessary. The root cannot change the disposition.

## Execution audit

Begin the final response with:

- mode: `real-subagents` plus routing mode;
- every required and optional thread identifier/name and status;
- lifetime/static quota preflight and core thread reservations;
- prompt mechanism and observable context-exposure labels;
- candidate classification when present;
- skipped, failed, retried, blocking, or late optional artifacts;
- retries and protocol failures.

Never fabricate identifiers or isolation claims.

## Behavioral invariants

A valid run requires:

1. three distinct substantive core threads;
2. no missing role authored by root;
3. every round has counterexample, falsifier, response, closing assessment, and verdict;
4. changes appear as diffs or risk updates;
5. the Chief is fresh and receives the completed valid record;
6. the disposition is evidence-traceable;
7. missing critical evidence causes deferral, not invented certainty;
8. every invoked optional role exists in a separate thread and stays within its contract;
9. all three core roles complete readiness-only PREPARE before Proposing TL receives substantive
   material or any optional role is dispatched;
10. optional failure, lateness, or static quota consumption cannot prevent the prepared core from
    completing;
11. capacity failure produces a non-authorizing continuation packet and no partial-role reuse; and
12. prompt/thread separation is never reported as proof of cognitive independence.
