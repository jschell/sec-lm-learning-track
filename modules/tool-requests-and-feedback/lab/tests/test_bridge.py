"""Synthetic contract tests; these do not test model competence."""
import copy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_model as feedback_verifier
from bridge import (EXAMPLE_MESSAGES, LocalModel, ScriptedExchange, Tools, Trace, Workspace, WIRE_SCHEMA,
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
    def test_actual_ci_prefix_failure_has_valid_feedback_but_still_fails_exact_task(self):
        source=Path(__file__).resolve().parents[2]/'observations/main-2026-10-17.json'
        record=json.loads(source.read_text(encoding='utf-8'))
        self.assertFalse(feedback_verifier.example_task_check(record)['passed'])
        self.assertTrue(feedback_verifier.example_feedback_check(record)['passed'])
        first=record['runs']['example_ordinary_1']['report']
        self.assertEqual(first['final_answer'],'092a8a02')
        self.assertFalse(first['task_passed'])

    def test_cli_feedback_and_strict_task_requirements_remain_separate(self):
        source=Path(__file__).resolve().parents[2]/'observations/main-2026-10-17.json'
        original=json.loads(source.read_text(encoding='utf-8'))
        for flags, expected_exit in [(['--require-feedback'],0),
                                     (['--require-feedback','--require-example-task'],1)]:
            with self.subTest(flags=flags):
                output=io.StringIO()
                with patch.object(feedback_verifier,'verify',return_value=copy.deepcopy(original)), \
                     patch.object(sys,'argv',['verify_model.py','--model','360m',*flags]), \
                     redirect_stdout(output):
                    self.assertEqual(feedback_verifier.main(),expected_exit)
                captured=json.loads(output.getvalue())
                self.assertTrue(captured['required_feedback_check']['passed'])
                self.assertFalse(captured['runs']['example_ordinary_1']['report']['task_passed'])

    def test_feedback_check_rejects_dropped_native_feedback_and_mismatched_call_id(self):
        source=Path(__file__).resolve().parents[2]/'observations/main-2026-10-17.json'
        record=json.loads(source.read_text(encoding='utf-8'))
        run=record['runs']['example_ordinary_1']
        native=[e for e in run['events'] if e['event']=='local_request'][-1]
        native['messages'][-1]['content']='feedback was dropped'
        self.assertFalse(feedback_verifier.example_feedback_check(record)['passed'])
        record=json.loads(source.read_text(encoding='utf-8'))
        native=[e for e in record['runs']['example_ordinary_1']['events'] if e['event']=='local_request'][-1]
        native['formatted_prompt']='formatted input lost feedback'
        self.assertFalse(feedback_verifier.example_feedback_check(record)['passed'])
        record=json.loads(source.read_text(encoding='utf-8'))
        canonical=[e for e in record['runs']['example_ordinary_1']['events'] if e['event']=='request'][-1]
        canonical['request']['messages'][-1]['content']=[]
        self.assertFalse(feedback_verifier.example_feedback_check(record)['passed'])
        record=json.loads(source.read_text(encoding='utf-8'))
        tool=next(e for e in record['runs']['example_ordinary_1']['events'] if e['event']=='tool')
        tool['result']['tool_use_id']='wrong-id'
        self.assertFalse(feedback_verifier.example_feedback_check(record)['passed'])

    def test_recipe_check_rejects_failed_and_missing_cases(self):
        record={'runs':{f'example_ordinary_{trial}':{'report':{'task_passed':True}}
                        for trial in range(1,4)}}
        self.assertTrue(feedback_verifier.example_task_check(record)['passed'])
        record['runs']['example_ordinary_2']['report']['task_passed']=False
        self.assertFalse(feedback_verifier.example_task_check(record)['passed'])
        del record['runs']['example_ordinary_2']
        self.assertFalse(feedback_verifier.example_task_check(record)['passed'])

    def test_required_recipe_failure_still_emits_observations_and_never_falls_back(self):
        record={'runs':{'example_ordinary_1':{'report':{'task_passed':False}}}}
        output=io.StringIO()
        with patch.object(feedback_verifier,'verify',return_value=record) as actual, \
             patch.object(sys,'argv',['verify_model.py','--model','360m','--require-example-task']), \
             redirect_stdout(output):
            self.assertEqual(feedback_verifier.main(),1)
        actual.assert_called_once_with('360m')
        captured=json.loads(output.getvalue())
        self.assertFalse(captured['required_task_check']['passed'])
        self.assertEqual(captured['runs'],record['runs'])

    def test_example_adds_only_fixed_demonstration_and_does_not_mutate_history(self):
        request = copy.deepcopy(REQUEST)
        plain = wire_messages(request)
        example = wire_messages(request, 'example')
        self.assertEqual(request, REQUEST)
        self.assertEqual(example[0], plain[0])
        self.assertEqual(example[1:5], EXAMPLE_MESSAGES)
        self.assertEqual(example[5:], plain[1:])
        self.assertEqual(example[-1]['content'], 'Read status.txt.')
        example[1]['content'] = 'changed copy'
        self.assertEqual(EXAMPLE_MESSAGES[0]['content'], 'Read status.txt, then report the code stored in it.')

    def test_example_answer_without_real_read_is_still_a_failed_task(self):
        result = {'status': 'completed', 'messages': [
            {'role': 'assistant', 'content': [{'type': 'text', 'text': 'LAB-example'}]}]}
        self.assertFalse(evaluate(result, [], 'LAB-example')['task_passed'])

    def test_copy_line_clarifies_system_only_and_keeps_example_and_actual_task(self):
        example = wire_messages(REQUEST, 'example')
        precise = wire_messages(REQUEST, 'copy-line')
        self.assertEqual(precise[1:], example[1:])
        self.assertTrue(precise[0]['content'].startswith(example[0]['content']))
        self.assertIn('including the LAB- prefix', precise[0]['content'])
        self.assertIn('Do not answer with tool_use_id', precise[0]['content'])

    def test_example_style_is_live_only_and_validated_before_workspace_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'run'
            with self.assertRaises(ValueError):
                exercise(output, prompt_style='example')
            self.assertFalse(output.exists())
            with self.assertRaises(ValueError):
                wire_messages(REQUEST, 'unknown')

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
