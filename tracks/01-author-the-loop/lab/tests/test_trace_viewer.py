"""Permission/simulation labels must not be presented as completed effects."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from inspect_trace import summary


class TraceViewerTests(unittest.TestCase):
    def test_stage_two_exposes_matching_feedback_in_request_two(self):
        root = LAB.parents[2]
        result = subprocess.run([sys.executable, str(root / 'learn.py'), 'stage', '2'],
                                cwd=root, capture_output=True, text=True, check=True)
        trace = Path(next(line.removeprefix('Trace: ') for line in result.stdout.splitlines()
                          if line.startswith('Trace: ')))
        rows = [json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        request_two = [r for r in rows if r['event'] == 'request'][1]
        proposed = summary(next(r for r in rows if r['event'] == 'response'))
        supplied = summary(request_two)
        self.assertIn('proposed_call=', proposed)
        self.assertIn('"id": "read-1"', proposed)
        self.assertIn('"name": "read_file"', proposed)
        self.assertIn('input_snapshot(cumulative', supplied)
        self.assertIn('"tool_use_id": "read-1"', supplied)
        self.assertIn('FizzBuzz', supplied)
        self.assertNotIn('observed_effect=', supplied)
        self.assertFalse(any(r['event'] == 'tool' for r in rows))

    def test_repeated_error_feedback_is_labelled_cumulative(self):
        messages = [{'role': 'assistant', 'content': [{'type': 'tool_use', 'id': 'e1',
                     'name': 'read_file', 'input': {'path': 'missing.txt'}}]},
                    {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': 'e1',
                     'is_error': True, 'content': 'not found'}]}]
        first = summary({'seq': 1, 'event': 'request', 'request': {'messages': messages}})
        later = summary({'seq': 2, 'event': 'request', 'request': {'messages': messages +
                        [{'role': 'assistant', 'content': [{'type': 'text', 'text': 'retry'}]}]}})
        for text in (first, later):
            self.assertIn('cumulative', text)
            self.assertIn('"is_error": true', text)
            self.assertIn('"tool_use_id": "e1"', text)
            self.assertNotIn('observed_effect=', text)
        self.assertIn('messages=3', later)

    def test_multiple_calls_and_payloads_are_bounded_and_escaped(self):
        calls = [{'type': 'tool_use', 'id': str(i), 'name': 'read_file',
                  'input': {'path': 'unsafe\n' + 'x' * 1000}} for i in range(12)]
        response = summary({'seq': 1, 'event': 'response', 'response': {'content': calls}})
        snapshot = summary({'seq': 2, 'event': 'request', 'request': {'messages':
                           [{'role': 'assistant', 'content': calls}]}})
        self.assertEqual(response.count('proposed_call='), 8)
        self.assertIn('omitted_proposals=4', response)
        self.assertIn('omitted=4', snapshot)
        self.assertIn('"id": "11"', snapshot)
        for text in (response, snapshot):
            self.assertEqual(len(text.splitlines()), 1)
            self.assertLess(len(text), 2500)

    def test_history_is_distinct_from_tool_observation(self):
        text = summary({'seq': 1, 'event': 'history', 'messages': [{'role': 'user', 'content':
                       [{'type': 'tool_result', 'tool_use_id': 'h1', 'is_error': False,
                         'content': 'recorded bytes'}]}]})
        self.assertIn('history_snapshot(cumulative', text)
        self.assertIn('"tool_use_id": "h1"', text)
        self.assertNotIn('observed_effect=', text)

    def test_allow_and_denial_do_not_claim_execution(self):
        for decision in ('allow', 'deny'):
            text = summary({'seq': 1, 'event': 'decision', 'decision': decision,
                            'call': {'id': 'x', 'name': 'edit_file', 'input': {'path': 'notes.txt'}},
                            'reason': 'fixture'})
            self.assertIn('permission=', text)
            self.assertIn(decision, text)
            self.assertIn('edit_file', text)
            self.assertNotIn('observed_effect=', text)
            self.assertNotIn('executed', text)

    def test_recording_only_and_actual_effect_have_different_labels(self):
        recorded = summary({'seq': 2, 'event': 'recording_only_decision', 'label': 'edit',
                            'decision': 'would_allow', 'executed': False, 'scope': 'nothing invoked'})
        effect = summary({'seq': 3, 'event': 'effect', 'operation': 'read_file',
                          'path': 'note.txt', 'characters_returned': 20})
        self.assertIn('simulation=', recorded)
        self.assertIn('"executed": false', recorded)
        self.assertNotIn('observed_effect=', recorded)
        self.assertIn('observed_effect=', effect)
        self.assertIn('read_file', effect)
        self.assertIn('note.txt', effect)

    def test_untrusted_proposal_is_data_and_unknown_events_remain_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / 'must-not-exist'
            text = f'__import__("pathlib").Path({str(marker)!r}).touch()\nforged event'
            rows = [{'seq': 1, 'event': 'proposal', 'origin': 'authored fixture',
                     'proposal': {'label': text, 'call': {'name': 'edit_file', 'input': {}}}},
                    {'seq': 2, 'event': 'new_future_event'}]
            trace = root / 'trace.jsonl'
            trace.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
            result = subprocess.run([sys.executable, str(LAB / 'inspect_trace.py'), str(trace)],
                                    capture_output=True, text=True, check=True)
            self.assertFalse(marker.exists())
            self.assertEqual(len(result.stdout.splitlines()), 2)
            self.assertIn('proposed=', result.stdout)
            self.assertIn('new_future_event', result.stdout)


if __name__ == '__main__':
    unittest.main()
