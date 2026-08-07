# CAP conformance corpus

This directory is the implementation-neutral resistance and acceptance corpus for CAP.

- `fixtures/` contains valid, invalid and malformed assessment records.
- `expectations.json` is the machine-readable oracle for every fixture.
- `test_conformance.py` proves total corpus coverage, validates the JSON Schema metaschema, checks all six CAP outcomes, and separates structural from semantic rejection.
- `RESISTANCE_CORPUS.md` summarizes the adversarial cases.

A fixture MUST NOT exist without an entry in `expectations.json`, and an expectation MUST NOT name a missing fixture.

Run the complete conformance layer with:

```bash
python -m unittest conformance.test_conformance -v
```

Run all repository checks with:

```bash
python -m unittest discover -v
```
