# P5 evidence review packet

Date: 2026-08-25  
Decision requested: whether unchanged P3 may now be approved for installed-skill implementation or
offering, based only on the named evidence below.

## Frozen design

P3 remains the revised A+B architecture recorded in `P5_DESIGN_DEBATE_RAW.md`: immutable literal
B0; admission of every non-identical delta before classification; per-delta Peer attestation;
stable terminal findings that survive preemptive repair; substantive per-finding closure; zero
cycles only after complete-diff reconciliation; fail-closed authority projection, receipt, route,
and epoch rules. Grader inference (C) remains rejected. No installed-skill behavior was changed.

## New deterministic evidence

- `src/p5_protocol.py` implements deterministic baseline capture, delta admission, Peer attestation,
  candidate/finding linkage, independent `PEER_DISCOVERY`, substantive closure, cycle routing,
  terminal reconciliation, injective projection validation, authority route/receipt validation,
  and future-epoch rollback.
- `schemas/adaptive-axes-v2.schema.json` is a separate canonical V2 schema; legacy V1 artifacts and
  defaults remain unchanged.
- `fixtures/p5_adversarial_traces.json` contains 18 frozen failure/positive-control traces.
- The full suite passes 67 tests. Four Draft 2020-12 schemas validate. P5 worker prompts are
  label-free, version-paired, and blind graders redact both protocol and materiality-contract IDs.

## New live evidence

| Blind alias | Frozen case | Worker result | Protocol-blind grade |
| --- | --- | --- | --- |
| `RUN-P5A7` | F2-noisy | 9 deltas, stable resolved finding, 1 substantive cycle, APPROVE | both gold issues detected; no false closure; specificity 1.0; audit valid |
| `RUN-P5C4` | F3-short | exact B0/P0, 0 deltas/findings/cycles, APPROVE | no unsupported finding; disposition consistent; audit valid |
| `RUN-P5N8` | F3-noisy | exact B0/P0, 0 deltas/findings/cycles, APPROVE | no unsupported finding; disposition consistent; audit valid |

Every accepted worker used fresh `fork_turns=none` Proposing, Peer, and Chief subagent threads. Peer
and Chief first returned readiness-only messages. Chief froze a terminal-only scan before receiving
the debate record. Observable thread and instruction separation is not called cognitive
independence.

## Excluded attempts and environment deviations

- One P5 structured-output preflight failed before sampling because `const` fields lacked explicit
  `type`; the schema and recursive regression test were corrected.
- Five Windows sandbox attempts could not read the required skill contract and performed no role
  work.
- One unsandboxed `codex exec` attempt read the hash-verified skill and references but repeatedly
  called empty `wait` without `spawn_agent`; it was terminated. Pre/post hashes showed no changed or
  added evidence file and the installed skill hash remained
  `D7C599444A4E85FBB089DB7972D060537FB68DC21D6D3068929A95F31B9AD57F`.
- Accepted workers therefore used the current task's native collaboration facility, not the failed
  external CLI orchestration path. Graders were isolated single-agent `codex exec` sessions.

## Chief's eleven named packages — honest status

| # | Required evidence | Status | Evidence / gap |
| --- | --- | --- | --- |
| 1 | canonical and legacy schema derivation/compatibility | **PARTIAL** | separate V2 canonical and worker schemas exist; legacy defaults/tests remain stable, but no independent legacy derivation or full authoritative compatibility matrix was produced |
| 2 | complete authoritative-route inventory | **NOT PROVIDED** | evidence package has reference route IDs only; real installed/production consumer inventory is outside scope |
| 3 | runtime proof for unknown/stale/bypass/shadow/unacked/mismatched routes | **PARTIAL** | deterministic fail-closed unit traces pass; no deployed authority gate or real consumer runtime exists |
| 4 | F2 stable identity/cycle/detected-ID/parity | **PASS for bounded live gate** | `F2-noisy_adaptive_p5_native1.json`, native audit, and `p5_blind_grade_P5A7.json` |
| 5 | F3 zero finding/cycle/no blocker | **PASS for two bounded live gates** | F3 short/noisy artifacts, audits, and clean blind grades |
| 6 | adversarial classification/closure fixtures | **PASS locally** | 18 frozen adversarial/positive-control traces including batching, generic, copied, unsupported, and already-fixed closure |
| 7 | projection loss/injectivity/round trip/parity | **PARTIAL** | deterministic equality and loss tests pass; no independent legacy consumer round-trip implementation |
| 8 | grader contract and receipt parity | **PARTIAL** | protocol-blind graders pass and authority receipts are tested synthetically; graders are not registered authority consumers and emitted no authority receipt |
| 9 | rollout/rollback epoch and historical replay | **PARTIAL** | future-epoch and future-history rejection tests pass; no real rollout or issued-artifact replay |
| 10 | collision/lineage/reconciliation/receipt-canary negatives | **PARTIAL** | stable IDs, collision, missing-link, reconciliation, projection, route, and receipt negatives pass; no live receipt canary or external lineage store |
| 11 | shadow clean-path cost telemetry | **NOT PROVIDED** | native subagent token/cost telemetry is unavailable; grader usage and excluded CLI timings do not establish end-to-end worker cost |

## Authorization boundary

This packet asks for a new binding adjudication. It does not authorize installing V2, changing the
skill, registering consumers, enabling authority, deploying, offering adaptive behavior, or
claiming production readiness. A bounded live gate PASS is not a substitute for missing consumer
and runtime authority evidence.
