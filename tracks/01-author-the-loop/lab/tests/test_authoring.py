"""Behavioral contracts and rejection regressions for original teaching exercises."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from authoring_checks import check_stage
from loop import Workspace
from transfer_support import CountLinesTools


def load(path):
    spec = importlib.util.spec_from_file_location('exercise', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TeachingChecks(unittest.TestCase):
    def test_complete_stages_and_full_reference(self):
        stages = load(LAB / 'solutions/stages.py')
        for stage in (1, 2, 3):
            with self.subTest(stage=stage):
                self.assertTrue(check_stage(stages, stage, guards=stage == 3))
        self.assertTrue(check_stage(load(LAB / 'loop.py'), 3, guards=True))

    def test_reject_fabricated_single_response(self):
        fake = SimpleNamespace(infer_once=lambda model, prompt: {
            'content':[{'type':'text', 'text':'Looks correct'}], 'stop_reason':'end_turn'})
        with self.assertRaisesRegex(AssertionError, 'inference request'):
            check_stage(fake, 1)

    def test_reject_missing_second_inference(self):
        def exchange(model, tools, prompt):
            messages = [{'role':'user', 'content':prompt}]
            first = model.complete({'system':'Instructions', 'messages':messages,
                                    'tools':tools.definitions, 'max_tokens':100})
            messages.append({'role':'assistant', 'content':first['content']})
            results = [tools.dispatch(c) for c in first['content'] if c['type']=='tool_use']
            messages.append({'role':'user', 'content':results})
            return {'stop_reason':'end_turn','content':[]}, messages
        with self.assertRaisesRegex(AssertionError, '2 inference request'):
            check_stage(SimpleNamespace(exchange=exchange), 2)

    def test_reject_dropped_feedback(self):
        stages = load(LAB / 'solutions/stages.py')
        def broken(model, tools, prompt):
            class DropResults:
                definitions = tools.definitions
                def dispatch(self, call):
                    tools.dispatch(call)
                    return {'type':'tool_result','tool_use_id':call['id'],'content':'fabricated'}
            return stages.exchange(model, DropResults(), prompt)
        with self.assertRaisesRegex(AssertionError, 'actual tool results'):
            check_stage(SimpleNamespace(exchange=broken), 2)

    def test_transfer_content_and_boundary(self):
        count = load(LAB / 'solutions/transfer.py').count_lines
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = Workspace(root)
            for text, expected in [('',0), ('a',1), ('a\n',1), ('a\n\nb\n',3)]:
                (root/'sample.txt').write_text(text, encoding='utf-8')
                self.assertEqual(count(workspace, 'sample.txt'), expected)
            tools = CountLinesTools(workspace, count)
            for args in ({'path':'../outside'}, {'path':1}, {'path':'sample.txt','extra':True}):
                result = tools.dispatch({'id':'call', 'name':'count_lines','input':args})
                self.assertTrue(result['is_error'])
            self.assertEqual(tools.observed, [])

    def test_launchers_and_unfinished_starter(self):
        root = LAB.parents[2]
        for args in [('stage','1'), ('stage','2'), ('stage','3'), ('transfer',),
                     ('check','--stage','3','--file',str(LAB/'solutions/stages.py'))]:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(root/'learn.py'), *args],
                    capture_output=True, text=True, encoding='utf-8', timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable,str(root/'learn.py'),'check','--stage','1',
            '--file',str(LAB/'starter/stages.py')], capture_output=True,
            text=True, encoding='utf-8', timeout=15)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('NOT VERIFIED',result.stderr)
