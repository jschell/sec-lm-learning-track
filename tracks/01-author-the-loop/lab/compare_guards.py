"""Observe missing guards using recorded proposals, without executing actions.

Original teaching exercise inspired by Huntley's minimal dispatch loop.
See ../08-learn-from-missing-guards.md for source and interpretation.
"""
import argparse
import copy
import json
from pathlib import Path
import tempfile

from loop import Trace, run_loop, schema


class Model:
    """Return authored responses, with a hard bound on inference calls."""
    def __init__(self, responses: list[dict]) -> None:
        self.responses = copy.deepcopy(responses)
        self.requests = 0

    def complete(self, request: dict) -> dict:
        index = self.requests
        self.requests += 1
        if index >= len(self.responses):
            raise ValueError('comparison replay exhausted')
        return self.responses[index]


class RecordedActions:
    """Record a proposal only. No filesystem, subprocess or network operations."""
    def __init__(self) -> None:
        self.definitions = [schema('record_action', 'Record a simulated action label.', ('label',))]
        self.recorded: list[str] = []

    def dispatch(self, call: dict) -> dict:
        self.recorded.append(call['input']['label'])
        return {'type':'tool_result','tool_use_id':call['id'],
                'content':'Simulated action recorded; nothing executed.','is_error':False}


def minimal_loop(model, tools, prompt: str, trace, max_calls: int) -> dict:
    """Deliberately incomplete: dispatch calls without checking reason/budget.

    Use only with RecordedActions in this comparison. The outer loop is bounded
    so observing missing guards cannot create an unending learning exercise.
    """
    messages = [{'role':'user','content':prompt}]
    for _ in range(4):
        response = model.complete({'system':'Compare synthetic proposals.',
            'messages':messages, 'tools':tools.definitions, 'max_tokens':100})
        messages.append({'role':'assistant','content':response['content']})
        calls = [b for b in response['content'] if b['type']=='tool_use']
        if not calls:
            return {'status':'completed','tool_calls':len(tools.recorded)}
        results = [tools.dispatch(call) for call in calls]
        messages.append({'role':'user','content':results})
    return {'status':'turn_limit','tool_calls':len(tools.recorded)}


def compare() -> list[dict]:
    def response(reason: str, labels: list[str]) -> dict:
        return {'stop_reason':reason,'content':[
            {'type':'tool_use','id':label,'name':'record_action','input':{'label':label}}
            for label in labels]}
    final = response('end_turn',[])
    cases = [
        ('truncated proposal',[response('max_tokens',['partial']),final],2),
        ('two-call batch, budget one',[response('tool_use',['a','b']),final],1),
        ('prior call plus two-call batch, total budget two',[
            response('tool_use',['a']),response('tool_use',['b','c']),final],2),
    ]
    observations = []
    with tempfile.TemporaryDirectory(prefix='guard-comparison-') as temp:
        for index,(name,responses,budget) in enumerate(cases):
            for label,controller in [('minimal',minimal_loop),('guarded',run_loop)]:
                tools = RecordedActions()
                trace = Trace(Path(temp)/f'{index}-{label}.jsonl')
                try:
                    result = controller(Model(responses),tools,'Compare authored proposals.',trace,
                                        max_calls=budget)
                finally:
                    trace.close()
                observations.append({'case':name,'controller':label,
                    'budget':budget,'recorded_proposals':tools.recorded,'status':result['status']})
    return observations


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps({'mode':'simulated proposals; no actions executed','observations':compare()},indent=2))
