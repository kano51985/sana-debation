# P5 evidence implementation plan

Date: 2026-08-25  
Status: completed as an evidence tranche; binding result remains deferred

The requested `writing-plans` skill is unavailable in this environment. This explicit fallback plan
implements the already approved P5 design without changing the installed skill.

1. Add failing deterministic tests for baseline capture, delta admission, stable finding identity,
   zero-cycle eligibility, terminal reconciliation, authority receipts, projection parity, and
   epoch rollback.
2. Implement `src/p5_protocol.py` and `schemas/adaptive-axes-v2.schema.json` until those tests pass.
3. Add failing prompt/schema tests for `adaptive-axes-v2`, `baseline-delta-ledger-v1`, label
   redaction, B0-to-P0 delta retention, and legacy-default stability.
4. Implement the versioned P5 worker prompt and `eval/e6_run_output_p5.schema.json`.
5. Add golden/adversarial fixtures and produce deterministic evidence summaries.
6. Run the full unit suite and schema validation.
7. Run fresh F2-noisy, F3-short, and F3-noisy P5 adaptive workers, host audits, and blinded graders.
8. Consolidate evidence and submit unchanged P3 plus the new evidence package to a fresh Chief.

Any failure stops expansion at that stage. Live calls begin only after deterministic gates pass.

## Frozen live matrix

The deterministic gate passed before any P5 worker call: 66 unit tests passed; four Draft 2020-12
schemas validated; all three prompts were label-free. The installed skill hash at that point was
`D7C599444A4E85FBB089DB7972D060537FB68DC21D6D3068929A95F31B9AD57F`.

| Case | Worker run ID | Sealed blind alias |
| --- | --- | --- |
| F2-noisy | `F2N-ADAPTIVE-P5-MEDIUM1` | `RUN-P5A7` |
| F3-short | `F3S-ADAPTIVE-P5-MEDIUM1` | `RUN-P5C4` |
| F3-noisy | `F3N-ADAPTIVE-P5-MEDIUM1` | `RUN-P5N8` |

All workers and graders use `gpt-5.6-sol / medium`. Workers use the P5 structured output schema,
read-only sandbox, no user-configured plugins, and fresh persisted sessions so host facts can be
audited. Graders use fresh single-agent sessions with protocol and contract names redacted.

The first `F2-noisy` command reached no model sampling: Codex rejected the response schema because
its `const` fields lacked explicit `type` declarations. Session
`01a0395e-4a6a-74f2-92ee-692a2a451214` is retained as a preflight failure, not counted as worker
evidence. The schema and a recursive structured-output regression assertion were corrected before
the matrix resumed; the sampled worker run uses suffix `MEDIUM2`.

`MEDIUM2` entered sampling but its read-only workspace could not read the installed skill outside
the workspace, emitted only explicitly interim `PROTOCOL_INVALID` objects, spawned no role agent,
and was terminated while idling. Session `01a0395f-2cdc-7603-8452-7bf8259d19c9` is also excluded
from worker evidence. The next run preserves read-only mode while adding only the installed skill
directory as a readable root; its suffix is `MEDIUM3`.

Windows read-only sandboxing also rejected the `--add-dir` read path in `MEDIUM3`; session
`01a03961-fcf7-7212-bf20-3d6023689efc` likewise emitted no role work and is excluded. `MEDIUM4`
therefore uses the installed skill directory itself as the worker's read-only root, while the case
contract remains frozen on stdin and the output schema/result paths are absolute evidence-package
paths. This changes filesystem reachability, not protocol content or model settings.

`MEDIUM4` proved the current Windows CLI read-only policy blocks shell reads even when the skill
directory is the working root; session `01a03963-1bc3-76c2-913f-2b435d8e5e62` performed no role
work. `MEDIUM5` uses `workspace-write` rooted only at this isolated evidence package so the worker
can read the installed contract. The prompt still forbids implementation or unrelated inspection;
the installed skill hash and package changes are checked after execution. This sandbox deviation
is disclosed and must not be described as a read-only worker.

`MEDIUM5` could execute workspace commands but the installed locator remained outside its readable
root; session `01a03964-00d9-7e00-9301-5295569f918a` performed no role work. A byte-identical
workspace snapshot `SKILL.md` was then created with the already frozen installed-skill hash. The
label-free worker prompt now names this hash-pinned fallback and requires disclosure when used.
`MEDIUM6` is the first candidate run with a reachable skill contract.

`MEDIUM6` showed that this CLI's non-interactive Windows `workspace-write` policy also rejects local
shell reads; session `01a03966-e013-7ce3-8dfd-6079624a5aa4` performed no role work. Before the only
remaining execution mode (`MEDIUM7`, no sandbox), the orchestrator froze SHA-256 values for every
file under `src`, `eval`, `schemas`, `tests`, `fixtures`, and `docs`, plus the installed skill. The
worker still has plugins/apps disabled and a no-implementation closed-world prompt. Post-run hash
comparison is an audit gate; any unexpected mutation invalidates the result.

## Final accepted matrix and adjudication

| Case | Accepted native worker | Blind alias | Result |
| --- | --- | --- | --- |
| F2-noisy | `F2N-ADAPTIVE-P5-NATIVE1` | `RUN-P5A7` | both gold issues, specificity 1.0, 1 cycle |
| F3-short | `F3S-ADAPTIVE-P5-NATIVE1` | `RUN-P5C4` | 0 findings/cycles, clean disposition |
| F3-noisy | `F3N-ADAPTIVE-P5-NATIVE1` | `RUN-P5N8` | 0 findings/cycles, no noise blocker |

Fresh Chief `/root/p5_evidence_fresh_chief` inspected and reran the evidence. Its binding result is
`defer pending named evidence`: local/bounded behavior passes, but complete real route inventory,
runtime authority enforcement, independent legacy round-trip, actual consumer receipts, real
rollout/rollback replay, live lineage/canary proof, and end-to-end worker cost remain incomplete.
See `P5_IMPLEMENTATION_REPORT.md` and `P5_EVIDENCE_REVIEW_PACKET.md`.
