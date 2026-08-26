# E6 Live Pilot Diagnostic

Date: 2026-08-25  
Case: `F2-short / fixed-three-v1`  
Status: **RECOVERED FOR ONE MATCHED PAIR — earlier attempts excluded**

Two bounded launch attempts were made only to verify the fresh-session, real-subagent, structured
output path before authorizing a 24-run campaign. Neither produced a final JSON artifact, so no
behavioral observation or protocol comparison was recorded.

## Attempt 1

- Isolated `codex exec --ephemeral`, read-only sandbox, default `gpt-5.6-sol / xhigh`.
- Three separate subagent-hook events were observed, which is evidence of dispatch attempts but not
  proof of three complete or auditable role threads.
- The ephemeral parent had no resolvable transcript for subagent hooks.
- The host reported model-cache schema errors, remote plugin-catalog failures, and websocket stream
  retries.
- No output file was created; the stalled run was terminated and excluded.

## Focused retry

- Session persistence retained; irrelevant plugin loading disabled.
- `--ignore-user-config` unexpectedly changed reasoning effort from `xhigh` to `none`, breaking the
  matched-setting requirement.
- The model-cache schema error persisted and the run remained in repeated collaboration waits.
- No output file was created; the stalled run was terminated and excluded.

## Decision

No adaptive counterpart and no batch run were started. Starting them would mix infrastructure and
configuration differences into the protocol comparison. Before live E6, the host must provide:

1. a model cache compatible with the installed Codex CLI;
2. stable model streaming;
3. persisted, resolvable parent/subagent audit metadata;
4. a frozen model and reasoning setting that remains identical across both protocols;
5. a successful single matched pilot that emits both schema-valid artifacts.

This diagnostic is not evidence for or against either debate protocol.

## 0.149.1 medium pilot correction

An initial medium fixed run completed with three real threads and a schema-valid artifact, but the
worker prompt contained conflicting Chief instructions: the common paragraph required a blind scan
while the specific fixed contract required a single complete-record handoff. The worker followed
the specific fixed contract. The run is excluded as `prompt_contract_unambiguous=false`; its
substantive findings and token count are not used in the matched comparison. The common prompt was
then corrected to defer to each protocol-defined Chief handoff. Adaptive remains two-stage; fixed
remains the installed one-stage behavior.

A later fixed artifact exposed a related representation defect: the shared worker schema lacked a
stage name for a finding first introduced by fixed's one-stage Chief. The worker used
`TERMINAL_RECONCILIATION` even though no extra Peer stage ran. Schema-1 was extended additively with
`CHIEF_DECISION`; one focused format correction of the same session is allowed, but no substantive
finding or disposition may change.

## Recovery and valid pair

The globally installed CLI was updated from `0.147.0` to `0.149.1`, matching the refreshed model
cache format. No cache was deleted. Medium reasoning was then frozen for parent and subagents,
plugins were disabled, and the corrected protocol-specific Chief prompt was reused unchanged for
both arms.

One adaptive and one fixed `F2-short` run completed with three distinct, fresh, auditable core
threads each. Their terminal artifacts and host audits were schema-valid. Fresh protocol-blinded
single-agent graders detected both gold issues in both artifacts, found no false closure, and gave
both a 1.0 trace-specificity score. The valid pair is documented in `PILOT_REPORT.md`.

The successful pair supersedes only the infrastructure conclusion that live execution was
unavailable. It does not rehabilitate the excluded attempts, and one pair cannot satisfy the
twelve-case E6 gate.
