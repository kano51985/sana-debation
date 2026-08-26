# E14 A1/G1 acquisition review — INCONCLUSIVE

Date: 2026-08-27  
Scope: `e14/vendor-acquisition-v1`  
Disposition: **INCONCLUSIVE; A2 remains unauthorized**

## Bound authorization

- runner v2 SHA-256: `534E9709A3969E165DD3F34BF7035BB28F74DF44D9C94CA0B8C9C21F8F48F5F3`
- manifest v2 SHA-256: `9A4CB9CE7C497C4296453DA0B150762CB7F46F4A05E696A5617D239E7BE07D15`
- authorization receipt v3 SHA-256: `91D8022994F64304E5720A5BFA7879A0E6871BDD9A41AF60192B7FAAB7D3BDAA`

The receipt was valid when the runner started, and its runner and manifest hashes matched the
executed inputs.

## Observed acquisition state

The create-new acquisition root contains 19 files totaling 107,481 bytes:

- three copied control records (`acquisition-manifest.json`, `authorization-receipt.json`, and
  `runner-identity.json`);
- eight response bodies; and
- eight response-metadata records.

All eight requested objects are present. Read-only recomputation established:

- npm metadata selected `canonicalize@4.0.0`, license `Apache-2.0`, and the exact recorded tarball
  URL;
- the npm tarball matches both the registry SHA-512 SRI and SHA-1 shasum;
- the npm tarball local SHA-256 is
  `AE9A1851B4D3489FBA0D6A45A6B779296C5FE7F9DD626EB2C6D12045D47CBA87`;
- PyPI metadata selected `rfc8785==0.1.4` and exactly one wheel matching the recorded URL, size,
  and digest; and
- the wheel SHA-256 matches its official PyPI metadata.

These checks establish payload presence and integrity only. They do not promote the acquisition
to a successful terminal state.

## Terminal-seal failure

No `terminal-receipt.json` exists. The runner exited nonzero with
`ACQUISITION_UNEXPECTED_FAILURE` after downloading the objects while calculating its terminal
inventory.

The reproduced local defect is type-specific: `Get-OutputInventory` returns
`System.Collections.Specialized.OrderedDictionary` records, while the runner asks
`Measure-Object -Property bytes -Sum` to read `bytes` as a PowerShell object property. The key is
available by dictionary indexing but is not exposed to `Measure-Object` as that property. An
explicit loop over the same records produces the observed total of 107,481 bytes.

This is a terminal-sealing implementation defect, not evidence that the downloaded bodies failed
their upstream integrity checks. Nevertheless, the missing terminal receipt is decisive under the
fail-closed protocol.

## Binding disposition

1. G1 is `INCONCLUSIVE`, not `PASS`.
2. A2 and all downstream fixture construction remain unauthorized.
3. The failed acquisition root is retained as immutable evidence. It must not be retried in place,
   deleted, overwritten, or repaired by adding a terminal receipt after the fact.
4. Any corrected runner requires a separately reviewed version, fresh authorization, and a new
   create-new acquisition root.
5. Publishing this evidence to a private repository preserves the record; it does not change the
   gate disposition.
