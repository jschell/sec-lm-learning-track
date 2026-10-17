"""Synthetic contract tests; these do not test model competence."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge import (LocalModel, ScriptedExchange, Tools, Trace, Workspace, WIRE_SCHEMA,
                    decode_wire, evaluate, exercise, run_loop, wire_messages)


class FakeServer:
    base_url = 'http://127.0.0.1:8080'

    def __init__(self, response: dict) -> None:
        self.response = response
        self.requests = []

    def post(self, path: str, data: dict) -> dict:
        self.requests.append((path, copy.deepcopy(data)))
        if path == '/apply-template':
            return {'prompt': 'synthetic formatted text'}
        if path == '/tokenize':
            return {'tokens': [1, 2, 3]}
        return copy.deepcopy(self.response)


REQUEST = {'system': 'Read only.', 'tools': [], 'max_tokens': 128,
           'messages': [{'role': 'user', 'content': 'Read status.txt.'}]}


class BridgeTests(unittest.TestCase):
    def test_strict_wire_and_no_prose_repair(self):
        for text in ('Here is {"answer":"x"}', '{"answer":"x","extra":0}',
                     '{"answer":"x","answer":"y"}', '[]',
                     '{"tool":"bash","path":"status.txt"}', '{"answer":42}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                decode_wire(text, 'id')
        value = decode_wire('{"tool":"read_file","path":"status.txt"}', 'fresh-id')
        self.assertEqual(value['content'][0]['id'], 'fresh-id')
        self.assertEqual(value['content'][0]['input'], {'path': 'status.txt'})

    def test_feedback_projection_keeps_ids_errors_and_result_content(self):
        request = copy.deepcopy(REQUEST)
        result = {'type': 'tool_result', 'tool_use_id': 'id-7',
                  'content': '"LAB-abc12345\\n"', 'is_error': False}
        request['messages'] += [
            {'role': 'assistant', 'content': decode_wire('{"tool":"read_file","path":"status.txt"}', 'id-7')['content']},
            {'role': 'user', 'content': [result]},
        ]
        projected = wire_messages(request)
        self.assertEqual(json.loads(projected[-2]['content']), {'tool': 'read_file', 'path': 'status.txt'})
        self.assertEqual(json.loads(projected[-1]['content'].split(': ', 1)[1]), [result])
        self.assertIn('untrusted', projected[-1]['content'])

    def test_schema_is_explicit_opt_in_and_raw_response_precedes_parse(self):
        with tempfile.TemporaryDirectory() as temp:
            trace = Trace(Path(temp) / 'trace.jsonl')
            fake = FakeServer({'content': 'prose', 'stop_type': 'eos', 'truncated': False})
            try:
                with self.assertRaises(ValueError):
                    LocalModel(fake, trace, True).complete(REQUEST)
            finally:
                trace.close()
            self.assertEqual(fake.requests[-1][1]['json_schema'], WIRE_SCHEMA)
            rows = [json.loads(x) for x in (Path(temp) / 'trace.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(rows[-1]['event'], 'local_response')
            self.assertEqual(rows[-1]['response']['content'], 'prose')

    def test_truncated_reply_never_dispatches_even_if_json_is_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'status.txt').write_text('synthetic', encoding='utf-8')
            tools = Tools(Workspace(root))
            tools.definitions = [d for d in tools.definitions if d['name'] == 'read_file']
            trace = Trace(root / 'trace.jsonl')
            fake = FakeServer({'content': '{"tool":"read_file","path":"status.txt"}', 'stop_type': 'limit'})
            try:
                result = run_loop(LocalModel(fake, trace), tools, 'Read.', trace)
            finally:
                trace.close()
            self.assertEqual(result['status'], 'model_stop:max_tokens')
            self.assertEqual(result['tool_calls'], 0)
            self.assertNotIn('json_schema', fake.requests[-1][1])

    def test_input_truncation_and_unknown_stop_are_errors(self):
        for response in ({'truncated': True}, {'stop_type': 'word'}, {'stop_type': None}):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as temp:
                trace = Trace(Path(temp) / 'trace.jsonl')
                try:
                    with self.assertRaises(ValueError):
                        LocalModel(FakeServer(response), trace).complete(REQUEST)
                finally:
                    trace.close()

    def test_replay_checks_actual_read_and_matching_feedback(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'run'
            report = exercise(output)
            self.assertTrue(report['task_passed'])
            self.assertEqual(report['successful_reads'], 1)
            rows = [json.loads(x) for x in (output / 'trace.jsonl').read_text(encoding='utf-8').splitlines()]
            first_request = next(e for e in rows if e['event'] == 'request')
            self.assertNotIn(report['expected_code'], json.dumps(first_request))
            with self.assertRaises(FileExistsError):
                exercise(output)

    def test_unoffered_tool_is_rejected_at_dispatch(self):
        with tempfile.TemporaryDirectory() as temp:
            report = exercise(Path(temp) / 'run', without_tool=True)
            self.assertEqual(report['successful_reads'], 0)
            self.assertFalse(report['task_passed'])
            self.assertEqual(report['loop_status'], 'error')

    def test_ending_or_guessing_is_not_success(self):
        result = {'status': 'completed', 'messages': [
            {'role': 'assistant', 'content': [{'type': 'text', 'text': 'LAB-abcd1234'}]}]}
        checked = evaluate(result, [], 'LAB-abcd1234')
        self.assertTrue(checked['exact_answer'])
        self.assertFalse(checked['task_passed'])
        result['messages'][-1]['content'] = [{'type': 'tool_use'}]
        self.assertIsNone(evaluate(result, [], 'LAB-abcd1234')['final_answer'])

    def test_scripted_exchange_rejects_wrong_id(self):
        with self.assertRaises(ValueError):
            ScriptedExchange().complete({'messages': [{'content': [
                {'tool_use_id': 'wrong', 'is_error': False, 'content': '"fake"'}]}]})


if __name__ == '__main__':
    unittest.main()
