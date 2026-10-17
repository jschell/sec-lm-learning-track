"""Small behavioral checks, not a certificate or adversarial anti-cheating system.

Original project tests inspired by explicit implementation contracts such as
Stanford CS336's adapters; see ../SOURCES.md. No upstream test code is copied.
"""
import copy
from pathlib import Path
import tempfile
import uuid

from loop import Tools, Trace, Workspace


class ObservedTools:
    """Record real dispatch calls and results, not learner-supplied history alone."""
    def __init__(self, workspace: Workspace) -> None:
        self.inner = Tools(workspace)
        self.inner.definitions = [d for d in self.inner.definitions if d['name'] == 'read_file']
        self.definitions = self.inner.definitions
        self.calls: list[dict] = []
        self.results: list[dict] = []

    def dispatch(self, call: dict) -> dict:
        self.calls.append(copy.deepcopy(call))
        result = self.inner.dispatch(call)
        self.results.append(copy.deepcopy(result))
        return result


class CheckedModel:
    """Release each next response only after the required feedback arrived."""
    def __init__(self, prompt: str, tools: ObservedTools, batches: list[list[str]]) -> None:
        self.prompt = prompt
        self.tools = tools
        self.batches = batches
        self.requests: list[dict] = []
        self.history = [{'role': 'user', 'content': prompt}]
        self.pending: list[dict] = []
        self.expected_calls: list[dict] = []
        self.last_response: dict | None = None
        self.marker = uuid.uuid4().hex
        self.failure: str | None = None

    def require(self, condition: bool, explanation: str) -> None:
        if not condition:
            self.failure = explanation
            raise AssertionError(explanation)

    def complete(self, request: dict) -> dict:
        index = len(self.requests)
        self.requests.append(copy.deepcopy(request))
        self.require(index <= len(self.batches), 'unexpected additional inference request')
        self.require(request.get('tools') == self.tools.definitions,
                     'request must expose the supplied tool definitions')
        self.require(isinstance(request.get('system'), str) and bool(request['system']),
                     'request needs explicit system instructions')
        self.require(type(request.get('max_tokens')) is int and request['max_tokens'] > 0,
                     'request needs a positive output-token limit')
        if self.pending:
            self.require(self.tools.calls == self.expected_calls,
                         'dispatch every requested call exactly once before the next inference')
            self.history.append({'role': 'user', 'content': copy.deepcopy(self.tools.results[-len(self.pending):])})
            self.pending = []
        self.require(request.get('messages') == self.history,
                     'next inference must contain the original task, assistant calls, and matching actual tool results')
        if index < len(self.batches):
            calls = [{'type': 'tool_use', 'id': f'{self.marker}-{index}-{i}',
                      'name': 'read_file', 'input': {'path': path}}
                     for i, path in enumerate(self.batches[index])]
            content = [{'type': 'text', 'text': 'Inspecting the synthetic fixture.'}, *calls]
            response = {'stop_reason': 'tool_use', 'content': content}
            self.pending = calls
            self.expected_calls.extend(copy.deepcopy(calls))
        else:
            response = {'stop_reason': 'end_turn', 'content': [
                {'type': 'text', 'text': 'Observed final response ' + self.marker}]}
        self.last_response = copy.deepcopy(response)
        self.history.append({'role': 'assistant', 'content': copy.deepcopy(response['content'])})
        return copy.deepcopy(response)

    def finish(self, expected_requests: int, expected_calls: int) -> None:
        self.require(self.failure is None, self.failure or 'previous request validation failed')
        self.require(len(self.requests) == expected_requests,
                     f'expected {expected_requests} inference request(s), observed {len(self.requests)}')
        self.require(len(self.tools.calls) == expected_calls,
                     f'expected {expected_calls} dispatched call(s), observed {len(self.tools.calls)}')
        self.require(self.tools.calls == self.expected_calls,
                     'executed calls do not match the model-requested IDs/arguments')


def check_stage(module, stage: int) -> list[str]:
    """Check actual learner behavior using changing IDs and synthetic file contents.

    Raises:
        AssertionError: A required request, dispatch, feedback or stop was missing.
    """
    passed = []
    with tempfile.TemporaryDirectory(prefix='authoring-check-') as temp:
        root = Path(temp)
        value = 'Synthetic observation ' + uuid.uuid4().hex
        (root / 'notes.txt').write_text(value, encoding='utf-8')
        prompt = 'Read the supplied synthetic fixture: ' + uuid.uuid4().hex
        if stage == 1:
            tools = ObservedTools(Workspace(root))
            tools.definitions = []
            model = CheckedModel(prompt, tools, [])
            result = module.infer_once(model, prompt)
            model.finish(1, 0)
            model.require(result == model.last_response, 'return the actual inference response, not a fabricated answer')
            return ['one request with the supplied task; returned actual response']
        cases = [('one call', [['notes.txt']])]
        if stage == 3:
            cases = [('no tool', []), ('one call', [['notes.txt']]),
                     ('multiple calls', [['notes.txt', 'notes.txt']]),
                     ('multiple turns', [['notes.txt'], ['notes.txt']]),
                     ('error feedback', [['missing.txt']])]
        for name, batches in cases:
            tools = ObservedTools(Workspace(root))
            model = CheckedModel(prompt, tools, batches)
            if stage == 2:
                result, history = module.exchange(model, tools, prompt)
                model.finish(2, 1)
                model.require(result == model.last_response, 'return the response from the second inference')
                model.require(history == model.history[:-1], 'returned history must include the actual tool feedback')
            else:
                trace = Trace(root / (name.replace(' ', '-') + '.jsonl'))
                try:
                    result = module.run_loop(model, tools, prompt, trace, max_turns=6, max_calls=8)
                finally:
                    trace.close()
                model.finish(len(batches) + 1, sum(map(len, batches)))
                model.require(result.get('status') == 'completed', 'valid end_turn should stop as completed')
                model.require(result.get('messages') == model.history, 'returned conversation lost or fabricated messages')
                model.require(result.get('tool_calls') == len(tools.calls), 'tool-call count must reflect actual dispatch')
            passed.append(name + ': requested calls dispatched and actual results fed back')
        if stage == 3:
            tools = ObservedTools(Workspace(root))
            model = CheckedModel(prompt, tools, [['notes.txt'], ['notes.txt'], ['notes.txt']])
            trace = Trace(root / 'limit.jsonl')
            try:
                result = module.run_loop(model, tools, prompt, trace, max_turns=2, max_calls=8)
            finally:
                trace.close()
            model.finish(2, 2)
            model.require(result.get('status') == 'turn_limit', 'stop explicitly at the supplied two-turn limit')
            model.require(result.get('messages') == [*model.history, {'role':'user','content':tools.results[-1:]}],
                          'preserve the final tool result when the controller reaches its turn limit')
            passed.append('finite stop: two requests and two dispatches; no third inference')
    return passed
