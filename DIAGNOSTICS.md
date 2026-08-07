# CAP Diagnostic Codes

Diagnostic codes are the stable machine-readable interface of the CAP reference validator. Human-readable messages may become clearer without changing the code assigned to the same failure class.

## Namespaces

| Namespace | Meaning |
|---|---|
| `CAP-JSON-*` | JSON parsing and strict JSON representation failures |
| `CAP-SCHEMA-*` | structural non-conformance to the record profile |
| `CAP-SEM-*` | semantic non-conformance to CAP composition rules |
| `CAP-TOOL-*` | failure of the validation implementation itself |

## Current registry

- `CAP-JSON-001`: duplicate JSON key
- `CAP-JSON-002`: non-finite JSON number
- `CAP-SCHEMA-001`: JSON Schema validation failure
- `CAP-SEM-001` through `CAP-SEM-029`: semantic rules in validator evaluation order
- `CAP-TOOL-999`: unclassified implementation failure

The exact semantic mapping is defined by `validator/diagnostics.py` and tested against `conformance/expectations.json`.

## Output contract

The diagnostic-aware CLI emits:

```json
{
  "validation_status": "INVALID",
  "cap_result": null,
  "diagnostic_codes": ["CAP-SEM-003"],
  "errors": ["CAP-SEM-003 pin mismatch for claude.bec"]
}
```

Consumers MUST branch on `diagnostic_codes`, not on human-readable message text. Codes are ordered by first occurrence and deduplicated. A valid record emits an empty diagnostic list.

## Compatibility

Within the `0.x` line:

- an existing code MUST NOT be reassigned to a different failure class;
- clarification of message text is non-breaking;
- adding a new code is additive;
- splitting one broad code into narrower codes requires a conformance profile revision.
