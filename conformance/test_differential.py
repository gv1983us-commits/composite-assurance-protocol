import contextlib
import copy
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from validator import cap_validate_diagnostic

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "conformance" / "fixtures" / "valid-bounded-acceptable.json"
NODE = ROOT / "independent" / "node" / "cap_validate.mjs"


def python_validate(path):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exit_code = cap_validate_diagnostic.main([str(path)])
    return exit_code, json.loads(output.getvalue())


def node_validate(path):
    completed = subprocess.run(
        ["node", str(NODE), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode not in {0, 1, 2}:
        raise AssertionError(
            f"Node validator returned unexpected exit code {completed.returncode}: {completed.stderr}"
        )
    return completed.returncode, json.loads(completed.stdout)


def mutation_cases(base):
    cases = []

    def add(name, mutate):
        record = copy.deepcopy(base)
        mutate(record)
        cases.append((name, record))

    add("pin_mismatch", lambda r: r["source_records"][0].__setitem__("reviewed_revision", "0" * 40))
    add("native_owner_mismatch", lambda r: r["source_records"][0].__setitem__("native_status_owner", "claude.mpaa"))
    add("carried_only_false", lambda r: r["source_records"][0].__setitem__("carried_only", False))
    add("native_validity_redecided", lambda r: r["source_records"][0].__setitem__("native_record_validity_established_by_cap", True))
    add("duplicate_source_id", lambda r: r["source_records"][1].__setitem__("source_id", r["source_records"][0]["source_id"]))
    add("missing_domain_result", lambda r: r["domain_results"].pop())

    def extra_domain_result(r):
        item = copy.deepcopy(r["domain_results"][0])
        item["domain"] = "unexpected_domain"
        r["domain_results"].append(item)

    add("extra_domain_result", extra_domain_result)
    add("dangling_basis_source", lambda r: r["domain_results"][0].__setitem__("basis_source_ids", ["src:missing"]))
    add("empty_satisfied_basis", lambda r: r["domain_results"][0].__setitem__("basis_source_ids", []))
    add("unknown_without_unknown_record", lambda r: r["domain_results"][0].__setitem__("disposition", "UNKNOWN"))
    add("conflicting_without_conflict_record", lambda r: r["domain_results"][0].__setitem__("disposition", "CONFLICTING"))

    def partial_without_omissions(r):
        r["composition_policy"]["scope_coverage"] = "partial"
        r["composition_policy"]["known_omissions"] = []

    add("partial_without_omissions", partial_without_omissions)

    def full_with_omission(r):
        r["composition_policy"]["scope_coverage"] = "full"
        r["composition_policy"]["known_omissions"] = ["declared omission"]

    add("full_with_omission", full_with_omission)
    add("result_mismatch", lambda r: r["result"].__setitem__("status", "BOUNDED_UNACCEPTABLE"))
    add("missing_mandatory_boundary", lambda r: r["claims_not_made"].remove("world_truth_not_established"))

    def unsupported_artifact(r):
        r["source_records"][0]["artifact_id"] = "claude.unknown"
        r["source_records"][0]["native_status_owner"] = "claude.unknown"

    add("unsupported_artifact", unsupported_artifact)
    return cases


class CrossRuntimeDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("node") is None:
            raise unittest.SkipTest("Node runtime is not installed; enforced by the dedicated differential CI job")
        cls.base = json.loads(BASE.read_text(encoding="utf-8"))

    def test_reference_and_independent_implementations_agree_on_adversarial_mutations(self):
        cases = mutation_cases(self.base)
        self.assertGreaterEqual(len(cases), 16)
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            for name, record in cases:
                with self.subTest(case=name):
                    path = directory / f"{name}.json"
                    path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
                    py_code, py_payload = python_validate(path)
                    node_code, node_payload = node_validate(path)
                    self.assertEqual(py_code, node_code)
                    self.assertEqual(py_payload["validation_status"], node_payload["validation_status"])
                    self.assertEqual(py_payload["cap_result"], node_payload["cap_result"])
                    self.assertEqual(py_payload["diagnostic_codes"], node_payload["diagnostic_codes"])
                    self.assertNotEqual("VALID", py_payload["validation_status"])

    def test_reference_and_independent_implementations_agree_on_valid_baseline(self):
        py_code, py_payload = python_validate(BASE)
        node_code, node_payload = node_validate(BASE)
        self.assertEqual(py_code, node_code)
        self.assertEqual(0, py_code)
        self.assertEqual(py_payload["validation_status"], node_payload["validation_status"])
        self.assertEqual(py_payload["cap_result"], node_payload["cap_result"])
        self.assertEqual(py_payload["diagnostic_codes"], node_payload["diagnostic_codes"])


if __name__ == "__main__":
    unittest.main()
