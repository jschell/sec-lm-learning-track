"""Plan 16 regressions: worked-code duplicate IDs, output contracts and boundary mutations."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import shutil
import tempfile
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[2]
sys.path.insert(0, str(LAB))
from loop import DOCKER_IMAGE, MAX_FILE_BYTES, DockerExecutor, Tools, Trace, Workspace
import manifest
from run_support import RunDirectory


def load(path: Path):
    spec = importlib.util.spec_from_file_location('worked_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CountingTools:
    """Real read-only tools that also count dispatch attempts."""
    def __init__(self, root: Path) -> None:
        self.inner = Tools(Workspace(root))
        self.definitions = self.inner.definitions
        self.dispatched = 0

    def dispatch(self, call: dict) -> dict:
        self.dispatched += 1
        return self.inner.dispatch(call)


class ScriptedModel:
    def __init__(self, responses: list[dict]) -> None:
        self.responses = list(responses)

    def complete(self, request: dict) -> dict:
        return self.responses.pop(0)


def call(call_id: str) -> dict:
    return {'type': 'tool_use', 'id': call_id, 'name': 'read_file', 'input': {'path': 'notes.txt'}}


FINAL = {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'done'}]}


class WorkedDuplicateIdTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stages = load(LAB / 'solutions/stages.py')
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'notes.txt').write_text('synthetic', encoding='utf-8')

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_loop(self, responses: list[dict]) -> tuple[dict, CountingTools]:
        tools = CountingTools(self.root)
        trace = Trace(self.root / 'trace.jsonl')
        try:
            result = self.stages.run_loop(ScriptedModel(responses), tools, 'task', trace)
        finally:
            trace.close()
        return result, tools

    def test_exchange_refuses_repeated_ids_before_dispatch(self):
        tools = CountingTools(self.root)
        model = ScriptedModel([{'stop_reason': 'tool_use', 'content': [call('x'), call('x')]}, FINAL])
        with self.assertRaisesRegex(ValueError, 'duplicate tool call ID'):
            self.stages.exchange(model, tools, 'task')
        self.assertEqual(tools.dispatched, 0)

    def test_run_loop_refuses_repeated_ids_within_a_response(self):
        result, tools = self.run_loop([{'stop_reason': 'tool_use', 'content': [call('x'), call('x')]}, FINAL])
        self.assertEqual((result['status'], tools.dispatched, result['tool_calls']), ('error', 0, 0))

    def test_run_loop_refuses_an_id_reused_on_a_later_turn(self):
        result, tools = self.run_loop([{'stop_reason': 'tool_use', 'content': [call('x')]},
                                       {'stop_reason': 'tool_use', 'content': [call('x')]}, FINAL])
        self.assertEqual((result['status'], tools.dispatched, result['tool_calls']), ('error', 1, 1))

    def test_distinct_ids_still_complete(self):
        result, tools = self.run_loop([{'stop_reason': 'tool_use', 'content': [call('a'), call('b')]}, FINAL])
        self.assertEqual((result['status'], tools.dispatched), ('completed', 2))


def learn(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / 'learn.py'), *args], cwd=ROOT, capture_output=True,
                          text=True, encoding='utf-8', timeout=30)


class OutputContractTests(unittest.TestCase):
    def test_json_commands_keep_stdout_valid_and_print_inspect_on_stderr(self):
        for args in (('stage', '3'), ('stage', '2', '--json'), ('--scenario', 'multi'), ('transfer',), ('guards',)):
            with self.subTest(args=args):
                result = learn(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                json.loads(result.stdout)
                self.assertIn('Inspect: uv run --frozen --offline python learn.py trace ', result.stderr)

    def test_bare_entry_shows_help_without_running(self):
        before = set((ROOT / '.cache/exercises/track-1').glob('*/*')) if (ROOT / '.cache/exercises/track-1').exists() else set()
        result = learn()
        self.assertEqual(result.returncode, 0)
        self.assertIn('Usage: learn.py COMMAND', result.stdout)
        after = set((ROOT / '.cache/exercises/track-1').glob('*/*')) if (ROOT / '.cache/exercises/track-1').exists() else set()
        self.assertEqual(before, after)

    def test_usage_names_the_learn_command(self):
        for command in ('stage', 'trace', 'transfer', 'check', 'guards', 'fix'):
            with self.subTest(command=command):
                self.assertTrue(learn(command, '--help').stdout.startswith(f'usage: learn.py {command}'))
        self.assertIn('learn.py stage: error', learn('stage', '1', '--read', 'x').stderr)

    def test_untouched_transfer_starter_says_what_to_do(self):
        result = learn('transfer', '--file', str(LAB / 'starter/transfer.py'))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['learner_status'], 'count_lines not implemented')
        self.assertIn('count_lines is not implemented yet', result.stderr)


class BoundaryMutationTests(unittest.TestCase):
    """Each test fails if its named check is removed (Plan 16 mutation probes)."""
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.work = self.root / 'work'
        shutil.copytree(LAB / 'fixtures', self.work)
        self.tools = Tools(Workspace(self.work))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def dispatch(self, name: str, **args: str) -> dict:
        return self.tools.dispatch({'type': 'tool_use', 'id': 'probe', 'name': name, 'input': args})

    def test_docker_command_keeps_each_advertised_protection(self):
        with patch('loop.shutil.which', return_value='/usr/bin/docker'):
            argv = DockerExecutor(self.work, LAB / 'grader').argv('true', 'probe')
        for flag in ('--network=none', '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
                     '--pull=never'):
            self.assertIn(flag, argv)
        self.assertEqual(argv[argv.index('--user') + 1], '65534:65534')
        tmpfs = argv[argv.index('--tmpfs') + 1].split(':', 1)[1].split(',')
        for option in ('noexec', 'nosuid', 'nodev', 'size=8m'):
            self.assertIn(option, tmpfs)

    def test_edit_result_size_is_bounded(self):
        before = (self.work / 'notes.txt').read_text(encoding='utf-8')
        result = self.dispatch('edit_file', path='notes.txt', old_str='Synthetic', new_str='x' * (MAX_FILE_BYTES - 10))
        self.assertTrue(result['is_error'])
        self.assertIn('exceeds 64 KiB', result['content'])
        self.assertEqual((self.work / 'notes.txt').read_text(encoding='utf-8'), before)

    def test_tool_arguments_are_bounded_before_use(self):
        result = self.dispatch('edit_file', path='new.txt', old_str='', new_str='x' * (MAX_FILE_BYTES + 1))
        self.assertTrue(result['is_error'])
        self.assertIn('bounded strings', result['content'])
        self.assertFalse((self.work / 'new.txt').exists())

    def test_dangling_symlink_in_run_root_is_rejected(self):
        repo = self.root / 'repo'
        (repo / '.cache').mkdir(parents=True)
        (repo / '.cache' / 'exercises').symlink_to(self.root / 'missing-target', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            RunDirectory('fixture', repo)

    def test_symlink_substituted_during_creation_is_rejected(self):
        repo = self.root / 'repo'
        repo.mkdir()
        outside = self.root / 'outside'
        outside.mkdir()
        real_mkdir = Path.mkdir

        def racing_mkdir(path: Path, *args, **kwargs):
            if path.name == 'exercises' and not path.exists():
                path.symlink_to(outside, target_is_directory=True)  # simulated race
                return None
            return real_mkdir(path, *args, **kwargs)

        with patch.object(Path, 'mkdir', racing_mkdir), self.assertRaisesRegex(ValueError, 'real directory'):
            RunDirectory('fixture', repo)
        self.assertEqual(list(outside.iterdir()), [])


class PinTests(unittest.TestCase):
    def test_executor_image_is_digest_pinned_and_matches_ci_pull(self):
        self.assertRegex(DOCKER_IMAGE, r'@sha256:[0-9a-f]{64}$')
        workflow = (ROOT / '.github/workflows/track1.yml').read_text(encoding='utf-8')
        self.assertIn('docker pull ' + DOCKER_IMAGE, workflow)

    def test_workflow_actions_are_pinned_to_full_commit_shas(self):
        import re
        for path in sorted((ROOT / '.github/workflows').glob('*.yml')):
            for line in path.read_text(encoding='utf-8').splitlines():
                if 'uses:' in line:
                    with self.subTest(workflow=path.name, line=line.strip()):
                        self.assertRegex(line, r'uses: [\w.-]+/[\w.-]+@[0-9a-f]{40}\b')


class ManifestTests(unittest.TestCase):
    def test_fixtures_and_teaching_code_match_their_manifests(self):
        self.assertEqual(manifest.check(), [], 'if intended, run lab/manifest.py --update and review the diff')


if __name__ == '__main__':
    unittest.main()
