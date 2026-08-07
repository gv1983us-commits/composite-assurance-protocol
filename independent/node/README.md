# Independent Node.js CAP Validator

This directory contains the independent CAP implementation used by the CAP 0.2 conformance matrix.

It does not import or execute the Python reference validator. It independently performs strict JSON parsing, structural validation, semantic invariant checks, ordered result derivation, and diagnostic-code emission using the shared schema, machine-readable specification, expectations manifest, and fixture corpus.

Run:

```bash
node independent/node/test_conformance.mjs
node independent/node/cap_validate.mjs examples/bounded-runtime-assessment.json
```

Supported release runtimes are Node.js 20 and 22, as locked in `PROFILE_LOCK.json`.