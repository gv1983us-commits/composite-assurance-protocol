# CAP Relations

CAP has asymmetric fixed-revision relations with six existing artifacts. The neighboring repositories do not need to point back to the CAP acceptance revision.

| Artifact | Reviewed revision | CAP role |
|---|---|---|
| BEC | `62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261` | execution evidence source |
| MPAA | `0d1aaf35cc4826622f3312fdd2a1c2d40890b965` | runtime architecture source |
| PCA | `a669f023198615ad929f42df84f19380b57ca5ea` | process continuation source |
| Repository Canon and Review Protocol | `b4205ffd91a6316ab40243cbf8161a1c512cae1f` | source and review policy |
| ARB | `bcf9f628ee1d7c2075673b00f660674680bb6f62` | analytical boundary context |
| CDTS | `ffb9719ae06db0f4f0cdd20b937c2648181a4e4a` | correlation trace source |

## BEC → CAP

BEC can supply a native execution-evidence result. CAP may map that carried result to one declared assessment domain, but it does not re-run BEC semantics or turn task-scoped evidence into global reliability.

## MPAA → CAP

MPAA can supply architecture and runtime-report conclusions. CAP does not convert MPAA conformance into task success, continuity, source quality, or universal runtime fitness.

## PCA → CAP

PCA can supply a bounded continuation assessment. CAP does not treat continuation as identity, memory, subjectivity, or uninterrupted persistence.

## Review Protocol → CAP

Review Protocol can supply source-selection and fixed-revision receipts. CAP does not treat a valid review receipt as source truth, donor safety, or neighboring conformance.

## ARB → CAP

ARB supplies analytical boundary context. It has no external normative force; CAP may use its distinctions only as declared analysis, never as an imported standard verdict.

## CDTS → CAP

CDTS can establish admissibility of a cross-domain correlation trace. CAP does not interpret `ADMISSIBLE` as event identity, causality, authenticity, completeness, or `BOUNDED_ACCEPTABLE`.

## Shared boundary

```text
source relation != conclusion ownership transfer
exact pin != source truth
native status carried != native status re-decided
CAP composition != merged specification
```
