"""Small behavioral checks, not a certificate or adversarial anti-cheating system.

Original project tests inspired by explicit implementation contracts such as
Stanford CS336's adapters; see ../SOURCES.md. No upstream test code is copied.
"""
import copy
from pathlib import Path
import tempfile
from contextlib import nullcontext
import uuid

from loop import Tools, Trace, Workspace

HISTORY_RULE = 'next inference must contain the original task, assistant calls, and matching actual tool results'


def _tool_blocks(message: object, block_type: str) -> list[dict]:
    content = message.get('content') if isinstance(message, dict) else None
    if not isinstance(content, list):
        return []
    return [b for b in content if isinstance(b, dict) and b.get('type') == block_type]


def _diagnosis(observed: str, expected: str, why: str, look: str) -> str:
    return (f'{observed}\n  Expected: {expected}\n  Why it matters: {why}\n'
            f'  Look at: {look}\n  Rule: {HISTORY_RULE}.')


def describe_history_mismatch(observed: object, expected: list[dict], request_number: int) -> str:
    """Name a common wrong feedback history from observed messages and actual dispatch.

    Teaching messages adapt futurecoder's targeted-message pattern; see ../SOURCES.md.
    Returns the general rule when no specific pattern applies.
    """
    where = f'request {request_number}'
    if not isinstance(observed, list) or not observed or observed[0] != expected[0]:
        return _diagnosis(f'{where} does not start with the original user task.',
                          'the first message is the task exactly as supplied.',
                          'later requests extend one conversation; the task must stay in it.',
                          'where your function creates the message list.')
    calls = _tool_blocks(expected[-2], 'tool_use') if len(expected) >= 2 else []
    actual = _tool_blocks(expected[-1], 'tool_result')
    if not calls or not actual:
        return HISTORY_RULE
    ids = [c['id'] for c in calls]
    shown = ', '.join(ids)
    call_at = next((i for i, m in enumerate(observed) if isinstance(m, dict) and m.get('role') == 'assistant'
                    and {b.get('id') for b in _tool_blocks(m, 'tool_use')} >= set(ids)), None)
    result_at = next((i for i, m in enumerate(observed) if isinstance(m, dict) and m.get('role') == 'user'
                      and _tool_blocks(m, 'tool_result')), None)
    no_result = _diagnosis(f'{where} contains the assistant call(s) {shown} but no tool_result after them.',
                           'a following user message with one tool_result per call.',
                           'the model never receives what the tool returned.',
                           'the line that appends dispatch results to messages.')
    if call_at is None:
        if result_at is None:
            return HISTORY_RULE
        return _diagnosis(f'{where} has a tool_result but not the assistant message that requested {shown}.',
                          "the response's assistant content appended before the results message.",
                          'each result answers a call in the preceding assistant message; without it the '
                          'result has nothing to match.',
                          "where your function appends the response's content.")
    if result_at is not None and result_at < call_at:
        return _diagnosis(f'{where} places the tool_result before the assistant call {shown}.',
                          'assistant call first, then the user message carrying its results.',
                          'a result answers a call that has already been made.',
                          'the order of the two append operations.')
    following = observed[call_at + 1] if call_at + 1 < len(observed) else None
    if not (isinstance(following, dict) and following.get('role') == 'user'
            and isinstance(following.get('content'), list)):
        return no_result
    supplied = _tool_blocks(following, 'tool_result')
    by_id = {b.get('tool_use_id'): b for b in supplied}
    unknown = [b.get('tool_use_id') for b in supplied if b.get('tool_use_id') not in ids]
    if unknown:
        return _diagnosis(f'{where} has tool_use_id {unknown[0]!r}, which matches no requested call ({shown}).',
                          'each tool_use_id equal to the id of the call it answers.',
                          'IDs, not function names, associate results with calls.',
                          'how the result block is built or which call it is paired with.')
    missing = [r for r in actual if r['tool_use_id'] not in by_id]
    if missing:
        if any(r.get('is_error') for r in missing):
            return _diagnosis(f'{where} omits the error result for {missing[0]["tool_use_id"]}.',
                              'every result, including is_error=true results, supplied to the next request.',
                              'an error is feedback too; without it the model cannot see that the call failed.',
                              'any filtering of results before they are appended.')
        return _diagnosis(f'{where} has no result for call {missing[0]["tool_use_id"]}.',
                          'one tool_result per requested call.',
                          'an unanswered call leaves the model without that observation.',
                          'the loop over requested calls.')
    if any(by_id[r['tool_use_id']] != r for r in actual):
        return _diagnosis(f'{where} has a result for {shown} that differs from what dispatch actually returned.',
                          'the exact result object returned by tools.dispatch.',
                          'feedback must report the real operation, not a substitute.',
                          'where the result is created or changed before appending.')
    return HISTORY_RULE


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
        self.expected_system: str | None = None

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
        if self.expected_system is not None:
            self.require(request.get('system') == self.expected_system,
                         'preserve the system policy supplied by the caller')
        if self.pending:
            self.require(self.tools.calls == self.expected_calls,
                         'dispatch every requested call exactly once before the next inference')
            self.history.append({'role': 'user', 'content': copy.deepcopy(self.tools.results[-len(self.pending):])})
            self.pending = []
        if request.get('messages') != self.history:
            self.require(False, describe_history_mismatch(request.get('messages'), self.history, index + 1))
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
        missing_inference = ''
        if self.tools.calls and len(self.requests) < expected_requests:
            missing_inference = ('\n  Why it matters: a final answer that did not come from an inference after the '
                                 'results cannot reflect them.\n  Look at: whether your function sends another '
                                 'request with the updated messages and returns that response.')
        self.require(len(self.requests) == expected_requests,
                     f'expected {expected_requests} inference request(s), observed {len(self.requests)}'
                     + missing_inference)
        self.require(len(self.tools.calls) == expected_calls,
                     f'expected {expected_calls} dispatched call(s), observed {len(self.tools.calls)}')
        self.require(self.tools.calls == self.expected_calls,
                     'executed calls do not match the model-requested IDs/arguments')


class GuardModel:
    """Script terminal hazards, with a final response so wrong loops can stop."""
    def __init__(self, responses: list[dict]) -> None:
        self.responses = responses
        self.requests: list[dict] = []

    def complete(self, request: dict) -> dict:
        self.requests.append(copy.deepcopy(request))
        index = len(self.requests) - 1
        assert index < len(self.responses), 'unexpected inference after a guard should have stopped'
        return copy.deepcopy(self.responses[index])


def check_guards(module, root: Path, prompt: str) -> list[str]:
    """Reject unauthorized dispatch as well as incorrect stopping labels."""
    marker = uuid.uuid4().hex
    def call(index: int) -> dict:
        return {'type':'tool_use', 'id':f'{marker}-{index}', 'name':'read_file',
                'input':{'path':'notes.txt'}}
    def response(reason: str, calls: list[dict]) -> dict:
        return {'stop_reason':reason, 'content':calls}
    final = response('end_turn', [])
    first = call(0)
    cases = [
        ('truncated response', [response('max_tokens', [first]), final], 8, [], 'model_stop:max_tokens', 1),
        ('batch call limit', [response('tool_use', [first,call(1)]), final], 1, [], 'tool_limit', 1),
        ('cumulative call limit', [response('tool_use', [first]),
             response('tool_use', [call(1),call(2)]), final], 2, [first], 'tool_limit', 2),
        ('inconsistent stop reason', [response('end_turn', [first]), final], 8, [], 'error', 1),
    ]
    passed = []
    for name, responses, budget, expected, status, requests in cases:
        tools = ObservedTools(Workspace(root))
        model = GuardModel(responses)
        trace = Trace(root / (name.replace(' ', '-') + '.jsonl'))
        try:
            result = module.run_loop(model, tools, prompt, trace, max_turns=4, max_calls=budget)
        finally:
            trace.close()
        assert tools.calls == expected, name + ': unauthorized dispatch occurred before stop'
        assert len(model.requests) == requests, name + ': inferred again after required stop'
        assert result.get('status') == status, name + ': wrong terminal status'
        assert result.get('tool_calls') == len(expected), name + ': incorrect dispatch count'
        passed.append(name + ': stopped before unauthorized dispatch')
    return passed


def check_stage(module, stage: int, guards: bool = False, output: Path | None = None) -> list[str]:
    """Check actual learner behavior using changing IDs and synthetic file contents.

    Raises:
        AssertionError: A required request, dispatch, feedback or stop was missing.
    """
    passed = []
    with (nullcontext(str(output)) if output is not None else tempfile.TemporaryDirectory(prefix='authoring-check-')) as temp:
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
                model.require(history in (model.history[:-1], model.history),
                              'history must preserve the supplied task, actual call and matching result; '
                              'only the actual final assistant response may be additionally present')
            else:
                trace = Trace(root / (name.replace(' ', '-') + '.jsonl'))
                model.expected_system = 'Synthetic inspection policy ' + uuid.uuid4().hex
                try:
                    result = module.run_loop(model, tools, prompt, trace, max_turns=6, max_calls=8,
                                             system=model.expected_system)
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
            model.require(result.get('status') == 'turn_limit', "expected status='turn_limit' at max_turns=2; observed " + repr(result.get('status')))
            model.require(result.get('messages') == [*model.history, {'role':'user','content':tools.results[-1:]}],
                          'preserve the final tool result when the controller reaches its turn limit')
            passed.append('finite stop: two requests and two dispatches; no third inference')
            if guards:
                passed.extend(check_guards(module, root, prompt))
    return passed
