# CAP Conflict and Unknown Handling 0.1-draft

## Conflicts

A conflict records materially incompatible evidence or mappings. It includes affected domains, source IDs, blocking status, description, and resolution status.

```text
conflict disclosed != conflict resolved
```

An unresolved blocking conflict yields `BLOCKED_BY_CONFLICT` regardless of otherwise satisfied domains.

A resolved conflict must include `resolution_evidence` and must not remain `blocking: true`.

## Unknowns

An unknown records a missing, unavailable, ambiguous, or non-comparable basis. It names one required domain and whether it blocks acceptance.

A required-domain `UNKNOWN` always prevents `BOUNDED_ACCEPTABLE`. `blocks_acceptance: false` is allowed only for an unknown outside the required-domain decision path; record profile `0.1-draft` normally records such matters as `known_omissions` instead.

```text
missing evidence != success
null != typed unknown
```

## Known omissions

Known omissions describe relevant but intentionally excluded coverage. They must be non-empty when coverage is `partial` and must not be hidden inside free prose.

## Tool failures

A tool failure describes a failed pipeline stage and message. It yields `TOOL_FAILURE` and makes all semantic subject conclusions unavailable.

A `TOOL_FAILURE` record must not use its result rationale to claim that the subject passed or failed.

## Non-blocking conflicts

A resolved, non-blocking conflict may coexist with another result if resolution evidence is disclosed. An unresolved conflict affecting a required domain cannot be made non-blocking merely to obtain acceptance.
