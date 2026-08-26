# E14 A2 G2 physical scanner evidence

Date: 2026-08-27

Gate result: PASS for A1-PHYS-01 against the exact production scanner bytes recorded by G1.

The tests import and call src/e14_admission.py directly. There is no tarfile fallback, zipfile
fallback, package extraction, package import, or alternate test-only parser.

Command:

    python -m unittest tests.test_e14_admission -v

Result: 15 tests passed, 0 failed.

## A1-PHYS-01 coverage

- strict production npm archive and wheel accepted;
- PAX local/global, GNU longname/longlink, sparse, links, directories, NUL, and unknown tar
  typeflags rejected after repairing the malicious header checksum;
- base-256 tar size rejected;
- nonzero tar padding rejected;
- concatenated gzip and bytes after the final member rejected;
- ZIP encryption and data-descriptor flags rejected;
- ZIP local/central header mismatch rejected;
- ZIP symlink mode rejected;
- ZIP archive comments/trailing bytes rejected;
- parent, absolute, drive, backslash, ADS, reserved-device, dot, traversal, and normalization
  collision paths rejected;
- replay mutation changes the physical transcript root; and
- dynamic Node loading and unapproved Python imports fail closed.

The valid production scan also verifies gzip CRC/ISIZE, ZIP CRC, wheel RECORD, exact member sets,
package identities, registry digests, aggregate caps, and domain-separated roots.

## Limits

This gate proves behavior for the named adversarial corpus and exact scanner bytes. It does not
prove an absence of all parser defects, semantic dependency completeness, runtime integrity,
network isolation, or permission to execute A2.
