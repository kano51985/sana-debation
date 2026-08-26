# P6 P3.1 E14 A0 acquisition materials static review

Date: 2026-08-27

Status: static review complete; A1 remains unauthorized.

## Scope

This record reviews the exact A0 manifest and download-only runner bytes without invoking the
runner. No network request, package download, archive extraction, module import, package script,
fixture creation, verifier execution, authorization receipt, or E14 execution root was created.

The approved bounded change produced only:

- an A0 review-only acquisition manifest;
- a PowerShell download-only runner source file;
- this static review record.

## Controlling proposal

| Artifact | SHA-256 |
|---|---|
| `2026-08-27-p6-p3-1-e14-exact-fixture-construction-proposal.md` | `43DB3ED4E57F71BA4CE58E3C0C4D22088E3F9A5905F74E369529B5D8409A74CD` |

The manifest binds this exact proposal root.

## Reviewed artifacts

| Artifact | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| `2026-08-27-p6-p3-1-e14-a0-download-only-runner.ps1` | 728 | 29,134 | `0232F074C4D328F49F5E1C765C0B97EE0DD1B0E89740EB26822DB8D69D1D500D` |
| `2026-08-27-p6-p3-1-e14-a0-acquisition-manifest.json` | 187 | 6,322 | `48AFFF7D04A6A3E665D63192BA97181FD80EB8A7981F514AC895FAD916D4CA9F` |

The manifest's `tool.runner_sha256` equals the reviewed runner hash.

## Static checks

| Check | Result |
|---|---|
| PowerShell AST parse errors | 0 |
| Manifest strict UTF-8 JSON parse errors | 0 |
| Manifest duplicate JSON member names | 0 |
| Required acquisition objects | 8 |
| Unique object IDs | 8 |
| Unique requested URLs | 8 |
| Allowed hosts | exactly 5 |
| Requested URL hosts outside allowlist | 0 |
| Successful output-file formula | 3 control + 16 object + 1 terminal = 20 |
| Manifest-declared successful output files | 20 |
| Forbidden command names found in runner AST | 0 |
| Trailing-whitespace lines | 0 |
| Merge-conflict markers | 0 |
| Configured unfinished-work markers | 0 |
| Network calls executed during review | 0 |
| Reserved `e14` root exists after review | false |

The forbidden-command scan included:

- `Invoke-WebRequest` and `Invoke-RestMethod`;
- `Start-Process`;
- `Remove-Item`, `Clear-Content`, `Set-Content`, and `Out-File`;
- `npm`, `npx`, `pip`, `git`, `ssh`, and `scp`.

The runner uses `System.Net.Http.HttpClient` only inside its guarded main path. Static review parsed
the file as source and did not enter that path.

`PSScriptAnalyzer` was not installed in the local bundled environment, so no result from that
optional analyzer is claimed. Native PowerShell AST parsing completed successfully.

## Bound identities and limits

The manifest binds:

- Node package `canonicalize@4.0.0` metadata and tarball URLs;
- Python package `rfc8785==0.1.4` metadata and the exact wheel URL;
- Python wheel size `9240` and registry-published SHA-256
  `520D690B448ECF0703691C76E1A34A24DDCD4FC5BC41D589CB7C58EC651BCD48`;
- RFC 8785 and RFC 7493 text snapshots;
- verified errata 7920 and 6292 snapshots;
- the five-host HTTPS allowlist;
- 8 successful payloads, 16 HTTP exchanges, at most 2 redirects per object, 1 MiB per response,
  8 MiB total response bytes, 32 output files, and 16 MiB total output bytes;
- one process, one concurrent request, 180 wall seconds, 120 CPU seconds, 256 MiB peak memory,
  and bounded stdout/stderr;
- the exact absent output root
  `C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\vendor-acquisition-v1`.

## Runner safety behavior

Before constructing an HTTP client, the runner requires and checks:

- a future `sana.e14.a1-authorization-receipt.v1` file;
- decision `APPROVE_A1_DOWNLOAD_ONLY` and effect `DOWNLOAD_ONLY`;
- exact manifest, runner, PowerShell executable, and output-root bindings;
- UTC issue and expiry times with at most 24 hours validity;
- the exact eight-object set and exact five-host allowlist;
- an absent output root and no reparse-point ancestor.

During a future authorized run it would:

- use HTTPS GET only, with cookies, proxy, authentication, automatic decompression, and automatic
  redirects disabled;
- validate every redirect before following it;
- stream each body into a create-new partial file while enforcing per-object and total byte caps;
- check wall, CPU, and observed peak-memory caps at request and stream checkpoints;
- recompute SHA-256 for every received object;
- verify npm SHA-512 SRI and SHA-1 shasum from the received version metadata;
- verify the selected Python wheel against its metadata and fixed SHA-256;
- retain partial evidence on ambiguity without retry;
- end only at `ACQUISITION_COMPLETE_AWAITING_G1` or `ACQUISITION_INCONCLUSIVE`;
- leave A2 unauthorized in either state.

The future authorization receipt is a local safety interlock and audit binding. It is not a digital
signature, native approval channel, or proof of independent authority.

## Residual limitations

- The npm tarball SHA-256 is necessarily unknown before A1. The runner cross-checks registry SRI and
  shasum during A1, then records a locally recomputed SHA-256 for G1 review.
- URI host validation does not itself impose an operating-system IP egress firewall. DNS and TLS
  behavior remain properties of the host runtime. Any future requirement for IP-level egress
  enforcement needs a separately approved OS/network control.
- CPU and peak-memory caps are observed at runner checkpoints, not enforced by a Windows Job Object.
  A process could transiently cross a cap between checks; the next check would fail closed. A hard
  kernel-enforced resource boundary would require a separately reviewed launcher.
- The runner has passed syntax and invariant review but not a live or simulated HTTP execution.
  Runtime compatibility therefore remains unproven until an explicitly authorized A1 attempt.
- Successful acquisition proves byte custody and registry consistency only. It does not admit,
  trust, import, or execute either package.

These limitations do not broaden A1. They must be included in any future authorization decision.

## Decision

The A0 materials are internally consistent and ready for user review.

They do not authorize A1. The next possible state-changing step is a fresh, explicit approval of the
exact manifest and runner hashes followed by creation of a short-lived A1 authorization receipt.
Without that approval and receipt, the runner must not be invoked.
