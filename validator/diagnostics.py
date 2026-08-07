"""Stable machine-readable diagnostic codes for the CAP reference validator."""
from __future__ import annotations

import re

CODE_RE = re.compile(r"^(CAP-[A-Z]+-[0-9]{3})\b")

TEXT_RULES = (
    ("duplicate JSON key:", "CAP-JSON-001"),
    ("non-finite JSON number:", "CAP-JSON-002"),
    ("schema:", "CAP-SCHEMA-001"),
    ("duplicate source_id:", "CAP-SEM-001"),
    ("unsupported artifact_id:", "CAP-SEM-002"),
    ("pin mismatch for", "CAP-SEM-003"),
    ("native_status_owner mismatch", "CAP-SEM-004"),
    ("native verdict ownership violated", "CAP-SEM-005"),
    ("duplicate domain result:", "CAP-SEM-006"),
    ("missing domain results:", "CAP-SEM-007"),
    ("non-required domain results:", "CAP-SEM-008"),
    ("duplicate conflict_id:", "CAP-SEM-009"),
    ("duplicate unknown_id:", "CAP-SEM-010"),
    ("dangling source reference", "CAP-SEM-011"),
    ("domain lacks source basis:", "CAP-SEM-012"),
    ("domain uses unvalidated source", "CAP-SEM-013"),
    ("UNKNOWN domain lacks unknown entry:", "CAP-SEM-014"),
    ("CONFLICTING domain lacks conflict entry:", "CAP-SEM-015"),
    ("dangling conflict source reference:", "CAP-SEM-016"),
    ("conflict references non-required domain:", "CAP-SEM-017"),
    ("resolved conflict remains blocking:", "CAP-SEM-018"),
    ("resolved conflict lacks evidence:", "CAP-SEM-019"),
    ("unresolved conflict has resolution evidence:", "CAP-SEM-020"),
    ("unresolved required-domain conflict must block:", "CAP-SEM-021"),
    ("dangling unknown source reference:", "CAP-SEM-022"),
    ("required-domain unknown must block acceptance:", "CAP-SEM-023"),
    ("partial coverage requires known_omissions", "CAP-SEM-024"),
    ("full coverage cannot declare known_omissions", "CAP-SEM-025"),
    ("composition policy cannot derive a result", "CAP-SEM-026"),
    ("result mismatch:", "CAP-SEM-027"),
    ("missing mandatory claims_not_made:", "CAP-SEM-028"),
    ("TOOL_FAILURE rationale makes a semantic subject verdict", "CAP-SEM-029"),
)


def classify(message: str) -> str:
    match = CODE_RE.match(message)
    if match:
        return match.group(1)
    for fragment, code in TEXT_RULES:
        if fragment in message:
            return code
    return "CAP-TOOL-999"


def annotate(message: str) -> str:
    if CODE_RE.match(message):
        return message
    return f"{classify(message)} {message}"


def codes(messages: list[str]) -> list[str]:
    ordered = []
    for message in messages:
        code = classify(message)
        if code not in ordered:
            ordered.append(code)
    return ordered
