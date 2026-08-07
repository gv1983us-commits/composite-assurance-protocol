# Composite Assurance Protocol (CAP)

**Composite Assurance Protocol** defines how independently owned technical records may support one bounded cross-artifact assessment without collapsing their claim domains into a global verdict.

```text
several valid records != one valid global conclusion
```

CAP does not replace BEC, MPAA, PCA, Repository Canon and Review Protocol, ARB, or CDTS. It carries their native statuses, preserves their owners, applies an explicit composition policy, and produces a new decision whose authority is limited to one declared assessment question and scope.

## Canonical identity

```text
artifact_id: claude.cap
artifact_version: 0.2
record_profile_version: 0.1-draft
status: canonical_public_release
claim_domain: bounded_cross_artifact_assessment
```

The machine-readable passport is [`ARTIFACT.json`](ARTIFACT.json). Citation and authority order are fixed in [`CANON.md`](CANON.md). Release stability is fixed in [`PROFILE_LOCK.json`](PROFILE_LOCK.json), and lifecycle policy is under [`lifecycle/`](lifecycle/).

## Six normative surfaces

| Surface | Owns |
|---|---|
| [`spec/01_CAP_CORE.md`](spec/01_CAP_CORE.md) | assessment semantics, scope and ownership boundaries |
| [`spec/02_ASSESSMENT_VOCABULARY.md`](spec/02_ASSESSMENT_VOCABULARY.md) | status, disposition and claim-class meanings |
| [`spec/03_COMPOSITION_POLICY.md`](spec/03_COMPOSITION_POLICY.md) | deterministic composition and precedence rules |
| [`spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md`](spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md) | conflicts, unknowns, omissions and failure handling |
| [`spec/05_CONFORMANCE.md`](spec/05_CONFORMANCE.md) | validation pipeline, result statuses and exit codes |
| [`schema/composite-assessment-record.schema.json`](schema/composite-assessment-record.schema.json) | record profile `0.1-draft` structural representation |

The normative surface remains exactly six files. Machine-readable profiles and implementations are executable contracts but do not acquire independent normative authority.

## Implementations

- [`validator/cap_validate.py`](validator/cap_validate.py) is the non-normative fail-closed Python reference implementation.
- [`independent/node/cap_validate.mjs`](independent/node/cap_validate.mjs) is an independent Node.js implementation that does not import Python code.

Both implementations are checked against the same schema, machine specification, diagnostic registry, expectations manifest, and resistance corpus. A separate differential stress suite mutates valid records adversarially and requires both implementations to agree on exit class, validation status, CAP result, and stable diagnostic codes.

## Result statuses

```text
BOUNDED_ACCEPTABLE
BOUNDED_UNACCEPTABLE
INSUFFICIENT_EVIDENCE
BLOCKED_BY_CONFLICT
PARTIAL_ASSESSMENT
TOOL_FAILURE
```

No status means universal safety, permanent certification, world truth, agent identity, or validity outside the declared question and scope.

## Composition precedence

```text
tool failure
  > blocking conflict
  > decisive unsatisfied domain
  > required unknown
  > all required domains satisfied + partial coverage
  > all required domains satisfied + full coverage
```

## Source discipline

CAP pins the reviewed revisions of all six neighboring artifacts in [`references/PINNED_ARTIFACT_REVISIONS.md`](references/PINNED_ARTIFACT_REVISIONS.md). A source record remains owned by its native artifact.

```text
native verdict carried != native verdict re-decided
source validation receipt != CAP validation of the source specification
CDTS admissible != CAP acceptable
bounded assessment != world truth
assessment for one task != permanent runtime certification
```

## Conformance and diagnostics

[`conformance/expectations.json`](conformance/expectations.json) is the machine-readable oracle for the complete fixture corpus. The conformance tests require one-to-one coverage between fixtures and expectations, exercise all six result statuses, validate the schema against the Draft 2020-12 metaschema, and prove that structural rejection is distinct from CAP semantic rejection.

[`conformance/test_differential.py`](conformance/test_differential.py) adds a second class of evidence: deterministic adversarial mutations are evaluated by both the Python reference implementation and the independent Node.js implementation, and CI fails on any divergence in machine-visible outcome.

Stable diagnostic identifiers are defined in [`DIAGNOSTICS.md`](DIAGNOSTICS.md) and [`specification/diagnostics.json`](specification/diagnostics.json). Automation reads codes; humans read messages.

## Machine-readable specification

The [`specification/`](specification/) directory separates protocol rules from implementation language:

- vocabulary;
- ordered derivation rules;
- semantic invariants;
- diagnostic registry.

CI prevents the Python implementation, Node implementation, machine specification, and conformance corpus from drifting apart.

## Lifecycle

CAP 0.2 includes explicit versioning, compatibility, migration, roadmap, and stability policies. The release keeps the record profile at `0.1-draft`; protocol version and record-profile version are intentionally independent.

## Reproducible checks

```bash
python -m unittest discover -v
python -m review.test_artifact_canon
python -m review.test_release_0_2
node independent/node/test_conformance.mjs
python -m unittest conformance.test_differential -v
```

The permanent CI matrix covers Python 3.10–3.13 and Node.js 20/22. A dedicated differential job provisions Python 3.13 and Node.js 22 together and enforces cross-runtime agreement on adversarial mutations.

## Release provenance

The accepted CAP 0.2 release baseline is recorded in [`RELEASE_ACCEPTANCE.json`](RELEASE_ACCEPTANCE.json). `PROVENANCE.md` and `review/PUBLICATION_MANIFEST.md` distinguish that historical accepted revision from later hardening or corpus-level canonization work; a later acceptance must name its own exact revision.

## License

MIT. See [`LICENSE`](LICENSE).