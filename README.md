# Composite Assurance Protocol (CAP)

**Composite Assurance Protocol** defines how independently owned technical records may support one bounded cross-artifact assessment without collapsing their claim domains into a global verdict.

```text
several valid records != one valid global conclusion
```

CAP does not replace BEC, MPAA, PCA, Repository Canon and Review Protocol, ARB, or CDTS. It carries their native statuses, preserves their owners, applies an explicit composition policy, and produces a new decision whose authority is limited to one declared assessment question and scope.

## Canonical identity

```text
artifact_id: claude.cap
artifact_version: 0.1-draft
record_profile_version: 0.1-draft
status: canonical_public_draft
claim_domain: bounded_cross_artifact_assessment
```

The machine-readable passport is [`ARTIFACT.json`](ARTIFACT.json). Citation and authority order are fixed in [`CANON.md`](CANON.md).

## Six normative surfaces

| Surface | Owns |
|---|---|
| [`spec/01_CAP_CORE.md`](spec/01_CAP_CORE.md) | assessment semantics, scope and ownership boundaries |
| [`spec/02_ASSESSMENT_VOCABULARY.md`](spec/02_ASSESSMENT_VOCABULARY.md) | status, disposition and claim-class meanings |
| [`spec/03_COMPOSITION_POLICY.md`](spec/03_COMPOSITION_POLICY.md) | deterministic composition and precedence rules |
| [`spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md`](spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md) | conflicts, unknowns, omissions and failure handling |
| [`spec/05_CONFORMANCE.md`](spec/05_CONFORMANCE.md) | validation pipeline, result statuses and exit codes |
| [`schema/composite-assessment-record.schema.json`](schema/composite-assessment-record.schema.json) | record profile `0.1-draft` structural representation |

[`validator/cap_validate.py`](validator/cap_validate.py) is a non-normative fail-closed reference implementation.

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

This yields, respectively:

```text
TOOL_FAILURE
BLOCKED_BY_CONFLICT
BOUNDED_UNACCEPTABLE
INSUFFICIENT_EVIDENCE
PARTIAL_ASSESSMENT
BOUNDED_ACCEPTABLE
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

## Conformance hardening

[`conformance/expectations.json`](conformance/expectations.json) is the machine-readable oracle for the complete fixture corpus. The conformance tests require one-to-one coverage between fixtures and expectations, exercise all six result statuses, validate the schema against the Draft 2020-12 metaschema, and prove that structural rejection is distinct from CAP semantic rejection.

A new fixture without an expectation, or an expectation without a fixture, fails CI.

## Reproducible checks

```bash
python -m unittest discover -v
python -m unittest conformance.test_conformance -v
python -m json.tool ARTIFACT.json >/dev/null
python validator/cap_validate.py examples/bounded-runtime-assessment.json
python -m review.test_artifact_canon
```

## License

MIT. See [`LICENSE`](LICENSE).
