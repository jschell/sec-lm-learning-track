"""Direct contract behavior without installing MCP."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contract import EventLookup, dispatch, feedback_example
from direct import run


class ContractTests(unittest.TestCase):
    def test_invalid_inputs_and_unknown_tool_never_enter_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            lookup = EventLookup(Path(tmp) / 'audit.jsonl')
            for args in ({}, {'event_id': 1}, {'event_id': True}, {'event_id': 'E001', 'extra': True},
                         {'event_id': 'E1'}, {'event_id': '../E001'}, None, []):
                self.assertEqual(dispatch(lookup, 'lookup_event', args)['status'], 'invalid_arguments')
            self.assertEqual(dispatch(lookup, 'delete_event', {'event_id': 'E001'})['status'], 'unknown_tool')
            self.assertEqual(lookup.execution_count, 0)
            self.assertEqual(lookup.audit.read_text(encoding='utf-8'), '')

    def test_not_found_is_executed_domain_result_not_execution_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            lookup = EventLookup(Path(tmp) / 'audit.jsonl')
            missing = dispatch(lookup, 'lookup_event', {'event_id': 'E999'})
            fault = dispatch(lookup, 'lookup_event', {'event_id': 'E500'})
            self.assertEqual(missing['status'], 'not_found')
            self.assertNotIn('error', missing)
            self.assertEqual(fault['status'], 'execution_error')
            self.assertTrue(missing['executed'] and fault['executed'])
            audit = [json.loads(line) for line in lookup.audit.read_text(encoding='utf-8').splitlines()]
            self.assertEqual([row['event_id'] for row in audit], ['E999', 'E500'])

    def test_feedback_uses_proposal_id_and_marks_error(self):
        proposal = {'id': 'model-proposal-X', 'name': 'lookup_event', 'arguments': {'event_id': 1}}
        outcome = {'status': 'invalid_arguments', 'executed': False}
        feedback = feedback_example(proposal, outcome)
        self.assertEqual(feedback['feedback']['content'][0]['tool_use_id'], 'model-proposal-X')
        self.assertTrue(feedback['feedback']['content'][0]['is_error'])
        self.assertTrue(feedback['inspection_only'])

    def test_complete_direct_run_has_three_entries_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'direct'
            report = run(output)
            self.assertEqual(report['execution_count'], 3)
            self.assertEqual(report['calls'][0]['outcome']['data']['event']['outcome'], 'blocked')
            original = (output / 'report.json').read_bytes()
            with self.assertRaises(FileExistsError):
                run(output)
            self.assertEqual((output / 'report.json').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
