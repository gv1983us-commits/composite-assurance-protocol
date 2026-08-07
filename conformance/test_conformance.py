import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from validator import cap_validate
from validator import cap_validate_diagnostic
from validator.diagnostics import CODE_RE, classify

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "fixtures"
EXPECTATIONS = ROOT / "conformance" / "expectations.json"
SCHEMA = ROOT / "schema" / "composite-assessment-record.schema.json"


class ConformanceCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expectations = json.loads(EXPECTATIONS.read_text(encoding="utf-8"))["fixtures"]
        cls.schema = cap_validate.load_json(SCHEMA)
        cls.schema_validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(self.schema)

    def test_expectations_cover_the_entire_corpus(self):
        fixture_names = {path.name for path in FIXTURES.glob("*.json")}
        self.assertEqual(fixture_names, set(self.expectations))

    def test_every_fixture_matches_its_machine_readable_expectation(self):
        observed_results = set()
        observed_diagnostics = set()
        for name, expected in sorted(self.expectations.items()):
            with self.subTest(fixture=name):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    exit_code = cap_validate_diagnostic.main([str(FIXTURES / name)])
                payload = json.loads(output.getvalue())
                self.assertEqual(expected["exit_code"], exit_code)
                self.assertEqual(expected["validation_status"], payload["validation_status"])
                self.assertEqual(expected["cap_result"], payload["cap_result"])
                self.assertEqual(expected["diagnostic_codes"], payload["diagnostic_codes"])
                for error in payload["errors"]:
                    self.assertRegex(error, CODE_RE)
                    self.assertEqual(error.split(" ", 1)[0], classify(error))
                observed_diagnostics.update(payload["diagnostic_codes"])
                if payload["cap_result"] is not None:
                    observed_results.add(payload["cap_result"])
        self.assertEqual(
            {
                "BOUNDED_ACCEPTABLE",
                "BOUNDED_UNACCEPTABLE",
                "INSUFFICIENT_EVIDENCE",
                "BLOCKED_BY_CONFLICT",
                "PARTIAL_ASSESSMENT",
                "TOOL_FAILURE",
            },
            observed_results,
        )
        self.assertTrue({"CAP-JSON-001", "CAP-SCHEMA-001", "CAP-SEM-003"} <= observed_diagnostics)

    def test_structural_and_semantic_validation_are_distinct(self):
        valid = cap_validate.load_json(FIXTURES / "valid-bounded-acceptable.json")
        self.assertEqual([], list(self.schema_validator.iter_errors(valid)))
        self.assertEqual([], cap_validate.semantic_errors(valid))

        structurally_invalid = copy.deepcopy(valid)
        structurally_invalid["global_pass"] = True
        self.assertTrue(list(self.schema_validator.iter_errors(structurally_invalid)))

        semantically_invalid = copy.deepcopy(valid)
        semantically_invalid["source_records"][0]["reviewed_revision"] = "0" * 40
        self.assertEqual([], list(self.schema_validator.iter_errors(semantically_invalid)))
        self.assertTrue(
            any("pin mismatch" in error for error in cap_validate.semantic_errors(semantically_invalid))
        )

    def test_validate_stops_after_structural_failure(self):
        valid = cap_validate.load_json(FIXTURES / "valid-bounded-acceptable.json")
        valid["global_pass"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(valid), encoding="utf-8")
            _, errors = cap_validate.validate(path)
        self.assertTrue(errors)
        self.assertTrue(all(error.startswith("schema: ") for error in errors))


if __name__ == "__main__":
    unittest.main()
