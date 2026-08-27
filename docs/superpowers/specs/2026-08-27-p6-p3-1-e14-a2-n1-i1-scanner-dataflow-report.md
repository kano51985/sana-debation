# E14 P3-N1 I1 scanner dataflow report

Date: 2026-08-27

Status: **FAIL — I1_FAIL_STOP**

This is an evidence failure, not an execution incident. The production scanner treated every
adversarial sample as source bytes and never executed it. The failure is that its Node/Python
source-closure analyzers accepted patterns which could perform dynamic behavior if the analyzed
package were later run, while still returning an `ABSENT_BY_*_SCAN` closure claim.

The evidence run did not modify the production scanner, create a new scanner hash, issue an N1
artifact, or authorize I2.

## Frozen target

The exact scanner remains:

```text
src/e14_admission.py
D8D51375723E8B705736CD9492825FCE03BC65CDACCE0DD6BE7791E3E51259C7
```

This equals the existing G1 production-freeze hash. Static inventory found no scanner-source
execution, network, subprocess, native/deserializer, or filesystem-mutation sink. The trusted
callback manifest records the local JSON pairs hook, CPython email header factory, fixed codec
registry, and ambient interpreter hooks. None is selected by vendor bytes; the host interpreter
and standard library remain explicit TCB.

## Negative result

The corpus contains seven attack families in both Node and Python. Required outcome: 14 rejects.
Actual outcome: 5 rejects and 9 unexpected accepts.

Unexpected accepts:

- Node: aliased `eval`, reflected `Function`, deserializer callback, indirect native load, indirect
  subprocess resolution, and scanner-output-driven re-entry;
- Python: aliased `eval`, reflected `exec`, and scanner-output-driven global dispatch.

The direct Node dynamic import and direct Python `compile` cases were rejected. Python imports of
`pickle`, `ctypes`, and `subprocess` were also rejected by the external-import allowlist. These five
successes do not compensate for the nine gaps.

The negative cases are synthetic capability probes. This report does not assert that the two
currently frozen RFC 8785 vendor packages contain any of the accepted patterns. It shows that the
analyzer is not strong enough to prove their absence for the required language family.

## Reproducible evidence

- `evidence/n1/scanner-data-nonexecution-policy-v1.json`
- `evidence/n1/trusted-callback-manifest-v1.json`
- `evidence/n1/scanner-dataflow-review-v1.json`
- `fixtures/e14_n1_scanner_dataflow_cases_v1.json`
- `tools/e14_n1_dataflow_audit.py`
- `tests/test_e14_n1_scanner_dataflow.py`

Artifact hashes:

```text
tools/e14_n1_dataflow_audit.py
  1E141E05496018499327B96E17168F67DF7566C7D6FEB4EE32C26384B58B4DF2
fixtures/e14_n1_scanner_dataflow_cases_v1.json
  5A1B5A8890B418A700E4D0F51697C036371C399DA0F505810D9FE2235699408C
tests/test_e14_n1_scanner_dataflow.py
  AB73D9B1EF199D10493135CBD6C10421E59E40261C00F4CF13178940B2C8299F
evidence/n1/scanner-dataflow-review-v1.json
  9BC16CD18FC0D2672C6D9C12E4EAD21D03246B377F5AC918358B9654E40A9971
```

Seven focused I1 evidence tests pass. A passing test suite means the audit and fail-stop result are
reproducible; it does not convert the I1 gate itself into PASS.

## Binding stop and remediation boundary

I2 remains blocked. The scanner must not be silently patched inside this evidence run. A future
remediation must choose and review a language-analysis strategy, version the analyzers and claims,
produce a new production scanner hash and freeze manifest, rerun physical/archive regression, and
then rerun this unchanged negative corpus. No earlier G1 evidence may be rewritten in place.
