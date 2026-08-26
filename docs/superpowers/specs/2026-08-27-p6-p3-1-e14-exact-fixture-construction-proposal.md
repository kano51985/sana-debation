# P6 P3.1 E14 exact fixture-construction proposal

Date: 2026-08-27

Status: proposal only; reviewed direction, not execution authority.

This document freezes a staged route for acquiring, admitting, constructing, sealing, and later
executing the E14 compatibility corpus. It does not download a package or standard, create an E14
directory, extract or import third-party code, create fixture bytes, run a verifier, or produce an
E14 result.

The user's confirmation authorizes this proposal document only. Every state-changing stage below
requires a later, stage-specific authorization that binds the then-known hashes. No stage may
automatically start the next stage.

## Decision

Use a two-lineage, two-phase verifier supply path followed by a fully offline fixture path:

1. acquire two exact official package artifacts and four primary-standard snapshots into a sealed
   download-only root;
2. after the user reviews the actual archive and response hashes, inspect and admit them offline;
3. after the admitted source roots, builder bytes, wrapper bytes, and caps are all known and
   separately approved, construct and seal the 48-case corpus offline;
4. after the corpus root is reviewed and separately approved, execute both verifiers and compare
   their results offline.

The selected decisive JCS implementations are:

| Path | Package | Version | Runtime | Published claim | Admission stance |
|---|---|---:|---|---|---|
| A | npm `canonicalize` | 4.0.0 | Node.js | RFC 8785, Apache-2.0, zero dependencies | Untrusted until offline admission |
| B | PyPI `rfc8785` | 0.1.4 | CPython | pure Python RFC 8785, Apache-2.0, no runtime dependencies | Untrusted until offline admission |

They have different languages, package registries, repositories, owners, source roots, runtime
entry points, and decisive canonicalizer code. This establishes observable implementation-path
separation. It does not establish cognitive independence or prove that agreement is correct.

The Python project discloses that portions are adapted from Andrew Rundgren's reference
implementation, while the Node package is maintained by an RFC 8785 co-author. The two paths may
therefore share specification lineage even though their executable source roots differ. E14 must
report this limitation; the frozen RFC/errata oracle and independent P3.1 graph review remain
decisive when both paths agree.

## Controlling inputs

| Artifact | SHA-256 |
|---|---|
| P3.1 authorization-DAG design | B6DBE2702C6CBB0CA69E3BAF2F595DB8E4D57ADA8BC23B810DFF109955EC6E20 |
| P3.1 acquisition amendment | C3ECEB8CB3E47EADA03A85F3479EA7EED9D668C507F53231225349BB1933D5DA |
| P3.1 conformance record | 3CAE47A62B2B5DD4A3BED7108CB61E827F511439D1643E813311CBA6544F48FA |
| E14 compatibility/root-carriage design | 74F96D292B7D3B1E85E3EA0847ACB9DB39798930D9D15ADE65AFEE125B2DF2F8 |
| E14 read-only fixture plan | EADD0BD6FE58CF2243ED2B365A3B1F52BF80D26EE2A3642E227826928402D9D1 |
| E14 document conformance record | FA004C4E5B86389EE48D6563FE6D43999F2E2FF258640824AF9AE2A7424E9FBF |

All predecessor documents remain immutable. This proposal refines the future physical result
topology to satisfy the existing 160-object ceiling; it does not change E14 semantics, cases,
expectations, or authority boundaries.

## Exact reserved roots

All paths below are reservations. The common `e14` parent was absent at proposal time.

| Purpose | Exact future root |
|---|---|
| Download-only acquisition | `C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\vendor-acquisition-v1` |
| Offline vendor admission | `C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\vendor-admission-v1` |
| Builder and verifier wrappers | `C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\verifier-build-v1` |
| Sealed fixture corpus | `C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\p31-compat-corpus-v1` |
| Sealed verifier results | `C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\p31-compat-run-v1` |

Every stage uses create-new-only semantics. If its exact output root exists, that stage stops before
writing with `ROOT_ALREADY_EXISTS`. No overwrite, merge, resume-in-place, cleanup, or delete is
authorized. A replacement requires a new versioned root and a new authorization.

## Exact primary identities

### Path A: Node.js

- package identity: `npm:canonicalize@4.0.0`;
- metadata URL: `https://registry.npmjs.org/canonicalize/4.0.0`;
- archive URL: `https://registry.npmjs.org/canonicalize/-/canonicalize-4.0.0.tgz`;
- repository identity: `https://github.com/erdtman/canonicalize`;
- expected license declaration: `Apache-2.0`;
- expected runtime dependency count: zero;
- runtime executable:
  `C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe`;
- observed runtime version: `v24.19.0`;
- observed runtime SHA-256:
  `3602F2BB1A10F2CBAB4C36886218A33C1AB3DB87290E73B033C46C77147D0237`.

The npm archive SHA-256 is intentionally not guessed. The acquisition receipt must record the
registry's `dist.integrity` and `dist.shasum`, recompute SHA-256 over the received bytes, and bind all
three values. A later user authorization must approve the recomputed SHA-256 before extraction.

### Path B: CPython

- package identity: `pypi:rfc8785==0.1.4`;
- metadata URL: `https://pypi.org/pypi/rfc8785/0.1.4/json`;
- selected artifact: `rfc8785-0.1.4-py3-none-any.whl`;
- artifact URL:
  `https://files.pythonhosted.org/packages/4d/78/119878110660b2ad709888c8a1614fce7e2fab39080ab960656dc8605bf6/rfc8785-0.1.4-py3-none-any.whl`;
- registry-published artifact size: `9240` bytes;
- registry-published artifact SHA-256:
  `520D690B448ECF0703691C76E1A34A24DDCD4FC5BC41D589CB7C58EC651BCD48`;
- repository identity: `https://github.com/trailofbits/rfc8785.py`;
- expected license declaration: `Apache-2.0`;
- expected runtime dependency count: zero;
- runtime executable:
  `C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`;
- observed runtime version: `Python 3.12.13`;
- observed runtime SHA-256:
  `D8E3F0ADF246DB00358C0C4ED349CF714898178F9558FB0E944F79F5C07F8EAA`.

The wheel is selected instead of an sdist so no build backend or installation step is required.
Offline admission extracts ordinary files only and later executes directly from the admitted tree.

### Primary-standard snapshots

The acquisition stage proposes four immutable response objects:

| ID | Exact URL | Use |
|---|---|---|
| RFC8785-TXT | `https://www.rfc-editor.org/rfc/rfc8785.txt` | JCS base text and vectors |
| RFC7493-TXT | `https://www.rfc-editor.org/rfc/rfc7493.txt` | I-JSON constraints |
| RFC8785-E7920 | `https://errata.rfc-editor.org/eid7920/` | verified negative-zero technical erratum |
| RFC8785-E6292 | `https://errata.rfc-editor.org/eid6292/` | verified section-reference editorial erratum |

The downloaded bytes, final URL, retrieval time, status, media type, response length, and SHA-256
must be preserved. The source index must distinguish the immutable RFC publications from mutable
HTTP retrieval metadata. Later fixture construction uses only the locally admitted snapshots.

## Stage and authorization DAG

```text
this proposal
    -> A0 exact acquisition-manifest authorization
    -> A1 download-only acquisition
    -> G1 user review of received hashes
    -> A2 offline archive/snapshot admission
    -> G2 user review of admitted source/dependency roots
    -> B0 exact builder/wrapper authorization
    -> F0 offline fixture construction
    -> G3 user review of the sealed corpus root
    -> R0 offline dual-verifier execution
    -> E14 PASS / FAIL / INCONCLUSIVE evidence packet
```

Every arrow is a review dependency, not automatic authority. `A1`, `A2`, `F0`, and `R0` each require
a fresh user authorization. Failure or expiry at one node leaves all later nodes unauthorized.

### A0/A1: download-only acquisition

The future `AcquisitionManifest` must bind:

- all eight exact requested URLs: two package metadata objects, two package artifacts, and four
  standard objects;
- the exact downloader executable, arguments or script bytes, and SHA-256;
- the output root, request budget, byte budget, host allowlist, redirect policy, TLS policy, expiry,
  and stop rules;
- create-new-only behavior and a no-execution declaration.

Allowed hosts are exactly:

- `registry.npmjs.org`;
- `pypi.org`;
- `files.pythonhosted.org`;
- `www.rfc-editor.org`;
- `errata.rfc-editor.org`.

Only HTTPS GET is allowed. Authentication, cookies, upload methods, package-manager commands,
Git operations, repository checkout, proxy credentials, and redirects outside the allowlist are
forbidden. Automatic decompression, archive extraction, package installation, package lifecycle
scripts, module import, and test execution are forbidden.

Proposed A1 numeric caps:

| Dimension | Cap |
|---|---:|
| Required successful payloads | exactly 8 |
| HTTP exchanges including redirects | 16 |
| Redirects per requested object | 2 |
| Concurrent requests | 1 |
| Response bytes per object | 1 MiB |
| Total response bytes | 8 MiB |
| Output files | 32 |
| Total output bytes | 16 MiB |
| Processes | 1 |
| Wall time | 180 seconds |
| CPU time | 120 seconds |
| Peak memory | 256 MiB |
| Captured stdout | 128 KiB |
| Captured stderr | 128 KiB |

The proposed acquisition executable is PowerShell only:

- path:
  `C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe`;
- version: `PowerShell 7.6.4`;
- SHA-256: `DB6DD81183FE57D22E03B911EC9A30A2FD7C40542E97743615355A6FB44F458F`.

The actual acquisition runner bytes do not yet exist and therefore cannot yet be authorized. A0
must bind those exact bytes before A1. The runner must disable automatic redirects, validate every
redirect target before following it, stream into create-new files, enforce length while streaming,
and hash the final received bytes.

### G1: received-hash review

A1 may produce evidence only. It cannot start A2. G1 requires the user to review an inventory that
contains, for every object:

- requested and final URL;
- response and redirect facts;
- exact byte count;
- SHA-256 of received bytes;
- registry integrity fields where present;
- package name/version parsed without importing package code;
- acquisition terminal state and any discrepancy.

Any missing object, unexpected redirect, metadata/artifact identity mismatch, byte-cap event, digest
mismatch, or ambiguous HTTP result makes acquisition `INCONCLUSIVE` and blocks admission.

### A2: offline admission

A2 has `network = NONE`. It may read only the sealed A1 root and the exact admission-tool bytes
authorized after G1. It must not execute or import package code.

Archive admission rejects:

- absolute, drive-qualified, UNC, or parent-traversing paths;
- symlink, hardlink, junction, reparse-point, device, FIFO, socket, or other non-regular members;
- duplicate normalized names and Windows case-fold collisions;
- alternate data streams and reserved Windows device names;
- encrypted members, unsupported compression, decompression bombs, or cap violations;
- package name/version drift;
- any runtime dependency, peer dependency, optional dependency, or bundled dependency not
  explicitly accepted by a later amendment;
- any npm install/publish hook named `preinstall`, `install`, `postinstall`, `prepare`, `prepublish`,
  or `prepublishOnly`; all other declared scripts are recorded but never executed;
- license declaration or license-file mismatch;
- archive bytes that do not match the G1-approved hash.

Proposed A2 numeric caps:

| Dimension | Cap |
|---|---:|
| Input files | 32 |
| Input bytes | 16 MiB |
| Archive members | 512 |
| Expanded regular files | 512 |
| Expanded bytes | 32 MiB |
| Path depth | 12 |
| Single expanded file | 2 MiB |
| Processes | 1 |
| Wall time | 120 seconds |
| CPU time | 120 seconds |
| Peak memory | 512 MiB |
| Output files | 520 |
| Total output bytes | 40 MiB |
| Network | 0 requests / 0 bytes |

A2 emits a `VendorBundleManifest` binding raw archive roots, extracted file roots, normalized path
inventory, package metadata, dependency inventory, lifecycle-script inventory, license evidence,
source-root calculation, tool identity, and terminal state. It cannot label a bundle admitted unless
all mandatory checks pass.

### G2/B0: admitted-root and tool review

G2 must approve the exact admitted Node and Python source roots. Only after G2 may a builder and two
thin verifier wrappers be prepared as a separate non-executing artifact. B0 must then bind:

- every builder and wrapper path, byte length, and SHA-256;
- the exact admitted source roots and runtime executable hashes;
- wrapper entry commands and environment variables;
- parser, canonicalizer, graph-order, hashing, and comparison dependency disclosures;
- all F0 and R0 caps and prohibitions.

Wrappers may adapt input/output shape only. They may not repair input, normalize Unicode, suppress
errors, synthesize missing fields, share decisive graph-order code, call one another, or download
anything. Path A and Path B must each implement P3.1 graph validation and Kahn ready-set ordering in
separate source files with distinct roots.

## F0: offline fixture construction

F0 has `network = NONE` and does not execute Path A or Path B. It constructs goldens from the frozen
local specifications, admitted standard snapshots, exact case catalog, and small hand-auditable P3.1
graphs. RFC-derived vectors use the RFC or verified erratum as the primary oracle. P3.1-derived
expectations require an independent review record before sealing.

The fixture builder and oracle reviewer are not either compatibility verifier. Dual-verifier
agreement is never allowed to create or silently update `expected.json`.

### Exact corpus file inventory

The corpus contains exactly 154 regular files:

| Group | File rule | Count |
|---|---|---:|
| Root control | `corpus-manifest.json`, `clause-coverage.json`, `detail-code-registry.json`, `construction-ledger.lfr`, `terminal-seal.json` | 5 |
| Source identity | `standards/source-index.json`, `vendor/node-identity.json`, `vendor/python-identity.json` | 3 |
| Verifier identity | `verifier-a/identity.json`, `verifier-b/identity.json` | 2 |
| Case artifacts | `cases/<case-id>/case.json`, `cases/<case-id>/input.bin`, `cases/<case-id>/expected.json` | 144 |
| Total |  | 154 |

`<case-id>` expands to exactly this ordered set:

```text
JCS-01 JCS-02 JCS-03 JCS-04 JCS-05 JCS-06 JCS-07 JCS-08 JCS-09 JCS-10 JCS-11 JCS-12
ENV-01 ENV-02 ENV-03 ENV-04
ROL-01 ROL-02 ROL-03 ROL-04
GRF-01 GRF-02 GRF-03 GRF-04 GRF-05 GRF-06 GRF-07 GRF-08 GRF-09 GRF-10
CAP-01 CAP-02 CAP-03 CAP-04 CAP-05 CAP-06
APR-01 APR-02 APR-03 APR-04
CLS-01 CLS-02 CLS-03 CLS-04
ALG-01 ALG-02
MET-01 MET-02
```

No additional corpus file is permitted. Directories do not count as objects but must match the
listed topology exactly. Source snapshots and admitted package files stay in their separately sealed
roots and are referenced by root; they are not copied into the corpus.

### Exact case rules

For every case:

- `case.json` contains descriptive contract fields, clause trace, one primary causal distinction,
  risk IDs, oracle method, and `authority_effect = NONE`;
- `input.bin` is the only authoritative input byte sequence;
- `expected.json` contains the exact expected parse, canonical bytes or rejection, typed content
  root, role, graph, capability, activation, subordinate detail, inherited tuple, closure, and
  limitation fields;
- display text is derivative and must not replace `input.bin`;
- no expected result is `ACTIVATED_FINAL`;
- every final-shaped fixture uses only synthetic non-filesystem identifiers and remains
  `FINALIZED_NOT_AUTHORIZED` or an earlier rejection;
- no file contains a live approval, credential, production identifier, real filesystem target,
  user text, holdout, oracle secret, script, executable, symlink, external include, or reparse point.

### Manifest and seal rules

All JSON control objects must be strict UTF-8 without BOM, duplicate names, comments, or trailing
data. Their canonical identity uses JCS over the parsed object. A manifest cannot include its own
root.

`construction-ledger.lfr` uses this exact framing:

```text
E14-LFR-1\n
<eight lowercase hexadecimal byte-length digits>\n
<that many UTF-8 bytes containing one JCS JSON object>\n
```

There are exactly 48 case-construction records in case-ID order. The ledger is an audit record, not
an oracle and not executable input.

`terminal-seal.json` binds an ordered inventory of every other corpus-relative path, file length,
and SHA-256. The inventory is sorted by ordinal UTF-8 bytes of normalized forward-slash paths. The
corpus content root is SHA-256 over the JCS encoding of that inventory. `terminal-seal.json` is
excluded from its own root and declares `authority_effect = NONE`.

### Proposed F0 numeric caps

| Dimension | Cap |
|---|---:|
| Source files read | 256 |
| Source bytes read | 16 MiB |
| Case directories | exactly 48 |
| Corpus files created | exactly 154 |
| Corpus bytes before raw run logs | 2 MiB |
| Single output file | 128 KiB |
| Temporary files | 32 |
| Temporary bytes | 4 MiB |
| Tool invocations | 4 |
| Concurrent processes | 1 |
| Total processes | 4 |
| Wall time | 300 seconds |
| CPU time | 300 seconds |
| Peak memory | 512 MiB |
| Captured stdout | 1 MiB |
| Captured stderr | 1 MiB |
| Network | 0 requests / 0 bytes |

F0 stops without a terminal seal if any count, byte, oracle, provenance, topology, or semantic rule
is unmet. A partial root is retained for audit and is not a corpus.

## G3/R0: sealed-corpus review and offline execution

G3 reviews the exact 154-file inventory, corpus content root, builder identity, source roots, oracle
review, and discrepancies. G3 does not start R0. R0 requires a fresh authorization that binds the
sealed corpus root, both wrapper roots, both runtime hashes, admitted dependency roots, exact entry
commands, absent run root, and numeric caps.

R0 reads the corpus and writes exactly five regular files:

| File | Records or purpose |
|---|---|
| `verifier-a-results.lfr` | exactly 48 Path A raw result records |
| `verifier-b-results.lfr` | exactly 48 Path B raw result records |
| `comparison.lfr` | exactly 48 expected/A/B comparison records |
| `e14-result.json` | complete decision packet and roots |
| `terminal-seal.json` | ordered inventory root of the other four files |

Each verifier is invoked once and processes all 48 cases sequentially. The comparator is a third,
non-deciding adapter: it performs byte and field equality checks against the frozen oracle and
cannot rewrite any result.

Proposed R0 numeric caps:

| Dimension | Cap |
|---|---:|
| Corpus files read | exactly 154 |
| Cases processed per verifier | exactly 48 |
| Verifier processes | exactly 2 |
| Comparator/seal processes | at most 2 |
| Concurrent processes | 1 |
| Total processes | 4 |
| Wall time | 300 seconds |
| CPU time | 300 seconds |
| Peak memory per process | 512 MiB |
| Captured stdout per process | 1 MiB |
| Captured stderr per process | 1 MiB |
| Run files created | exactly 5 |
| Run bytes | 4 MiB |
| Temporary files | 16 |
| Temporary bytes | 4 MiB |
| Network | 0 requests / 0 bytes |

The 154 corpus files plus 5 run files total 159 objects, remaining within the approved planning
ceiling of 160 corpus-and-result objects.

### Topology refinement P1

The read-only plan illustrated `results/<case-id>-a.json` and `results/<case-id>-b.json`. That would
produce at least 250 files when combined with the 144 required case files and therefore contradict
the same plan's 160-object ceiling.

This proposal resolves the contradiction without weakening evidence:

- per-case records remain complete and individually addressable by `case_id`;
- A results, B results, and comparisons use three deterministic length-framed ledgers;
- raw order is fixed to the 48-case catalog;
- every record is independently hashed in the result packet;
- the total becomes 159.

This is a physical-storage refinement only. It does not permit aggregation, majority voting,
omission, or partial PASS.

## Outcome and failure semantics

Acquisition, admission, and construction failures are pre-E14 failures. They never become E14 FAIL
or PASS and never change operational authority.

| Stage | Example typed failure | Required effect |
|---|---|---|
| A1 | `ACQUISITION_ROOT_EXISTS` | stop before write |
| A1 | `ACQUISITION_REDIRECT_FORBIDDEN` | stop; retain receipt; later stages unauthorized |
| A1 | `ACQUISITION_SIZE_CAP_EXCEEDED` | stop; mark acquisition INCONCLUSIVE |
| A1 | `ACQUISITION_METADATA_MISMATCH` | stop; mark acquisition INCONCLUSIVE |
| A1 | `ACQUISITION_REGISTRY_DIGEST_MISMATCH` | stop; mark acquisition INCONCLUSIVE |
| A2 | `VENDOR_ARCHIVE_HASH_MISMATCH` | reject bundle |
| A2 | `VENDOR_ARCHIVE_UNSAFE` | reject bundle |
| A2 | `VENDOR_DEPENDENCY_UNEXPECTED` | reject bundle |
| A2 | `VENDOR_INSTALL_HOOK_PRESENT` | reject bundle |
| A2 | `VENDOR_LICENSE_MISMATCH` | reject bundle |
| F0 | `CORPUS_ROOT_EXISTS` | stop before write |
| F0 | `CORPUS_FILE_LIST_MISMATCH` | no terminal seal |
| F0 | `CORPUS_ORACLE_UNAVAILABLE` | no terminal seal |
| F0 | `CORPUS_ORACLE_DISAGREEMENT` | no terminal seal; retain discrepancy |
| F0 | `CORPUS_AUTHORITY_SHAPED_INPUT` | no terminal seal |
| R0 | `VERIFIER_PATH_UNAVAILABLE` | E14 INCONCLUSIVE |
| R0 | `DEPENDENCY_IDENTITY_MISMATCH` | E14 INCONCLUSIVE |
| R0 | deterministic expected/actual mismatch | E14 FAIL |
| R0 | unsafe acceptance or activation | E14 FAIL |

For every P3.1 prelaunch case, the inherited tuple remains:

```text
execution_state = NOT_STARTED
outcome = INCONCLUSIVE
reason_code = PRELAUNCH_CHAIN_MISMATCH
decision_effect = LEAVES_NAMED_GAP_UNCHANGED
```

The E14 subordinate detail may vary but cannot replace a top-level field.

## Retention, expiry, and rollback

- Every authorization expires 24 hours after its explicit issuance unless it states an earlier
  time. Expiry never carries forward to a later stage.
- Raw HTTP bytes, receipts, archives, admitted sources, source inventories, fixtures, failed partial
  roots, raw verifier records, discrepancies, and terminal seals are retained until a later explicit
  disposal authorization.
- Rollback means withholding a root from the next stage. It never means editing a golden, deleting a
  failure, overwriting an existing root, falling back to another package/version, or changing P3.1.
- A changed package version, artifact hash, runtime hash, standard snapshot, wrapper, builder,
  fixture, expectation, cap, host, URL, command, or root requires a new proposal or explicit
  amendment and a new authorization.

## Prohibitions common to all future stages

- no model, plugin, MCP, browser automation, Git, package-manager install, or dynamic dependency
  resolution during acquisition, admission, construction, or execution;
- no `npm install`, `npm ci`, `npx`, `pip install`, build backend, lifecycle script, package test, or
  repository checkout;
- no secrets, credentials, signing, native approval creation, root reservation, claim, fence,
  network service, database, Redis, Model Gateway, or application API;
- no real authorization object, operational path, user content, production data, or holdout;
- no symlink, junction, hardlink, reparse traversal, external include, or output outside the exact
  stage root;
- no automatic retry after an ambiguous network result and no automatic progression between stages;
- no oracle update after verifier output; a correction creates a retained new corpus version;
- no inference from E14 to E13, E11, EA0, L0, EA1, L2, or production authority.

## Acceptance gates

This proposal is ready for user review when:

- the exact package identities, versions, official URLs, primary references, and current runtime
  hashes are named;
- unknown npm archive SHA-256 is explicitly deferred to A1/G1 rather than guessed;
- package acquisition, offline admission, offline fixture construction, and offline execution are
  separately authorized;
- the corpus inventory is exactly 154 files and the run inventory exactly 5 files;
- all 48 original case IDs remain mandatory;
- oracle separation, implementation-path separation, numeric caps, expiry, retention, typed
  failures, and common prohibitions are explicit;
- no package, snapshot, directory, fixture, wrapper, or result has been created.

The next allowable action after approving this proposal is to prepare the exact A0 acquisition
manifest and acquisition-runner bytes for review. Approval of this document alone still does not
authorize A1 or any network request.

## Self-review

- Four distinct future state-changing stages are separated by human review gates.
- The two decisive canonicalizers do not share language, registry, repository, source root, or
  runtime entry point.
- A recent Node release is treated as untrusted until content inspection, not trusted by popularity
  or registry presence.
- Registry digests are cross-checks; locally recomputed SHA-256 is the admitted byte identity.
- The Python wheel is pinned by official URL, size, and registry-published SHA-256.
- Both verifier paths remain systems under test and cannot be their own sole oracle.
- No positive activation case or operational authority enters the corpus.
- The P1 result-ledger refinement preserves per-case evidence while satisfying the 160-object cap.
- Every stage is bounded, fail-closed, create-new-only, and network-free except the separately
  authorized download-only A1 stage.
- This document creates no E14 artifact other than itself.
