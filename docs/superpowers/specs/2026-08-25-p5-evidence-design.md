# P5 provenance-preserving adaptive protocol evidence design

Date: 2026-08-25  
Status: approved for evidence-package implementation by the user's continuation after the P5 Chief
debate. Installed skill and production systems remain out of scope.

## Decision

Publish the P5 evidence behavior as `adaptive-axes-v2/schema-1`. Do not change the behavior or wire
meaning of `adaptive-axes-v1/schema-1`. The P5 worker materiality contract is
`baseline-delta-ledger-v1`.

The design implements the Chief's revised A+B P3:

- retain an immutable literal baseline B0;
- admit every non-identical B0-to-P0 delta before semantic classification;
- require Peer attestation for every delta candidate;
- route decision-relevant and uncertain candidates through substantive cycles;
- retain resolved findings terminally with stable identity and provenance;
- reject final-proposal inference as proof of detection;
- allow zero cycles only when complete-diff reconciliation finds no supplied/verified material
  conflict and every non-relevant delta is Peer-attested;
- fail closed at authoritative publication when a required consumer, projection, receipt, or epoch
  is invalid.

## Decomposition

### 1. Deterministic core

`src/p5_protocol.py` owns baseline capture, delta admission, stable candidate/finding identity,
cycle eligibility, terminal reconciliation, projection parity, authority receipts, and epoch
rollback validation. It has no model or network dependency.

All functions return deterministic records or raise stable `P5ProtocolViolation` codes. Missing
telemetry or evidence never becomes a zero or an empty approval.

### 2. Canonical schemas and fixtures

`schemas/adaptive-axes-v2.schema.json` defines the full normative P5 run. The existing E6 worker
uses a smaller `eval/e6_run_output_p5.schema.json` that still exposes B0, all delta candidates,
stable terminal findings, cycle accounting, and Chief disposition.

Golden and adversarial fixtures cover:

- F2-style preemptive repair retained as a resolved baseline-delta finding;
- supplied behavior change with unknown severity routed as uncertain, never duplicate;
- F3 clean and editorial-only zero-cycle paths;
- classification exclusion, missing Peer attestation, missing candidate/finding links;
- unjustified batching, generic response, copied/unsupported closure;
- identity collision and replay stability;
- projection loss/non-injectivity;
- unknown, stale, bypassing, unacknowledged, and receipt-mismatched authority routes;
- future-epoch rollback and immutable historical interpretation.

### 3. Versioned live prompt

`eval/build_e6_prompt.py` gains `adaptive-axes-v2` and `baseline-delta-ledger-v1` as explicit opt-ins.
Legacy defaults remain unchanged. The P5 prompt treats `initial_proposal` as literal B0 and requires
the Proposing TL to declare every behavioral B0-to-P0 change before Peer activation.

The live gate runs fresh real-subagent workers and protocol-blinded graders:

- F2-noisy P5 adaptive must detect both gold issues with specificity 1.0;
- F3-short and F3-noisy P5 adaptive must use zero cycles, produce no terminal findings, and receive
  clean consistent dispositions;
- host audits must verify three distinct `fork_turns=none` core threads and protocol-defined Chief
  exposure.

## Canonical data flow

`B0 capture -> P0 -> mechanical delta admission -> semantic classification -> Peer attestation ->
finding admission -> cycle routing -> per-finding closure -> terminal reconciliation -> canonical
artifact -> authority projection/receipt validation`

A proposer may improve P0, but cannot suppress, classify finally, or close its own delta. A grader
counts detection only from explicit stable terminal findings.

## Compatibility and authorization

V1 consumers must reject V2 artifacts unless they explicitly negotiate an injective projection.
Projection must preserve detected finding IDs, disposition, approval semantics, and accepted/open
risk meaning. Rollback creates a new future authority epoch and never rewrites issued artifacts.

This package creates only local reference code, schemas, fixtures, tests, and fresh evaluation
artifacts. It does not modify the installed skill, register real consumers, deploy an authority
gate, or authorize production behavior.

## Self-review

- No placeholders or unstated implementation choices remain.
- Behavioral versioning is separated from legacy compatibility.
- Deterministic core, authority model, and live evaluation are independently testable.
- The design preserves both required asymmetric outcomes: F2 detection and F3 zero-cycle clean
  behavior.
