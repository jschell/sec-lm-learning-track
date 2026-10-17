"""Small original worked stages. Protocol sources: ../SOURCES.md.

Inspect these functions before the supporting production-style reference guards.
Use read-only tools here; use loop.run_loop for the contained command exercise.
"""
from loop import SYSTEM


def infer_once(model, prompt: str) -> dict:
    request = {'system': SYSTEM, 'messages': [{'role': 'user', 'content': prompt}],
               'tools': [], 'max_tokens': 1024}
    return model.complete(request)


def exchange(model, tools, prompt: str) -> tuple[dict, list]:
    messages = [{'role': 'user', 'content': prompt}]
    first_request = {'system': SYSTEM, 'messages': messages,
                     'tools': tools.definitions, 'max_tokens': 1024}
    first = model.complete(first_request)
    messages.append({'role': 'assistant', 'content': first['content']})
    results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
    messages.append({'role': 'user', 'content': results})
    # Build the next request explicitly: this is the feedback transition.
    second_request = {'system': SYSTEM, 'messages': messages,
                      'tools': tools.definitions, 'max_tokens': 1024}
    return model.complete(second_request), messages


def run_loop(model, tools, prompt: str, trace, max_turns: int = 12,
             max_calls: int = 24, max_tokens: int = 1024) -> dict:
    messages = [{'role': 'user', 'content': prompt}]
    count = 0
    status = 'turn_limit'
    for turn in range(1, max_turns + 1):
        request = {'system': SYSTEM, 'messages': messages,
                   'tools': tools.definitions, 'max_tokens': max_tokens}
        trace.write('request', turn=turn, request=request)
        response = model.complete(request)
        trace.write('response', turn=turn, response=response)
        if response['stop_reason'] not in {'tool_use', 'end_turn'}:
            status = 'model_stop:' + response['stop_reason']
            break
        messages.append({'role': 'assistant', 'content': response['content']})
        calls = [b for b in response['content'] if b['type'] == 'tool_use']
        if not calls:
            status = 'completed'
            break
        if count + len(calls) > max_calls:
            status = 'tool_limit'
            break
        results = []
        for call in calls:
            result = tools.dispatch(call)
            trace.write('tool', turn=turn, call=call, result=result)
            results.append(result)
            count += 1
        messages.append({'role': 'user', 'content': results})
    trace.write('stop', status=status, tool_calls=count)
    return {'status': status, 'messages': messages, 'tool_calls': count}
