"""Exercise artifacts stay private and inspectable in one ignored checkout location."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[2]
sys.path.insert(0, str(LAB))
from run_support import RunDirectory
import stage_demo
from loop import Trace
from contextlib import redirect_stderr, redirect_stdout
import io
from authoring_checks import check_stage


class RunArtifactTests(unittest.TestCase):
    def command(self, *args, cwd=ROOT):
        return subprocess.run([sys.executable, str(ROOT / 'learn.py'), *args], cwd=cwd,
                              capture_output=True, text=True, timeout=20)

    def report(self, output):
        # JSON-output commands print their run paths on stderr; summary commands on stdout.
        if isinstance(output, subprocess.CompletedProcess):
            output = output.stdout + '\n' + output.stderr
        lines = [line[7:] for line in output.splitlines() if line.startswith('Trace: ')]
        if lines:
            return json.loads(Path(lines[-1]).with_name('result.json').read_text())
        return json.JSONDecoder().raw_decode(output)[0]

    def test_parallel_unique_runs_refuse_collisions_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            repository = Path(tmp)
            with ThreadPoolExecutor(max_workers=4) as pool:
                runs = list(pool.map(lambda _: RunDirectory('fixture', repository), range(12)))
            self.assertEqual(len({run.root for run in runs}), 12)
            report = runs[0].finish({'mode': 'fixture', 'status': 'completed'})
            original = runs[0].result.read_bytes()
            with self.assertRaises(FileExistsError):
                runs[0].finish({'status': 'changed'})
            self.assertEqual(runs[0].result.read_bytes(), original)
            with patch('run_support.uuid.uuid4', return_value=SimpleNamespace(hex=runs[0].root.name)):
                with self.assertRaises(FileExistsError):
                    RunDirectory('fixture', repository)
            self.assertEqual(report['directory'], str(runs[0].root))

    def test_output_symlinks_and_unsafe_exercise_names_are_rejected(self):
        for component in ('.cache', '.cache/exercises', '.cache/exercises/track-1', '.cache/exercises/track-1/fixture'):
            with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
                repo = Path(tmp)
                link = repo / component
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(outside, target_is_directory=True)
                with self.assertRaises(ValueError):
                    RunDirectory('fixture', repo)
                self.assertEqual(list(Path(outside).iterdir()), [])
        for name in ('../escape', '/absolute', 'nested/name', ''):
            with self.assertRaises(ValueError):
                RunDirectory(name)

    @unittest.skipIf(os.name == 'nt', 'POSIX permission contract')
    def test_private_run_and_workspace_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run = RunDirectory('fixture', repo)
            work = run.copy_fixtures(LAB / 'fixtures')
            run.finish({'status': 'completed'})
            for directory in [run.root, work]:
                self.assertEqual(directory.stat().st_mode & 0o777, 0o700)
            for item in [run.result, *[p for p in work.rglob('*') if p.is_file()]]:
                self.assertEqual(item.stat().st_mode & 0o777, 0o600)
            docker = RunDirectory('docker-fixture', repo)
            docker_work = docker.copy_fixtures(LAB / 'fixtures', docker=True)
            self.assertEqual(docker.root.stat().st_mode & 0o777, 0o700)
            self.assertEqual(docker_work.stat().st_mode & 0o777, 0o777)

    def test_all_learner_routes_retain_trace_and_summary_outside_cwd(self):
        fixture_bytes = {p.name: p.read_bytes() for p in (LAB / 'fixtures').iterdir() if p.is_file()}
        commands = [('stage', '1'), ('stage', '2'), ('stage', '3'),
                    ('--scenario', 'multi', '--max-calls', '1'), ('transfer',), ('guards',),
                    ('check', '--stage', '1', '--file', str(LAB / 'solutions/stages.py'))]
        with tempfile.TemporaryDirectory() as cwd:
            for args in commands:
                with self.subTest(args=args):
                    result = self.command(*args, cwd=cwd)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    report = self.report(result)
                    root = Path(report['directory'])
                    self.assertTrue(root.is_relative_to(ROOT / '.cache/exercises/track-1'))
                    self.assertTrue(Path(report['trace']).is_file())
                    self.assertEqual(json.loads(Path(report['result']).read_text()), report)
                    ignored = subprocess.run(['git', 'check-ignore', str(Path(report['result']))], cwd=ROOT,
                                             capture_output=True)
                    self.assertEqual(ignored.returncode, 0)
        self.assertEqual(fixture_bytes, {p.name: p.read_bytes() for p in (LAB / 'fixtures').iterdir() if p.is_file()})

    def test_repeated_runs_preserve_prior_workspace(self):
        first = self.command('stage', '2')
        report = self.report(first)
        trace = Path(report['trace']).read_bytes()
        second = self.report(self.command('stage', '2'))
        self.assertNotEqual(report['directory'], second['directory'])
        self.assertEqual(Path(report['trace']).read_bytes(), trace)

    def test_common_learner_errors_have_actionable_retained_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            syntax = root / 'syntax.py'
            syntax.write_text('def broken(\n', encoding='utf-8')
            replay = root / 'replay.json'
            replay.write_text(json.dumps({'turns': [{'response': {}, 'checks': [{}]}]}), encoding='utf-8')
            commands = [('stage', '2', '--replay-file', str(root / 'absent.json')),
                        ('stage', '2', '--replay-file', str(replay)),
                        ('--scenario', 'read', '--loop-file', str(root / 'absent.py')),
                        ('--scenario', 'read', '--loop-file', str(syntax)),
                        ('transfer', '--file', str(syntax)),
                        ('check', '--stage', '2', '--file', str(syntax))]
            for args in commands:
                with self.subTest(args=args):
                    result = self.command(*args)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn('Traceback (most recent call last)', result.stdout + result.stderr)
                    report = self.report(result)
                    self.assertIn(report['status'], ('error', 'not_verified'))
                    self.assertTrue(Path(report['trace']).exists())
                    if 'checks' in result.stdout:
                        self.assertIn('nonempty id', result.stdout)

    def test_stage_two_accepts_feedback_history_with_or_without_actual_final(self):
        spec = importlib.util.spec_from_file_location('history_worked', LAB / 'solutions/stages.py')
        worked = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(worked)
        self.assertTrue(check_stage(worked, 2))
        def complete_history(*args, **kwargs):
            response, history = worked.exchange(*args, **kwargs)
            return response, history + [{'role': 'assistant', 'content': response['content']}]
        self.assertTrue(check_stage(SimpleNamespace(exchange=complete_history), 2))
        def wrong_history(*args, **kwargs):
            response, history = complete_history(*args, **kwargs)
            history[-1]['content'] = [{'type': 'text', 'text': 'fabricated'}]
            return response, history
        with self.assertRaisesRegex(AssertionError, 'actual final assistant response'):
            check_stage(SimpleNamespace(exchange=wrong_history), 2)

    def test_trace_storage_failure_is_not_reported_as_complete(self):
        class BrokenTrace(Trace):
            def write(self, event, **values):
                raise OSError('synthetic storage failure')
        console, paths = io.StringIO(), io.StringIO()
        with patch.object(stage_demo, 'Trace', BrokenTrace), \
             patch.object(sys, 'argv', ['stage_demo.py', '1']), redirect_stdout(console), redirect_stderr(paths):
            self.assertEqual(stage_demo.main(), 1)
        report = self.report(console.getvalue() + '\n' + paths.getvalue())
        self.assertEqual(report['status'], 'error')
        self.assertTrue(report['trace_incomplete'])
        self.assertTrue(Path(report['result']).is_file())

    def test_pre_dispatch_setup_failure_reports_zero_known_attempts(self):
        output = self.command('transfer', '--file', str(ROOT / 'missing-learner-implementation.py'))
        report = self.report(output)
        self.assertEqual(report['status'], 'error')
        self.assertEqual(report['tool_calls'], 0)
        self.assertEqual(report['dispatch_attempts'], 0)
        self.assertFalse(report['dispatch_uncertain'])

    def test_synthetic_read_only_policy_matches_exposed_tools(self):
        output = self.command('--scenario', 'read')
        report = self.report(output)
        rows = [json.loads(line) for line in Path(report['trace']).read_text().splitlines()]
        requests = [row['request'] for row in rows if row['event'] == 'request']
        for request in requests:
            self.assertNotIn('edit_file', {tool['name'] for tool in request['tools']})
            self.assertIn('Do not edit', request['system'])


if __name__ == '__main__':
    unittest.main()
