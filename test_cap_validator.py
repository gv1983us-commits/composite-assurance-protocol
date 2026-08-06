import copy, json, tempfile, unittest
from pathlib import Path
from validator.cap_validate import validate, derive

ROOT = Path(__file__).resolve().parent

class CapValidatorTests(unittest.TestCase):
    def test_all_valid_fixtures(self):
        for path in sorted((ROOT/'conformance/fixtures').glob('valid-*.json')):
            with self.subTest(path=path.name):
                record, errors = validate(path)
                self.assertEqual([], errors)
                self.assertEqual(record['result']['status'], derive(record))

    def test_all_invalid_fixtures(self):
        for path in sorted((ROOT/'conformance/fixtures').glob('invalid-*.json')):
            with self.subTest(path=path.name):
                _, errors = validate(path)
                self.assertTrue(errors)

    def test_malformed_fixtures_rejected(self):
        for path in sorted((ROOT/'conformance/fixtures').glob('malformed-*.json')):
            with self.subTest(path=path.name):
                with self.assertRaises((ValueError, json.JSONDecodeError)):
                    validate(path)

    def test_canonical_example_is_acceptable(self):
        record, errors = validate(ROOT/'examples/bounded-runtime-assessment.json')
        self.assertEqual([], errors)
        self.assertEqual('BOUNDED_ACCEPTABLE', record['result']['status'])

if __name__ == '__main__': unittest.main()
