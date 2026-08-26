# E14 N1 I0 hash-envelope correction debate

Date: 2026-08-27

Disposition: **APPROVE WITH REQUIRED CHANGES**. The pre-code gates below must pass before the pure
I0 verifier is implemented. This decision grants no operational or artifact-issuing authority.

## Trigger

The unissued lifecycle-v1 draft committed only `artifact_kind` and `payload`. Its top-level
`fixture_only`, top-level `authority_effect`, schema, and profile were outside the root. A consumer
could therefore observe a different operational classification without observing a different root.
The draft also duplicated `authority_effect` between envelope and payload.

No issued or live v1 N1 root existed. At repository commit
`50a78ab608f99f49d1869237e4179f5db82b78ff`, all v1 strings were confined to the specification,
schema, schema tests, and README index.

## Execution audit

- mode: `real-subagents/core`;
- Proposing TL: `/root/e14_i0_hash_proposing`;
- Peer TL: `/root/e14_i0_hash_peer`;
- Chief Architect: `/root/e14_i0_hash_chief`;
- each role used a fresh, separately instructed thread;
- Peer received only its role contract until P0 existed;
- Chief received only its readiness contract until all three rounds closed;
- no optional role, role retry, or protocol failure occurred; and
- this proves thread and instruction isolation only, not cognitive independence.

## Three-round record

| Round | Attack axis | Peer disposition | Binding correction |
|---|---|---|---|
| 1 | root identity and canonicalization | `modified`, then `accepted` | Replace v1 with v2. Commit exact `schema`, `artifact_kind`, `profile_kind`, and `payload`; use a new domain and typed-root prefix; reject v1 without migration. |
| 2 | fixture/operational consumer confusion | `modified`, then `accepted` | Remove top-level fixture/effect flags; require nominal lifecycle route, media type, API, verified type, and result type; prohibit generic normalization, wrapping, stripping, defaulting, conversion, and root-only trust. |
| 3 | bounded parsing, proportionality, and purity | `modified` | Claim only an RFC-8785-equivalent restricted subset; use a single-pass bounded raw-byte parser; freeze caps, error precedence, offsets, and pointers; separate pure content verification from explicit-time/revocation use evaluation. |

## Final v2 decision

The five-field envelope contains `schema`, `artifact_kind`, `profile_kind`, `content_root`, and
`payload`. The root commits the other four values under domain
`sana.e14.n1.lifecycle-artifact.v2\n` and prefix `sha256-jcs-e14-n1-v2:`. Arrays, non-ASCII keys,
floats, exponents, negative zero, duplicate keys, invalid UTF-8, BOM, comments, and trailing data
are rejected. Unicode string values are preserved without normalization.

The verification route is exactly selector `N1_LIFECYCLE_ARTIFACT_V2` and media type
`application/vnd.sana.e14.n1-lifecycle-artifact-v2+json`. Route and media failures precede raw
parsing. Content verification is pure and nonauthoritative. Time and revocation are explicit,
immutable inputs to a separate pure evaluation.

## Required pre-code gates

1. Freeze the corrected schema, envelope, canonical subset, hash domain, nominal routes, caps, and
   failure contract.
2. Produce a reproducible cap report showing every schema-valid shape is parser-admissible and
   safety caps retain at least two-times headroom.
3. Produce a repository-wide v1 retirement manifest and prove no issued/live v1 root exists.

These gates are satisfied by the corrected v2 schema, `tools/e14_n1_precode_audit.py`,
`evidence/e14-n1-v2-precode-cap-report-v1.json`, and
`evidence/e14-n1-draft-v1-retirement-v1.json` once their hashes and scans agree.

## Authorized implementation boundary

After the gates pass, I0 may add only pure nominal types, a bounded raw-byte parser, restricted
canonical encoder, root verifier, explicit routing, pure validity/revocation evaluation, and tests.
It must not add Docker, persistence, keys, ledger, network/filesystem integration, live roots,
operational routing, G8/G9 execution, or authority grant. Later N1 stages remain separately gated.
