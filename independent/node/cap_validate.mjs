#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const SCHEMA = JSON.parse(fs.readFileSync(path.join(ROOT, 'schema/composite-assessment-record.schema.json'), 'utf8'));
const DERIVATION = JSON.parse(fs.readFileSync(path.join(ROOT, 'specification/derivation.json'), 'utf8'));
const DIAGNOSTICS = JSON.parse(fs.readFileSync(path.join(ROOT, 'specification/diagnostics.json'), 'utf8'));

const PINS = new Map([
  ['claude.bec', ['gv1983us-commits/behavioral-execution-contract', '62f2b7940b5ca7a4a8b24150b9c45a6ab5d97261']],
  ['claude.mpaa', ['gv1983us-commits/mpaa', '0d1aaf35cc4826622f3312fdd2a1c2d40890b965']],
  ['claude.pca', ['gv1983us-commits/pca', 'a669f023198615ad929f42df84f19380b57ca5ea']],
  ['claude.review_protocol', ['gv1983us-commits/repository-canon-review-protocol', 'b4205ffd91a6316ab40243cbf8161a1c512cae1f']],
  ['claude.arb', ['gv1983us-commits/agent-runtime-boundaries', 'bcf9f628ee1d7c2075673b00f660674680bb6f62']],
  ['claude.cdts', ['gv1983us-commits/cdts', 'ffb9719ae06db0f4f0cdd20b937c2648181a4e4a']],
]);
const MANDATORY_BOUNDARIES = new Set([
  'world_truth_not_established',
  'global_acceptability_not_established',
  'permanent_runtime_certification_not_claimed',
  'neighbor_conformance_not_imported',
  'native_verdicts_not_redecided',
  'identity_or_subjectivity_not_established',
]);

class StrictJsonParser {
  constructor(text) { this.text = text; this.i = 0; }
  parse() { const value = this.value(); this.ws(); if (this.i !== this.text.length) this.fail('trailing JSON data'); return value; }
  ws() { while (/\s/.test(this.text[this.i] ?? '')) this.i += 1; }
  fail(message) { throw new Error(message); }
  value() {
    this.ws(); const c = this.text[this.i];
    if (c === '{') return this.object();
    if (c === '[') return this.array();
    if (c === '"') return this.string();
    if (c === '-' || /[0-9]/.test(c ?? '')) return this.number();
    for (const [token, value] of [['true', true], ['false', false], ['null', null]]) {
      if (this.text.startsWith(token, this.i)) { this.i += token.length; return value; }
    }
    this.fail(`invalid JSON token at offset ${this.i}`);
  }
  object() {
    const out = {}; const seen = new Set(); this.i += 1; this.ws();
    if (this.text[this.i] === '}') { this.i += 1; return out; }
    while (true) {
      this.ws(); if (this.text[this.i] !== '"') this.fail('object key must be a string');
      const key = this.string();
      if (seen.has(key)) this.fail(`duplicate JSON key: ${key}`);
      seen.add(key); this.ws(); if (this.text[this.i++] !== ':') this.fail('missing colon after object key');
      out[key] = this.value(); this.ws(); const c = this.text[this.i++];
      if (c === '}') return out;
      if (c !== ',') this.fail('missing comma in object');
    }
  }
  array() {
    const out = []; this.i += 1; this.ws();
    if (this.text[this.i] === ']') { this.i += 1; return out; }
    while (true) {
      out.push(this.value()); this.ws(); const c = this.text[this.i++];
      if (c === ']') return out;
      if (c !== ',') this.fail('missing comma in array');
    }
  }
  string() {
    const start = this.i; this.i += 1; let escaped = false;
    while (this.i < this.text.length) {
      const c = this.text[this.i++];
      if (escaped) { escaped = false; continue; }
      if (c === '\\') { escaped = true; continue; }
      if (c === '"') return JSON.parse(this.text.slice(start, this.i));
      if (c.charCodeAt(0) < 0x20) this.fail('control character in string');
    }
    this.fail('unterminated string');
  }
  number() {
    const rest = this.text.slice(this.i); const match = rest.match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
    if (!match) this.fail(`invalid JSON number at offset ${this.i}`);
    this.i += match[0].length; const value = Number(match[0]);
    if (!Number.isFinite(value)) this.fail(`non-finite JSON number: ${match[0]}`);
    return value;
  }
}

function parseStrict(text) { return new StrictJsonParser(text).parse(); }
function resolveRef(ref) {
  if (!ref.startsWith('#/')) throw new Error(`unsupported schema ref: ${ref}`);
  return ref.slice(2).split('/').reduce((node, part) => node[part.replace(/~1/g, '/').replace(/~0/g, '~')], SCHEMA);
}
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function schemaErrors(value, schema, location = '$') {
  if (schema.$ref) return schemaErrors(value, resolveRef(schema.$ref), location);
  const errors = [];
  if ('const' in schema && !same(value, schema.const)) errors.push(`${location}: const mismatch`);
  if (schema.enum && !schema.enum.some(v => same(v, value))) errors.push(`${location}: value not in enum`);
  if (schema.type === 'object') {
    if (value === null || Array.isArray(value) || typeof value !== 'object') return [`${location}: expected object`];
    for (const key of schema.required ?? []) if (!(key in value)) errors.push(`${location}: missing required property ${key}`);
    if (schema.additionalProperties === false) {
      for (const key of Object.keys(value)) if (!(key in (schema.properties ?? {}))) errors.push(`${location}: additional property ${key}`);
    }
    for (const [key, child] of Object.entries(schema.properties ?? {})) if (key in value) errors.push(...schemaErrors(value[key], child, `${location}.${key}`));
  } else if (schema.type === 'array') {
    if (!Array.isArray(value)) return [`${location}: expected array`];
    if (schema.minItems !== undefined && value.length < schema.minItems) errors.push(`${location}: minItems`);
    if (schema.uniqueItems && new Set(value.map(v => JSON.stringify(v))).size !== value.length) errors.push(`${location}: duplicate array item`);
    if (schema.items) value.forEach((item, index) => errors.push(...schemaErrors(item, schema.items, `${location}[${index}]`)));
  } else if (schema.type === 'string') {
    if (typeof value !== 'string') return [`${location}: expected string`];
    if (schema.minLength !== undefined && value.length < schema.minLength) errors.push(`${location}: minLength`);
    if (schema.pattern && !(new RegExp(schema.pattern).test(value))) errors.push(`${location}: pattern mismatch`);
    if (schema.format === 'date-time' && Number.isNaN(Date.parse(value))) errors.push(`${location}: invalid date-time`);
  } else if (schema.type === 'boolean' && typeof value !== 'boolean') errors.push(`${location}: expected boolean`);
  return errors;
}

function facts(record) {
  const dispositions = (record.domain_results ?? []).map(d => d.disposition);
  return {
    tool_failure_present: Object.hasOwn(record, 'tool_failure'),
    unresolved_blocking_conflict_present: (record.conflicts ?? []).some(c => c.blocking && c.resolution_status === 'UNRESOLVED'),
    unsatisfied_domain_present: dispositions.includes('UNSATISFIED'),
    unknown_domain_present: dispositions.includes('UNKNOWN'),
    blocking_unknown_present: (record.unknowns ?? []).some(u => u.blocks_acceptance),
    conflicting_domain_present: dispositions.includes('CONFLICTING'),
    all_domains_satisfied: dispositions.length > 0 && dispositions.every(d => d === 'SATISFIED'),
    scope_coverage: record.composition_policy?.scope_coverage,
  };
}
function matches(condition, f) {
  if (condition.fact) return f[condition.fact] === condition.equals;
  if (condition.any) return condition.any.some(c => matches(c, f));
  if (condition.all) return condition.all.every(c => matches(c, f));
  return false;
}
function derive(record) {
  const f = facts(record);
  for (const rule of DERIVATION.rules) if (matches(rule.when, f)) return rule.result;
  return DERIVATION.no_match;
}
function unique(values, code, label, errors) {
  const seen = new Set();
  for (const value of values) { if (seen.has(value)) errors.push([code, `duplicate ${label}: ${value}`]); seen.add(value); }
}
function semanticErrors(record) {
  const errors = []; const sources = record.source_records ?? [];
  unique(sources.map(s => s.source_id), 'CAP-SEM-001', 'source_id', errors);
  const sourceMap = new Map(sources.map(s => [s.source_id, s]));
  for (const s of sources) {
    const pin = PINS.get(s.artifact_id);
    if (!pin) errors.push(['CAP-SEM-002', `unsupported artifact_id: ${s.artifact_id}`]);
    else if (s.repository !== pin[0] || s.reviewed_revision !== pin[1]) errors.push(['CAP-SEM-003', `pin mismatch for ${s.artifact_id}`]);
    if (s.native_status_owner !== s.artifact_id) errors.push(['CAP-SEM-004', `native_status_owner mismatch for ${s.source_id}`]);
    if (!s.carried_only || s.native_record_validity_established_by_cap) errors.push(['CAP-SEM-005', `native verdict ownership violated for ${s.source_id}`]);
  }
  const required = record.required_domains ?? []; const results = record.domain_results ?? [];
  unique(results.map(d => d.domain), 'CAP-SEM-006', 'domain result', errors);
  const resultDomains = new Set(results.map(d => d.domain));
  const missing = required.filter(d => !resultDomains.has(d));
  const extra = [...resultDomains].filter(d => !required.includes(d));
  if (missing.length) errors.push(['CAP-SEM-007', `missing domain results: ${missing.sort().join(', ')}`]);
  if (extra.length) errors.push(['CAP-SEM-008', `non-required domain results: ${extra.sort().join(', ')}`]);
  const conflicts = record.conflicts ?? []; const unknowns = record.unknowns ?? [];
  unique(conflicts.map(c => c.conflict_id), 'CAP-SEM-009', 'conflict_id', errors);
  unique(unknowns.map(u => u.unknown_id), 'CAP-SEM-010', 'unknown_id', errors);
  const conflictDomains = new Set(conflicts.flatMap(c => c.domains)); const unknownDomains = new Set(unknowns.map(u => u.domain));
  for (const d of results) {
    for (const ref of d.basis_source_ids) if (!sourceMap.has(ref)) errors.push(['CAP-SEM-011', `dangling source reference ${ref} in domain ${d.domain}`]);
    if (['SATISFIED', 'UNSATISFIED'].includes(d.disposition)) {
      if (!d.basis_source_ids.length) errors.push(['CAP-SEM-012', `${d.disposition} domain lacks source basis: ${d.domain}`]);
      for (const ref of d.basis_source_ids) if (sourceMap.has(ref) && sourceMap.get(ref).validation_receipt.status !== 'VALIDATED') errors.push(['CAP-SEM-013', `${d.disposition} domain uses unvalidated source ${ref}`]);
    }
    if (d.disposition === 'UNKNOWN' && !unknownDomains.has(d.domain)) errors.push(['CAP-SEM-014', `UNKNOWN domain lacks unknown entry: ${d.domain}`]);
    if (d.disposition === 'CONFLICTING' && !conflictDomains.has(d.domain)) errors.push(['CAP-SEM-015', `CONFLICTING domain lacks conflict entry: ${d.domain}`]);
  }
  for (const c of conflicts) {
    for (const ref of c.source_ids) if (!sourceMap.has(ref)) errors.push(['CAP-SEM-016', `dangling conflict source reference: ${ref}`]);
    for (const domain of c.domains) if (!required.includes(domain)) errors.push(['CAP-SEM-017', `conflict references non-required domain: ${domain}`]);
    if (c.resolution_status === 'RESOLVED') {
      if (c.blocking) errors.push(['CAP-SEM-018', `resolved conflict remains blocking: ${c.conflict_id}`]);
      if (!c.resolution_evidence.length) errors.push(['CAP-SEM-019', `resolved conflict lacks evidence: ${c.conflict_id}`]);
    } else if (c.resolution_evidence.length) errors.push(['CAP-SEM-020', `unresolved conflict has resolution evidence: ${c.conflict_id}`]);
    if (c.resolution_status === 'UNRESOLVED' && c.domains.some(d => required.includes(d)) && !c.blocking) errors.push(['CAP-SEM-021', `unresolved required-domain conflict must block: ${c.conflict_id}`]);
  }
  for (const u of unknowns) {
    for (const ref of u.source_ids) if (!sourceMap.has(ref)) errors.push(['CAP-SEM-022', `dangling unknown source reference: ${ref}`]);
    if (required.includes(u.domain) && !u.blocks_acceptance) errors.push(['CAP-SEM-023', `required-domain unknown must block acceptance: ${u.unknown_id}`]);
  }
  const policy = record.composition_policy ?? {}; const omissions = policy.known_omissions ?? [];
  if (policy.scope_coverage === 'partial' && !omissions.length) errors.push(['CAP-SEM-024', 'partial coverage requires known_omissions']);
  if (policy.scope_coverage === 'full' && omissions.length) errors.push(['CAP-SEM-025', 'full coverage cannot declare known_omissions']);
  const expected = derive(record); const actual = record.result?.status;
  if (expected === null) errors.push(['CAP-SEM-026', 'composition policy cannot derive a result']);
  else if (actual !== expected) errors.push(['CAP-SEM-027', `result mismatch: expected ${expected}, got ${actual}`]);
  const boundaries = new Set(record.claims_not_made ?? []); const missingBoundaries = [...MANDATORY_BOUNDARIES].filter(v => !boundaries.has(v)).sort();
  if (missingBoundaries.length) errors.push(['CAP-SEM-028', `missing mandatory claims_not_made: ${missingBoundaries.join(', ')}`]);
  if (actual === 'TOOL_FAILURE' && ['passed', 'acceptable', 'unacceptable', 'failed subject'].some(word => (record.result?.rationale ?? '').toLowerCase().includes(word))) errors.push(['CAP-SEM-029', 'TOOL_FAILURE rationale makes a semantic subject verdict']);
  return errors;
}
function payload(status, result, pairs) {
  return {
    validation_status: status,
    cap_result: result,
    diagnostic_codes: [...new Set(pairs.map(([code]) => code))],
    errors: pairs.map(([code, message]) => `${code} ${message}`),
    implementation: 'cap-node-independent/0.1',
  };
}
export function validateFile(filename) {
  let record;
  try { record = parseStrict(fs.readFileSync(filename, 'utf8')); }
  catch (error) {
    const message = String(error.message);
    const code = message.startsWith('duplicate JSON key:') ? 'CAP-JSON-001' : 'CAP-JSON-002';
    return [1, payload('INVALID', null, [[code, message]])];
  }
  try {
    const structural = schemaErrors(record, SCHEMA).map(message => ['CAP-SCHEMA-001', message]);
    if (structural.length) return [1, payload('INVALID', null, structural)];
    const semantic = semanticErrors(record);
    if (semantic.length) return [1, payload('INVALID', null, semantic)];
    return [0, payload('VALID', record.result.status, [])];
  } catch (error) { return [2, payload('TOOL_FAILURE', null, [['CAP-TOOL-001', String(error.message)]])]; }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 3) { console.error('usage: node cap_validate.mjs RECORD.json'); process.exit(2); }
  const [code, result] = validateFile(process.argv[2]);
  console.log(JSON.stringify(result)); process.exit(code);
}
