"""Observe data flow, authored proposals and independently enforced effects."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from inspect_authority import (FIXTURES, ReadOnlyTools, Trace, description_only_recording,
                               inspect_authority, inspect_exposure, make_workspace)


def events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


class AuthorityTests(unittest.TestCase):
    def test_injected_content_reaches_second_request_with_identical_authored_responses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = inspect_exposure(root)
            traces = {v: events(root / v / 'trace.jsonl') for v in ('benign', 'injected')}
            initial = [[e['request'] for e in traces[v] if e['event'] == 'request'][0] for v in traces]
            self.assertEqual(initial[0], initial[1])
            responses = [[e['response'] for e in traces[v] if e['event'] == 'response'] for v in traces]
            self.assertEqual(responses[0], responses[1])
            benign = (FIXTURES / 'benign.txt').read_text(encoding='utf-8')
            injected = (FIXTURES / 'injected.txt').read_text(encoding='utf-8')
            self.assertTrue(injected.startswith(benign))
            for variant in traces:
                requests = [e['request'] for e in traces[variant] if e['event'] == 'request']
                result_block = requests[1]['messages'][-1]['content'][0]
                self.assertEqual(result_block['tool_use_id'], 'read-note')
                self.assertEqual(json.loads(result_block['content']), (FIXTURES / f'{variant}.txt').read_text(encoding='utf-8'))
                self.assertEqual((root / variant / 'work/notes.txt').read_text(encoding='utf-8'), 'Investigation open.\n')
            self.assertEqual([r['forbidden_proposals'] for r in result['cases']], [0, 0])

    def test_same_proposals_recorded_vs_executed_and_edit_denial_reaches_next_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = inspect_authority(root)
            self.assertEqual([r['recording_only']['decision'] for r in report['cases']], ['would_allow'] * 3)
            self.assertTrue(all(r['recording_only']['executed'] is False for r in report['cases']))
            self.assertEqual([r['bounded_decision'] for r in report['cases']], ['allow', 'deny', 'deny'])
            self.assertEqual([r['bounded_executed'] for r in report['cases']], [True, False, False])
            self.assertEqual(report['forbidden_execution_count'], 0)
            self.assertEqual(report['scripted_attempt']['forbidden_proposals'], 1)
            trace = events(root / 'scripted-attempt/trace.jsonl')
            requests = [e['request'] for e in trace if e['event'] == 'request']
            self.assertEqual(len(requests), 3)
            denial = requests[2]['messages'][-1]['content'][0]
            self.assertTrue(denial['is_error'])
            self.assertEqual(denial['tool_use_id'], 'proposal-edit')
            self.assertEqual([e['operation'] for e in trace if e['event'] == 'effect'], ['read_file'])
            for work in (root / 'work', root / 'scripted-attempt/work'):
                self.assertEqual((work / 'notes.txt').read_text(encoding='utf-8'), 'Investigation open.\n')
                self.assertEqual((work / 'private.txt').read_text(encoding='utf-8'), 'SYNTHETIC-NOT-A-SECRET\n')

    def test_wrong_operation_path_and_extra_arguments_never_reach_read_primitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = make_workspace(root / 'work', 'injected')
            trace = Trace(root / 'trace.jsonl')
            tools = ReadOnlyTools(workspace, trace)
            try:
                with patch.object(workspace, 'read', side_effect=AssertionError('unauthorized read reached primitive')):
                    calls = [
                        {'id': 'edit', 'name': 'edit_file', 'input': {'path': 'notes.txt'}},
                        {'id': 'private', 'name': 'read_file', 'input': {'path': 'private.txt'}},
                        {'id': 'extra', 'name': 'read_file', 'input': {'path': 'note.txt', 'approved': True}},
                        {'id': 'traversal', 'name': 'read_file', 'input': {'path': '../note.txt'}},
                    ]
                    for call in calls:
                        result = tools.dispatch(call)
                        self.assertTrue(result['is_error'])
                        self.assertEqual(result['tool_use_id'], call['id'])
                self.assertEqual(tools.executions, [])
            finally:
                trace.close()

    def test_description_changes_only_flawed_recording_policy_not_authority(self):
        proposal = json.loads((FIXTURES / 'proposals.json').read_text(encoding='utf-8'))[1]
        denied_description = copy.deepcopy(proposal)
        denied_description['display_description'] = 'No permission.'
        self.assertEqual(description_only_recording(proposal)['decision'], 'would_allow')
        self.assertEqual(description_only_recording(denied_description)['decision'], 'would_deny')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = make_workspace(root / 'work', 'injected')
            trace = Trace(root / 'trace.jsonl')
            try:
                tools = ReadOnlyTools(workspace, trace)
                for variant in (proposal, denied_description):
                    self.assertTrue(tools.dispatch(variant['call'])['is_error'])
                self.assertEqual(tools.executions, [])
            finally:
                trace.close()

    def test_negated_approval_still_tricks_only_the_deliberately_wrong_recorder(self):
        proposal = {'display_description': 'Not approved.', 'call': {'name': 'edit_file'}}
        result = description_only_recording(proposal)
        self.assertEqual(result['decision'], 'would_allow')
        self.assertFalse(result['executed'])

    def test_allowed_filename_symlink_is_rejected_without_read_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = make_workspace(root / 'work', 'benign')
            note = root / 'work/note.txt'
            note.unlink()
            note.symlink_to(root / 'work/private.txt')
            trace = Trace(root / 'trace.jsonl')
            try:
                tools = ReadOnlyTools(workspace, trace)
                with self.assertRaisesRegex(ValueError, 'symlink'):
                    tools.dispatch({'id': 'read', 'name': 'read_file', 'input': {'path': 'note.txt'}})
                self.assertEqual(tools.executions, [])
            finally:
                trace.close()

    def test_cli_keeps_artifacts_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'exposure'
            command = [sys.executable, str(LAB / 'inspect_authority.py'), 'exposure', '--output', str(root)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = (root / 'report.json').read_bytes()
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual((root / 'report.json').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
