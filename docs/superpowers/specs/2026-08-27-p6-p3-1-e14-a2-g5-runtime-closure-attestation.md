# E14 A2 G5 runtime closure attestation

Date: 2026-08-27

Gate result: PASS for bounded source semantics, with reviewer-independence limitation disclosed.

The production scanner first performed structural analysis. A separate source-level review then
inspected all four executable source files. Both are bound to the G3 roots below. The source review
was performed by the primary agent, so this record does not claim cognitive independence or
two-person review.

## Frozen roots and source bytes

| Package | Source root | File | SHA-256 |
|---|---|---|---|
| npm | 26BA914DF24AFB64001E804A759DD014EBC173DAB032932F4B06A47CABEBC82B | bin/canonicalize.js | CF81826EEE228EF4D56F14F2272E635F38BC262DD4D0FAA0E2B1065A0AE388F0 |
| npm | 26BA914DF24AFB64001E804A759DD014EBC173DAB032932F4B06A47CABEBC82B | lib/canonicalize.js | 4A909B5C7574EE55C37E372D47B54A37F9E36E217FC20B4D6451F5DC78CB87C1 |
| wheel | 25F89B2E280A08167908D123BB7A09A33BD1036BF63587A7E1474C74D7138D4A | rfc8785/__init__.py | FA44927AFD547CAF7547247078BCF28863D1E69CAF116D258C532B3F20FFD154 |
| wheel | 25F89B2E280A08167908D123BB7A09A33BD1036BF63587A7E1474C74D7138D4A | rfc8785/_impl.py | C25BC3A046528482D53BEE3487B837F31DD9C05F33E8F13288C7AAB320932CEC |

## Node closure

bin/canonicalize.js has one static relative import resolving to lib/canonicalize.js. Its remaining
effects are stdin read, JSON parsing, a call to the in-bundle canonicalizer, stdout write, and
ordinary error propagation. It has no filesystem, socket, HTTP, child-process, native-addon,
WebAssembly, eval, Function-constructor, require, or dynamic-import path.

lib/canonicalize.js operates on supplied JavaScript values with language built-ins. It has no
import, bare module, filesystem, network, child-process, native, or dynamic-code reference. The
package entry fields resolve only to the two JavaScript files and the inert declaration file.

## Python closure

rfc8785/__init__.py performs one relative import resolving to rfc8785/_impl.py.

rfc8785/_impl.py imports __future__, math, re, typing, and io.BytesIO. The reviewed calls operate on
numbers, strings, mappings, sequences, regexes, and byte streams. re.compile is regular-expression
compilation, not Python code compilation. There is no os, sys, pathlib, socket, urllib, http,
subprocess, multiprocessing, importlib, ctypes, cffi, native extension, eval, exec, compile,
__import__, filesystem, network, process, or dynamic-load path.

## Closure result

- all in-package references resolve to the same frozen inventory;
- the Node external module allowlist is empty;
- the Python standard-library allowlist is exactly __future__, io, math, re, and typing;
- unresolved references: none;
- finite dynamic-load allowlist: empty;
- structural coverage: complete for the frozen grammar/source roots;
- bounded semantic review: complete for the four named files; and
- ambient runtime integrity and enforcement: intentionally not claimed here; G6/G7 must establish
  those properties externally.

Any source-root change invalidates this attestation. The disclosed same-agent review limitation is
available to the fresh Chief as a reason to require an additional reviewer without weakening the
fail-closed runtime boundary.
