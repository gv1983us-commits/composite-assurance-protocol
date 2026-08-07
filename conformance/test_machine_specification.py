import json
import unittest
from pathlib import Path

from validator import cap_validate, diagnostics

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specification"
FIXTURES = ROOT / "conformance" / "fixtures"


def facts(record):
    dispositions = [item["disposition"] for item in record.get("domain_results", [])]
    return {
        "tool_failure_present": "tool_failure" in record,
        "unresolved_blocking_conflict_present": any(
            item["blocking"] and item["resolution_status"] == "UNRESOLVED"
            for item in record.get("conflicts", [])
        ),
        "unsatisfied_domain_present": "UNSATISFIED" in dispositions,
        "unknown_domain_present": "UNKNOWN" in dispositions,
        "blocking_unknown_present": any(
            item["blocks_acceptance"] for item in record.get("unknowns", [])
        ),
        "conflicting_domain_present": "CONFLICTING" in dispositions,
        "all_domains_satisfied": bool(dispositions) and all(
            item == "SATISFIED" for item in dispositions
        ),
        "scope_coverage": record.get("composition_policy", {}).get("scope_coverage"),
    }


def condition_matches(condition, observed):
    if "fact" in condition:
        return observed.get(condition["fact"]) == condition["equals"]
    if "all" in condition:
        return all(condition_matches(item, observed) for item in condition["all"])
    if "any" in condition:
        return any(condition_matches(item, observed) for item in condition["any"])
    raise AssertionError(f"unsupported condition: {condition}")


def machine_derive(record, derivation):
    observed = facts(record)
    for rule in derivation["rules"]:
        if condition_matches(rule["when"], observed):
            return rule["result"]
    return derivation["no_match"]


class MachineSpecificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vocabulary = json.loads((SPEC / "vocabulary.json").read_text(encoding="utf-8"))
        cls.derivation = json.loads((SPEC / "derivation.json").read_text(encoding="utf-8"))
        cls.invariants = json.loads((SPEC / "invariants.json").read_text(encoding="utf-8"))
        cls.diagnostic_registry = json.loads((SPEC / "diagnostics.json").read_text(encoding="utf-8"))

    def test_profiles_and_rule_ids_are_unique(self):
        self.assertEqual("cap-machine-vocabulary/0.1", self.vocabulary["profile"])
        self.assertEqual("cap-derivation-rules/0.1", self.derivation["profile"])
        self.assertEqual("cap-semantic-invariants/0.1", self.invariants["profile"])
        self.assertEqual("cap-diagnostic-registry/0.1", self.diagnostic_registry["profile"])
        rule_ids = [rule["rule_id"] for rule in self.derivation["rules"]]
        invariant_ids = [item["invariant_id"] for item in self.invariants["invariants"]]
        self.assertEqual(len(rule_ids), len(set(rule_ids)))
        self.assertEqual(len(invariant_ids), len(set(invariant_ids)))

    def test_vocabulary_matches_reference_implementation(self):
        expected_results = {
            "TOOL_FAILURE", "BLOCKED_BY_CONFLICT", "BOUNDED_UNACCEPTABLE",
            "INSUFFICIENT_EVIDENCE", "PARTIAL_ASSESSMENT", "BOUNDED_ACCEPTABLE",
        }
        self.assertEqual(expected_results, set(self.vocabulary["results"]))
        self.assertEqual(
            {"SATISFIED", "UNSATISFIED", "UNKNOWN", "CONFLICTING"},
            set(self.vocabulary["dispositions"]),
        )

    def test_machine_derivation_matches_python_for_entire_parseable_corpus(self):
        compared = 0
        for path in sorted(FIXTURES.glob("*.json")):
            try:
                record = cap_validate.load_json(path)
            except ValueError:
                continue
            with self.subTest(fixture=path.name):
                self.assertEqual(cap_validate.derive(record), machine_derive(record, self.derivation))
                compared += 1
        self.assertGreaterEqual(compared, 15)

    def test_invariants_reference_registered_diagnostics(self):
        registered = set(self.diagnostic_registry["codes"])
        invariant_codes = {item["diagnostic_code"] for item in self.invariants["invariants"]}
        self.assertTrue(invariant_codes <= registered)
        self.assertEqual(29, len(invariant_codes))

    def test_python_diagnostic_classifier_is_covered_by_registry(self):
        registered = set(self.diagnostic_registry["codes"])
        implementation_codes = {code for _, code in diagnostics.TEXT_RULES} | {"CAP-TOOL-999"}
        self.assertEqual(implementation_codes, registered)

    def test_derivation_priority_is_complete_and_unambiguous(self):
        expected = [
            "TOOL_FAILURE", "BLOCKED_BY_CONFLICT", "BOUNDED_UNACCEPTABLE",
            "INSUFFICIENT_EVIDENCE", "BLOCKED_BY_CONFLICT",
            "PARTIAL_ASSESSMENT", "BOUNDED_ACCEPTABLE",
        ]
        self.assertEqual(expected, [rule["result"] for rule in self.derivation["rules"]])
        self.assertEqual("first_matching_rule", self.derivation["evaluation"])


if __name__ == "__main__":
    unittest.main()
