# CAP Canon

## 1. Canonical object

This repository publishes **Composite Assurance Protocol (CAP)** as artifact `claude.cap`, protocol version `0.2`, record profile `0.1-draft`, and status `canonical_public_release`.

CAP owns only the domain `bounded_cross_artifact_assessment`.

## 2. Authority order

When surfaces appear to conflict, interpret them in this order, limited by domain ownership:

1. `spec/01_CAP_CORE.md` for CAP assessment semantics, scope and owner boundaries.
2. `spec/02_ASSESSMENT_VOCABULARY.md` for normative token meanings.
3. `spec/03_COMPOSITION_POLICY.md` for composition and precedence.
4. `spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md` for conflicts, unknowns, omissions and tool failures.
5. `spec/05_CONFORMANCE.md` for validation procedure, output and exit codes.
6. `schema/composite-assessment-record.schema.json` for record-profile structure.

The normative surface is closed at exactly these six entries for CAP 0.2. No other file acquires normative authority merely by being executable, machine-readable, or canonical.

## 3. Executable and canonical support surfaces

The following support the canon without independently overriding it:

- `specification/` — machine-readable vocabulary, derivation, invariants, and diagnostic registry;
- `validator/` — fail-closed Python reference implementation;
- `independent/node/` — independent Node.js implementation;
- `conformance/` — expected outcomes and resistance corpus;
- `PROFILE_LOCK.json` — stability and implementation obligations;
- `lifecycle/` — versioning, compatibility, migration, roadmap, and stability policy;
- `references/PINNED_ARTIFACT_REVISIONS.md` — exact compatibility receipt;
- `review/` — publication, cross-reference, lifecycle, and canon verification;
- `README.md`, `RELATIONS.md`, and `PROVENANCE.md` — canonical navigation and disclosure.

## 4. Citation rule

A conforming citation states at least:

- repository;
- exact reviewed revision;
- protocol version;
- record profile version when a record is cited;
- normative surface and section;
- assessment question and scope when a CAP result is cited.

A branch name such as `main` is navigation, not a reproducible citation.

## 5. Core invariants

```text
several valid records != one valid global conclusion
native verdict carried != native verdict re-decided
all required domains satisfied != universal acceptance
missing required evidence != implicit success
conflict disclosed != conflict resolved
partial coverage != full coverage
CAP result != neighbor conformance
CAP result != world truth
```

CAP may derive a new bounded result only through the declared composition policy. It must not rename a neighboring status into a CAP status without an explicit domain result and mapping rule.

## 6. Exact source set

The active compatibility set is fixed in `references/PINNED_ARTIFACT_REVISIONS.md` and mirrored in `ARTIFACT.json` and both implementations.

These pins identify reviewed historical states. They are not aliases for latest and do not impose reciprocal latest-SHA requirements on neighboring repositories.

## 7. Release boundary

`canonical_public_release` means CAP 0.2 has canonical identity, a closed normative surface, explicit lifecycle and compatibility policy, stable diagnostic identifiers, machine-readable rules, a complete conformance corpus, and successful Python and independent Node implementations.

It does not mean external certification, frozen 1.0 semantics, universal safety, permanent correctness, or authority outside the declared bounded assessment scope.
