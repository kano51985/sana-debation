# E14 A2 G7 external module-observation gap debate

Date: 2026-08-27

Chief disposition: **defer pending named evidence**

This was a read-only sana-debation core run. It evaluated one narrow architecture decision after
the G6 envelope canary passed and G7 remained partial. It authorized no observer implementation,
platform rebuild, P3 revision, G8/G9 progression, A2 execution, or terminal finalization.

## Execution audit

- execution: real-subagents / core;
- Proposing TL: /root/e14_g7_proposing, fresh-thread, separately instructed, completed;
- Peer TL: /root/e14_g7_peer, fresh-thread, separately instructed, completed;
- Chief Architect: /root/e14_g7_chief, fresh-thread, separately instructed, completed;
- all three identities were pre-created before substantive routing;
- Peer and Chief initially received readiness contracts only;
- no optional role, candidate X0, retry, malformed core response, or protocol failure occurred;
- rounds closed as modified, modified, unresolved; and
- separate prompts and threads demonstrate separate instruction and execution, not cognitive
  independence.

## Decision frame

Decision: determine whether image/rootfs identity, isolated Python launch, and guest module
enumeration can substitute for P3 external loaded-module observation; whether an external observer
should be engineered; or whether G7 must remain fail-closed.

The fixed axes were:

1. epistemic sufficiency and substitution;
2. observer feasibility, process accounting, and TCB effects; and
3. proportionality, denial/finalizer semantics, compatibility, and operability.

The controlling invariants were network NONE with external zero-byte observation; one target
process and child denial; exact image/tool/input hashes; no vendor import or execution; read-only
input/rootfs with sole temporary output; external finalizer-only future terminal authority; and no
G8/G9/A2 progression when invariant evidence is missing.

## Evidence ledger

| ID | Class | Evidence | Limitation |
|---|---|---|---|
| E1 | verified fact | Prior P3/Chief requires external process/module observation and defers on missing invariant evidence | Does not identify accountable requirement owner |
| E2 | verified fact | G1-G5 production freeze, physical scanner tests, pre-scan roots, policy, and source closure exist | Does not prove runtime envelope |
| E3 | verified fact | Persisted G6/G7 canary records network none, 0B/0B, PID1, child EAGAIN, EROFS, exact hashes, and G6 PASS | G7 status remains partial |
| E4 | verified fact | Docker inspect/top/stats are external for image, command, mounts, process, network, and resources | Loaded module origins are guest-reported |
| E5 | verified fact | Exact image digest and CPython 3.12.14 are measured | Image is large; per-module external coverage absent |
| E6 | verified fact | vendor-admission-v1 is absent and admission_executed is false | No A2 output exists |
| E7 | unresolved risk | No evidenced Docker Desktop VM eBPF/audit semantic module feed | Feasibility unknown |
| E8 | product preference | Prefer minimal tool-centric change and no platform rebuild merely for evidence wording | Cannot weaken P3 |

## P0

P0 selected fail-closed deferral. It rejected image/rootfs identity, -I/-S, read-only mounts, and
guest enumeration as substitution. It tentatively allowed only a pre-existing external host or
VM-kernel observer that was armed before first exec, exactly bound, externally origin-resolving,
loss-detecting, noninterfering, and evidence-only. Target hooks, injected launchers, and sidecars
were rejected.

## Round 1 — epistemic sufficiency

Peer showed that a loss-free event stream proves delivery of emitted events, not that the source
generated an event for every pure-Python import. A pure module could load without exec or native
mapping, leaving a semantically incomplete but transport-complete trace.

P1 accepted the trace and:

- defined U-PROC, U-PYMOD, and U-NATIVE, including initial, pure, archive, built-in/frozen,
  dynamic, custom-loader, direct-registry, extension, and native cases;
- split G-SOURCE semantic event-generation coverage from G-TRANSPORT delivery integrity;
- prohibited negative-event interpretation unless both gates and per-run probe attachment pass;
  and
- added blocking coverage, attachment, unsupported-mechanism, and baseline failures.

Peer closing verdict: modified. The contract became epistemically coherent, but no source exists
that meets it.

## Round 2 — feasibility and observer TCB

Peer showed that U-PYMOD may be invisible to a purely external kernel observer without an
in-process hook, injected helper, altered launcher, or sidecar. It also exposed an undeclared
privileged TCB: kernel/probe loader/collector/resolver/verifier/finalizer components can fabricate
evidence or influence the target, while hashes alone prove neither configuration nor faithful
operation.

P2 accepted the objection and:

- downgraded all observer families to unproven future research hypotheses;
- made the current path solely G7 PARTIAL and no G8/G9/A2;
- rejected target hooks, sidecars, and per-run VM helpers;
- defined explicit host, hypervisor, VM-kernel, collector, resolver, sealer, verifier, and
  finalizer trust roots, configuration, privilege, tamper, and noninterference requirements; and
- required an executable exact-image adversarial matrix rather than a manifest assertion.

Peer closing verdict: modified. No eligible feed, feasibility proof, or qualified observer TCB
exists.

## Round 3 — proportionality and failure semantics

Peer showed that indefinite defer can become a governance deadlock when no accountable owner has
reaffirmed the absolute requirement. It also showed that a normal G9-capable finalizer writing a
signed defer record could be misread by downstream consumers as completion. A large privileged
observer can reduce net assurance even if it improves telemetry.

P3 accepted the state-machine and proportionality objections:

- a future blocker must be denial-only PRE_G8_G9_GATE_BLOCK_V1, state RUN_CLOSED_BLOCKED,
  p3_satisfied=false, progression_allowed=false, and unable to encode PASS;
- consumers must require a distinct positive G7_PASS and negative-test signed blockers, generic
  completion, missing subtype, contradiction, replay, and unknown schema;
- when that denial path is not evidenced, no completion-like artifact is emitted;
- an accountable P3 owner must explicitly reaffirm, narrow, or replace the requirement; and
- observer work requires NET_ASSURANCE_POSITIVE covering threat closure, privilege/TCB expansion,
  noninterference, production fidelity, resources, privacy, upgrades, rollback, and E8.

Peer closing verdict: unresolved. No accountable owner disposition or net-assurance evidence was
supplied.

## Chief Architect decision

Disposition: **defer pending named evidence**.

Binding current behavior:

- G6 remains PASS and G7 remains PARTIAL;
- identity, read-only rootfs, -I/-S, restricted import paths, and guest module lists are not
  substitutes for external module observation;
- observer engineering and platform rebuild are not approved;
- G8, G9, A2, and admission terminal finalization remain blocked;
- current evidence does not create vendor-admission-v1; and
- no completion-like blocker artifact should be emitted until its denial-only schema, authority,
  and negative consumers are evidenced.

Named next evidence:

1. an attributable P3-owner decision choosing reaffirm, narrow, or replace;
2. NET_ASSURANCE_POSITIVE before any observer program;
3. if reaffirmed, an eligible pre-existing interface plus exact-runtime G-SOURCE, G-TRANSPORT,
   I-OBS, production-fidelity, failure-injection, resource, and privacy evidence; or
4. if narrowed/replaced, an authoritative revised G7 rule and matching evidence; and
5. separate denial-consumer conformance proving that no blocker can be consumed as G7_PASS/G9/A2.

Residual risks remain open: no interface, semantic blindness, event loss/drift, privileged TCB
fabrication/interference, qualification/production divergence, resources/privacy, governance
deadlock, blocker/success confusion, and negative net assurance.
