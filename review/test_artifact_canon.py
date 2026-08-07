import json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
 'README.md','CANON.md','ARTIFACT.json','RELATIONS.md','PROVENANCE.md','LICENSE','AGENTS.md','DIAGNOSTICS.md',
 'spec/01_CAP_CORE.md','spec/02_ASSESSMENT_VOCABULARY.md','spec/03_COMPOSITION_POLICY.md',
 'spec/04_CONFLICT_AND_UNKNOWN_HANDLING.md','spec/05_CONFORMANCE.md',
 'schema/composite-assessment-record.schema.json','validator/cap_validate.py',
 'validator/cap_validate_diagnostic.py','validator/diagnostics.py',
 'conformance/__init__.py','conformance/expectations.json','conformance/test_conformance.py',
 'conformance/test_machine_specification.py','specification/README.md',
 'specification/vocabulary.json','specification/derivation.json',
 'specification/invariants.json','specification/diagnostics.json',
 'independent/node/cap_validate.mjs','independent/node/test_conformance.mjs',
 'references/PINNED_ARTIFACT_REVISIONS.md','.github/workflows/ci.yml'
}

class ArtifactCanonTests(unittest.TestCase):
    def setUp(self):
        self.artifact=json.loads((ROOT/'ARTIFACT.json').read_text())
        self.schema=json.loads((ROOT/'schema/composite-assessment-record.schema.json').read_text())

    def test_required_surfaces_exist(self):
        missing=[p for p in EXPECTED if not (ROOT/p).is_file()]
        self.assertEqual([], missing)

    def test_identity(self):
        self.assertEqual('claude.cap', self.artifact['artifact_id'])
        self.assertEqual('canonical_public_draft', self.artifact['artifact_status'])
        self.assertEqual('bounded_cross_artifact_assessment', self.artifact['claim_domain'])
        self.assertEqual(6, self.artifact['normative_surface_count'])
        self.assertEqual(6, len(self.artifact['normative_surfaces']))

    def test_six_exact_relations(self):
        self.assertEqual(6, len(self.artifact['relations']))
        self.assertEqual(6, len({r['artifact_id'] for r in self.artifact['relations']}))
        for relation in self.artifact['relations']:
            self.assertRegex(relation['reviewed_revision'], r'^[0-9a-f]{40}$')
            self.assertTrue(relation['native_verdict_carried_only'])
            self.assertFalse(relation['native_verdict_redecided'])
            self.assertFalse(relation['global_conclusion_imported'])

    def test_schema_identity(self):
        self.assertEqual('https://json-schema.org/draft/2020-12/schema', self.schema['$schema'])
        self.assertIn('gv1983us-commits/composite-assurance-protocol', self.schema['$id'])
        self.assertFalse(self.schema['additionalProperties'])

    def test_conformance_oracle_is_declared(self):
        expectations=json.loads((ROOT/'conformance/expectations.json').read_text())
        self.assertEqual('cap-conformance-expectations/0.3', expectations['profile'])
        self.assertTrue(expectations['fixtures'])
        for expected in expectations['fixtures'].values():
            self.assertIn('diagnostic_codes', expected)

    def test_machine_specification_profiles_are_declared(self):
        expected={
            'vocabulary.json':'cap-machine-vocabulary/0.1',
            'derivation.json':'cap-derivation-rules/0.1',
            'invariants.json':'cap-semantic-invariants/0.1',
            'diagnostics.json':'cap-diagnostic-registry/0.1',
        }
        for name, profile in expected.items():
            payload=json.loads((ROOT/'specification'/name).read_text())
            self.assertEqual(profile, payload['profile'])

    def test_independent_node_implementation_is_declared(self):
        text=(ROOT/'independent/node/cap_validate.mjs').read_text()
        self.assertIn("implementation: 'cap-node-independent/0.1'", text)
        self.assertNotIn('validator/cap_validate.py', text)

    def test_no_placeholders_or_sensitive_markers(self):
        bad=('TO'+'DO','TB'+'D','REPLACE'+'_ME','BEGIN PRIVATE'+' KEY')
        for path in ROOT.rglob('*'):
            if path.is_file() and '.git' not in path.parts and path.suffix in {'.md','.json','.py','.yml','.mjs'}:
                text=path.read_text(encoding='utf-8')
                for token in bad:
                    self.assertNotIn(token,text,f'{token} in {path}')

if __name__ == '__main__': unittest.main()
