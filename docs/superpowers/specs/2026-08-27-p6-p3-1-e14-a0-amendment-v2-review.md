# P6 P3.1 E14 A0 amendment v2 review

Date: 2026-08-27

Status: corrected A0 materials ready for review; A1 retry is unauthorized.

## Reason for amendment

The user approved one A1 download-only acquisition using the reviewed v1 manifest and runner. Two
attempts stopped before creation of the acquisition output root:

1. The first receipt used RFC3339 timestamps. PowerShell 7.6 `ConvertFrom-Json` automatically
   converted them to local `DateTime` values, so string conversion lost the terminal `Z`. The runner
   returned `A1_AUTHORIZATION_TIME_INVALID`.
2. A second receipt used a UTC string representation that avoided automatic date conversion. The
   exact object and host sets matched, so `Compare-Object` returned `$null`. Under
   `Set-StrictMode -Version Latest`, accessing `.Count` on `$null` raised an unclassified exception.
   The runner returned `ACQUISITION_UNEXPECTED_FAILURE`.

The output root is created only after both checks. It remained absent after both attempts. Therefore:

- HTTP client construction did not occur;
- network calls executed equal zero;
- no download, response, archive, partial file, or terminal receipt exists;
- the failures are deterministic preflight failures, not ambiguous network results.

## Preserved v1 artifacts

| Artifact | SHA-256 | Status |
|---|---|---|
| v1 runner | `0232F074C4D328F49F5E1C765C0B97EE0DD1B0E89740EB26822DB8D69D1D500D` | preserved; retired |
| v1 manifest | `48AFFF7D04A6A3E665D63192BA97181FD80EB8A7981F514AC895FAD916D4CA9F` | preserved; retired |
| first receipt | `0C02B13B5BC7F7F9A98859E9F0CC7F81DE1E25FEE76E51A1A64C18B5B47A923E` | preserved; failed; not reusable |
| second receipt | `668BE3ACA4276CAA70F8B7B97DEA7E630925588ACDAC0154A9F82A1BC9BFC1A2` | preserved; failed; not reusable |

Neither receipt can authorize v2 because both bind the v1 manifest and runner hashes.

## v2 artifacts

| Artifact | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| `2026-08-27-p6-p3-1-e14-a0-download-only-runner-v2.ps1` | 728 | 29,153 | `534E9709A3969E165DD3F34BF7035BB28F74DF44D9C94CA0B8C9C21F8F48F5F3` |
| `2026-08-27-p6-p3-1-e14-a0-acquisition-manifest-v2.json` | 194 | 6,658 | `9A4CB9CE7C497C4296453DA0B150762CB7F46F4A05E696A5617D239E7BE07D15` |

The v2 manifest names and binds the exact v2 runner path and SHA-256. It also binds the v1 manifest
hash as its predecessor.

## Exact runner changes

There are exactly three removed/added line pairs between runner v1 and v2:

1. `ConvertFrom-Json -Depth 100` becomes
   `ConvertFrom-Json -Depth 100 -DateKind String`.
2. The object-ID `Compare-Object` result is wrapped in `@(...)` before reading `.Count`.
3. The allowed-host `Compare-Object` result is wrapped in `@(...)` before reading `.Count`.

No URL, host, package, version, output root, cap, TLS setting, redirect rule, byte limit, retention
rule, failure effect, or stage boundary changed.

## v2 static checks

| Check | Result |
|---|---|
| PowerShell AST parse errors | 0 |
| Manifest JSON parse errors | 0 |
| Manifest-bound runner hash equals actual v2 hash | true |
| Date fields remain `System.String` with `-DateKind String` | true |
| Identical `Compare-Object` sets produce safe count | 0 |
| v1/v2 line-difference records | 6: three removals plus three additions |
| Required objects | 8 |
| Unique object IDs | 8 |
| Unique requested URLs | 8 |
| Network calls during v2 review | 0 |
| Reserved `e14` root exists | false |

## Authorization result

The earlier user confirmation cannot be silently transferred to changed executable bytes. The v2
runner and manifest require a fresh explicit approval of these exact hashes.

After that approval, a new receipt may be created with at most one hour validity and bindings to:

```text
manifest_sha256 = 9A4CB9CE7C497C4296453DA0B150762CB7F46F4A05E696A5617D239E7BE07D15
runner_sha256   = 534E9709A3969E165DD3F34BF7035BB28F74DF44D9C94CA0B8C9C21F8F48F5F3
output_root     = C:\Users\Administrator\Documents\Codex\2026-08-25\zh\outputs\sana-v22-evidence\e14\vendor-acquisition-v1
```

No v2 receipt has been created, and runner v2 has not been invoked.
