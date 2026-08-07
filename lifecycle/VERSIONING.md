# CAP Versioning Policy

Profile: `cap-versioning/0.2`

CAP versions use `MAJOR.MINOR` for protocol releases and optional `.PATCH` implementation maintenance.

- **MAJOR** changes normative meaning, removes a previously valid interpretation, or breaks record/profile compatibility.
- **MINOR** adds a compatible normative capability, machine-readable profile, conformance obligation, or independent implementation requirement.
- **PATCH** repairs implementations, tests, diagnostics text, or documentation without changing normative outcomes.

The protocol version and the record-profile version are independent. CAP 0.2 continues to assess records using the `0.1-draft` record profile; changing the record profile requires an explicit compatibility statement.

Released identifiers are never silently reused. Every incompatible change must declare migration and compatibility consequences.