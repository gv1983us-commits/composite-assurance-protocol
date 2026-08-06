# CAP Assessment Vocabulary 0.1-draft

## Domain dispositions

### `SATISFIED`
The CAP mapping asserts that available validated source evidence satisfies the declared domain requirement within scope.

### `UNSATISFIED`
The CAP mapping asserts a decisive domain failure within scope.

### `UNKNOWN`
The available evidence cannot support either satisfaction or decisive failure.

### `CONFLICTING`
Relevant source evidence is materially incompatible and requires conflict handling.

`CONFLICTING` is never equivalent to `UNKNOWN`; it asserts known disagreement.

## CAP result statuses

### `BOUNDED_ACCEPTABLE`
All required domains are satisfied under full declared coverage with no higher-precedence blocker.

### `BOUNDED_UNACCEPTABLE`
At least one required domain is decisively unsatisfied and no higher-precedence tool failure or blocking conflict controls the result.

### `INSUFFICIENT_EVIDENCE`
At least one required domain remains unknown and no higher-precedence condition controls the result.

### `BLOCKED_BY_CONFLICT`
At least one unresolved blocking conflict prevents a bounded decision.

### `PARTIAL_ASSESSMENT`
All required in-scope domains are satisfied, but declared coverage is partial and known omissions prevent a full bounded acceptance claim.

### `TOOL_FAILURE`
The assessment pipeline failed before it could produce a reliable semantic result. This status is not evidence about the assessed subject.

## Validation-receipt statuses

- `VALIDATED`: a named source-owned or explicitly identified validator receipt exists.
- `NOT_VALIDATED`: validation was not performed.
- `UNAVAILABLE`: validation evidence could not be obtained.

CAP validation checks the receipt declaration and CAP mapping. It does not thereby establish the native record’s truth.

## Claim classes

- `native`: owned by a source artifact.
- `mapped_domain`: asserted by CAP for one required domain.
- `composite`: the final CAP status.
- `boundary`: an explicit claim not made.

No claim class silently upgrades another.
