# Operator-Comprehension Instrument

Status: **prepared; no respondents collected**

Present the six items in randomized order without showing the expected answer. For each item, ask
the operator to select the protocol that will run and whether substantive work begins.

| Item | Invocation | Expected protocol/outcome |
|---|---|---|
| O1 | `use sana-debation for this decision` | `fixed-three-v1`; begins |
| O2 | `run a three-round debate` | `fixed-three-v1`; begins |
| O3 | `请运行三轮辩论` | `fixed-three-v1`; begins |
| O4 | structured `protocol=adaptive-axes-v1` | `adaptive-axes-v1`; begins |
| O5 | `run a three-round debate` plus structured `protocol=adaptive-axes-v1` | `PROTOCOL_SELECTION_CONFLICT`; no substantive work |
| O6 | structured `protocol=adaptive-latest` | `UNKNOWN_PROTOCOL`; no substantive work |

Collect the answer, explanation, response time, and whether the operator expected zero-cycle
adaptive completion to count as “three rounds.” Do not reveal the resolver table until all answers
are frozen. Report raw responses; this package defines no unsupported pass-rate threshold.

The deterministic resolver tests establish machine semantics, not human comprehension. Until real
responses are collected, the operator portion of E7 remains incomplete.
