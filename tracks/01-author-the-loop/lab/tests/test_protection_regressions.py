"""Focused missed boundary cases; actual container probes live in verify_docker."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from loop import Tools, Trace, Workspace, run_loop


class ProtectionRegressions(unittest.TestCase):
    def test_cross_turn_duplicate_id_refuses_second_dispatch(self):
        class Model:
            def complete(self, request):
                return {'stop_reason':'tool_use','content':[{'type':'tool_use','id':'same',
                    'name':'read_file','input':{'path':'notes.txt'}}]}
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/'notes.txt').write_text('actual bytes',encoding='utf-8')
            tools=Tools(Workspace(root)); trace=Trace(root/'trace.jsonl')
            with patch.object(tools,'dispatch',wraps=tools.dispatch) as dispatch:
                try: result=run_loop(Model(),tools,'read',trace)
                finally: trace.close()
            self.assertEqual(dispatch.call_count,1)
            self.assertEqual(result['status'],'error')
            self.assertEqual(result['tool_calls'],1)

    def test_extra_read_argument_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace=Workspace(Path(temp)); tools=Tools(workspace)
            with patch.object(workspace,'read',return_value='actual bytes') as read:
                result=tools.dispatch({'id':'extra','name':'read_file',
                    'input':{'path':'notes.txt','extra':'ignored?'}})
            self.assertTrue(result['is_error']); read.assert_not_called()

    def test_parent_symlink_rejected_for_read_and_new_edit(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); work=root/'work'; work.mkdir(); outside=root/'outside';outside.mkdir()
            (outside/'notes.txt').write_text('protected',encoding='utf-8')
            (work/'parent').symlink_to(outside,target_is_directory=True)
            (work/'inner').mkdir(); (work/'alias').symlink_to(work/'inner',target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'symlinks'): Workspace(work).path('alias/new.txt')
            tools=Tools(Workspace(work))
            for name,args in [('read_file',{'path':'parent/notes.txt'}),
                              ('edit_file',{'path':'parent/new.txt','old_str':'','new_str':'effect'})]:
                self.assertTrue(tools.dispatch({'id':name,'name':name,'input':args})['is_error'])
            self.assertFalse((outside/'new.txt').exists())
            self.assertEqual((outside/'notes.txt').read_text(encoding='utf-8'),'protected')

    def test_trace_exclusive_create_preserves_bytes_and_private_mode(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'trace.jsonl'; trace=Trace(path)
            try: trace.write('start',mode='synthetic')
            finally: trace.close()
            original=path.read_bytes()
            with self.assertRaises(FileExistsError): Trace(path)
            self.assertEqual(path.read_bytes(),original)
            if os.name=='posix': self.assertEqual(path.stat().st_mode & 0o777,0o600)
            target=Path(temp)/'symlink.jsonl';target.symlink_to(path)
            with self.assertRaises(FileExistsError): Trace(target)
            self.assertEqual(path.read_bytes(),original)
