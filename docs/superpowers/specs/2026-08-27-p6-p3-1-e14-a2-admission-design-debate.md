# E14 A2 offline admission design debate

Date: 2026-08-27

Chief disposition: **defer pending named evidence**

This was a read-only `sana-debation` core run. It changed no A2 code and created no admission root.

## 1. Execution audit

- execution: `real-subagents / core`;
- Proposing TL: `/root/e14_a2_proposing`, `fresh-thread`, separately instructed, completed;
- Peer TL: `/root/e14_a2_peer`, `fresh-thread`, separately instructed, completed;
- Chief Architect: `/root/e14_a2_chief`, `fresh-thread`, separately instructed, completed;
- Peer received only its readiness contract before P0;
- Chief received only its readiness contract before the three round records closed;
- no optional roles, candidate X0, retries, protocol failure, or root-authored substitute role;
- the host exposed four active slots and no reliable lifetime-quota reservation, so all three core
  identities were pre-created before substantive routing; and
- these facts demonstrate separately instructed execution and thread separation, not cognitive
  independence. The threads shared the workspace as an evidence surface.

## 2. Frozen decision frame

Decision: design the minimum safe A2 tool that reads the sealed
`e14/vendor-acquisition-v2` root and may produce a create-new
`e14/vendor-admission-v1` root. It must not execute or import package code or implement G2, B0, F0,
or R0.

The fixed attack axes were:

1. archive/path safety and two-pass extraction;
2. package metadata, dependency, license, and source-root semantics; and
3. runtime/offline trust, crash sealing, authority, operability, and proportionality.

The non-negotiable invariants were network `NONE`; exact sealed inputs; rejection of path, member,
link, device, encryption, compression, bomb, collision, and cap hazards; exact G1 hashes; no
unapproved declared or runtime dependency; package/license identity; validate-before-create;
exclusive creation; no overwrite or resume; deterministic roots and terminal receipts; authority
`NONE`; no automatic later stage; and immutable legacy roots.

## 3. Evidence ledger

| ID | Class | Evidence | Limitation |
|---|---|---|---|
| E1 | verified fact | A2 rules, caps, and failures in the controlling exact-fixture proposal | Design text, not implementation evidence |
| E2 | verified fact | G1 PASS; 20 files, 111,225 bytes; A1 terminal SHA-256 `33C3035DC90D7758A6D92BDE3D9CA629088AB94B1347881E929CEA21AED11879` | Establishes sealed inputs only |
| E3 | verified fact | npm tar has six regular members; `canonicalize@4.0.0`, Apache-2.0, no declared runtime/peer/optional/bundled dependency or prohibited hook | Benign sample does not prove parser safety or runtime closure |
| E4 | verified fact | wheel has seven regular deflated, unencrypted members; `rfc8785==0.1.4`; dependencies are extra-gated; Apache classifier/license | Metadata does not prove source-level dependency closure |
| E5 | verified fact | failed acquisition v1 is immutable; successful acquisition v2 exists; admission v1 is absent | No A2 effect yet |
| E6 | verified fact | no A2 implementation or execution envelope exists | Blocks implementation evidence |
| E7 | inference | interpreter/stdlib/assembly and ambient runtime closure are under-specified | Requires an explicit trust boundary |
| E8 | unresolved risk | exact parser, runtime, and enforcement profile | Decision-critical |
| E9 | product preference | prefer a minimal, single-process, deterministic design | Cannot weaken an invariant |

## 4. P0

P0 proposed a single Python 3.12.13 process launched with `-I -S -B`, plus immutable policy,
authorization, and runtime-closure inputs. It used two passes: pass 1 validates and creates a
logical extraction plan without output; pass 2 exclusively creates output while repeating every
check and matching the plan. It included strict npm/PyPI/wheel/RECORD/dependency/hook/license
checks, domain-separated source and bundle roots, terminal-last fail-closed handling, and separate
vendor-rejection versus operational-inconclusive codes.

## 5. Round 1 — physical archive safety

Peer showed that a normalizing tar API could consume PAX or GNU extension records internally and
expose only a safe effective regular member. Two passes through the same projection could agree and
still admit a physically prohibited archive. The falsifier `A1-PHYS-01` requires the production
parser to expose and reject every physical header, concatenated or trailing gzip, sparse/base-256,
and replay mutation.

The Proposing TL accepted the objection and issued P1:

- direct RFC 1952 framing with raw zlib deflate;
- exact EOF, CRC32, ISIZE, and final-trailer checks;
- a runner-owned 512-byte physical ustar scanner accepting only strict regular typeflag `0`;
- rejection of PAX, GNU longname/link, sparse, base-256, links, aliases, and unknown types;
- a physical header/payload/padding transcript root compared across both passes; and
- blocking adversarial tests against the exact production scanner.

Peer closing verdict: `modified`. R1 remains invariant-blocking until `A1-PHYS-01` passes.

## 6. Round 2 — dependency and source-root claims

Peer showed that clean declared metadata does not prove that source bytes lack undeclared,
conditional, or dynamic imports. A downstream run could fail offline or load an ambient component
even when npm/PyPI metadata and wheel `RECORD` agree. The falsifier
`A2-RUNTIME-CLOSURE-01` must bind each source root, runtime boundary, every syntactic reference,
dynamic-loading search, and unresolved finding.

The Proposing TL accepted the objection and issued P2:

- `declared_dependency_set` and `runtime_dependency_closure` are independent;
- a separately reviewed, source-root/raw-hash/bundle-root/runtime-bound attestation is mandatory;
- in-package references must resolve to the same inventory;
- bare references are not presumed built-in;
- the external allowlist is empty unless amended;
- dynamic loads must be absent or exact source-location/finite-target allowlisted; and
- unknown or incomplete closure produces a typed failure and cannot become success.

Peer closing verdict: `modified`. Root schemas, algorithms, file kinds, analyzers, and the
production-equivalent scanner must freeze before the pre-scan that produces attested roots.
Structural coverage must not be reported as semantic completeness. R7 remains invariant-blocking.

## 7. Round 3 — bootstrap and enforceable offline execution

Peer showed that Python cannot attest its own integrity before it begins executing and that source
review or selected DLL hashes cannot enforce network `NONE`. A replaced interpreter or native
dependency could create network or child-process effects before runner checks and then falsify
in-process evidence. The falsifier `A3-BOOT-NET-01` requires pre-launch measurement, network and
child denial from process creation, external module observation, and adversarial zero-packet
evidence.

The Proposing TL accepted the objection and issued P3:

- Python self-checks become observability only, not the trust root;
- a measured external envelope must establish image/input identity, read-only inputs, sole writable
  output, restricted token, pre-instruction network denial, child denial, and resource caps;
- the runner writes only a nonauthorizing `runner-terminal.json`;
- an externally measured and authorized finalizer alone may write `terminal-receipt.json`;
- the final receipt binds image/envelope measurements, exact inputs, process/module/network/child/
  resource observations, output inventory, and bundle manifest;
- missing evidence is `RUNTIME_ENVELOPE_UNPROVEN`; inconsistent evidence is
  `ENVELOPE_OBSERVATION_MISMATCH`; and
- unknown executable source kinds and semantically incomplete dependency analysis fail closed.

Peer closing verdict: `modified`. The external finalizer must itself be measured and authorized;
otherwise the bootstrap problem merely moves outward. R8 remains invariant-blocking.

## 8. Final P3 gates and risks

The final gate order is:

1. G0 — approve guest-process versus external-TCB cap accounting;
2. G1 — freeze schemas, codes, scanners, ZIP policy, file kinds, analyzers, roots, and production bytes;
3. G2 — pass `A1-PHYS-01` against the production scanner;
4. G3 — compute deterministic roots with that frozen scanner;
5. G4 — freeze dependency/extras/hooks/license policy and the named license decision;
6. G5 — pass `A2-RUNTIME-CLOSURE-01` with structural and semantic coverage;
7. G6 — provide a concrete measured execution envelope;
8. G7 — pass `A3-BOOT-NET-01` from process start;
9. G8 — bind G1–G7, A1/G1, and the absent output into fresh authorization; and
10. G9 — measure and authorize the external finalizer and its terminal-only effect.

R1, R7, and R8 remain invariant-blocking. R2 filesystem race and R6 crash handling are acceptable
only inside the verified envelope. R4 requires a named policy/legal decision because the Python
package supplies an Apache classifier and license bytes but no exact SPDX expression.

## 9. Chief Architect decision

Disposition: **defer pending named evidence**.

The Chief found P3 structurally implementable and traced every decisive change to a closed round,
but current evidence cannot rule out violations of network isolation, sealed-input trust, physical
archive rejection, or runtime dependency closure. No normalizing tar fallback, metadata-only
closure, ambient import assumption, Python self-attestation, runner-authored authoritative terminal,
overwrite, resume, or automatic progression is acceptable.

The next action is to prepare G0–G9 evidence and return the unchanged P3 plus that evidence to a
fresh Chief. The debate itself authorizes no code, envelope, admission execution, package execution,
or progression to G2/B0/F0/R0.

