# E14 P3-N1 I0 implementation report

Date: 2026-08-27

Status: **PASS — SOURCE ONLY**

This report records the bounded I0 implementation authorized by the hash-envelope correction
debate. It does not issue a lifecycle artifact, persist a root, contact a runtime, create a key,
grant a role, start a container, write a ledger, or authorize G8/G9.

## Pre-code gates

- The corrected five-field lifecycle-v2 schema binds `schema`, `artifact_kind`, `profile_kind`, and
  `payload` under a new domain and typed-root prefix.
- `tools/e14_n1_precode_audit.py` derives maximum shapes for all seven kinds. The largest is 67,399
  canonical bytes, depth 4, 290 nodes, 289 total members, and 128 members in one object. Every
  frozen cap passes, with at least two-times headroom for depth, nodes, members, and canonical bytes.
- The retirement inventory finds no issued or live root from the superseded draft. That draft is
  not accepted, converted, normalized, stripped, or re-rooted.

## Implemented surface

`src/e14_n1_artifacts.py` exports only:

- frozen nominal route, root, verified-artifact, revocation-snapshot, and use-result types;
- `verify_content(raw_bytes, explicit_route)`; and
- `evaluate_use(verified, now_utc, revocation)`.

The root and verified-artifact constructors reject direct public construction. Verification
requires the exact selector and media type before examining content. The production path uses a
purpose-built bounded raw-byte parser, not `json.loads`, a schema loader, or a generic normalizer.
It rejects BOM, invalid UTF-8, duplicates after key unescaping, arrays, floats, exponents, negative
zero, unsafe integers, malformed surrogates, non-ASCII keys, comments, trailing data, and resource
limit excesses.

The canonical encoder is deliberately private and supports only the frozen object/string/safe-
integer/boolean/null subset. Its output matches RFC 8785 for accepted values while preserving
Unicode without normalization. The verified payload is recursively read-only. Validity and
revocation evaluation receives explicit immutable inputs and grants no authority.

## Evidence

Focused tests: **27 passed, 0 failed**.

Repository tests: **119 passed, 0 failed**.

Additional deterministic differential check: 2,000 seeded restricted-JSON objects round-tripped
through the raw parser and matched an independent standard-library canonical oracle.

Frozen implementation hashes at completion:

```text
src/e14_n1_artifacts.py
  B0AD3752C263594819A22B84D0846E9A6ECC460DFC2912EC935192ECFA9067EC
tests/test_e14_n1_artifacts.py
  B73172382465D8585BBE15D0D392D81838443E94E6B2E6525D141B3EAF653390
schemas/e14-a2-n1-lifecycle-v2.schema.json
  FB1034063534C3461203A02D83A7203BF13B34E35067E985C3BF663BC5DFB711
```

## Remaining boundary

I0 proves local content verification semantics only. It does not prove scanner data
noninterpretation, an OCI final view, platform closure, output reservation, ledger durability,
exclusive start, role/key scope, replay resistance, live consumer routing, or terminal
finalization. Those remain I1 and later stages and cannot be inferred from an I0 PASS.
