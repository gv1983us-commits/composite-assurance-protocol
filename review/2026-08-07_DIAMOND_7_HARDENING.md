# 2026-08-07 Diamond 7 Hardening Review

## Scope

This review treats CAP 0.2 as a candidate for corpus-level canonization beside the six already canonized technical artifacts. It does not reopen the six-surface normative semantics unless a correctness blocker is found.

## Findings

### D7-001 — Cross-runtime agreement was corpus-bound only

Before this pass, Python and Node were independently exercised against the same committed fixture oracle, but there was no dedicated adversarial differential suite that generated the same mutated record for both implementations.

Disposition: **resolved**.

`conformance/test_differential.py` now generates deterministic hostile mutations and requires both implementations to agree on exit code, validation status, CAP result, and stable diagnostic codes. The permanent CI contains a dedicated Python+Node differential job.

### D7-002 — Release support surfaces contradicted the accepted 0.2 state

`PROVENANCE.md` and `review/PUBLICATION_MANIFEST.md` still contained pre-release language describing CAP as `canonical_public_draft` and acceptance as pending, while `ARTIFACT.json`, `CANON.md`, lifecycle state, and `RELEASE_ACCEPTANCE.json` already described the accepted 0.2 release.

Disposition: **resolved**.

The support surfaces now preserve the historical 0.2 accepted baseline and explicitly distinguish it from later hardening or corpus-level acceptance. `review/test_release_0_2.py` prevents regression to the stale state.

## Normative impact

No normative surface was added, removed, reordered, or amended by this hardening pass. The six-surface authority matrix and CAP 0.2 composition semantics remain unchanged.

## Evidence requirement

This review is not itself acceptance. A candidate revision is eligible for canonization only after the complete permanent CI succeeds, including:

- Python 3.10, 3.11, 3.12, and 3.13;
- independent Node.js 20 and 22;
- the cross-runtime adversarial differential job;
- release identity and canonical-surface regression tests.

The exact accepted revision and its CI receipt must be recorded separately. Branch names and later heads are not substitutes for that receipt.
