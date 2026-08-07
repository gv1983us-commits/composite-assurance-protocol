import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CapRelease02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = json.loads((ROOT / "ARTIFACT.json").read_text(encoding="utf-8"))
        cls.lock = json.loads((ROOT / "PROFILE_LOCK.json").read_text(encoding="utf-8"))
        cls.lifecycle = json.loads((ROOT / "lifecycle/LIFECYCLE.json").read_text(encoding="utf-8"))
        cls.derivation = json.loads((ROOT / "specification/derivation.json").read_text(encoding="utf-8"))
        cls.invariants = json.loads((ROOT / "specification/invariants.json").read_text(encoding="utf-8"))
        cls.diagnostics = json.loads((ROOT / "specification/diagnostics.json").read_text(encoding="utf-8"))
        cls.expectations = json.loads((ROOT / "conformance/expectations.json").read_text(encoding="utf-8"))

    def test_release_identity_is_synchronized(self):
        self.assertEqual("0.2", self.artifact["artifact_version"])
        self.assertEqual("canonical_public_release", self.artifact["artifact_status"])
        self.assertEqual("0.2", self.lock["protocol_version"])
        self.assertEqual("0.2", self.lifecycle["current_version"])
        self.assertEqual("released", self.lifecycle["status"])
        self.assertEqual("0.1-draft", self.artifact["record_profile_version"])
        self.assertEqual("0.1-draft", self.lock["record_profile_version"])

    def test_lifecycle_contract_is_complete(self):
        expected_profiles = {
            "VERSIONING.md": "cap-versioning/0.2",
            "CHANGELOG.md": "cap-changelog/0.2",
            "COMPATIBILITY.md": "cap-compatibility/0.2",
            "MIGRATION.md": "cap-migration/0.2",
            "ROADMAP.md": "cap-roadmap/0.2",
            "STABILITY_PROMISE.md": "cap-stability-promise/0.2",
        }
        declared = set(self.lifecycle["documents"].values())
        self.assertEqual({f"lifecycle/{name}" for name in expected_profiles}, declared)
        for name, profile in expected_profiles.items():
            text = (ROOT / "lifecycle" / name).read_text(encoding="utf-8")
            self.assertIn(f"`{profile}`", text)
        changelog = (ROOT / "lifecycle/CHANGELOG.md").read_text(encoding="utf-8")
        compatibility = (ROOT / "lifecycle/COMPATIBILITY.md").read_text(encoding="utf-8")
        migration = (ROOT / "lifecycle/MIGRATION.md").read_text(encoding="utf-8")
        self.assertIn("## 0.2", changelog)
        self.assertIn("CAP protocol 0.2", compatibility)
        self.assertIn("0.1-draft → 0.2", migration)

    def test_normative_surface_is_frozen_and_closed(self):
        declared = [item["path"] for item in self.artifact["normative_surfaces"]]
        expected = [
            "spec/01_CAP_CORE.md",
            "spec/02_ASSESSMENT_VOCABULARY.md",
            "spec/03_COMPOSITION_POLICY.md",
            "spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md",
            "spec/05_CONFORMANCE.md",
            "schema/composite-assessment-record.schema.json",
        ]
        self.assertEqual(expected, declared)
        self.assertEqual(len(expected), self.artifact["normative_surface_count"])
        observed_markdown = {str(path.relative_to(ROOT)).replace("\\", "/") for path in (ROOT / "spec").glob("*.md")}
        self.assertEqual(set(expected[:-1]), observed_markdown)
        for path in expected:
            self.assertTrue((ROOT / path).is_file())

    def test_cross_references_are_closed(self):
        result_statuses = set(self.artifact["result_statuses"])
        rule_ids = [rule["rule_id"] for rule in self.derivation["rules"]]
        invariant_ids = [item["invariant_id"] for item in self.invariants["invariants"]]
        codes = set(self.diagnostics["codes"])
        self.assertEqual(len(rule_ids), len(set(rule_ids)))
        self.assertEqual(len(invariant_ids), len(set(invariant_ids)))
        self.assertTrue(all(re.fullmatch(r"CAP-DERIVE-[0-9]{3}", rule_id) for rule_id in rule_ids))
        self.assertTrue({rule["result"] for rule in self.derivation["rules"]} <= result_statuses)
        self.assertTrue({item["diagnostic_code"] for item in self.invariants["invariants"]} <= codes)
        fixture_results = set()
        for expected in self.expectations["fixtures"].values():
            self.assertTrue(set(expected["diagnostic_codes"]) <= codes)
            if expected["cap_result"] is not None:
                fixture_results.add(expected["cap_result"])
        self.assertEqual(result_statuses, fixture_results)

    def test_profile_lock_matches_implementations_and_ci(self):
        self.assertEqual(6, self.lock["normative_surface_count"])
        self.assertEqual("stable", self.lock["diagnostic_registry"])
        self.assertEqual("stable", self.lock["machine_specification"])
        self.assertEqual("required", self.lock["independent_implementation"])
        self.assertTrue((ROOT / "validator/cap_validate.py").is_file())
        self.assertTrue((ROOT / "independent/node/cap_validate.mjs").is_file())
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        for version in self.lock["required_runtimes"]["python"]:
            self.assertIn(f'"{version}"', workflow)
        for version in self.lock["required_runtimes"]["node"]:
            self.assertIn(f'"{version}"', workflow)
        self.assertTrue(self.artifact["assertion_boundaries"]["multi_implementation_conformance_claimed"])


if __name__ == "__main__":
    unittest.main()
