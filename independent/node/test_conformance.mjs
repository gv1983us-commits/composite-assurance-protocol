#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateFile } from './cap_validate.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const expectations = JSON.parse(fs.readFileSync(path.join(ROOT, 'conformance/expectations.json'), 'utf8'));
const fixtures = path.join(ROOT, 'conformance/fixtures');
let failures = 0;

for (const [name, expected] of Object.entries(expectations.fixtures).sort()) {
  const [exitCode, payload] = validateFile(path.join(fixtures, name));
  const checks = [
    ['exit_code', exitCode, expected.exit_code],
    ['validation_status', payload.validation_status, expected.validation_status],
    ['cap_result', payload.cap_result, expected.cap_result],
    ['diagnostic_codes', payload.diagnostic_codes, expected.diagnostic_codes],
  ];
  for (const [field, observed, wanted] of checks) {
    if (JSON.stringify(observed) !== JSON.stringify(wanted)) {
      failures += 1;
      console.error(`${name}: ${field}: observed=${JSON.stringify(observed)} expected=${JSON.stringify(wanted)}`);
    }
  }
}

if (failures) {
  console.error(`Node conformance failed: ${failures} mismatches`);
  process.exit(1);
}
console.log(`Node conformance passed: ${Object.keys(expectations.fixtures).length} fixtures`);
