"""Small original worked stages. Protocol sources: ../SOURCES.md.

Inspect these functions before the supporting production-style reference guards.
Use read-only tools here; use loop.run_loop for the contained command exercise.
"""
from loop import SYSTEM, safe_diagnostic, system_for_task


def infer_once(model, prompt: str, system: str | None = None) -> dict:
    system = system or system_for_task("inference")
    request = {'system': system, 'messages': [{'role': 'user', 'content': prompt}],
               'tools': [], 'max_tokens': 1024}
    return model.complete(request)


def exchange(model, tools, prompt: str, system: str | None = None) -> tuple[dict, list]:
    system = system or system_for_task("inspect")
    messages = [{'role': 'user', 'content': prompt}]
    first_request = {'system': system, 'messages': messages,
                     'tools': tools.definitions, 'max_tokens': 1024}
    first = model.complete(first_request)
    messages.append({'role': 'assistant', 'content': first['content']})
    results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
    messages.append({'role': 'user', 'content': results})
    # Build the next request explicitly: this is the feedback transition.
    second_request = {'system': system, 'messages': messages,
                      'tools': tools.definitions, 'max_tokens': 1024}
    return model.complete(second_request), messages


def run_loop(model, tools, prompt: str, trace, max_turns: int = 12,
             max_calls: int = 24, max_tokens: int = 1024, system: str = SYSTEM) -> dict:
    messages = [{'role': 'user', 'content': prompt}]
    count = 0
    attempts = 0
    dispatch_in_progress = False
    status = 'turn_limit'
    try:
        for turn in range(1, max_turns + 1):
            request = {'system': system, 'messages': messages,
                       'tools': tools.definitions, 'max_tokens': max_tokens}
            trace.write('request', turn=turn, request=request)
            response = model.complete(request)
            trace.write('response', turn=turn, response=response)
            if (not isinstance(response, dict) or not isinstance(response.get('content'), list)
                    or not isinstance(response.get('stop_reason'), str)
                    or any(not isinstance(b, dict) or b.get('type') not in {'text', 'tool_use'}
                           for b in response['content'])):
                raise ValueError('response needs stop_reason and a list of text/tool_use blocks')
            if response['stop_reason'] not in {'tool_use', 'end_turn'}:
                status = 'model_stop:' + response['stop_reason']
                break
            messages.append({'role': 'assistant', 'content': response['content']})
            calls = [b for b in response['content'] if b['type'] == 'tool_use']
            if bool(calls) != (response['stop_reason'] == 'tool_use'):
                raise ValueError('stop_reason and tool calls disagree')
            if not calls:
                status = 'completed'
                break
            if count + len(calls) > max_calls:
                status = 'tool_limit'
                break
            results = []
            for call in calls:
                attempts += 1
                dispatch_in_progress = True
                result = tools.dispatch(call)
                count += 1
                dispatch_in_progress = False
                trace.write('tool', turn=turn, call=call, result=result)
                results.append(result)
            messages.append({'role': 'user', 'content': results})
    except Exception as exc:
        # Teaching-loop boundary: preserve error evidence and uncertain effects.
        status = 'error'
        trace.write('error', error_type=type(exc).__name__, message=safe_diagnostic(exc, model),
                    dispatch_uncertain=dispatch_in_progress)
    accounting = {'tool_calls': None if dispatch_in_progress else count,
                  'completed_tool_calls': count, 'dispatch_attempts': attempts,
                  'dispatch_uncertain': dispatch_in_progress}
    trace.write('stop', status=status, **accounting)
    return {'status': status, 'messages': messages, **accounting}
