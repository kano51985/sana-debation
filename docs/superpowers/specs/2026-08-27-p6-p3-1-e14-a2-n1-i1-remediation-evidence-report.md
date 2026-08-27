# E14 P3-N1 I1 remediation evidence report

Date: 2026-08-27

Status: **DEFER_PENDING_NAMED_EVIDENCE**

This report records nonauthoritative preactivation evidence. It does not modify the
production scanner, issue or activate G1, acquire a parser dependency, authorize I2, or
execute vendor source.

## Bundle results

| Bundle | Status | Root |
|---|---|---|
| `OBLIGATION_COVERAGE` | `INCONCLUSIVE` | `sha256-e14-n1-i1-evidence-v1:27E284FA962E39077571BAFFEFD531A37F5240E44006B7D4FA7BF4D965FD19FD` |
| `HERMETIC_DIAGNOSTIC` | `NOT_RUN` | `sha256-e14-n1-i1-evidence-v1:85797923307A0B345BC9D0C90D96FB9BD1B7B103EF28B4C9C9BBBA13D4D71741` |
| `FREEZE_REPRODUCTION` | `PASS` | `sha256-e14-n1-i1-evidence-v1:05E526551482BADE0D1DB5E81B84F44E79D46AD37F82A03A72DF047E37EA5B6F` |
| `LIFECYCLE_AUTHORITY` | `INCONCLUSIVE` | `sha256-e14-n1-i1-evidence-v1:BBDB9189C7C53D37163741FBF1F62E9B1134F32096B15BF6FD27EE2C71D9155F` |
| `ROUTING_COMPATIBILITY` | `PASS` | `sha256-e14-n1-i1-evidence-v1:038F5BB152A737DA7682A7C72A3AE178C84B5E15FDA028C548BA7BE5697656A0` |
| `CONSUMER_CONFORMANCE` | `PASS` | `sha256-e14-n1-i1-evidence-v1:AFE60B2837279ED961A1E6E806D680ECBDF4E2D8AB7C6165BB60CDEB25EDEA2D` |
| `I2_AUTHORIZATION_CONTROL` | `PASS` | `sha256-e14-n1-i1-evidence-v1:C6FDE4BFF4D8249598D3460DD766CB7361BB0D0AA97E3B68FEB05F9F637D6CA9` |
| `ROLLBACK` | `PASS` | `sha256-e14-n1-i1-evidence-v1:1065F079A53507121B59FA12FC6AAC6F700FDD098D5688DACD32EFB6B90D0EC6` |
| `DEPENDENCY_APPROVAL` | `NOT_RUN` | `sha256-e14-n1-i1-evidence-v1:F2D0F87C53014363147BB05B80A61563C3BAFF82933804EC981CB6326D243DC9` |

## Decisive observations

- The original scanner, G1 freeze, failed I1 review, and 14-case corpus remain byte-exact.
- The new direct diagnostic rules block all 14 frozen source cases without archive identity checks.
- Obligation coverage remains `INCONCLUSIVE` because no v2 scanner or independently complete reachability basis exists.
- Real Node/Acorn closure remains `NOT_RUN`; only the dependency-free supervisor fault model was exercised.
- Synthetic G1 reproduction, routing, consumer, I2-control, and rollback models pass their frozen cases.
- Real lifecycle authority roles/current-state custody remain `INCONCLUSIVE`.
- The dependency decision remains `NOT_RUN`; generalized language-safety claims remain forbidden.

## Decision effect

The Chief deferral is not lifted. `next_stage_authorized=false` for every bundle. A fresh
Chief adjudication is required after the unresolved real toolchain, v2 scanner coverage,
lifecycle authority, and dependency evidence is separately authorized and produced.
