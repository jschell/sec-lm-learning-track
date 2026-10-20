"""Stage 1/2 summary output, --json payloads and the stage 2 --read variation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[2]


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / 'learn.py'), 'stage', *args], cwd=ROOT,
                          capture_output=True, text=True, encoding='utf-8', timeout=20, check=check)


def trace_rows(stdout: str) -> list[dict]:
    path = Path(stdout.rsplit('Trace: ', 1)[1].strip())
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


def second_request_results(rows: list[dict]) -> list[dict]:
    second = [r for r in rows if r['event'] == 'request'][1]
    return [b for b in second['request']['messages'][-1]['content'] if b.get('type') == 'tool_result']


class StageOutputTests(unittest.TestCase):
    def test_default_summary_does_not_reveal_exchange(self):
        for stage, requests, calls in (('1', 1, 0), ('2', 2, 1)):
            with self.subTest(stage=stage):
                out = run(stage).stdout
                self.assertIn(f'Inference requests: {requests}', out)
                self.assertIn(f'Completed tool calls: {calls}', out)
                self.assertIn('learn.py trace ', out)
                for revealing in ('Synthetic exercise', 'FizzBuzz', 'tool_result', '"history"'):
                    self.assertNotIn(revealing, out)

    def test_json_restores_full_payload(self):
        out = run('2', '--json').stdout
        payload = json.JSONDecoder().raw_decode(out)[0]
        self.assertEqual(set(payload), {'history', 'response'})
        rows = trace_rows(out)
        self.assertEqual(payload['history'], next(r for r in rows if r['event'] == 'history')['messages'])
        self.assertIn('FizzBuzz', payload['response']['content'][0]['text'])

    def test_read_missing_file_returns_error_feedback_without_editing_fixture(self):
        source = LAB / 'replay/read.json'
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        out = run('2', '--read', 'missing.txt').stdout
        results = second_request_results(trace_rows(out))
        self.assertEqual([(r['tool_use_id'], r['is_error']) for r in results], [('read-1', True)])
        changed = Path(out.rsplit('Run: ', 1)[1].splitlines()[0]) / 'read-replay.json'
        self.assertEqual(json.loads(changed.read_text(encoding='utf-8'))['turns'][0]['response']['content'][0]
                         ['input']['path'], 'missing.txt')
        self.assertEqual(changed.stat().st_mode & 0o777, 0o600)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)

    def test_read_existing_and_confined_paths(self):
        ok = second_request_results(trace_rows(run('2', '--read', 'notes.txt').stdout))
        self.assertFalse(ok[0]['is_error'])
        escaped = second_request_results(trace_rows(run('2', '--read', '../pyproject.toml').stdout))
        self.assertTrue(escaped[0]['is_error'])

    def test_read_rejects_unsupported_combinations(self):
        for args, message in ((('1', '--read', 'notes.txt'), 'only to stage 2'),
                              (('2', '--read', 'notes.txt', '--replay-file', 'x.json'), 'cannot be combined'),
                              (('2', '--read', 'notes.txt', '--live', '--model', 'm'), 'cannot be combined')):
            with self.subTest(args=args):
                result = run(*args, check=False)
                self.assertEqual(result.returncode, 2)
                self.assertIn(message, result.stderr)


if __name__ == '__main__':
    unittest.main()
