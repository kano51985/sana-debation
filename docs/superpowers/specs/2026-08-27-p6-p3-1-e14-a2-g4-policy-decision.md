# E14 A2 G4 dependency, hook, and license policy

Date: 2026-08-27

Gate result: PASS for the two exact G3 source roots; no reusable ecosystem-wide license policy is
created.

## Declared dependency decision

For canonicalize 4.0.0, dependencies, peerDependencies, optionalDependencies,
bundledDependencies, and bundleDependencies must be absent or empty. They are all empty in the
frozen inventory. Development dependencies are not admitted and no package-manager operation is
allowed.

For rfc8785 0.1.4, every Requires-Dist record must be guarded by an exact declared extra. The dev,
doc, lint, and test extras are recorded but not installed or admitted. The base runtime
distribution dependency set is empty. No entry points or install hooks are admitted.

Registry dependency metadata and source-level runtime closure are separate claims. Empty registry
runtime sets do not imply an empty runtime boundary.

## Runtime boundary decision

- Node: the later measured Node.js runtime and its built-in language/global facilities. Bare
  module references are not allowed. The current source has one in-bundle relative import.
- Python: the later measured CPython 3.12.x image plus exactly __future__, io, math, re, and typing
  from that image's standard library. The current source has one in-bundle relative import.
- No ambient site-packages, NODE_PATH, PYTHONPATH, package manager, dynamic download, native
  extension, WebAssembly module, subprocess, or unlisted module is accepted.

The exact interpreter/image identity remains a G6/G7 measurement, not a G4 assumption.

## Lifecycle decision

The npm hooks preinstall, install, postinstall, prepare, prepublish, and prepublishOnly are
prohibited. None is present. Other scripts are recorded as inert metadata and are never executed.
Python has no admitted entry point or installation hook. Wheel installation is not performed.

## Named license decision

For these exact bytes only:

- canonicalize is accepted as Apache-2.0 because package.json declares Apache-2.0 and LICENSE has
  SHA-256 C71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4;
- rfc8785 is accepted as Apache-2.0 because METADATA contains the Apache Software License
  classifier and its bundled LICENSE has SHA-256
  0D542E0C8804E39AA7F37EB00DA5A762149DC682D7829451287E11B938E94594; and
- the absent PyPI license_expression field is recorded rather than silently converted into a
  registry SPDX claim.

This is a bounded technical fixture-admission decision, not legal advice and not authority to
redistribute or deploy. Any byte, version, classifier, declaration, or license-file change requires
a new decision.
