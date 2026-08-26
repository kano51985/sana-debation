# P5 provenance-preserving adaptive evidence report

Date: 2026-08-25  
Final binding disposition: **defer pending named evidence**

## Outcome

P5 repairs the bounded failure observed in P4 without regressing the two seeded clean cases:

| Gate | Result |
| --- | --- |
| Deterministic suite | 67/67 tests pass; four Draft 2020-12 schemas validate |
| Adversarial reference gate | 18 frozen traces pass, including generic, copied, unsupported, already-fixed, batching, link, projection, authority, receipt, and epoch negatives |
| F2-noisy | one substantive cycle; one stable resolved finding; blind grader detected both gold issues; specificity 1.0; no false closure; audit valid |
| F3-short | zero deltas, findings, and substantive cycles; clean blind grade; audit valid |
| F3-noisy | zero deltas, findings, and substantive cycles; no noise-induced blocker; clean blind grade; audit valid |

This is evidence that immutable B0 plus admission-before-classification fixes the specific
preemptive-repair provenance loss. It is not production authority proof or general behavioral
non-inferiority.

## Accepted execution path

Each accepted worker used three new native `fork_turns=none` subagent threads. Peer and Chief first
returned readiness-only messages. Chief performed a terminal-only scan before seeing the complete
record. The execution supports `fresh-thread` and `separately-instructed` claims only; it does not
prove cognitive independence.

F2 legitimately used one substantive cycle. F3-short and F3-noisy legitimately used zero. No empty
interaction or readiness message was counted as a substantive cycle, and no second/third cycle was
created after complete terminal reconciliation.

## Excluded attempts

The implementation plan preserves all failed external CLI attempts:

- one pre-sampling structured-output schema rejection;
- five Windows sandbox runs that could not read the required skill and spawned no roles;
- one unsandboxed external run that read and hash-verified the skill but repeatedly called empty
  `wait` without spawning a role.

None counts as behavioral evidence. Pre/post hashes for the unsandboxed attempt showed no package
or installed-skill mutation. The installed skill remained at SHA-256
`D7C599444A4E85FBB089DB7972D060537FB68DC21D6D3068929A95F31B9AD57F`.

The blind graders were separate single-agent CLI sessions with protocol ID, materiality-contract
ID, and original run ID redacted.

## Fresh Chief re-adjudication

Fresh Chief thread `/root/p5_evidence_fresh_chief` first returned
`READY_CHIEF / NO_EVIDENCE_OR_PREFERENCE_PROVIDED`, then inspected the frozen P3, reference code,
schemas, fixtures, tests, all three live artifacts, blind grades, audits, and excluded-attempt plan.
It independently reran 67 tests and validated all four schemas.

The Chief classified the original eleven packages as:

- bounded PASS: F2 live gate, two F3 live gates;
- local-reference PASS: adversarial closure/classification fixtures;
- PARTIAL: schema compatibility, runtime route failures, projection round trip, grader receipts,
  epoch replay, collision/lineage/canary;
- NOT PROVIDED: complete real authority-route inventory and end-to-end native cost telemetry.

The binding decision therefore remains **defer pending named evidence**. Required next evidence is:

1. owner-attested inventory of every real authority route and consumer;
2. typed canonical/legacy compatibility matrix plus independent projection/reverse round trip;
3. installed-skill shadow proof that every inventoried route fails closed;
4. integrity-bound receipts from actual graders and authority consumers;
5. real issued-artifact forward rollout and future-epoch rollback replay;
6. candidate/finding collision, merge/split lineage, and live receipt-canary negatives;
7. end-to-end F3 token, latency, interaction, and cost telemetry, followed by F2/F3 parity through
   the same non-authoritative shadow boundary.

## Authorization boundary

No installed-skill change, consumer registration, authority enablement, deployment, offering, or
production-readiness claim is authorized. A separately authorized isolated, non-authoritative
shadow implementation may gather the remaining evidence but must not publish authority.
