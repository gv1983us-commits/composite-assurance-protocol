# CAP Composition Policy 0.1-draft

## 1. Required policy

Record profile `0.1-draft` supports the policy:

```text
cap.all_required_domains_satisfied_no_blocking_conflict.v1
```

Its rule token is:

```text
all_required_domains_satisfied_no_blocking_conflict
```

## 2. Preconditions

Before result derivation:

1. source pins must belong to the active compatibility set;
2. record IDs, source IDs, required domains, conflict IDs and unknown IDs must be unique;
3. domain results must cover required domains exactly once;
4. every source reference must resolve;
5. `SATISFIED` and `UNSATISFIED` mappings must cite at least one `VALIDATED` source;
6. `UNKNOWN` must have a matching unknown entry;
7. `CONFLICTING` must have a matching conflict entry;
8. native verdicts must be carried only and not re-decided.

## 3. Precedence

The deterministic result order is:

1. if `tool_failure` exists → `TOOL_FAILURE`;
2. else if an unresolved conflict is `blocking: true` → `BLOCKED_BY_CONFLICT`;
3. else if any required domain is `UNSATISFIED` → `BOUNDED_UNACCEPTABLE`;
4. else if any required domain is `UNKNOWN` or any blocking unknown exists → `INSUFFICIENT_EVIDENCE`;
5. else if any required domain is `CONFLICTING` → `BLOCKED_BY_CONFLICT`;
6. else if all required domains are `SATISFIED` and coverage is `partial` → `PARTIAL_ASSESSMENT`;
7. else if all required domains are `SATISFIED` and coverage is `full` → `BOUNDED_ACCEPTABLE`;
8. otherwise the record is invalid.

## 4. No score averaging

CAP `0.1-draft` forbids numeric averaging, majority vote, confidence-weighted global pass, or silent domain substitution.

A strong result in one domain cannot compensate for a missing or failed required domain.

## 5. Decisive negative

A decisive `UNSATISFIED` domain controls over unknowns but not over tool failure or a blocking conflict. The negative is still limited to the declared assessment question and scope.

## 6. Partial coverage

`partial` coverage requires at least one non-empty `known_omissions` entry. It cannot yield `BOUNDED_ACCEPTABLE`.
