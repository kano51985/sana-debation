# P6 evidence proposal P4: NE1-NE5 acquisition plan

Date: 2026-08-26

Status: acquisition design for user review. No probe, worker, fixture, schema, key, journal, or runtime
artifact has been created by this plan.

This document plans the named evidence required by the Chief before the P4 minimum slice may enter
implementation. It does not authorize the evidence acquisition itself.

## Objective

Produce a bounded, traceable packet for:

- **NE1:** corpus and worker provenance;
- **NE2:** Windows closure capability;
- **NE3:** canonicalization differential behavior;
- **NE4:** slice burden and decision advancement;
- **NE5:** positive/negative control validity.

Each item ends independently as `PASS`, `FAIL`, or `INCONCLUSIVE`. Missing, ambiguous, or unsupported
evidence never becomes a pass. The combined packet goes to a fresh Chief before any minimum-slice
implementation decision.

## Authorization boundary

The current authorization covers this written plan only.

A later evidence-acquisition authorization must state:

- allowed filesystem roots, all inside the existing `outputs` tree;
- allowed read-only source roots;
- whether bounded subprocesses and loopback-only denial probes are allowed;
- maximum files and bytes scanned;
- maximum process count, wall time, CPU time, working set, and written bytes;
- whether throwaway contract implementations may be created for differential tests;
- permitted cleanup and retention behavior;
- prohibited system, plugin, MCP, network, credential, and production mutations.

If any required numeric cap or permission is absent, the affected probe does not start.

## Evidence action levels

Every planned action is assigned one level:

- **L0 — read-only inventory:** hash and inspect approved existing files and structural metadata.
- **L1 — bounded evidence probe:** create synthetic inputs and outputs under a dedicated run directory,
  launch bounded local subprocesses, and retain the result. Requires separate authorization.
- **L2 — retained slice implementation:** create production-quality P4 components. Not part of this plan
  and forbidden until fresh Chief and user approval.

L1 output is evidence, not automatically reusable implementation. Reuse later requires review against
the approved implementation plan.

## Common packet rules

Every NE item records:

- evidence item and run ID;
- source path or logical source ID;
- source hash and acquisition-command hash;
- start/end time and declared local clock;
- authorization and resource-cap hashes;
- stdout/stderr sizes and exit status;
- expected and actual stable outcome;
- limitation and uncertainty fields;
- immutable output manifest and content root.

No private key, secret value, conversation body, real holdout, or real oracle content enters the packet.
Synthetic canaries are used wherever leak behavior must be tested.

## NE1 — Corpus and worker provenance

### Question

Can every v1-v7 compatibility claim be traced to an inspectable, byte-frozen source, and can the
legacy-contract worker be shown structurally separate from the current parser without claiming
cognitive or deployed independence?

### L0 acquisition

Inventory all candidate v1-v7 schemas, fixtures, generators, expected hashes, and compatibility tests
inside the approved evidence-package scope. For each candidate record:

- declared version and contract source;
- current absolute and relative path;
- raw byte length and SHA-256;
- existing canonical hash and the code/test that establishes it;
- creation or derivation source when inspectable;
- semantic expectation and responsible test;
- whether the artifact has a complete provenance chain or only a current-file hash.

The package is not a Git repository, so a commit identifier must not be invented. Files lacking a
traceable derivation are explicitly `PROVENANCE_INCOMPLETE` even when their current hash is known.

### L1 acquisition

Create a frozen public legacy-contract packet containing only the historical schemas, byte fixtures,
expected interface, and permitted standard dependencies. A separately constructed worker source tree:

- may read only that packet;
- may not import the current producer, current consumer, shared parser, shared normalization code, or
  their source directories;
- receives unchanged raw bytes, not a P6-normalized representation;
- emits a validation-only result through the proposed transport boundary;
- records source, dependency, command, and input-contract hashes.

Separate source trees and instructions establish implementation separation, not cognitive independence.
The worker is called `legacy-contract worker`, never a deployed legacy consumer.

Use synthetic canaries to prove that private-key, holdout, oracle, sibling-worker, and aggregate-result
locations are absent from the worker input manifest and observable outputs.

### Required artifacts

- `CorpusProvenanceManifest` for every v1-v7 entry;
- `CorpusGapReport` for missing origin, derivation, or expected-hash evidence;
- frozen legacy-contract input manifest;
- legacy worker source/dependency/command manifest;
- prohibited-import and input-mount report;
- byte/hash comparison report;
- synthetic secret-custody report.

### Outcome

`PASS` requires complete provenance for every claimed fixture, byte-exact input, stable expected hashes,
no prohibited code dependency, and no synthetic secret exposure.

`FAIL` applies to a changed byte/hash, prohibited import, or actual synthetic secret leak.

`INCONCLUSIVE` applies when current hashes exist but historical provenance, worker separation, or custody
cannot be established. Inconclusive NE1 blocks the v1-v7 completeness claim and minimum-slice
implementation unless a fresh Chief explicitly narrows the corpus.

## NE2 — Windows closure capability

### Question

Can the local Windows environment observe or deny every operation required for
`EXECUTABLE_SLICE_CLOSURE_COMPLETE`, including final-object substitution and monitoring event loss?

### Capability matrix

For each edge, record `observe`, `deny`, `identify final object`, `detect loss`, required privilege,
mechanism, positive control, negative control, and limitation:

- executable/interpreter/module load;
- descendant process creation;
- inherited handle and artifact-handle exposure;
- named pipe and other declared IPC;
- network and loopback socket creation;
- file read and artifact-capable file sink;
- stdout/stderr and receipt-spool output;
- path alias, hard link, symbolic link, junction, and other reparse behavior;
- file replacement between preflight and launch;
- monitor buffer overflow, dropped event, or monitor termination.

Candidate native mechanisms may be evaluated, but none is assumed sufficient in advance. The probe must
name the actual Win32, job-object, tracing, sandbox, or runtime control used and its privilege boundary.
A source-only import graph or worker self-report cannot prove OS-observed closure.

### L0 acquisition

- identify available non-admin and approved host mechanisms;
- inspect current process identity, filesystem type, and path/reparse semantics without modifying them;
- record which required primitives have no available observation or denial mechanism;
- freeze the proposed final-object identity tuple and path-normalization rules.

### L1 canaries

Under a dedicated synthetic tree, attempt:

1. an omitted helper load;
2. redirected alias or reparse target;
3. replacement after preflight but before launch;
4. late executable/module load;
5. undeclared child process;
6. undeclared named-pipe/IPC edge;
7. loopback-only socket creation when explicitly authorized;
8. undeclared file sink;
9. intentional monitor termination or event-pressure condition.

Each canary specifies whether it must be blocked before artifact availability or detected after
publication and converted to `INCONCLUSIVE`. Artifact data is synthetic.

### Required artifacts

- Windows capability and privilege matrix;
- final-object and reparse resolution report;
- clean trace with zero unmatched edges;
- per-canary expected/actual outcomes;
- monitor source/configuration hash;
- event-loss accounting report;
- explicit list of unobservable or non-deniable primitives.

### Outcome

`PASS` for the stronger closure claim requires every necessary edge to be observed or denied, every
positive control to be detected, no unexplained event loss, and all canaries to produce the frozen
fail-closed outcome.

`FAIL` applies to unexpected artifact exposure, silent unmatched edge, alias substitution, or missed
positive control.

`INCONCLUSIVE` applies when a required edge cannot be observed/denied or loss cannot be distinguished
from zero events. P4 may still use `DECLARED_SLICE_COMPLETE`; it may not emit
`EXECUTABLE_SLICE_CLOSURE_COMPLETE`.

## NE3 — Canonicalization differential

### Question

Do every signing and verification path produce byte-identical canonical records and domain-separated
signature inputs for valid data, and identical typed rejection for invalid data?

### Specification freeze

Before L1 execution, freeze:

- `canonical-json-v1` byte rules;
- NFC normalization policy;
- key ordering;
- integer range and representation;
- null, empty object/list/string, and boolean behavior;
- duplicate-key, float, NaN/Infinity, invalid Unicode, unknown-field, and oversize rejection;
- length framing and hash preimages;
- distinct domain tags for owner, issuer/gate, consumer receipt, journal, checkpoint, history, and bundle;
- Ed25519 public-key and signature encoding.

Historical payloads are excluded from P6 JSON canonicalization. They remain raw bytes and retain their
existing canonical-hash rules from NE1.

### Vector set

The vector corpus covers:

- ASCII and multilingual NFC-equivalent strings;
- Unicode key-order boundaries;
- minimum/maximum permitted integers and rejected overflow;
- all empty/null/boolean forms;
- alternate whitespace and object member order;
- duplicate keys and malformed UTF-8/UTF-16 boundary input;
- forbidden numeric forms;
- unknown and oversize fields;
- cross-domain replay of a valid signature;
- predecessor, unresolved-set, checkpoint, key-transition, and artifact-identity records;
- truncated or altered journal frames.

### L1 execution paths

Run vectors through the issuer/gate path, current worker, legacy-contract transport path where applicable,
history/checkpoint writer, and independent public verifier. Implementations may share a reviewed crypto
library but not application record-building code or private keys.

### Required artifacts

- frozen vector manifest and expected bytes/outcomes;
- per-implementation source/dependency hashes;
- canonical byte and signature-preimage report;
- malformed-input typed-rejection matrix;
- domain-separation replay report;
- independent-verifier result.

### Outcome

`PASS` requires byte-identical valid encodings and preimages, expected typed rejection for every invalid
vector, and rejection of every cross-domain signature replay.

Any valid-vector divergence, accepted invalid vector, or accepted cross-domain signature is `FAIL` and
invalidates the proposed integrity claim.

Unavailable implementation paths or an incomplete vector family produce `INCONCLUSIVE` and block the
replay/receipt slice.

## NE4 — Slice burden and advancement contract

### Question

What does the bounded evidence work consume, and which named gap can each output actually change?

### Existing evidence separation

Retain the prior native-run derivative separately:

| Run | Input | Output | Cached-input subset | Reasoning output | Total | Turns | Summed turn duration |
|---|---:|---:|---:|---:|---:|---:|---:|
| F2 | 181,713 | 14,340 | 148,224 | 9,648 | 196,053 | 9 | 424,246 ms |
| F3-short | 110,140 | 1,120 | 102,912 | 588 | 111,260 | 6 | 63,478 ms |
| F3-noisy | 110,106 | 1,304 | 103,936 | 735 | 111,410 | 6 | 97,736 ms |

These values are not P4 harness cost, and summed turn duration is not wall time. Cached input is a subset
of input and is not added again.

### L0 acquisition

- hash the named SQLite and rollout sources and the numeric-only extraction logic;
- map every proposed case to the binding admissibility classification;
- define whether its result closes, narrows, leaves unchanged, or invalidates the named gap;
- identify which monetary inputs are absent.

### L1 measurements

For every evidence probe record:

- wall time and process CPU time;
- peak working set where the approved mechanism can measure it;
- process and attempt counts;
- files and bytes scanned;
- input, payload, journal, spool, receipt, stdout/stderr, and final-output bytes;
- verifier time and evidence-compilation time;
- failure and retry count, with retries forbidden for ambiguous delivery;
- cap consumption and first exceeded cap.

The evidence authorization provides hard numeric caps. Cap breach stops the probe and records a failure;
the probe may not expand its own budget.

### Advancement matrix

For each case emit:

`gap -> admissibility class -> artifact -> actual result -> closes/narrows/unchanged/invalid -> residual risk`

The three real-integration gaps remain unchanged by local evidence. Cost remains `COST_UNAVAILABLE`
without an authoritative provider/model/date/rate source and traceable rate mapping.

### Required artifacts

- sanitized prior-native telemetry derivative with provenance;
- per-probe resource ledger;
- cap and stop report;
- `DecisionEffectMatrix`;
- external-pricing limitation record;
- recommendation for later slice numeric caps, clearly labeled as evidence-derived product input rather
  than an already approved budget.

### Outcome

`PASS` requires complete measurements within authorized caps and at least one Chief-admissible gap that
the packet can demonstrably narrow.

`FAIL` applies to cap bypass, missing required measurement presented as zero, mixed prior/P4 totals, or
unsupported monetary cost.

If all technical measurements succeed but no named gap narrows, the result is
`STOP_DECISION_GATE_NON_ADVANCEMENT`, not a request to build more components.

## NE5 — Positive and negative control validity

### Question

Can the evidence system distinguish a real absence of forbidden data from a scanner that failed to
observe anything, and can expected-negative fault cases remain isolated from the clean case?

### Canary families

Generate unique, synthetic, per-run canaries for:

- holdout location;
- oracle location;
- sibling consumer key location;
- forbidden aggregate-result location;
- prohibited environment value;
- safe positive-control output.

Canaries contain no real secret or user data. Their plain values are confined to the acquisition work
area; manifests and final evidence may retain hashes and detection locations.

### Run isolation

- clean, positive-control, and each expected-negative case use different run and attempt IDs;
- each has a separate working directory, receipt spool, journal segment, manifest, and terminal status;
- a poisoned or inconclusive fault lineage cannot become the clean lineage;
- expected negative outcomes pass only when the exact frozen reason code is observed;
- compiler output reports clean validity and canary/fault-test validity separately.

### L1 execution

1. Run the safe positive control and require the scanner to identify its exact location.
2. Run the clean case and require zero forbidden-canary detections.
3. Place each forbidden canary only in its prohibited synthetic location and demonstrate that it is not
   present in consumer input manifests, receipts, stdout/stderr, journals, temporary outputs, or bundle.
4. Inject one deliberate forbidden-canary copy into an isolated negative output and require detection.
5. Execute the selected ambiguous-recovery negative case and verify it cannot contaminate clean status.

### Required artifacts

- canary generation and hash manifest;
- scanner source/configuration hash;
- positive-control detection report;
- clean negative scan;
- deliberate-leak detection report;
- run-directory and lineage-isolation report;
- expected-negative reason-code matrix;
- final control-validity status.

### Outcome

`PASS` requires detection of the safe positive control and deliberate leak, zero forbidden canaries in
the clean outputs, and complete run isolation.

A missed positive control, missed deliberate leak, or clean-output leak is `FAIL`.

Unavailable scan coverage, ambiguous run separation, or an unobservable output channel is
`INCONCLUSIVE`; a zero-result scan under those conditions cannot support a DLP claim.

NE5 proves bounded leak detection behavior only. It does not prove OS/network access prevention.

## Dependency and execution order

```text
NE1 L0 corpus inventory
       |
       +----> NE1 L1 worker separation
       |                |
       |                v
       +-----------> NE3 canonical differential

NE2 L0 capability survey ---> NE2 L1 closure canaries

NE4 L0 source/effect map ----> authorization caps ----> all L1 measurements

NE5 control design ----------> runs alongside authorized L1 probes

NE1-NE5 immutable packet ----> fresh Chief re-review
```

NE1 corpus identity precedes NE3 historical/hash vectors. NE2 determines whether the stronger closure
status is even available. NE4 caps every L1 action. NE5 accompanies, rather than follows, the actions it
is intended to validate.

## Combined packet and fresh-Chief gate

The combined packet contains:

- authorization, scope, cap, source, tool, and output manifests;
- each NE report with `PASS`, `FAIL`, or `INCONCLUSIVE`;
- cross-report hashes and dependency links;
- P4 invariants and risk mapping;
- the binding gap-classification table;
- the `DecisionEffectMatrix`;
- a limitation ledger;
- a statement that no installed, configured, production, or external state was changed.

The fresh Chief chooses one normal architecture disposition and separately states whether the minimum
slice may enter implementation planning. The root or evidence compiler cannot convert NE passes into
approval.

## Stop rules

- Stop before L1 if authorization or any numeric cap is missing.
- Stop the affected probe at its first resource-cap breach.
- Stop compatibility claims on NE1 failure or inconclusive provenance.
- Stop stronger executable-closure claims on NE2 failure or inconclusive monitoring.
- Stop receipt/replay integrity claims on NE3 failure or incompleteness.
- Stop expansion when NE4 shows no named-gap advancement.
- Stop DLP claims on NE5 failure or inconclusive control coverage.
- Preserve all failed and inconclusive records; do not delete or silently rerun them.
- Never widen filesystem, process, network, system, or production scope automatically.

## Self-review

- Every named evidence item has a question, permitted acquisition level, artifacts, and typed outcome.
- The plan distinguishes current-file hashes from historical provenance.
- A separately constructed worker is not described as cognitively independent or deployed.
- Windows monitoring capability is tested rather than assumed.
- Canonicalization covers valid bytes, malformed input, domain separation, and history records.
- Prior native telemetry remains separate from future P4 probe resources.
- Numeric probe caps are required before execution and cannot be self-expanded.
- DLP uses both positive and negative controls and does not claim containment.
- A technically successful packet with no decision effect stops instead of expanding.
- The plan authorizes no L0 scan, L1 probe, L2 implementation, network call, or external mutation.

