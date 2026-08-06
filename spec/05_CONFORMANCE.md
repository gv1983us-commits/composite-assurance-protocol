# CAP Conformance 0.1-draft

## Validation pipeline

A conforming implementation must fail closed and perform, in order:

1. strict JSON parsing with duplicate-key and non-finite-number rejection;
2. Draft 2020-12 schema validation;
3. exact compatibility-pin validation;
4. reference and uniqueness validation;
5. native-verdict preservation validation;
6. domain coverage and receipt validation;
7. conflict, unknown and omission consistency validation;
8. deterministic result derivation;
9. mandatory claim-boundary validation.

## Validator result

The reference validator prints JSON:

```json
{"validation_status":"VALID","cap_result":"BOUNDED_ACCEPTABLE","errors":[]}
```

or:

```json
{"validation_status":"INVALID","cap_result":null,"errors":["..."]}
```

## Exit codes

- `0`: CAP record valid, including any valid CAP result status.
- `1`: record invalid.
- `2`: validator tool failure such as unreadable input or internal exception.

The CAP record status `TOOL_FAILURE` is different from validator exit code `2`: the former is a valid subject record about its producing pipeline; the latter means this validator failed to evaluate the file.

## Implementation obligations

Implementations must not:

- accept duplicate JSON keys;
- accept NaN or Infinity;
- infer generic success from native status spelling;
- ignore pin mismatch;
- allow missing required domains;
- return `BOUNDED_ACCEPTABLE` under partial coverage;
- downgrade blocking conflicts or unknowns silently;
- mutate source records during validation;
- claim conformance beyond tested profile `0.1-draft`.

## Conformance claim

Passing this repository’s corpus demonstrates conformance to the published CAP `0.1-draft` test corpus for the tested implementation. It does not prove independent multi-implementation agreement, external truth, or correctness for future versions.
