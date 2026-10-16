"""Functional checks of protocol, mutation safety, failure handling and replay."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from loop import AnthropicHTTP, DockerExecutor, Replay, Tools, Trace, Workspace, run_loop
from scenarios import ScriptedExecutor


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.work=self.root/'work'
        shutil.copytree(HERE/'fixtures',self.work)
        self.tools=Tools(Workspace(self.work))

    def tearDown(self): self.temp.cleanup()

    def run_case(self,scenario,**limits):
        if scenario=='repair':
            self.tools=Tools(Workspace(self.work),ScriptedExecutor())
        trace=Trace(self.root/'trace.jsonl')
        try: result=run_loop(Replay(HERE/'replay'/f'{scenario}.json'),self.tools,'Synthetic task',trace,**limits)
        finally: trace.close()
        rows=[json.loads(line) for line in (self.root/'trace.jsonl').read_text().splitlines()]
        self.assertEqual(rows[-1]['event'],'stop')
        self.assertEqual(rows[-1]['status'],result['status'])
        return result,rows

    def dispatch(self,name,**args):
        return self.tools.dispatch({'type':'tool_use','id':'t1','name':name,'input':args})

    def test_inference_has_no_tools(self):
        result,rows=self.run_case('inference')
        self.assertEqual(result['status'],'completed')
        self.assertFalse(any(row['event']=='tool' for row in rows))

    def test_read_exchange_ids_and_history(self):
        result,rows=self.run_case('read')
        self.assertEqual(result['status'],'completed')
        self.assertEqual([m['role'] for m in result['messages']],['user','assistant','user','assistant'])
        self.assertEqual(result['messages'][1]['content'][0]['id'],result['messages'][2]['content'][0]['tool_use_id'])
        requests=[r for r in rows if r['event']=='request']
        self.assertEqual(len(requests[0]['request']['messages']),1)
        self.assertEqual(len(requests[1]['request']['messages']),3)

    def test_multiple_calls_batched_in_order(self):
        result,_=self.run_case('multi')
        self.assertEqual(result['tool_calls'],2)
        self.assertEqual(len(result['messages'][2]['content']),2)

    def test_error_recovery(self):
        result,rows=self.run_case('recover')
        self.assertEqual(result['status'],'completed')
        errors=[r['result']['is_error'] for r in rows if r['event']=='tool']
        self.assertEqual(errors,[True,True,True,False])

    def test_repair_changes_actual_file_but_commands_scripted(self):
        result,rows=self.run_case('repair')
        self.assertEqual(result['status'],'completed')
        self.assertEqual((self.work/'fizzbuzz.py').read_text(),(HERE/'solutions/fizzbuzz.py').read_text())
        outputs=[r['result']['content'] for r in rows if r['event']=='tool' and r['call']['name']=='run_command']
        self.assertTrue(all('SCRIPTED OBSERVATION' in o for o in outputs))

    def test_turn_limit(self):
        result,_=self.run_case('limit',max_turns=2)
        self.assertEqual(result['status'],'turn_limit')
        self.assertEqual(result['tool_calls'],2)

    def test_batch_limit_prevents_partial_execution(self):
        result,_=self.run_case('multi',max_calls=1)
        self.assertEqual(result['status'],'tool_limit')
        self.assertEqual(result['tool_calls'],0)

    def test_truncated_response_cannot_edit(self):
        before=(self.work/'notes.txt').read_text()
        result,_=self.run_case('truncated')
        self.assertEqual(result['status'],'model_stop:max_tokens')
        self.assertEqual((self.work/'notes.txt').read_text(),before)

    def test_path_boundaries(self):
        (self.root/'outside.txt').write_text('synthetic secret')
        (self.work/'link.txt').symlink_to(self.root/'outside.txt')
        for path in ['../outside.txt',str(self.root/'outside.txt'),'link.txt']:
            with self.subTest(path=path): self.assertTrue(self.dispatch('read_file',path=path)['is_error'])
        self.assertTrue(self.dispatch('edit_file',path='link.txt',old_str='synthetic',new_str='changed')['is_error'])
        self.assertEqual((self.root/'outside.txt').read_text(),'synthetic secret')

    def test_edit_is_unambiguous(self):
        self.assertTrue(self.dispatch('edit_file',path='notes.txt',old_str='',new_str='overwrite')['is_error'])
        (self.work/'twice.txt').write_text('same same')
        self.assertTrue(self.dispatch('edit_file',path='twice.txt',old_str='same',new_str='x')['is_error'])
        self.assertEqual((self.work/'twice.txt').read_text(),'same same')
        self.assertFalse(self.dispatch('edit_file',path='new.txt',old_str='',new_str='new')['is_error'])

    def test_bounded_output_and_large_file(self):
        (self.work/'large.txt').write_text('x'*5000)
        answer=self.dispatch('read_file',path='large.txt')
        self.assertIn('[truncated]',answer['content'])
        (self.work/'large.txt').write_text('x'*65537)
        self.assertTrue(self.dispatch('read_file',path='large.txt')['is_error'])

    def test_disabled_commands_fail_closed(self):
        self.assertTrue(self.dispatch('run_command',command='echo should-not-run')['is_error'])

    def test_duplicate_call_ids_stop_before_any_side_effect(self):
        class Model:
            def complete(self,request):
                return {'stop_reason':'tool_use','content':[
                    {'type':'tool_use','id':'same','name':'edit_file','input':{'path':'new.txt','old_str':'','new_str':'x'}},
                    {'type':'tool_use','id':'same','name':'read_file','input':{'path':'notes.txt'}}]}
        trace=Trace(self.root/'trace.jsonl')
        try: result=run_loop(Model(),self.tools,'task',trace)
        finally: trace.close()
        self.assertEqual(result['status'],'error')
        self.assertFalse((self.work/'new.txt').exists())

    def test_provider_failure_is_terminal_and_logged(self):
        class Model:
            def complete(self,request): raise RuntimeError('synthetic outage')
        trace=Trace(self.root/'trace.jsonl')
        try: result=run_loop(Model(),self.tools,'task',trace)
        finally: trace.close()
        self.assertEqual(result['status'],'error')
        self.assertIn('synthetic outage',(self.root/'trace.jsonl').read_text())

    def test_docker_configuration_and_no_key_forwarding(self):
        with patch('loop.shutil.which',return_value='/usr/bin/docker'):
            executor=DockerExecutor(self.work,HERE/'grader')
        argv=executor.argv('echo "$ANTHROPIC_API_KEY"','test-name')
        for flag in ['--network=none','--read-only','--cap-drop=ALL','--pids-limit','--memory','--cpus']:
            self.assertIn(flag,argv)
        self.assertNotIn('--env',argv)
        self.assertEqual(argv[-3:],['/bin/sh','-c','echo "$ANTHROPIC_API_KEY"'])
        self.assertTrue(any('dst=/grader,readonly' in arg for arg in argv))

    def test_http_protocol_without_live_network(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self): return b'{"content":[{"type":"text","text":"mock"}],"stop_reason":"end_turn"}'
        with patch.dict('os.environ',{'ANTHROPIC_API_KEY':'synthetic-key'}):
            with patch('loop.urllib.request.urlopen',return_value=Response()) as opener:
                result=AnthropicHTTP('account-selected-model').complete({'tools':[],'messages':[{'role':'user','content':'hello'}],'max_tokens':10,'system':'test'})
        self.assertEqual(result['stop_reason'],'end_turn')
        request=opener.call_args.args[0]
        self.assertEqual(request.full_url,'https://api.anthropic.com/v1/messages')
        body=json.loads(request.data)
        self.assertEqual(body['model'],'account-selected-model')
        self.assertNotIn('tools',body)
        self.assertNotIn('synthetic-key',request.data.decode())


if __name__=='__main__': unittest.main()
