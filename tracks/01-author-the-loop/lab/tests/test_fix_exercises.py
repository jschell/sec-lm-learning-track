"""Targeted checker diagnoses and the optional broken-file fix exercises."""
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

EXERCISES = LAB / 'exercises'
MANIFEST = json.loads((EXERCISES / 'exercises.json').read_text(encoding='utf-8'))


def load(path):
    spec = importlib.util.spec_from_file_location('fix_exercise_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request(tools, messages):
    return {'system': 'Instructions', 'messages': messages, 'tools': tools.definitions, 'max_tokens': 100}


class FixExerciseTests(unittest.TestCase):
    def test_each_exercise_fails_with_its_diagnosis_and_solution_passes(self):
        for name, entry in MANIFEST.items():
            with self.subTest(exercise=name):
                broken = load(EXERCISES / entry['file'])
                with self.assertRaises(AssertionError) as caught:
                    check_stage(broken, entry['stage'])
                self.assertIn(entry['diagnosis'], str(caught.exception))
                self.assertTrue(check_stage(load(EXERCISES / entry['solution']), entry['stage']))

    def test_manifest_entries_are_complete(self):
        for name, entry in MANIFEST.items():
            with self.subTest(exercise=name):
                source = (EXERCISES / entry['file']).read_text(encoding='utf-8')
                solution = (EXERCISES / entry['solution']).read_text(encoding='utf-8')
                self.assertIn('TODO', source)
                self.assertNotIn('TODO', solution)
                self.assertGreaterEqual(len(entry['hints']), 2)
                self.assertIn(entry['stage'], (2, 3))


class TargetedDiagnosisTests(unittest.TestCase):
    def exchange_failure(self, exchange):
        with self.assertRaises(AssertionError) as caught:
            check_stage(SimpleNamespace(exchange=exchange), 2)
        return str(caught.exception)

    def test_results_never_appended(self):
        def exchange(model, tools, prompt):
            messages = [{'role': 'user', 'content': prompt}]
            first = model.complete(request(tools, messages))
            messages.append({'role': 'assistant', 'content': first['content']})
            [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
            return model.complete(request(tools, messages)), messages
        self.assertIn('no tool_result after them', self.exchange_failure(exchange))

    def test_results_before_call(self):
        def exchange(model, tools, prompt):
            messages = [{'role': 'user', 'content': prompt}]
            first = model.complete(request(tools, messages))
            results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
            messages += [{'role': 'user', 'content': results}, {'role': 'assistant', 'content': first['content']}]
            return model.complete(request(tools, messages)), messages
        self.assertIn('places the tool_result before the assistant call', self.exchange_failure(exchange))

    def test_mismatched_result_id(self):
        def exchange(model, tools, prompt):
            messages = [{'role': 'user', 'content': prompt}]
            first = model.complete(request(tools, messages))
            messages.append({'role': 'assistant', 'content': first['content']})
            results = [{**tools.dispatch(b), 'tool_use_id': 'read-1'} for b in first['content'] if b['type'] == 'tool_use']
            messages.append({'role': 'user', 'content': results})
            return model.complete(request(tools, messages)), messages
        self.assertIn("tool_use_id 'read-1', which matches no requested call", self.exchange_failure(exchange))

    def test_substituted_result_content(self):
        def exchange(model, tools, prompt):
            messages = [{'role': 'user', 'content': prompt}]
            first = model.complete(request(tools, messages))
            messages.append({'role': 'assistant', 'content': first['content']})
            results = [{**tools.dispatch(b), 'content': 'fabricated'} for b in first['content'] if b['type'] == 'tool_use']
            messages.append({'role': 'user', 'content': results})
            return model.complete(request(tools, messages)), messages
        self.assertIn('differs from what dispatch actually returned', self.exchange_failure(exchange))

    def test_task_replaced(self):
        def exchange(model, tools, prompt):
            first = model.complete(request(tools, [{'role': 'user', 'content': 'A different task'}]))
            return first, []
        self.assertIn('does not start with the original user task', self.exchange_failure(exchange))

    def test_one_result_of_a_batch_dropped(self):
        solution = load(LAB / 'solutions/stages.py')
        def run_loop(model, tools, prompt, trace, **kwargs):
            class FirstOnly:
                definitions = tools.definitions
                def __init__(self):
                    self.seen = 0
                def dispatch(self, call):
                    self.seen += 1
                    return tools.dispatch(call)
            wrapper = FirstOnly()
            original = model.complete
            def complete(req):
                messages = req['messages']
                if messages and messages[-1]['role'] == 'user' and isinstance(messages[-1]['content'], list) \
                        and len(messages[-1]['content']) > 1:
                    req = {**req, 'messages': [*messages[:-1], {'role': 'user', 'content': messages[-1]['content'][:1]}]}
                return original(req)
            model.complete = complete
            return solution.run_loop(model, wrapper, prompt, trace, **kwargs)
        with self.assertRaises(AssertionError) as caught:
            check_stage(SimpleNamespace(run_loop=run_loop), 3)
        self.assertIn('has no result for call', str(caught.exception))


class FixCommandTests(unittest.TestCase):
    def invoke(self, *args, cwd=ROOT, check=True):
        return subprocess.run([sys.executable, str(ROOT / 'learn.py'), 'fix', *args], cwd=cwd,
                              capture_output=True, text=True, encoding='utf-8', check=check)

    def test_list_and_hint(self):
        listing = self.invoke().stdout
        for name in MANIFEST:
            self.assertIn(name, listing)
        hint = self.invoke('loop-drops-errors', '--hint', '2').stdout
        self.assertIn(MANIFEST['loop-drops-errors']['hints'][1], hint)

    def test_errors_are_actionable(self):
        unknown = self.invoke('no-such-exercise', check=False)
        self.assertEqual(unknown.returncode, 2)
        self.assertIn('choose one of', unknown.stderr)
        rung = self.invoke('exchange-missing-call', '--hint', '9', check=False)
        self.assertEqual(rung.returncode, 2)
        self.assertIn('has hints 1-2', rung.stderr)

    def test_copies_are_fresh_repo_local_and_leave_source_unchanged(self):
        source = EXERCISES / MANIFEST['exchange-missing-call']['file']
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as elsewhere:
            outputs = [self.invoke('exchange-missing-call', cwd=elsewhere).stdout for _ in range(2)]
        edits = [Path(line.split(': ', 1)[1]) for out in outputs for line in out.splitlines() if line.startswith('Edit: ')]
        self.assertEqual(len(edits), 2)
        self.assertNotEqual(edits[0], edits[1])
        cache = (ROOT / '.cache/exercises/track-1/fix-exchange-missing-call').resolve()
        for edit in edits:
            self.assertEqual(edit.resolve().parents[2], cache)
            self.assertEqual(edit.read_bytes(), source.read_bytes())
            self.assertEqual(edit.stat().st_mode & 0o777, 0o600)
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)


if __name__ == '__main__':
    unittest.main()
