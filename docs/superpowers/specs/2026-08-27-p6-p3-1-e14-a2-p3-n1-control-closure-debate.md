# P3-N1 G7 control-closure debate record

Date: 2026-08-27

Status: closed; Chief approved design only.

## Execution audit

- Mode: `real-subagents / core`
- Proposing TL: `/root/e14_n1_proposing`
- Peer TL: `/root/e14_n1_peer`
- Chief Architect: `/root/e14_n1_chief`
- Context labels: three fresh threads; separately instructed
- Peer isolation: received only its readiness contract before P0 routing
- Chief isolation: received only its readiness contract until all three rounds closed
- Optional roles: none; four active slots required reserving all three core identities
- Core retries: none
- Protocol failures: none
- Implementation or execution during debate: none

These observations prove separate instruction and thread execution. They do not prove cognitive
independence. The agents shared the same filesystem and model family.

## Frozen decision

Decide whether A2 may use an additive N1 G7 acceptance profile based on threat-model control closure,
and whether that profile may reuse the current exact but large image or must require a dedicated
finite-manifest image.

The debate did not authorize A2, G8, G9, image construction, container execution, qualification, or
terminal creation.

## Evidence ledger

| ID | Classification | Evidence |
|---|---|---|
| E0 | Product direction | User confirmed design of a narrow rule; not cryptographic or operational authority |
| E1 | Verified record | Prior Chief deferred; strict G7 observation gap recorded |
| E2 | Verified evidence | G6 PASS/G7 PARTIAL under exact Docker controls, network 0B/0B and one-process enforcement |
| E3 | Verified source/test | Exact scanner hash and adversarial tests; no package import or execution path found |
| E4 | Verified mechanism | Vendor Python is AST data and JavaScript is text; neither is imported/executed |
| E5 | Verified limitation | Current image is exact but large/unrelated; module and `sys.path` observations are guest-reported |
| E6 | Verified mechanism | `-I -S -B` and empty `PYTHONPATH`; interpreter/bootstrap remains trusted |
| E7 | Verified state | No admission root; 83 tests at debate start; no A2/G8/G9 |
| E8 | Unresolved risk | Transitive stdlib/native/image-bound executable closure absent |
| E9 | Inference | Control closure is sound only inside an explicit exact TCB and input-nonexecution boundary |
| E10 | Product direction | Prefer a dedicated minimal tool profile over rebuilding a privileged observer for v1 |

## Round record

| Round | Frozen axis | Peer counterexample | Proposal change | Peer verdict |
|---|---|---|---|---|
| 1 | Threat model and proof soundness | Origin closure alone permits the trusted scanner to become a confused deputy through input-derived callable/code/deserializer/native behavior | Split `EXECUTABLE_STORE_CLOSURE` and `INPUT_NONINTERPRETATION_CLOSURE`; bind scanner policy, review, callbacks, and adversarial dataflow roots | `modified` |
| 2 | Executable origin, OCI and platform closure | Ordinary ELF edges miss preload/audit/loader config/NSS/gconv/late load; `-B` does not prohibit existing bytecode; OCI whiteouts and mount shadowing defeat qualitative minimality | Require a dedicated image, exact canonical final-view equality, external OCI merge verifier, finite loader/bootstrap/native inventory, explicit embedded-interpreter TCB, and exact platform tuple | `modified` |
| 3 | Lifecycle, compatibility and rollback | A post-run G7 candidate cannot be a pre-G8 prerequisite; stale candidate replay or output-path replacement can pass a different run | Separate qualification, atomic output reservation, safe stopped preparation, one-run G8, nonauthoritative candidate, and external G9 CAS finalization; separate issuer roles and legacy routing | `modified` |

Each round used one attack axis. This was three total rounds, not three axes repeated three times.

## Decisive failure traces

### R1: trusted confused deputy

If untrusted input can select a callable, construct code, select a deserializer factory, or choose a
native path, an exact trusted scanner can execute attacker-controlled behavior without adding a new
module origin. Image identity alone does not falsify this path.

### R2: pre-interpreter native execution

An unclassified preload library can execute a constructor before CPython processes `-I -S -B`.
Ordinary dependency roots, command hashes, and later guest observations may all match. Exact merged
view, loader configuration, environment, and constructor inventory are required.

### R3: replay and output substitution

If a run authorization binds only a stable profile and a replaceable output path, a prior valid
candidate from the same profile can be inserted after an emptiness check. A failed current run can
then be finalized as PASS. Fresh nonce, prepared-container identity, immutable output object,
exclusive attachment history, predecessor, and CAS finalization break the trace.

## Final proposal

The final P3 proposal is recorded normatively in
`2026-08-27-p6-p3-1-e14-a2-p3-n1-control-closure-spec.md`. Its decisive commitments are:

- additive A2-only profile; strict legacy unchanged;
- current image `sha256:c459db0b82f43b3b8fe0fb7b5d12d902c449764e9f1260c8483ce459514b9e89`
  ineligible; dedicated exact-manifest image mandatory;
- dual executable-store and input-noninterpretation closure;
- external OCI merged-view, loader/bootstrap/late-load, and exact platform closure;
- distinct policy, qualification, G8, controller, and G9 roles;
- qualification -> exclusive output -> safe stopped preparation -> one-run G8 -> candidate -> G9;
- local single-writer CAS ledger as qualified TCB, without a distributed platform;
- PASS, determinate DENY, and infrastructure/uncertainty BLOCK separation; and
- mutual N1/legacy rejection with selector revocation rollback.

## Chief Architect disposition

**Approve — design only.**

The Chief found no remaining structural blocker. The complexity is proportionate to the concrete
confused-deputy, loader/bootstrap, output-rebinding, replay, and authority-conflation failures. The
current image was rejected for N1. A privileged observer was not selected for v1 and was not
rejected on comparative merit because no comparative cost/risk evidence was available. Strict
defer remains available through legacy routing.

Missing scanner, OCI, lifecycle, ledger, and finalizer evidence are qualification/implementation
gates rather than defects in the approved design.

## Next authorized step

Only document and static-fixture work is authorized:

- lifecycle schema and canonical root contract;
- role and transition matrix;
- normative final-view/OCI/loader inventory requirements;
- scanner dataflow and callback contract;
- nonauthoritative positive/negative fixture corpus;
- evidence, observability, rollback, and future implementation plan.

No state-changing N1 operation follows automatically.
