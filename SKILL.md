---
name: sana-debation
description: Run an auditable three-round technical architecture debate using separate Proposing TL, Peer TL, and Chief Architect subagent threads, with optional separately instructed alternative, evidence, or domain specialists. Use when the user explicitly asks for a TL/旧识 TL debate, multi-round architecture challenge, alternative architecture comparison, or independent red-team decision before implementation. Do not use for ordinary code review, casual brainstorming, or roleplay without a concrete technical decision.
---

# Sana Manager-Specialist Debate

Turn a concrete technical decision into an evidence-driven architecture disposition through real
subagent delegation. The root agent is a manager and protocol facilitator. The named agents are
bounded technical responsibilities, not fictional personalities or dialogue labels for the root to
imitate.

## Required decision core

Every successful run uses three distinct substantive agent threads:

- **Proposing TL** owns and revises the design.
- **Peer TL** independently attacks assumptions, mechanisms, and failure behavior.
- **Chief Architect** receives the completed record and takes binding decision ownership.

The root may assemble evidence, route packets, enforce budgets and protocol, and format returned
artifacts. It must not write a missing role's argument, soften a rebuttal, or substitute its own
judgment for the Chief's disposition.

Use the host's real subagent capability. Start each role with a fresh or minimally forked context
(`fork_turns: none` when available), then explicitly send the frozen frame, evidence ledger,
allowed artifacts, and that role's contract. Do not create user-owned top-level tasks as a
substitute for subagent threads.

If any required core thread cannot be created or inspected:

1. state: `Debate status: not run — real subagents unavailable`;
2. identify the missing role;
3. do not simulate dialogue or issue a Chief disposition;
4. offer a labeled single-agent review only if the user explicitly opts into it.

Before starting agents, read [role contracts](references/role-contracts.md) and the
[debate protocol](references/debate-protocol.md). Follow both for every run.

## Select the run mode and optional budget

Use a manager-controlled topology. Specialists return bounded artifacts to the root; they never
take over the user conversation or become additional judges.

- `core`: the default. Run only Proposing TL, Peer TL, and Chief Architect.
- `comparative`: add one **Alternative Architect** when the user asks for a genuinely different
  candidate or the frozen frame names multiple plausible architecture families.
- `specialist-assisted`: add one **Evidence Scout** or **Domain Specialist** when a named evidence
  or domain question requires materially different instructions, tools, or policy.

Modes may be combined when both conditions are explicit. Do not add specialists merely because
the host supports them. By default, admit at most one Alternative Architect and one evidence/domain
specialist. Exceed that budget only when the user explicitly asks for a broader panel.

Before dispatch, freeze a compact routing manifest containing:

- selected mode and the concrete reason;
- each optional role's bounded question and possible decision effect;
- its distinct prompt, tool, evidence, or policy contract;
- allowed and deliberately withheld inputs;
- the merge checkpoint and fallback;
- optional job count and retry budget.

Preflight both active concurrency and total thread-identity quota. Completed or interrupted threads
may continue to consume a host's lifetime quota, so available active slots are not sufficient proof
that later core roles can be created. Reserve three distinct thread identities for Proposing TL,
Peer TL, and Chief Architect before admitting any optional role.

When the host exposes no reliable lifetime-quota reservation, conservatively pre-create all three
core threads with fresh contexts before optional dispatch. Start Proposing TL immediately. Peer TL
and Chief Architect receive only their role contract and a readiness instruction; do not send them
candidate, rebuttal, verdict, or preference artifacts before their protocol stage. A pre-created
Chief remains eligible as fresh only while that boundary is preserved.

If three core identities cannot be reserved, fail before substantive debate. If the core can be
reserved but an optional identity cannot, record `OPTIONAL_THREAD_BUDGET_UNAVAILABLE`, downgrade to
the unaffected core, and state which requested comparison or specialist was not run. Do not retry a
thread-limit rejection unless the host reports a genuine quota increase.

Optional work must not occupy capacity or thread identities reserved for required roles. Optional
roles receive no automatic retry; malformed or failed optional work normally falls back to the
unaffected core. Retry once only when the artifact remains decision-critical, the run budget still
permits it, and the retry reason is recorded.

At the predeclared merge checkpoint, route only completed, valid optional artifacts. Exclude late
artifacts without delaying Peer TL. Waiting beyond the checkpoint is allowed only for named evidence
whose absence could conceal a non-negotiable invariant violation; record the maximum wait and let
the Chief defer if the evidence remains missing.

## Report isolation precisely

Use distinct role instructions. When the host supports custom agent profiles or developer-level
instructions, use the relevant role contract there. Otherwise, start a fresh thread and send an
explicit role task packet. The execution audit must state which mechanism was actually used.

Different prompts and threads demonstrate separate instruction and execution, not absolute
cognitive independence. Use only claims supported by observable setup:

- `separately-instructed` when prompts differ;
- `fresh-thread` when a new agent thread was used;
- `P0_NOT_PROVIDED` when the Alternative packet excluded Proposing TL's P0;
- `P0_EXPOSURE_REQUIRED` when the baseline proposal could not be withheld;
- `second candidate` for X0 unless stronger isolation is enforced and auditable.

Never describe an agent as cognitively independent merely because its prompt, thread, or role name
differs. Shared-workspace access is shared evidence access and may limit any blindness claim.

## Establish the decision frame

Inspect the available code, logs, data, specifications, and primary documentation needed for the
decision. Freeze:

- the exact decision and implementation boundary;
- non-negotiable invariants and production constraints;
- three materially different attack axes;
- uncertain assumptions;
- an evidence ledger with stable IDs such as E1, E2, and E3.

Label every material statement as verified fact, inference, product preference, or unresolved risk.
A verified fact must name an inspectable source. Repetition by multiple agents does not upgrade an
inference.

Prefer attack axes from correctness and trust boundaries; contracts, compatibility, migration and
rollback; security, failure modes, observability and operability; product/governance impact; and
adversarial generality. Freeze all three before the first rebuttal.

## Start candidates and specialists

Start **Proposing TL** with its role contract, the frozen frame, ledger, and relevant artifacts. Ask
for proposal P0 in implementable terms, including contracts, typed failures, migration, rollback,
observability, resource effects, and unresolved assumptions.

In `comparative` mode, start **Alternative Architect** concurrently when capacity permits. Give it
the same neutral requirements and validated evidence, but do not provide P0 or the facilitator's
preferred outcome. Freeze its output as X0 before any later exposure to P0. If the decision cannot
be framed without revealing the submitted baseline, record `P0_EXPOSURE_REQUIRED` and do not call
X0 blind.

Evidence Scouts return sourced evidence with limitations, not a proposal or verdict. Domain
Specialists return a bounded advisory memo with invariants, counterexamples, and uncertainty, not a
disposition. Validate new evidence before adding it to the ledger. Route every specialist memo that
affects the debate unchanged and symmetrically to Proposing TL and Peer TL.

After P0 and the merge checkpoint, start or activate **Peer TL** in its distinct reserved thread.
Give it the frozen frame, ledger, P0, on-time specialist artifacts, and X0 when present. Do not
provide a prepared rebuttal, intended verdict, private process, or facilitator preference.

When X0 exists, Peer TL first classifies the observed candidate relationship:

- `CAUSAL_DIVERGENCE_OBSERVED`: at least one mutually exclusive decision-critical commitment and
  materially different failure implication are identified;
- `ALT_DIVERSITY_UNPROVEN`: causal separation cannot be established;
- `ALT_ISOMORPHIC`: decisive commitments and failure implications are materially shared.

Component renaming or two surface-level differences are insufficient. The classification applies
only to this run and does not prove general cognitive independence.

Keep Proposing TL and Peer TL alive across all three rounds by sending follow-up tasks to the same
threads.

## Run three routed rounds

Use one frozen primary attack axis per round. Route artifacts in this order:

1. identify the Proposing TL's current mechanism for the axis;
2. ask Peer TL for its strongest rebuttal, one realistic failure trace or counterexample, and a
   falsifier naming evidence that would change its assessment;
3. send the rebuttal to Proposing TL and require itemized `accepted`, `rejected with evidence`, or
   `unresolved` responses plus a proposal diff when behavior changes;
4. send the response and current proposal to Peer TL for a closing assessment;
5. record `accepted`, `modified`, `rejected`, or `unresolved` with evidence and risk links.

A valid rebuttal changes the proposal, updates a risk, or requests named decision-relevant evidence.
Repetition, generic caution, confidence, and seniority are not arguments. Agreement requires a diff
or cited evidence.

Do not request hidden chain-of-thought. Require conclusions, mechanisms, counterexamples, evidence,
proposal diffs, and risk updates. After P0, keep routed packets compact instead of repeating the
entire proposal.

## Hand off binding decision ownership

After round three, start **Chief Architect** in a fresh third core thread, or activate its
pre-reserved thread if it has received no substantive debate artifacts. This is the only binding
ownership handoff in the workflow. Give it only:

- the frozen frame, routing manifest, and final evidence ledger;
- P0, X0 and its Peer classification when present, and the final proposal;
- validated specialist artifacts;
- all three complete round records and the final risk register;
- the Chief Architect role contract.

Do not tell it which outcome the facilitator or user prefers. It must choose exactly one:

- approve;
- approve with required changes;
- reject and redesign;
- defer pending named evidence.

The decision must trace facts, rebuttals, changes, optional artifacts, and residual risks by ID. It
may not add facts. Missing evidence that could conceal an invariant violation requires deferral.
The root validates format and traceability but never rewrites the disposition. One focused format
correction is allowed; if still invalid, report `defer pending valid chief-architect decision`.

## Failure and stopping rules

- Retry a failed or malformed required core response at most once with a focused correction.
- If a required core role still fails, stop and do not issue approve.
- Treat a thread-limit rejection as a quota fact, not a transient role-response failure. Do not
  repeatedly dispatch the same optional role without an observed quota change.
- Never replace an unavailable agent with root-authored content.
- Preserve unresolved disagreements, optional failures, late artifacts, and missing evidence.
- Debate agents remain read-only unless implementation is separately authorized.
- A debate request never authorizes code changes, deployment, purchases, or production mutation.

## Final output

Use this order unless the user requests another format:

1. Execution audit and run mode
2. Decision frame, routing manifest, and evidence ledger
3. P0 and X0/candidate classification when present
4. Round 1 — axis
5. Round 2 — axis
6. Round 3 — axis
7. Final proposal and risk register
8. Chief Architect decision
9. Required changes and next action

The audit states `real-subagents`, every required and optional thread status/identifier exposed by
the host, prompt/context isolation labels, skipped or late optional work, retries, and protocol
failures. If it cannot truthfully do so, report that the debate did not run.

Consolidate instead of dumping raw transcripts. Never omit evidence traceability, proposal changes,
candidate uncertainty, unresolved risks, or the execution audit to save space.
