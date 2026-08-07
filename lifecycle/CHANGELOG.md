# CAP Changelog

Profile: `cap-changelog/0.2`

## 0.2 — 2026-08-07

### Normative
- Preserves the six-surface CAP assessment semantics and bounded-result model.
- Declares CAP as a released protocol while retaining the `0.1-draft` record profile.

### Machine specification
- Adds machine-readable vocabulary, derivation, invariants, and diagnostic registry profiles.

### Reference implementation
- Retains the fail-closed Python reference validator.
- Adds stable machine-readable diagnostic codes.

### Independent implementations
- Adds an independent Node.js validator that does not import the Python implementation.

### Conformance
- Makes the complete fixture corpus and expectations manifest executable contracts.
- Adds cross-implementation and cross-reference checks.
- Adds deterministic adversarial cross-runtime differential verification for Python and Node.js without changing normative CAP semantics.

### CI
- Verifies Python 3.10–3.13 and Node.js 20/22.
- Adds a dedicated Python 3.13 + Node.js 22 differential job that fails on machine-visible implementation divergence.

### Lifecycle
- Adds versioning, compatibility, migration, roadmap, stability promise, profile lock, and release acceptance records.

### Canonization hardening
- Reconciles `PROVENANCE.md` and `review/PUBLICATION_MANIFEST.md` with the accepted CAP 0.2 release state.
- Adds regression checks preventing stale pre-release status or pending-acceptance language from reappearing on canonical support surfaces.
- Records the findings and dispositions in `review/2026-08-07_DIAMOND_7_HARDENING.md`.

## 0.1-draft
- Initial public canonical draft with six normative surfaces, JSON Schema, Python validator, resistance corpus, and pinned neighboring artifacts.