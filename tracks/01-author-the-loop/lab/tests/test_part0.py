"""Part 0: minimal loop transcript, history growth, error feedback, read-only tools and finiteness."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[2]
sys.path.insert(0, str(LAB))
from authoring_checks import check_stage
from loop import Replay, ReplayExhausted, Workspace
from part0 import minimal_loop


def learn(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / 'learn.py'), *args], cwd=cwd, capture_output=True,
                          text=True, encoding='utf-8', timeout=30)


def requests(stdout: str) -> list[dict]:
    path = Path(next(line[7:] for line in stdout.splitlines() if line.startswith('Trace: ')))
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    return [row['request'] for row in rows if row['event'] == 'request']


class Part0CommandTests(unittest.TestCase):
    def test_chat_resends_the_growing_history(self):
        result = learn('part0', 'chat')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('You: '), 2)
        self.assertEqual(result.stdout.count('Model (scripted): '), 2)
        sent = requests(result.stdout)
        self.assertEqual([len(r['messages']) for r in sent], [1, 3])
        self.assertEqual(sent[1]['messages'][0], sent[0]['messages'][0])  # the first turn is re-sent
        self.assertEqual(sent[0]['tools'], [])

    def test_exchange_shows_call_result_and_next_request(self):
        result = learn('part0', 'exchange')
        self.assertIn("tool: read_file({'path': 'notes.txt'})", result.stdout)
        self.assertIn('result: Synthetic exercise.', result.stdout)
        second = requests(result.stdout)[1]['messages']
        self.assertEqual(second[1]['content'][0]['id'], second[2]['content'][0]['tool_use_id'])

    def test_loop_feeds_an_error_back_as_an_ordinary_result(self):
        result = learn('part0', 'loop')
        self.assertIn('error: ', result.stdout)
        second = requests(result.stdout)[1]['messages'][-1]['content'][0]
        self.assertEqual((second['tool_use_id'], second['is_error']), ('p0-loop-1', True))
        self.assertEqual(len(requests(result.stdout)), 3)

    def test_more_tools_uses_the_same_loop_with_list_files(self):
        result = learn('part0', 'more-tools')
        self.assertIn("tool: list_files({'path': '.'})", result.stdout)
        self.assertEqual([d['name'] for d in requests(result.stdout)[0]['tools']], ['read_file', 'list_files'])

    def test_tools_step_shows_definitions_and_functions(self):
        out = learn('part0', 'tools').stdout
        for text in ('Tool: read_file', 'Tool: list_files', 'description (sent to the model)',
                     'runs (on the controller, looked up by name): read_file()'):
            self.assertIn(text, out)

    def test_live_mode_is_refused(self):
        result = learn('part0', 'loop', '--live')
        self.assertEqual(result.returncode, 2)
        self.assertIn('scripted replay only', result.stderr)

    def test_runs_are_retained_in_the_repository_from_any_directory(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            result = learn('part0', 'exchange', cwd=Path(elsewhere))
        run = Path(next(line[5:] for line in result.stdout.splitlines() if line.startswith('Run: ')))
        self.assertTrue(run.resolve().is_relative_to((ROOT / '.cache/exercises/track-1/part0-exchange').resolve()))
        self.assertEqual(json.loads((run / 'result.json').read_text(encoding='utf-8'))['tool_calls'], 1)
        self.assertIn('Inspect: uv run --frozen --offline python learn.py trace ', result.stdout)

    def test_help_and_usage_name_part0(self):
        self.assertIn('part0 STEP', learn('--help').stdout)
        self.assertTrue(learn('part0', '--help').stdout.startswith('usage: learn.py part0'))


class MinimalLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name)
        (self.work / 'notes.txt').write_text('synthetic', encoding='utf-8')

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_only_read_only_tools_exist(self):
        self.assertEqual(set(minimal_loop.FUNCTIONS), {'read_file', 'list_files'})
        tools = minimal_loop.ReadOnlyTools(Workspace(self.work), ['read_file'])
        for name, args in (('run_command', {'command': 'true'}), ('edit_file', {'path': 'notes.txt'}),
                           ('list_files', {'path': '.'})):
            result = tools.dispatch({'type': 'tool_use', 'id': name, 'name': name, 'input': args})
            self.assertTrue(result['is_error'])
            self.assertIn('not found', result['content'])
        escaped = tools.dispatch({'type': 'tool_use', 'id': 'x', 'name': 'read_file', 'input': {'path': '../x'}})
        self.assertTrue(escaped['is_error'])

    def test_guard_free_loop_still_ends_when_replay_ends(self):
        with tempfile.TemporaryDirectory() as tmp:
            replay = Path(tmp) / 'endless.json'
            call = {'type': 'tool_use', 'id': 'again', 'name': 'read_file', 'input': {'path': 'notes.txt'}}
            replay.write_text(json.dumps({'turns': [{'response': {'stop_reason': 'tool_use', 'content': [call]}}]}),
                              encoding='utf-8')
            tools = minimal_loop.ReadOnlyTools(Workspace(self.work), ['read_file'])
            with self.assertRaises(ReplayExhausted):
                minimal_loop.run_conversation(Replay(replay), tools, ['task'], lambda label, text: None)

    def test_part0_check_accepts_the_worked_loop_and_rejects_wrong_ones(self):
        self.assertTrue(check_stage(minimal_loop, 0))
        def drops_errors(model, tools, user_turns, show):
            conversation = [{'role': 'user', 'content': user_turns[0]}]
            message = model.complete(minimal_loop.request(conversation, tools))
            conversation.append({'role': 'assistant', 'content': message['content']})
            while any(b['type'] == 'tool_use' for b in message['content']):
                results = [r for r in (tools.dispatch(b) for b in message['content'] if b['type'] == 'tool_use')
                           if not r['is_error']]
                conversation.append({'role': 'user', 'content': results})
                message = model.complete(minimal_loop.request(conversation, tools))
                conversation.append({'role': 'assistant', 'content': message['content']})
            return conversation
        with self.assertRaisesRegex(AssertionError, 'omits the error result'):
            check_stage(SimpleNamespace(run_conversation=drops_errors), 0)
        spec = importlib.util.spec_from_file_location('part0_starter', LAB / 'part0/starter.py')
        starter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(starter)
        with self.assertRaises(NotImplementedError):
            check_stage(starter, 0)


if __name__ == '__main__':
    unittest.main()
