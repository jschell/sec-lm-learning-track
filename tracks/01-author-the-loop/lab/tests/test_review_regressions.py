"""Regressions for the external review: effect guards and live-task clarity."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
import urllib.error
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(LAB))
from authoring_checks import check_stage, check_guards
import cli
from loop import (COMMAND_OUTPUT_BYTES, TEXT_OUTPUT_CHARS, MessagesHTTP, Replay,
                  Tools, Trace, Workspace, bounded, run_loop, system_for_task)


def load_stages():
    spec=importlib.util.spec_from_file_location('stages',LAB/'solutions/stages.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReviewRegressions(unittest.TestCase):
    def test_checker_rejects_ignored_stop_reason(self):
        reference=load_stages()
        def wrong(model, tools, prompt, trace, **kwargs):
            class IgnoreTruncation:
                def complete(self, request):
                    response=model.complete(request)
                    if response['stop_reason']=='max_tokens':
                        response['stop_reason']='tool_use'
                    return response
            return reference.run_loop(IgnoreTruncation(),tools,prompt,trace,**kwargs)
        with self.assertRaisesRegex(AssertionError,'truncated response: unauthorized dispatch'):
            check_stage(SimpleNamespace(run_loop=wrong),3,guards=True)

    def test_checker_rejects_ignored_call_budget(self):
        reference=load_stages()
        def wrong(model, tools, prompt, trace, **kwargs):
            kwargs['max_calls']=1000
            return reference.run_loop(model,tools,prompt,trace,**kwargs)
        self.assertTrue(check_stage(SimpleNamespace(run_loop=wrong),3))  # Core mechanics remain observable.
        with self.assertRaisesRegex(AssertionError,'batch call limit: unauthorized dispatch'):
            check_stage(SimpleNamespace(run_loop=wrong),3,guards=True)

    def test_checker_rejects_per_turn_instead_of_cumulative_budget(self):
        def wrong(model, tools, prompt, trace, max_turns=4, max_calls=8):
            messages=[{'role':'user','content':prompt}]
            count=0
            status='turn_limit'
            for _ in range(max_turns):
                response=model.complete({'system':'Synthetic instructions','messages':messages,
                                         'tools':tools.definitions,'max_tokens':100})
                if response['stop_reason'] not in {'end_turn','tool_use'}:
                    status='model_stop:'+response['stop_reason']
                    break
                calls=[b for b in response['content'] if b['type']=='tool_use']
                if bool(calls)!=(response['stop_reason']=='tool_use'):
                    status='error'
                    break
                messages.append({'role':'assistant','content':response['content']})
                if not calls:
                    status='completed'
                    break
                if len(calls)>max_calls:  # BUG: ignores calls dispatched on previous turns.
                    status='tool_limit'
                    break
                results=[tools.dispatch(call) for call in calls]
                count+=len(calls)
                messages.append({'role':'user','content':results})
            return {'status':status,'messages':messages,'tool_calls':count}
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'notes.txt').write_text('Synthetic',encoding='utf-8')
            with self.assertRaisesRegex(AssertionError,'cumulative call limit: unauthorized dispatch'):
                check_guards(SimpleNamespace(run_loop=wrong),root,'Synthetic task')

    def test_checker_rejects_discarded_task_policy(self):
        reference=load_stages()
        def wrong(model, tools, prompt, trace, **kwargs):
            kwargs.pop('system',None)
            return reference.run_loop(model,tools,prompt,trace,**kwargs)
        with self.assertRaisesRegex(AssertionError,'preserve the system policy'):
            check_stage(SimpleNamespace(run_loop=wrong),3,guards=True)

    def test_missing_guard_comparison_records_proposals_only(self):
        from compare_guards import compare
        rows=compare()
        self.assertEqual([len(row['recorded_proposals']) for row in rows],[1,0,2,0,3,1])
        self.assertEqual([row['status'] for row in rows],
                         ['completed','model_stop:max_tokens','completed','tool_limit','completed','tool_limit'])

    def test_stage_trace_has_one_response_for_each_request(self):
        for stage in ('1','2'):
            result=subprocess.run([sys.executable,str(LAB.parents[2]/'learn.py'),'stage',stage],
                capture_output=True,text=True,encoding='utf-8',check=True,timeout=15)
            path=Path(result.stdout.rsplit('Trace: ',1)[1].strip())
            rows=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
            requests=[r for r in rows if r['event']=='request']
            responses=[r for r in rows if r['event']=='response']
            self.assertEqual(len(requests),int(stage))
            self.assertEqual([r['turn'] for r in responses],[r['turn'] for r in requests])

    def test_policies_do_not_instruct_unavailable_grader(self):
        for task in ('inference','inspect','missing-file','injection','transfer'):
            text=system_for_task(task)
            self.assertNotIn('/grader',text)
            self.assertNotIn('fizzbuzz',text)
        self.assertIn('/grader/check.py',system_for_task('repair'))

    def test_live_read_request_has_no_repair_instruction(self):
        with patch.object(cli,'MessagesHTTP',return_value=Replay(LAB/'replay/read.json')):
            with patch.object(sys,'argv',['cli.py','--live','--read-only','--model','synthetic']):
                output=io.StringIO()
                with redirect_stdout(output):self.assertEqual(cli.main(),0)
        path=Path(json.loads(output.getvalue())['directory'])/'trace.jsonl'
        requests=[r['request'] for r in map(json.loads,path.read_text(encoding='utf-8').splitlines()) if r['event']=='request']
        for request in requests:
            self.assertEqual(request['system'],system_for_task('inspect'))
            self.assertNotIn('/grader',json.dumps(request))

    def test_learner_replay_exhaustion_is_execution_failure_with_trace(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'learner.py'
            source.write_text("def run_loop(model, tools, prompt, trace, **kwargs):\n"
                              "    model.complete({'messages':[]})\n"
                              "    return model.complete({'messages':[]})\n",encoding='utf-8')
            result=subprocess.run([sys.executable,str(LAB/'cli.py'),'--scenario','inference',
                '--loop-file',str(source)],capture_output=True,text=True,encoding='utf-8',timeout=15)
        self.assertNotEqual(result.returncode,0)
        summary=json.loads(result.stdout)
        self.assertEqual(summary['failure_phase'],'execution')
        self.assertIsNone(summary['tool_calls'])
        rows=[json.loads(line) for line in (Path(summary['directory'])/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
        error=next(r for r in rows if r['event']=='error')
        self.assertEqual(error['error_type'],'ReplayExhausted')
        self.assertIn('completed tool effects',error['message'])

    def test_http_diagnostic_is_useful_bounded_and_redacts_key(self):
        with patch.dict('os.environ',{'OPENROUTER_API_KEY':'synthetic-key'},clear=True):
            model=MessagesHTTP('synthetic','openrouter')
        body=json.dumps({'error':{'type':'invalid_request_error',
            'message':'Unknown parameter; synthetic-key Bearer other-secret sk-example-token'}}).encode()
        error=urllib.error.HTTPError(model.endpoint,400,'ignored',{'x-request-id':'request-123'},io.BytesIO(body))
        with patch('loop.urllib.request.build_opener') as factory:
            factory.return_value.open.side_effect=error
            with self.assertRaises(RuntimeError) as caught:
                model.complete({'tools':[],'messages':[],'max_tokens':10,'system':'Synthetic'})
        text=str(caught.exception)
        for secret in ('synthetic-key','other-secret','sk-example-token'):self.assertNotIn(secret,text)
        self.assertIn('Unknown parameter',text)
        self.assertIn('request-123',text)
        self.assertIn('invalid_request_error',text)
        self.assertLess(len(text),1000)

    def test_unsupported_thinking_block_stops_before_dispatch(self):
        class Model:
            def complete(self,request):
                return {'stop_reason':'tool_use','content':[
                    {'type':'thinking','thinking':'Synthetic unsupported block'},
                    {'type':'tool_use','id':'call','name':'read_file','input':{'path':'notes.txt'}}]}
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);tools=Tools(Workspace(root));trace=Trace(root/'trace.jsonl')
            with patch.object(tools,'dispatch') as dispatch:
                try:result=run_loop(Model(),tools,'Synthetic',trace)
                finally:trace.close()
                dispatch.assert_not_called()
            self.assertEqual(result['status'],'error')
            self.assertIn('thinking',(root/'trace.jsonl').read_text(encoding='utf-8'))

    def test_injection_stays_in_tool_result_and_tools_remain_read_only(self):
        result=subprocess.run([sys.executable,str(LAB/'cli.py'),'--scenario','injection'],
            capture_output=True,text=True,encoding='utf-8',check=True,timeout=15)
        summary=json.loads(result.stdout);root=Path(summary['directory'])
        rows=[json.loads(line) for line in (root/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
        requests=[r['request'] for r in rows if r['event']=='request']
        for request in requests:
            self.assertNotIn('UNTRUSTED INSTRUCTION',request['system'])
            self.assertEqual({d['name'] for d in request['tools']},{'read_file','list_files','code_search'})
        self.assertNotIn('UNTRUSTED INSTRUCTION',json.dumps(requests[0]))
        last=requests[1]['messages'][-1]
        self.assertEqual(last['role'],'user')
        self.assertEqual(last['content'][0]['type'],'tool_result')
        self.assertIn('UNTRUSTED INSTRUCTION',last['content'][0]['content'])
        self.assertEqual((root/'work/notes.txt').read_bytes(),(LAB/'fixtures/notes.txt').read_bytes())

    def test_unicode_text_limit_is_characters(self):
        self.assertEqual(bounded('🔐'*5,3),'🔐'*3+'\n[truncated]')
        self.assertEqual(TEXT_OUTPUT_CHARS,4096)
        self.assertEqual(COMMAND_OUTPUT_BYTES,4096)
