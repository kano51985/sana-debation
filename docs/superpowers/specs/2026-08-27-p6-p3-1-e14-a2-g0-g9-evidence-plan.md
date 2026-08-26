# E14 A2 G0-G9 evidence plan

Date: 2026-08-27

Status: evidence construction authorized; A2 execution remains blocked.

This plan implements the unchanged P3 selected by the A2 architecture debate. It does not admit
either package, create e14/vendor-admission-v1, authorize G2/B0/F0/R0, or treat source review as
proof of network isolation.

## G0 trust and process accounting decision

The one-process A2 cap applies to exactly one guest admission process. The external container
controller and terminal finalizer are outside that guest-process count, but they are inside the
trusted computing base and must be measured, authorized, and reported separately. They may not
execute package code. The controller may only construct the measured envelope and launch the
guest. The finalizer may only inspect the stopped guest/output and create terminal-receipt.json
after all observations agree.

This split is accepted because enforcing network and child-process denial from process creation is
logically prior to guest code. Hiding the controller/finalizer from the TCB would be invalid. The
final evidence must report all three identities and effects.

## Frozen phase order

1. G1 freezes the production scanner, schema, error taxonomy, path rules, file kinds, source-root
   algorithm, ZIP policy, and analyzer bytes.
2. G2 runs A1-PHYS-01 against those exact production bytes.
3. G3 performs a read-only pre-scan of the sealed A1 root. It writes evidence outside the future
   admission root and does not extract files to a vendor tree.
4. G4 records the exact dependency, extras, lifecycle-hook, and license decisions.
5. G5 binds structural reference discovery and a separately reviewed semantic closure attestation
   to the G3 roots. Structural coverage is not described as semantic completeness.
6. G6 measures a concrete external envelope.
7. G7 attacks process-start network/child isolation and records external observations.
8. G8 requires fresh authorization bound to G1-G7, the passed A1/G1 receipt, and an absent
   e14/vendor-admission-v1 output.
9. G9 measures and authorizes the terminal-only finalizer.

No A2 guest execution occurs before a fresh Chief re-adjudicates the complete G0-G9 packet.

## G1 implementation boundary

The production pre-scanner is a standard-library-only Python module. It:

- verifies the exact A1 terminal inventory and the two G1-approved archive hashes;
- parses the npm gzip framing directly and uses raw zlib deflate;
- scans every physical 512-byte ustar header without tarfile or another normalizing tar API;
- parses ZIP local headers, central records, and EOCD directly, then inflates each member with raw
  zlib;
- rejects links, extensions, aliases, encryption, data descriptors, extra fields, comments,
  unsupported types/compression, non-ASCII names, unsafe paths, collisions, and numeric/cap
  violations;
- verifies package identity, declared dependencies, lifecycle hooks, wheel RECORD, license
  evidence, and fixed inventory;
- computes domain-separated physical-transcript, inventory, source, and bundle roots; and
- performs conservative source-reference discovery without importing or executing package code.

The read-only pre-scan may emit a JSON report through its caller, but the production module itself
does not create the admission output and cannot write an authoritative terminal.

## Frozen caps

| Dimension | Value |
|---|---:|
| A1 input files | 20 exactly |
| A1 input bytes | at most 16 MiB |
| archive members / expanded files | 512 |
| regular expanded bytes | 32 MiB |
| single expanded file | 2 MiB |
| normalized path depth | 12 |
| guest processes | 1 |
| guest wall / CPU | 120 seconds each |
| guest memory | 512 MiB |
| admission output files | 520 |
| admission output bytes | 40 MiB |
| guest network | zero interfaces capable of external routing; zero packets/bytes observed |
| guest child processes | denied from process creation |

## Fail-closed boundary

Any mismatch, incomplete scan, unknown source construct, unavailable external observation, or
controller/finalizer identity drift leaves the packet INCONCLUSIVE. Docker availability alone is
not G6/G7 evidence. A successful local pre-scan alone is not admission.
