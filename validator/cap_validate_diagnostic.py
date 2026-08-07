#!/usr/bin/env python3
"""Diagnostic-code CLI for the CAP reference validator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validator import cap_validate
from validator.diagnostics import annotate, codes


def build_payload(validation_status, cap_result, errors):
    annotated = [annotate(error) for error in errors]
    return {
        "validation_status": validation_status,
        "cap_result": cap_result,
        "diagnostic_codes": codes(annotated),
        "errors": annotated,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    try:
        record, errors = cap_validate.validate(args.record)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = build_payload("INVALID", None, [str(exc)])
        exit_code = 1
    except Exception as exc:
        payload = build_payload("TOOL_FAILURE", None, [str(exc)])
        exit_code = 2
    else:
        payload = build_payload(
            "INVALID" if errors else "VALID",
            None if errors else record["result"]["status"],
            errors,
        )
        exit_code = 1 if errors else 0
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
