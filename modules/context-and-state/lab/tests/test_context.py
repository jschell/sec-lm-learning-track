"""Behavioral checks for observable context transitions and inspection limits."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from inspect_context import compare_evidence, inspect_text, load_json, locate_state, select_records


class ContextTests(unittest.TestCase):
    def test_actual_feedback_is_new_input_and_counterfactual_does_not_mutate_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            locate_state(root)
            requests = json.loads((root / 'requests.json').read_text(encoding='utf-8'))
            data = (root / 'work/status.txt').read_text(encoding='utf-8')
            self.assertNotIn(data, json.dumps(requests[0]))
            call = requests[1]['messages'][-2]['content'][0]
            result = requests[1]['messages'][-1]['content'][0]
            self.assertEqual(result['tool_use_id'], call['id'])
            # Track 1 read_file JSON-encodes the returned string in content.
            self.assertEqual(data, json.loads(result['content']))
            cf = json.loads((root / 'counterfactual-omitted-result.json').read_text(encoding='utf-8'))
            self.assertTrue(cf['inspection_only'])
            self.assertEqual(cf['request']['messages'][-1]['role'], 'assistant')
            self.assertEqual(requests[1]['messages'][-1]['role'], 'user')
            trace = [json.loads(line) for line in (root / 'trace.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual([r['request'] for r in trace if r['event'] == 'request'], requests)

    def test_keyword_search_misses_gap_and_zero_hits_remain_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = compare_evidence(Path(tmp), 'select', 'alice')
            self.assertTrue(report['variants']['full']['all_literal_checks_pass'])
            selected = report['variants']['selected']
            self.assertEqual(selected['missing_required_ids'], ['C01'])
            self.assertEqual(selected['present_ids'], ['E01', 'E02'])
        self.assertEqual(select_records(load_json('packet.json')['records'], 'no-such-word'), [])
        with self.assertRaises(ValueError):
            select_records([], ' ')

    def test_summaries_retain_or_lose_known_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = compare_evidence(root, 'resume', 'unused')
            self.assertTrue(report['variants']['faithful']['all_literal_checks_pass'])
            self.assertEqual(report['variants']['lossy']['missing_required_ids'], ['E02', 'C01'])
            note = (root / 'faithful-note.txt').read_text(encoding='utf-8')
            before = json.loads((root / 'resume-without-loading.json').read_text(encoding='utf-8'))
            after = json.loads((root / 'resume-after-loading.json').read_text(encoding='utf-8'))
            self.assertNotIn(note, before['messages'][0]['content'])
            self.assertIn(note, after['messages'][0]['content'])

    def test_ids_alone_do_not_pass_anchor_check(self):
        report = inspect_text('E01 E02 C01', load_json('rubric.json'))
        self.assertEqual(report['missing_required_ids'], [])
        self.assertFalse(report['all_literal_checks_pass'])

    def test_literal_check_is_explicitly_not_semantic_validation(self):
        text = 'E01 was NOT failed. E02 was NOT success. C01 has NO collection gap at 10:02–10:05.'
        report = inspect_text(text, load_json('rubric.json'))
        self.assertTrue(report['all_literal_checks_pass'])
        self.assertIn('human review', report['scope'])

    def test_unicode_counts_do_not_claim_tokens(self):
        report = inspect_text('é', {'required': []})
        self.assertEqual(report['text_characters'], 1)
        self.assertEqual(report['text_utf8_bytes'], 2)
        self.assertNotIn('tokens', report)

    def test_cli_persists_files_and_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            command = [sys.executable, str(LAB / 'inspect_context.py'), 'state', '--output', str(root)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = (root / 'requests.json').read_bytes()
            self.assertTrue((root / 'work/status.txt').exists())
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual((root / 'requests.json').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
