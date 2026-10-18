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
