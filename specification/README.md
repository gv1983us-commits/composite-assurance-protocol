# CAP machine-readable specification

This directory is the language-neutral executable description of CAP semantics.

- `vocabulary.json` defines dispositions, result statuses and controlled values.
- `derivation.json` defines ordered first-match result derivation.
- `invariants.json` maps semantic invariants to stable diagnostic codes.
- `diagnostics.json` defines the diagnostic namespace and registry.

The files are normative representations of the corresponding rules already stated in `spec/`. They do not depend on Python. `conformance/test_machine_specification.py` interprets the rule format and proves that it agrees with the Python reference implementation across the complete parseable resistance corpus.

A conforming independent implementation must consume or faithfully implement these profiles and pass the shared conformance corpus. Agreement with Python source code alone is not sufficient.
