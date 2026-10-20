"""Synthetic credentials and effects exercise failure paths without network access."""
from contextlib import redirect_stdout, redirect_stderr
import http.client
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import cli
import stage_demo
from loop import MessagesHTTP, Trace, run_loop, safe_diagnostic

spec = importlib.util.spec_from_file_location('failure_worked_stages', LAB / 'solutions/stages.py')
worked = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worked)

SECRET = 'SYNTHETIC-OPAQUE-CREDENTIAL'


class FailureBoundaries(unittest.TestCase):
    def test_credentials_trim_surrounding_whitespace_for_both_providers(self):
        for provider, name in [('anthropic', 'ANTHROPIC_API_KEY'), ('openrouter', 'OPENROUTER_API_KEY')]:
            with patch.dict(os.environ, {name: ' \t' + SECRET + '\r\n'}):
                self.assertEqual(MessagesHTTP('fixture', provider).key, SECRET)

    def test_invalid_credentials_never_appear_in_configuration_errors(self):
        for value in (' \t\r\n', SECRET + '\rinternal', SECRET + ' space', SECRET + '\x01', SECRET + 'é'):
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': value}):
                with self.assertRaises(ValueError) as error:
                    MessagesHTTP('fixture')
            self.assertNotIn(SECRET, str(error.exception))
            self.assertNotIn(value, str(error.exception))

    def test_transport_local_failures_have_no_raw_exception_context(self):
        for failure in (ValueError(repr(SECRET + '\r')), OSError(SECRET), RuntimeError(SECRET)):
            with patch.dict(os.environ, {'ANTHROPIC_API_KEY': SECRET}):
                model = MessagesHTTP('fixture')
            with patch('loop.urllib.request.build_opener') as factory:
                factory.return_value.open.side_effect = failure
                with self.assertRaises(RuntimeError) as caught:
                    model.complete({'tools': [], 'messages': [], 'system': 'fixture', 'max_tokens': 2})
            self.assertNotIn(SECRET, str(caught.exception))
            self.assertIsNone(caught.exception.__context__)
            self.assertIsNone(caught.exception.__cause__)

    def test_local_header_validation_never_leaks_to_trace_or_console(self):
        class HeaderOnly:
            def open(self, request, timeout):
                connection = http.client.HTTPConnection('invalid.example')
                connection.putrequest('POST', '/')
                for name, value in request.header_items():
                    connection.putheader(name, value)
                raise AssertionError('No connection should be attempted')
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': SECRET}):
            model = MessagesHTTP('fixture')
        model.key += '\r'  # Simulate a local transport fault even after constructor validation.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.jsonl'
            trace = Trace(path)
            console = io.StringIO()
            with patch('loop.urllib.request.build_opener', return_value=HeaderOnly()), redirect_stdout(console), redirect_stderr(console):
                try:
                    result = run_loop(model, SimpleNamespace(definitions=[]), 'fixture', trace)
                finally:
                    trace.close()
            self.assertEqual(result['status'], 'error')
            self.assertNotIn(SECRET, path.read_text(encoding='utf-8') + console.getvalue())

    def test_terminal_redaction_covers_raw_and_escaped_configured_secrets(self):
        for value in (SECRET, SECRET + '\r\n', SECRET + '\ninside'):
            with patch.dict(os.environ, {'OPENROUTER_API_KEY': value}):
                for rendered in (value, repr(value), json.dumps(value)):
                    self.assertNotIn(SECRET, safe_diagnostic(rendered))

    def test_dispatch_accounting_survives_post_effect_failures(self):
        for controller in (run_loop, worked.run_loop):
            for phase in ('dispatch', 'trace'):
                with self.subTest(controller=controller.__module__, phase=phase), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    class Model:
                        def complete(self, request):
                            return {'stop_reason': 'tool_use', 'content': [
                                {'type': 'tool_use', 'id': 'effect-1', 'name': 'write_fixture', 'input': {}}]}
                    class Tools:
                        definitions = []
                        def dispatch(self, call):
                            (root / 'effect.txt').write_text('actual effect', encoding='utf-8')
                            if phase == 'dispatch':
                                raise RuntimeError('raised after effect')
                            return {'type': 'tool_result', 'tool_use_id': call['id'], 'is_error': False, 'content': 'done'}
                    class FailToolTrace(Trace):
                        def write(self, event, **values):
                            if event == 'tool':
                                raise OSError('cannot record returned dispatch')
                            super().write(event, **values)
                    trace = FailToolTrace(root / 'trace.jsonl')
                    try:
                        result = controller(Model(), Tools(), 'fixture', trace)
                    finally:
                        trace.close()
                    self.assertTrue((root / 'effect.txt').exists())
                    self.assertEqual(result['status'], 'error')
                    self.assertEqual(result['dispatch_attempts'], 1)
                    self.assertEqual(result['dispatch_uncertain'], phase == 'dispatch')
                    self.assertEqual(result['tool_calls'], None if phase == 'dispatch' else 1)
                    self.assertEqual(result['completed_tool_calls'], 0 if phase == 'dispatch' else 1)
                    rows = [json.loads(line) for line in (root / 'trace.jsonl').read_text().splitlines()]
                    self.assertEqual(rows[-1]['tool_calls'], result['tool_calls'])
                    self.assertTrue(any(row['event'] == 'error' for row in rows))

    def test_short_loop_malformed_responses_record_error_and_stop(self):
        malformed = ({'content': []}, {'content': [], 'stop_reason': None}, {'stop_reason': 'tool_use', 'content': [{}]},
                     {'stop_reason': 'tool_use', 'content': []})
        for response in malformed:
            with tempfile.TemporaryDirectory() as tmp:
                trace = Trace(Path(tmp) / 'trace.jsonl')
                try:
                    result = worked.run_loop(SimpleNamespace(complete=lambda request: response),
                                             SimpleNamespace(definitions=[]), 'fixture', trace)
                finally:
                    trace.close()
                rows = [json.loads(line) for line in Path(tmp, 'trace.jsonl').read_text().splitlines()]
                self.assertEqual(result['status'], 'error')
                self.assertEqual(rows[-2]['event'], 'error')
                self.assertEqual(rows[-1]['event'], 'stop')
                self.assertEqual(result['tool_calls'], 0)

    def test_short_live_stages_are_rejected_before_credentials_or_calls(self):
        for stage in ('1', '2'):
            console = io.StringIO()
            with patch.object(sys, 'argv', ['stage_demo.py', stage, '--live', '--model', 'fixture']), redirect_stderr(console):
                with patch.object(stage_demo, 'MessagesHTTP') as transport, self.assertRaises(SystemExit):
                    stage_demo.main()
                transport.assert_not_called()
            self.assertIn('live stages 1/2 are unsupported', console.getvalue())

    def test_live_stage_three_uses_guarded_reference(self):
        # Only the network transport is replaced; the real guarded loop runs and its result is observed.
        responses = [{'stop_reason': 'tool_use', 'content': [
                         {'type': 'tool_use', 'id': 'live-1', 'name': 'read_file', 'input': {'path': 'notes.txt'}}]},
                     {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'done'}]}]
        class ScriptedTransport:
            def __init__(self, model, provider):
                self.model, self.provider, self.endpoint, self.requests = model, provider, 'offline-test', []
            def complete(self, request):
                self.requests.append(request)
                return responses[len(self.requests) - 1]
        transports = []
        def transport(model, provider):
            transports.append(ScriptedTransport(model, provider))
            return transports[-1]
        console, paths = io.StringIO(), io.StringIO()
        with patch.object(sys, 'argv', ['stage_demo.py', '3', '--live', '--model', 'fixture']), \
             patch.object(stage_demo, 'MessagesHTTP', side_effect=transport), \
             patch.object(stage_demo, 'guarded_loop', wraps=stage_demo.guarded_loop) as guarded, \
             redirect_stdout(console), redirect_stderr(paths):
            self.assertEqual(stage_demo.main(), 0, console.getvalue())
        guarded.assert_called_once()
        result = json.loads(console.getvalue())
        self.assertEqual((result['status'], result['tool_calls']), ('completed', 1))
        self.assertEqual(len(transports[0].requests), 2)

    def test_launcher_records_malformed_exchange_without_traceback(self):
        class BadReplay:
            def complete(self, request):
                return {'content': [{}], 'stop_reason': 'tool_use'}
        console, paths = io.StringIO(), io.StringIO()
        with patch.object(sys, 'argv', ['stage_demo.py', '2']), patch.object(stage_demo, 'Replay', return_value=BadReplay()), \
             redirect_stdout(console), redirect_stderr(paths):
            self.assertEqual(stage_demo.main(), 1)
        json.loads(console.getvalue())  # error output is a single JSON document; paths go to stderr
        path = Path(paths.getvalue().rsplit('Trace: ', 1)[1].strip())
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual(rows[-1]['status'], 'error')
        self.assertEqual(rows[-1]['tool_calls'], 0)
        self.assertFalse(rows[-1]['dispatch_uncertain'])
        self.assertIn('error', [row['event'] for row in rows])

    def test_cli_learner_exception_redacts_configured_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            learner = Path(tmp) / 'learner.py'
            learner.write_text("import os\ndef run_loop(*args, **kwargs):\n    raise RuntimeError(repr(os.environ['OPENROUTER_API_KEY']))\n", encoding='utf-8')
            console, diagnostics = io.StringIO(), io.StringIO()
            with patch.dict(os.environ, {'OPENROUTER_API_KEY': SECRET + '\r'}), \
                 patch.object(sys, 'argv', ['cli.py', '--scenario', 'inference', '--loop-file', str(learner)]), \
                 redirect_stdout(console), redirect_stderr(diagnostics):
                self.assertEqual(cli.main(), 1)
            report = json.loads(console.getvalue())
            trace = Path(report['directory'], 'trace.jsonl').read_text()
            self.assertNotIn(SECRET, console.getvalue() + diagnostics.getvalue() + trace)


if __name__ == '__main__':
    unittest.main()
