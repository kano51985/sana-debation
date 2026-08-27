# E14 N1 I1 remediation next-stage debate

Date: 2026-08-27

Disposition: **DEFER PENDING NAMED EVIDENCE**. This is a governance defer, not a technical
rejection. The gated sequential two-lane architecture is conditionally admissible, but no
operational tranche is authorized because the record does not establish the required actors,
current authority, or receipts.

## Trigger

The I1 remediation evidence phase closed with five `PASS`, two `INCONCLUSIVE`, and two `NOT_RUN`
results. Exact frozen-case behavior, repository-local routing, synthetic lifecycle behavior, I2
control, and rollback were reproducible. Obligation coverage and lifecycle authority remained
inconclusive; the real hermetic Node/Acorn diagnostic and dependency approval were not run.

The decision was whether to create a source-only v2 candidate first, obtain real toolchain and
governance evidence first, or use a gated two-lane sequence without allowing either lane to grant
authority to the other.

## Execution audit

- mode: `real-subagents/core`;
- Proposing TL: `/root/evidence_next_proposing`;
- Peer TL: `/root/evidence_next_peer`;
- Chief Architect: `/root/evidence_next_chief`;
- each role used a fresh, separately instructed thread;
- Peer and Chief initially received readiness-only contracts;
- Chief received the frozen evidence ledger and closed three-round record only after the rounds;
- one Chief scheduling attempt was retried after a core slot became available; no substantive
  material was delivered during the failed scheduling attempt;
- no optional role was created because the four-slot core budget was exhausted; and
- this establishes thread and instruction separation only, not cognitive independence.

## Frozen evidence ledger

- E1: commit `3d0cd1c` contains nine bundles and the remediation report.
- E2: 136 repository tests and deterministic evidence regeneration passed.
- E3: scanner, G1-v1, and failed-I1 hashes were immutable.
- E4: result split was five `PASS`, two `INCONCLUSIVE`, and two `NOT_RUN`.
- E5: the direct diagnostic blocked all 14 exact frozen cases without archive identity.
- E6: synthetic route, lifecycle, I2, and rollback models passed without live integration.
- E7: no real Node/Acorn diagnostic ran.
- E8: no v2 scanner existed and obligation coverage was incomplete.
- E9: real lifecycle roles and custody were unresolved.
- E10: no production consumer was found by repository mechanisms; external consumers remained
  unknown.
- E11: two synthetic G1 oracles agreed but issued no authority.
- E12: `toJSON` was present while runtime dispatch and reachability remained unresolved.
- E13: every remediation bundle was nonauthoritative and the prior Chief disposition was defer.
- E14: candidate admission was unresolved.
- E15: acquisition authority was unresolved.
- E16: lifecycle ownership was unresolved.

## Three-round record

| Round | Attack axis | Peer disposition | Binding correction |
|---|---|---|---|
| 1 | evidence validity and tautology | `modified` | Reduce the claim to `CANDIDATE_MODEL_INTERNAL_CONSISTENCY_OBSERVED`; type the detector as `LEXICAL_HEURISTIC`; keep semantic completeness unestablished and the external oracle not run; require independent candidate admission and a full evidence-frame manifest. |
| 2 | ordering and circular dependency | `modified` | Characterize the exact toolchain before freezing the design; derive the actual entry model independently; define terminal governance states and typed defect handoffs; allow at most one separately authorized successor. |
| 3 | acquisition, governance, operability, and authority | `modified` | Set acquisition, execution, and executable-candidate authority to zero; separate acquisition, execution, and candidate-admission receipts; prohibit execution of fixture/candidate source; require real lifecycle actors before any later stage. |

The Round 3 technical correction is binding: only the hash-pinned Node runtime, runner, and Acorn
closure named by an `ExecutionReceiptV1` may load or execute. Fixture and candidate source may be
read only as inert bytes and must never be imported, evaluated, compiled as executable code, or
executed. Package lifecycle and install scripts are prohibited.

## Binding conditional sequence

If future authority lifts the defer one stage at a time, the only admitted order is:

`G0 -> D0a -> C1a acquisition -> C1a qualification -> D0b -> C0 -> C1b -> Chief B`

1. G0 validates the real issuer, current-state provider, custodian, acquisition operator,
   execution operator, evidence sealer, and each actor's current scope. Its terminal states are
   established authority, `DENIED`, or `ISSUER_NOT_ESTABLISHED`.
2. D0a may create only separately authorized inert questions, exclusions, and fixture
   specifications.
3. C1a acquisition requires `AcquisitionReceiptV1` and admits only hash- and size-verified archives
   into quarantine.
4. C1a qualification requires its own one-run `ExecutionReceiptV1` and establishes behavior only
   for the exact pinned runtime, runner, Acorn closure, procedure, caps, and corpus.
5. D0b freezes `CandidateDesignContractV1`, independently derived
   `CandidateActualEntryModelV1`, and `CandidateEvidenceFrameManifestV1`.
6. C0 requires a separate source-creation instruction and independently issued
   `CandidateAdmissionReceiptV1` before any executable-form candidate identity exists.
7. C1b requires a new one-run `ExecutionReceiptV1`; the C1a receipt is not reusable.
8. Chief B classifies the evidence but cannot issue G1, I2, production, or generalized semantic
   authority.

Every transition requires both applicable user authority and its evidence gate. Evidence and
receipts do not substitute for user authority.

## Receipt and capacity rules

`AcquisitionReceiptV1` binds immutable endpoints, object/version identities, hashes, sizes,
complete closure, licenses, quarantine rules, and prohibition of installation or execution.
Redirects, drift, partial or extra objects, mismatches, unknown licenses, and missing fields fail
closed.

`ExecutionReceiptV1` authorizes exactly one offline run using the exact pinned Node runtime,
runner, Acorn closure, inputs, read-only mounts, procedure, and resource caps. Network, fallbacks,
plugins, additional runs, or any mismatch fail closed.

`CandidateAdmissionReceiptV1` independently binds the candidate identity and an exact capacity of
one or two. Effective capacity is zero until receipt issuance. Every executable-form identity
consumes capacity and is terminal; only one successor may be requested, and it remains separately
gated.

## Current authority boundary

The current task may record this decision only. It authorizes no G0 investigation, external actor
lookup, D0a artifact, network access, acquisition, install, dependency resolution, execution,
candidate source, test run, legacy or `src` change, G1, I2, productionization, deployment, or
issuance.

Legacy remains immutable. Internal agreement is not semantic completeness, language truth,
external-consumer applicability, or authority. Missing or conflicting actor data yields
`ISSUER_NOT_ESTABLISHED`; any later stage failure stops without silently widening claims or
advancing to the next stage.

