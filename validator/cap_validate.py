#!/usr/bin/env python3
"""Fail-closed reference validator for CAP 0.1-draft."""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except Exception as exc:  # pragma: no cover
    Draft202012Validator = None
    FormatChecker = None
    JSONSCHEMA_IMPORT_ERROR = exc
else:
    JSONSCHEMA_IMPORT_ERROR = None

PINS = {
 "claude.bec": ("gv1983us-commits/behavioral-execution-contract", "62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261"),
 "claude.mpaa": ("gv1983us-commits/mpaa", "0d1aaf35cc4826622f3312fdd2a1c2d40890b965"),
 "claude.pca": ("gv1983us-commits/pca", "a669f023198615ad929f42df84f19380b57ca5ea"),
 "claude.review_protocol": ("gv1983us-commits/repository-canon-review-protocol", "b4205ffd91a6316ab40243cbf8161a1c512cae1f"),
 "claude.arb": ("gv1983us-commits/agent-runtime-boundaries", "bcf9f628ee1d7c2075673b00f660674680bb6f62"),
 "claude.cdts": ("gv1983us-commits/cdts", "ffb9719ae06db0f4f0cdd20b937c2648181a4e4a"),
}
MANDATORY_BOUNDARIES = {
 "world_truth_not_established",
 "global_acceptability_not_established",
 "permanent_runtime_certification_not_claimed",
 "neighbor_conformance_not_imported",
 "native_verdicts_not_redecided",
 "identity_or_subjectivity_not_established",
}

def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out

def reject_constant(value):
    raise ValueError(f"non-finite JSON number: {value}")

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_object, parse_constant=reject_constant)

def unique(values, label, errors):
    seen = set()
    for value in values:
        if value in seen:
            errors.append(f"duplicate {label}: {value}")
        seen.add(value)

def derive(record):
    if "tool_failure" in record:
        return "TOOL_FAILURE"
    conflicts = record.get("conflicts", [])
    if any(c["blocking"] and c["resolution_status"] == "UNRESOLVED" for c in conflicts):
        return "BLOCKED_BY_CONFLICT"
    dispositions = [d["disposition"] for d in record.get("domain_results", [])]
    if "UNSATISFIED" in dispositions:
        return "BOUNDED_UNACCEPTABLE"
    if "UNKNOWN" in dispositions or any(u["blocks_acceptance"] for u in record.get("unknowns", [])):
        return "INSUFFICIENT_EVIDENCE"
    if "CONFLICTING" in dispositions:
        return "BLOCKED_BY_CONFLICT"
    if dispositions and all(d == "SATISFIED" for d in dispositions):
        return "PARTIAL_ASSESSMENT" if record["composition_policy"]["scope_coverage"] == "partial" else "BOUNDED_ACCEPTABLE"
    return None

def semantic_errors(record):
    errors = []
    sources = record.get("source_records", [])
    source_ids = [s["source_id"] for s in sources]
    unique(source_ids, "source_id", errors)
    source_map = {s["source_id"]: s for s in sources}

    for s in sources:
        pin = PINS.get(s["artifact_id"])
        if not pin:
            errors.append(f"unsupported artifact_id: {s['artifact_id']}")
        elif (s["repository"], s["reviewed_revision"]) != pin:
            errors.append(f"pin mismatch for {s['artifact_id']}")
        if s["native_status_owner"] != s["artifact_id"]:
            errors.append(f"native_status_owner mismatch for {s['source_id']}")
        if not s["carried_only"] or s["native_record_validity_established_by_cap"]:
            errors.append(f"native verdict ownership violated for {s['source_id']}")

    required = record.get("required_domains", [])
    results = record.get("domain_results", [])
    result_domains = [d["domain"] for d in results]
    unique(result_domains, "domain result", errors)
    if set(required) != set(result_domains):
        missing = sorted(set(required)-set(result_domains)); extra = sorted(set(result_domains)-set(required))
        if missing: errors.append("missing domain results: " + ", ".join(missing))
        if extra: errors.append("non-required domain results: " + ", ".join(extra))

    conflicts = record.get("conflicts", [])
    unknowns = record.get("unknowns", [])
    unique([c["conflict_id"] for c in conflicts], "conflict_id", errors)
    unique([u["unknown_id"] for u in unknowns], "unknown_id", errors)
    conflict_domains = {d for c in conflicts for d in c["domains"]}
    unknown_domains = {u["domain"] for u in unknowns}

    for d in results:
        refs = d["basis_source_ids"]
        for ref in refs:
            if ref not in source_map: errors.append(f"dangling source reference {ref} in domain {d['domain']}")
        if d["disposition"] in {"SATISFIED","UNSATISFIED"}:
            if not refs: errors.append(f"{d['disposition']} domain lacks source basis: {d['domain']}")
            for ref in refs:
                if ref in source_map and source_map[ref]["validation_receipt"]["status"] != "VALIDATED":
                    errors.append(f"{d['disposition']} domain uses unvalidated source {ref}")
        if d["disposition"] == "UNKNOWN" and d["domain"] not in unknown_domains:
            errors.append(f"UNKNOWN domain lacks unknown entry: {d['domain']}")
        if d["disposition"] == "CONFLICTING" and d["domain"] not in conflict_domains:
            errors.append(f"CONFLICTING domain lacks conflict entry: {d['domain']}")

    for c in conflicts:
        for ref in c["source_ids"]:
            if ref not in source_map: errors.append(f"dangling conflict source reference: {ref}")
        for domain in c["domains"]:
            if domain not in required: errors.append(f"conflict references non-required domain: {domain}")
        if c["resolution_status"] == "RESOLVED":
            if c["blocking"]: errors.append(f"resolved conflict remains blocking: {c['conflict_id']}")
            if not c["resolution_evidence"]: errors.append(f"resolved conflict lacks evidence: {c['conflict_id']}")
        elif c["resolution_evidence"]:
            errors.append(f"unresolved conflict has resolution evidence: {c['conflict_id']}")
        if c["resolution_status"] == "UNRESOLVED" and any(domain in required for domain in c["domains"]) and not c["blocking"]:
            errors.append(f"unresolved required-domain conflict must block: {c['conflict_id']}")

    for u in unknowns:
        for ref in u["source_ids"]:
            if ref not in source_map: errors.append(f"dangling unknown source reference: {ref}")
        if u["domain"] in required and not u["blocks_acceptance"]:
            errors.append(f"required-domain unknown must block acceptance: {u['unknown_id']}")

    policy = record.get("composition_policy", {})
    omissions = policy.get("known_omissions", [])
    if policy.get("scope_coverage") == "partial" and not omissions:
        errors.append("partial coverage requires known_omissions")
    if policy.get("scope_coverage") == "full" and omissions:
        errors.append("full coverage cannot declare known_omissions")

    expected = derive(record)
    actual = record.get("result", {}).get("status")
    if expected is None:
        errors.append("composition policy cannot derive a result")
    elif actual != expected:
        errors.append(f"result mismatch: expected {expected}, got {actual}")

    boundaries = set(record.get("claims_not_made", []))
    missing_boundaries = sorted(MANDATORY_BOUNDARIES - boundaries)
    if missing_boundaries:
        errors.append("missing mandatory claims_not_made: " + ", ".join(missing_boundaries))

    if actual == "TOOL_FAILURE":
        rationale = record.get("result",{}).get("rationale","").lower()
        if any(word in rationale for word in ("passed", "acceptable", "unacceptable", "failed subject")):
            errors.append("TOOL_FAILURE rationale makes a semantic subject verdict")
    return errors

def validate(path: Path):
    if Draft202012Validator is None:
        raise RuntimeError(f"jsonschema unavailable: {JSONSCHEMA_IMPORT_ERROR}")
    record = load_json(path)
    schema_path = Path(__file__).resolve().parents[1] / "schema" / "composite-assessment-record.schema.json"
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = ["schema: " + e.message for e in sorted(validator.iter_errors(record), key=lambda e: list(e.path))]
    if not errors:
        errors.extend(semantic_errors(record))
    return record, errors

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    try:
        record, errors = validate(args.record)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = {"validation_status":"INVALID","cap_result":None,"errors":[str(exc)]}
        if not args.quiet: print(json.dumps(payload, ensure_ascii=False))
        return 1
    except Exception as exc:
        payload = {"validation_status":"TOOL_FAILURE","cap_result":None,"errors":[str(exc)]}
        if not args.quiet: print(json.dumps(payload, ensure_ascii=False))
        return 2
    payload = {"validation_status":"INVALID" if errors else "VALID","cap_result":None if errors else record["result"]["status"],"errors":errors}
    if not args.quiet: print(json.dumps(payload, ensure_ascii=False))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
