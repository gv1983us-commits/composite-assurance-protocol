# CAP Compatibility Contract

Profile: `cap-compatibility/0.2`

## Protocol and record profile

CAP protocol 0.2 consumes the `0.1-draft` composite-assessment record profile. A CAP 0.2 implementation must reject unknown future record profiles unless an explicit compatibility adapter is declared.

| Consumer | Required input compatibility |
|---|---|
| CAP 0.2 validator | record profile `0.1-draft` |
| CAP 0.2 conformance runner | expectations profile `0.3` |
| Independent implementation | machine specification profiles `0.1` |

## Stability classes

- CAP result meanings: normative and compatible within 0.x unless explicitly migrated.
- Diagnostic codes: stable identifiers; message wording is not an API.
- Rule and invariant IDs: stable and never reused.
- Fixture filenames: stable test identities; removal requires a major migration notice.
- Reference implementation internals: replaceable and non-normative.

No implementation may infer compatibility from a numerically higher version alone.