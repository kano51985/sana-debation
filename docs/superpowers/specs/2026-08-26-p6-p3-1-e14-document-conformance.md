# P6 P3.1 E14 design and fixture-plan conformance record

Date: 2026-08-26

Scope: document-only E14 compatibility/root-carriage design and read-only fixture planning. No fixture
bytes, corpus directory, executable schema, validator, result packet, authorization object, native
approval, EA0, L0, EA1, E10, E11, E13, L2, network, model, signing, configuration, or production
action occurred.

## Approved design choice

The user approved the matrix-first static corpus approach.

Rejected as the primary approach:

- producing full authorization-shaped golden bundles before compatibility boundaries are proven;
- using property generation as the only oracle.

The selected baseline has 48 mandatory clause-coverage cases. This is a bounded contract inventory,
not a statistical sample or generalization claim.

## Controlling predecessors preserved

| File | SHA-256 before | SHA-256 after | Result |
|---|---|---|---|
| 2026-08-26-p6-evidence-proposal-p4-design-p3-1.md | B6DBE2702C6CBB0CA69E3BAF2F595DB8E4D57ADA8BC23B810DFF109955EC6E20 | B6DBE2702C6CBB0CA69E3BAF2F595DB8E4D57ADA8BC23B810DFF109955EC6E20 | unchanged |
| 2026-08-26-p6-evidence-proposal-p4-ne1-ne5-acquisition-plan-p3-1.md | C3ECEB8CB3E47EADA03A85F3479EA7EED9D668C507F53231225349BB1933D5DA | C3ECEB8CB3E47EADA03A85F3479EA7EED9D668C507F53231225349BB1933D5DA | unchanged |
| 2026-08-26-p6-evidence-proposal-p4-p3-1-conformance.md | 3CAE47A62B2B5DD4A3BED7108CB61E827F511439D1643E813311CBA6544F48FA | 3CAE47A62B2B5DD4A3BED7108CB61E827F511439D1643E813311CBA6544F48FA | unchanged |

## New document artifacts

| File | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| 2026-08-26-p6-p3-1-e14-compatibility-root-carriage-design.md | 472 | 17,829 | 74F96D292B7D3B1E85E3EA0847ACB9DB39798930D9D15ADE65AFEE125B2DF2F8 |
| 2026-08-26-p6-p3-1-e14-read-only-fixture-plan.md | 410 | 16,865 | EADD0BD6FE58CF2243ED2B365A3B1F52BF80D26EE2A3642E227826928402D9D1 |

## Primary-standard trace

The design references:

- RFC 8785, JSON Canonicalization Scheme:
  https://www.rfc-editor.org/rfc/rfc8785.html
- RFC 7493, The I-JSON Message Format:
  https://www.rfc-editor.org/rfc/rfc7493.html
- verified RFC 8785 errata:
  https://www.rfc-editor.org/errata/rfc8785

The fixture plan includes:

- recursive property sorting and preserved array order;
- unchanged string data without Unicode normalization;
- invalid UTF-8 and lone-surrogate rejection;
- duplicate-member and out-of-domain input rejection;
- negative-zero rejection based on the verified RFC 8785 erratum.

## Case-count conformance

| Family | Count |
|---|---:|
| JCS and I-JSON | 12 |
| Envelope and typed root | 4 |
| Role mapping | 4 |
| Binding and graph closure | 10 |
| Capability, schema, and fallback | 6 |
| Native approval-root carriage | 4 |
| Output closure | 4 |
| Failure algebra | 2 |
| Metamorphic checks | 2 |
| Total | 48 |

Forty-eight unique case IDs were found. Every expected family is present. No case expects
ACTIVATED_FINAL.

## E14 contract conformance

- Every future fixture has authority_effect = NONE.
- E13 absence is preserved: approval cases test missing or mismatched carriage only.
- The plan contains no positive activation oracle.
- Canonical bytes and graph order require two separately implemented verification paths.
- Path separation is reported as implementation separation, not cognitive independence.
- The system under test cannot be its sole oracle.
- Exact byte inputs remain authoritative over display renderings.
- Detail codes remain subordinate to the inherited top-level tuple.
- Claim and fence detail encoding remains behaviorally gated by E11.
- E14 reports PASS, FAIL, or INCONCLUSIVE and never grants a next stage.
- No partial PASS, averaging, or majority threshold is permitted.

## Mechanical checks

- Both documents contain zero trailing-whitespace lines.
- Both documents contain zero merge-conflict markers.
- Both documents contain zero unfinished-work markers from the configured scan.
- The plan names one future absent corpus root but creates no such directory or file.
- No file matching a planned E14 corpus artifact was found.
- No existing P3.1 predecessor hash changed.

## Authorization result

The E14 design and read-only fixture plan are complete as documents. They do not satisfy E14 itself.

The next possible action is a separately authorized fixture-construction proposal that freezes the
exact corpus root, file list, tools, primary-source snapshots, two verifier paths, numeric caps,
network NONE, retention, and prohibitions. That future authorization may create inert fixture bytes
only; it cannot activate a P3.1 final or run EA0/EA1 work.
