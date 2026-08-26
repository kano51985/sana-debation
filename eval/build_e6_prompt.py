"""Build one label-free E6 live-debate prompt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROTOCOLS = {"fixed-three-v1", "adaptive-axes-v1", "adaptive-axes-v2"}
MATERIALITY_CONTRACTS = {
    "legacy-v1",
    "closed-world-provenance-v1",
    "baseline-delta-ledger-v1",
}


def load_case(path: Path, case_id: str) -> dict[str, Any]:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            case = json.loads(line)
            if case["case_id"] == case_id:
                return case
    raise ValueError(f"unknown case_id: {case_id}")


def public_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        key: case[key]
        for key in ("case_id", "decision", "axes", "initial_proposal", "revision_sequence", "noise_notes")
    }


def protocol_contract(protocol_id: str) -> str:
    if protocol_id == "fixed-three-v1":
        return """Use exactly three complete Proposing-TL/Peer-TL challenge-response rounds.
Each round must contain a concrete mechanism, realistic failure trace, falsifier, itemized response,
proposal delta, Peer closing assessment, and evidence/risk references. Apply the supplied revision
sequence in order across the three rounds; if fewer than three revisions are supplied, later rounds
must still re-inspect the resulting proposal and may not fabricate a material objection. After round
3, route the exact terminal proposal and complete record to a fresh Chief Architect for a binding
decision."""
    adaptive = """Freeze the three supplied attack axes. Peer first inspects all axes against P0 and
records either a material challenge or an evidenced no-material objection. Route zero through three
substantive challenge-response cycles, applying the supplied revision sequence in order as proposal
changes become due. Exact structured duplicates consume no cycle; changed observable effect,
direct/transitive revision impact, or uncertainty is new/indeterminate. Before Chief handoff, Peer
must reconcile every axis against the exact terminal proposal and every intervening revision. A new
material issue re-enters routing below the three-cycle ceiling and remains visibly open at the
ceiling. A fresh Chief performs a blind terminal scan before seeing the full record, then reconciles
and decides. Never fabricate an extra cycle."""
    if protocol_id == "adaptive-axes-v2":
        return adaptive + "\nApply the P5 baseline/delta/finding requirements before cycle selection."
    return adaptive


def materiality_contract(contract_id: str) -> str:
    if contract_id == "legacy-v1":
        return """Use the original evidence/materiality behavior supplied by the installed role
contracts. This compatibility mode exists only to reproduce earlier worker prompts."""
    if contract_id == "baseline-delta-ledger-v1":
        return """Preserve closed-world precondition provenance and add the P5 baseline-delta ledger.

Treat the supplied `initial_proposal` as literal immutable `B0`. Proposing TL may create an improved
P0, but it must enumerate every non-identical B0-to-P0 behavior, interface, failure, invariant,
rollout, or decision change as a delta candidate before semantic classification. Admission comes
before exclusion: no classifier, proposer, compaction step, or improved final proposal may erase a
candidate.

Classify every admitted delta exactly once as `NON_DECISION_RELEVANT`, `DECISION_RELEVANT`, or
`UNCERTAIN`, with `SUPPLIED_FACT`, `VERIFIED_EVIDENCE`, or `HYPOTHETICAL` precondition provenance.
Every delta must be Peer-attested against exact B0/Pn locations. A supplied decision-relevant
behavior change refutes equivalence even when its exact severity, implementation, or remediation is
not supplied; missing impact detail cannot prove equivalence or `NON_DECISION_RELEVANT`.

Every decision-relevant or uncertain delta becomes a stable terminal finding before cycle
selection. If Proposing TL repairs it preemptively, route at least one substantive Peer challenge,
itemized Proposing response, and independent Peer close. Resolution changes status only: resolved
findings remain in `terminal_findings` with immutable provenance and the same identity. An improved
final proposal is not detection evidence without an explicit terminal finding.

Peer-discovered supplied/verified conflicts that do not arise from a B0-to-P0 delta also become
terminal findings with `PEER_DISCOVERY` provenance. Purely hypothetical notes remain non-blocking
limitations exactly as in `closed-world-provenance-v1`.

Zero substantive cycles are permitted only after complete-diff reconciliation shows no
decision-relevant/uncertain candidate, no supplied/verified conflict, and every non-relevant delta
has a specific Peer attestation. A genuinely clean unchanged proposal may emit empty
`delta_candidates`, empty `terminal_findings`, and zero substantive cycles. Generic `addressed`,
`already fixed`, copied closure, unsupported batching, missing links, or missing attestation fail
the run instead of producing empty findings plus approval."""
    if contract_id != "closed-world-provenance-v1":
        raise ValueError(f"unknown materiality contract: {contract_id}")
    return """Use closed-world precondition provenance for every proposed challenge, risk, gate,
and Chief decision effect. Label each causal precondition as exactly one of:

- `SUPPLIED_FACT`: stated in the case chronology;
- `VERIFIED_EVIDENCE`: supported by an inspectable item inside this frozen packet;
- `HYPOTHETICAL`: plausible only in an unspecified implementation or environment.

Only `SUPPLIED_FACT` and `VERIFIED_EVIDENCE` may create a material challenge, consume an adaptive
cycle, appear in `terminal_findings`, remain OPEN/INDETERMINATE, require evidence, cause required
changes, or force Chief deferral/rejection. A `HYPOTHETICAL` item may be retained only as a
non-blocking implementation note in `limitations`; missing evidence for a self-created hypothetical
is not decision-relevant evidence. Specificity does not upgrade provenance.

Treat the supplied case commitments as authoritative. P0 may make them implementable but must not
invent production topology, consumers, capacity state, privacy properties, schema composition, or
new invariants and then use their absence as a blocker. A challenge that contradicts an explicit
case commitment requires supplied or verified counterevidence inside the packet. Noise notes remain
distractors.

For fixed-three-v1, an axis with no supplied/verified causal conflict still receives a complete
round record with an evidenced no-material assessment, but creates no terminal finding. Fixed still
reports `cycles_used=3`. For adaptive-axes-v1, a full initial axis inspection with no supplied or
verified material challenge routes zero cycles. Chief must approve a clean closed-world proposal
when no material finding remains; it may not defer for evidence needed only by hypothetical notes."""


def output_contract(
    case: dict[str, Any], protocol_id: str, run_id: str, materiality_contract_id: str
) -> str:
    if protocol_id == "adaptive-axes-v2":
        return f"""Return only the JSON object required by `e6_run_output_p5.schema.json`. Use
case_id `{case['case_id']}`, run_id `{run_id}`, protocol_id `adaptive-axes-v2`, and
materiality_contract_id `baseline-delta-ledger-v1`.

`baseline.literal_initial_proposal` must reproduce the supplied initial proposal exactly.
`delta_candidates` must contain every non-identical B0/Pn proposal delta, including candidates
Peer ultimately attests as non-relevant. Use local neutral `candidate_ref` and `finding_ref` values;
never invent gold issue IDs. A relevant/uncertain delta must link to a terminal finding. A
Peer-discovered finding may have `candidate_ref=null` but must retain `PEER_DISCOVERY` provenance.
All resolved and open findings remain terminal. `cycles_used` and
`cycle_accounting.substantive_cycles` must agree.

If real separate agents were not used, protocol mechanics were violated, a required delta/finding
link is missing, or terminal reconciliation is incomplete, set protocol_conformant=false and
audit_valid=false; never degrade the failure to empty findings plus approval."""
    return f"""Return only the JSON object required by the output schema. Use case_id
`{case['case_id']}` and run_id `{run_id}`. Never invent canonical issue IDs: `finding_ref` must be a
local neutral label such as FINDING-1. Include resolved and open terminal findings so a separate
grader can distinguish true detection, false no-material closure, and false duplicate closure.
`cycles_used` means completed substantive rounds/cycles and must be 3 for fixed-three-v1. If real
separate agents were not used, or protocol mechanics were violated, set protocol_conformant=false
and audit_valid=false."""


def build_prompt(
    case: dict[str, Any],
    protocol_id: str,
    run_id: str,
    materiality_contract_id: str = "legacy-v1",
) -> str:
    if protocol_id not in PROTOCOLS:
        raise ValueError(f"unknown protocol: {protocol_id}")
    if (protocol_id == "adaptive-axes-v2") != (
        materiality_contract_id == "baseline-delta-ledger-v1"
    ):
        raise ValueError("adaptive-axes-v2 requires baseline-delta-ledger-v1 and vice versa")
    public = json.dumps(public_case(case), ensure_ascii=False, indent=2, sort_keys=True)
    return f"""You are executing a blinded E6 conformance run, not designing the evaluation.

Read the required sana-debation skill contract completely before substantive work. If the installed
locator is outside the worker sandbox, read the byte-identical workspace snapshot `SKILL.md`
(expected SHA-256 `D7C599444A4E85FBB089DB7972D060537FB68DC21D6D3068929A95F31B9AD57F`)
instead and disclose that fallback in `limitations`; the snapshot changes reachability only.

Create three real, separate core subagent threads: Proposing TL, Peer TL, and a fresh Chief
Architect. Give each a role-specific contract. Preserve normal isolation: Peer must not receive a
preferred answer before its first inspection; Chief must receive no proposal, debate history, or
preferred outcome before the handoff defined by the selected protocol. For fixed-three-v1 that is
one complete-record handoff after round 3. For adaptive-axes-v1 it is a blind terminal scan followed
by full-record reconciliation. Do not use roleplay in one context. Do not add specialists.

This run is governed by `{protocol_id}` even if an installed skill has a different default:
{protocol_contract(protocol_id)}

This run also uses materiality contract `{materiality_contract_id}`:
{materiality_contract(materiality_contract_id)}

Case chronology (intentionally contains no expected labels or grading answer):
{public}

Execution budget (identical for both protocols): treat the case contract as a closed world; do not
browse or inspect unrelated workspace files after reading required skill contracts. Keep P0 under
700 words, each Peer challenge/inspection under 450 words, each Proposing response under 350 words,
each Peer closing under 250 words, and the Chief artifact under 700 words. Prefer compact structured
records. These are output ceilings, not permission to omit a required failure trace, falsifier,
proposal diff, protocol-defined terminal check, or binding disposition. Fixed-three-v1 has no Peer
terminal-reconciliation stage; a finding first introduced by its one-stage Chief uses
`CHIEF_DECISION`. Adaptive terminal Peer findings use `TERMINAL_RECONCILIATION`, while findings from
its two Chief stages use `CHIEF_STAGE_1` or `CHIEF_STAGE_2`.

Treat every `revision_sequence` entry as a mandatory chronological proposal mutation. The Root
orchestrator must ensure all listed mutations are present in the terminal proposal even if an
adaptive inspection initially finds no material issue. This prevents early stopping from hiding a
scheduled regression. Noise notes are context distractors, not findings.

{output_contract(case, protocol_id, run_id, materiality_contract_id)}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--protocol", choices=sorted(PROTOCOLS), required=True)
    parser.add_argument(
        "--materiality-contract",
        choices=sorted(MATERIALITY_CONTRACTS),
        default="legacy-v1",
    )
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    print(
        build_prompt(
            load_case(args.cases, args.case_id),
            args.protocol,
            args.run_id,
            args.materiality_contract,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
