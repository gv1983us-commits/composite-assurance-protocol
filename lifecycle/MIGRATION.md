# CAP Migration Guide

Profile: `cap-migration/0.2`

## 0.1-draft → 0.2

The assessment semantics and record schema remain compatible. Implementers should:

1. Keep accepting record profile `0.1-draft`.
2. Emit stable `diagnostic_codes` in addition to human-readable errors.
3. Consume the machine-readable vocabulary, derivation, invariants, and diagnostic registry.
4. Run the complete `conformance/expectations.json` corpus.
5. Demonstrate at least one implementation independent of the Python reference validator.
6. Verify the lifecycle and profile lock files.

Implementations that only run the original Python validator remain useful but are not fully CAP 0.2 conformant.

No migration step authorizes importing a neighboring artifact's global conclusion or re-deciding its native verdict.