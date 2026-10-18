"""Bounded outcome checks and explicit limits of reference validation."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from inspect_validation import (ROOT, broken_feedback, check_references, example_feedback_check,
                                grade_case, inspect_outcomes, read_json, recorded_observation)


class ValidationTests(unittest.TestCase):
    def test_valid_completed_exchange_can_have_wrong_exact_answer(self):
        record, _ = recorded_observation()
        name = 'example_ordinary_1'
        row = grade_case(record['runs'][name], example_feedback_check(record)['cases'][name])
        self.assertTrue(row['wire_format_valid'])
        self.assertTrue(row['successful_read_observed'])
        self.assertTrue(row['matching_feedback'])
        self.assertTrue(row['loop_completed'])
        self.assertEqual(row['answer'], '092a8a02')
        self.assertFalse(row['exact_answer'])
        self.assertFalse(row['task_passed'])

    def test_grade_does_not_trust_saved_task_label(self):
        record, _ = recorded_observation()
        case = copy.deepcopy(record['runs']['example_ordinary_1'])
        case['report']['task_passed'] = True
        row = grade_case(case, True)
        self.assertTrue(row['recorded_task_passed'])
        self.assertFalse(row['task_passed'])

    def test_synthetic_feedback_change_retains_answer_but_breaks_integration(self):
        original, _ = recorded_observation()
        before = json.dumps(original, sort_keys=True)
        changed = broken_feedback(original)
        name = 'example_ordinary_2'
        self.assertEqual(json.dumps(original, sort_keys=True), before)
        source_case, changed_case = original['runs'][name], changed['runs'][name]
        self.assertEqual([e for e in source_case['events'] if e['event'] == 'local_response'],
                         [e for e in changed_case['events'] if e['event'] == 'local_response'])
        feedback = example_feedback_check(changed)['cases'][name]
        row = grade_case(changed_case, feedback)
        self.assertFalse(row['matching_feedback'])
        self.assertTrue(row['exact_answer'])
        self.assertTrue(row['task_passed'])

    def test_bad_wire_text_does_not_inherit_completed_task_success(self):
        record, _ = recorded_observation()
        case = copy.deepcopy(record['runs']['example_ordinary_2'])
        final = [e for e in case['events'] if e['event'] == 'local_response'][-1]
        final['response']['content'] = '{"answer":"one","answer":"two"}'
        row = grade_case(case, True)
        self.assertFalse(row['wire_format_valid'])
        self.assertIsNone(row['answer'])
        self.assertTrue(row['loop_completed'])
        self.assertFalse(row['task_passed'])

    def test_output_does_not_change_retained_source(self):
        _, provenance = recorded_observation()
        source = ROOT / provenance['path']
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            result = inspect_outcomes(Path(tmp))
            self.assertEqual(len(result['cases']), 4)
            synthetic = read_json(Path(tmp) / 'synthetic-broken-feedback.json')
            self.assertIn('Synthetic', synthetic['origin'])
        self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())

    def test_changed_source_hash_is_rejected(self):
        _, provenance = recorded_observation()
        changed_manifest = dict(provenance, sha256='0' * 64)
        with patch('inspect_validation.read_json', return_value=changed_manifest):
            with self.assertRaisesRegex(ValueError, 'retained observation changed'):
                recorded_observation()

    def test_real_reference_does_not_establish_support(self):
        claims = read_json(LAB / 'claims.json')
        known = {'E01', 'E02', 'E03', 'C01'}
        self.assertTrue(check_references(claims[1], known)['references_resolve'])
        self.assertTrue(check_references(claims[3], known)['references_resolve'])
        self.assertEqual(check_references(claims[-1], known)['unresolved_ids'], ['E99'])
        changed = copy.deepcopy(claims[2])
        changed['evidence_ids'] = ['E03']
        checks = check_references(changed, known)
        self.assertTrue(checks['references_resolve'])
        self.assertIn('not graded', checks['semantic_support'])

    def test_bad_claim_shape_is_separate_from_unresolved_reference(self):
        for claim in ({}, {'claim_id': 'x', 'text': 'test', 'evidence_ids': 'E01'},
                      {'claim_id': 'x', 'text': 'test', 'evidence_ids': [1]}):
            self.assertFalse(check_references(claim, {'E01'})['object_shape_valid'])
        valid_shape = check_references({'claim_id': 'x', 'text': 'test', 'evidence_ids': ['E99']}, {'E01'})
        self.assertTrue(valid_shape['object_shape_valid'])
        self.assertFalse(valid_shape['references_resolve'])

    def test_cli_saves_blank_human_review_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'claims'
            command = [sys.executable, str(LAB / 'inspect_validation.py'), 'claims', '--output', str(root)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            notes = (root / 'claim-review.md').read_text(encoding='utf-8')
            self.assertIn('Judgment:', notes)
            report = read_json(root / 'report.json')
            self.assertNotIn('judgment', report['claims'][0])
            original = (root / 'report.json').read_bytes()
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(original, (root / 'report.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
