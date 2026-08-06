# CAP Core 0.1-draft

## 1. Purpose

CAP defines a bounded assessment record that composes explicitly mapped domain results derived from independently owned source records.

A CAP assessment answers exactly one `assessment_question` inside one declared `assessment_scope`.

## 2. Object of assessment

The object is not “the runtime in general.” It is the tuple:

```text
(subject, assessment_question, declared scope, required domains, source set, composition policy)
```

Changing any member creates a different assessment.

## 3. Ownership

Each source record retains:

- its artifact owner;
- native status vocabulary;
- native validity and conformance rules;
- original revision and record reference;
- limits on what its conclusion means.

CAP owns only:

- the declared assessment question and scope;
- the domain mapping recorded in `domain_results`;
- the selected CAP composition policy;
- the resulting bounded CAP status.

## 4. Required record properties

A CAP record must disclose:

- stable record identity and profile version;
- creation time and producer;
- subject, question and scope;
- exact source records and validation receipts;
- required domains;
- one domain result per required domain;
- conflicts and unknowns;
- composition policy and coverage;
- derived CAP result;
- claims explicitly not made.

## 5. Native-status preservation

`native_status` is an opaque token owned by the source artifact. CAP must not infer generic success from spelling such as `PASS`, `VALID`, `ADMISSIBLE`, or `CONFORMANT`.

Every domain result therefore includes a human-readable `mapping_rule` and source references. The mapping is a CAP assertion and does not alter the source status.

## 6. Scope closure

`BOUNDED_ACCEPTABLE` is valid only when:

- all required domains are present exactly once;
- every required domain is `SATISFIED`;
- every supporting source has a `VALIDATED` receipt;
- there is no blocking unresolved conflict;
- there is no blocking unknown;
- scope coverage is `full`;
- no tool failure is recorded.

## 7. Prohibited inferences

A CAP record must not claim, solely from CAP composition:

- universal or permanent acceptability;
- world truth;
- source authenticity from hash alone;
- neighboring conformance;
- agent identity, subjectivity, or memory;
- security, privacy, or safety certification;
- causal identity from correlation;
- resolution of a conflict merely because it is disclosed.
