"""Viewer diagnostics must distinguish malformed, incomplete and terminal traces."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[2]


class TraceReadinessTests(unittest.TestCase):
    def view(self, path, *args):
        return subprocess.run([sys.executable, str(ROOT / 'learn.py'), 'trace', str(path), *args],
                              capture_output=True, text=True, timeout=10)

    def test_missing_empty_blank_and_malformed_records_are_actionable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.jsonl'
            self.assertEqual(self.view(path).returncode, 2)
            for value in ('', '\n\n', '{"seq":1', '{"event":"stop"}\n', '{"seq":1,"event":"request"}\n'):
                path.write_text(value, encoding='utf-8')
                result = self.view(path)
                self.assertEqual(result.returncode, 2, value)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn(str(path), result.stderr)

    def test_truncated_tail_preserves_readable_records_without_completion_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.jsonl'
            path.write_text(json.dumps({'seq': 1, 'event': 'start'}) + '\n\n' + '{"seq":2', encoding='utf-8')
            result = self.view(path)
            self.assertEqual(result.returncode, 2)
            self.assertIn('01 start', result.stdout)
            self.assertIn(':3:', result.stderr)
            self.assertIn('INCOMPLETE/INVALID', result.stdout)
            path.write_text(json.dumps({'seq': 1, 'event': 'start'}) + '\n', encoding='utf-8')
            result = self.view(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn('INCOMPLETE TRACE', result.stdout)

    def test_default_new_feedback_and_cumulative_views_agree_on_records(self):
        result = subprocess.run([sys.executable, str(ROOT / 'learn.py'), 'stage', '3'],
                                capture_output=True, text=True, check=True)
        path = Path(next(line[7:] for line in result.stdout.splitlines() if line.startswith('Trace: ')))
        delta = self.view(path.parent)
        cumulative = self.view(path, '--cumulative')
        self.assertEqual(delta.returncode, 0)
        self.assertEqual(cumulative.returncode, 0)
        last_request = [line for line in delta.stdout.splitlines() if ' request ' in line][-1]
        self.assertIn('input_added', last_request)
        self.assertIn('ok-1', last_request)
        self.assertNotIn('bad-1', last_request)
        self.assertIn('input_snapshot(cumulative', cumulative.stdout)
        self.assertEqual(len([line for line in delta.stdout.splitlines() if ' request ' in line]), 5)
        self.assertEqual(len([line for line in cumulative.stdout.splitlines() if ' request ' in line]), 5)

    def test_history_replacement_is_reported_without_inferring_new_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.jsonl'
            rows = [{'seq': 1, 'event': 'request', 'request': {'messages': [{'role': 'user', 'content': 'one'}]}},
                    {'seq': 2, 'event': 'request', 'request': {'messages': [{'role': 'user', 'content': 'replacement'}]}},
                    {'seq': 3, 'event': 'stop', 'status': 'completed', 'tool_calls': 0}]
            path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
            result = self.view(path)
            self.assertEqual(result.returncode, 0)
            self.assertIn('input_reset(history changed', result.stdout)
            self.assertNotIn('observed_effect=', result.stdout)

    def test_budget_limits_counts_and_short_stage_completion_are_visible(self):
        output = subprocess.check_output([sys.executable, str(ROOT / 'learn.py'), '--scenario', 'multi', '--max-calls', '1'], text=True)
        report = json.loads(output)
        viewed = self.view(report['directory'])
        stop = [line for line in viewed.stdout.splitlines() if ' stop ' in line][-1]
        self.assertIn('tool_limit', stop)
        self.assertIn('"max_calls": 1', stop)
        self.assertIn('"tool_calls": 0', stop)
        for stage in ('1', '2'):
            output = subprocess.check_output([sys.executable, str(ROOT / 'learn.py'), 'stage', stage], text=True)
            path = Path(next(line[7:] for line in output.splitlines() if line.startswith('Trace: ')))
            viewed = self.view(path.parent)
            self.assertEqual(viewed.returncode, 0)
            self.assertIn('Short-stage response/history complete', viewed.stdout)


if __name__ == '__main__':
    unittest.main()
