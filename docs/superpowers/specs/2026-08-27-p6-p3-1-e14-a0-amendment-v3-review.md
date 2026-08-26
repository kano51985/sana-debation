# E14 A0 amendment v3 review

Date: 2026-08-27  
Status: corrected A0 materials frozen; execution requires a hash-bound receipt  
Authority effect: **NONE**

## Reason for amendment

The v2 acquisition obtained and independently verified all eight requested objects, but terminal
sealing failed. `Get-OutputInventory` emits `OrderedDictionary` records. PowerShell's
`Measure-Object -Property bytes` does not expose the dictionary key as an object property, so the
runner raised `ACQUISITION_UNEXPECTED_FAILURE` before writing `terminal-receipt.json`.

The failed `e14/vendor-acquisition-v1` root remains immutable and G1 remains `INCONCLUSIVE` for
that attempt.

## Frozen v3 identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `2026-08-27-p6-p3-1-e14-a0-download-only-runner-v3.ps1` | 29,968 | `08A8935121735B0D1100FFDD05BB6910439495B97A590736BF7F01F6C67F582F` |
| `2026-08-27-p6-p3-1-e14-a0-acquisition-manifest-v3.json` | 6,699 | `7E5203E0A9BD50FF3421DFBB1D136BBA0B6C1DD39274A45ACEABB72E4B33C9DD` |

The manifest binds the exact runner hash and path. Its create-new output root is
`e14/vendor-acquisition-v2`, which did not exist at review time.

## Exact code change

Runner v3 differs from runner v2 only in terminal inventory summation:

1. it adds `Get-InventoryTotalBytes`;
2. it reads `bytes` through `IDictionary` indexing;
3. it rejects absent byte keys, negative values, and Int64 overflow with
   `ACQUISITION_OUTPUT_SIZE_INVALID`; and
4. `Write-TerminalReceipt` calls that helper instead of `Measure-Object`.

Manifest v3 increments the revision, supersedes manifest v2, binds runner v3, and selects the new
immutable output root. The eight-object set, URLs, allowlist, GET-only network rules, resource caps,
retention, prohibitions, terminal schema, and A2 prohibition are unchanged.

## Verification

- PowerShell AST parse: `PASS` with zero parser errors.
- Manifest-to-runner path and SHA-256 binding: `PASS`.
- New output root absent before authorization: `PASS`.
- OrderedDictionary byte sum (`7 + 11 = 18`): `PASS`.
- Int64 overflow rejection: `PASS`.
- Offline terminal receipt creation over a two-file temporary root: `PASS`.
- Stale v2-bound receipt presented to v3: rejected with
  `A1_AUTHORIZATION_HASH_MISMATCH` before output-root creation.
- Complete Python suite: 68 tests, all passing.
- Failed v1 root after review: 19 files, 107,481 bytes, no terminal receipt, no Git changes.

The regression test is `tests/test_a1_runner_v3.py`. It first failed because runner v3 was absent,
then passed after the bounded amendment.

## Execution boundary

This review does not authorize network execution. Any A1 execution must use a fresh receipt that
binds the two frozen hashes above and the `vendor-acquisition-v2` root. The receipt is a local
safety and audit interlock, not cryptographic proof of identity or cognitive independence.

Successful A1 completion would still produce evidence only and the terminal state
`ACQUISITION_COMPLETE_AWAITING_G1`. A2 remains unauthorized until a separate G1 review passes.
