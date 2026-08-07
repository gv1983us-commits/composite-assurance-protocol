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

### CI
- Verifies Python 3.10–3.13 and Node.js 20/22.

### Lifecycle
- Adds versioning, compatibility, migration, roadmap, stability promise, profile lock, and release acceptance records.

## 0.1-draft
- Initial public canonical draft with six normative surfaces, JSON Schema, Python validator, resistance corpus, and pinned neighboring artifacts.