# CAP Stability Promise

Profile: `cap-stability-promise/0.2`

From CAP 0.2 onward:

- published diagnostic codes are not reassigned to different meanings;
- derivation rule IDs and semantic invariant IDs are never reused;
- conformance fixture filenames remain stable identities;
- machine profile identifiers change when their contract changes;
- deprecation is explicit and includes a migration path;
- reference implementation internals may change without changing protocol meaning;
- positive CAP results remain bounded and never become global assurance by version upgrade.

Before 1.0, compatible additions are permitted. Any incompatible semantic change requires an explicit release, compatibility statement, migration document, and new acceptance receipt.