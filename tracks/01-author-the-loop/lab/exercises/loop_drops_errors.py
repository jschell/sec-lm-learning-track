"""Fix exercise: a repeated loop that hides failed tool calls from the model.

Check with the command printed by `learn.py fix loop-drops-errors`.
"""
from loop import SYSTEM


def run_loop(model, tools, prompt: str, trace, max_turns: int = 12,
             max_calls: int = 24, max_tokens: int = 1024, system: str = SYSTEM) -> dict:
    messages = [{'role': 'user', 'content': prompt}]
    count = 0
    status = 'turn_limit'
    for turn in range(1, max_turns + 1):
        request = {'system': system, 'messages': messages,
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
            count += 1
            trace.write('tool', turn=turn, call=call, result=result)
            # TODO: Fix the feedback by changing only the next line.
            if not result.get('is_error'):
                results.append(result)
        messages.append({'role': 'user', 'content': results})
    trace.write('stop', status=status, tool_calls=count)
    return {'status': status, 'messages': messages, 'tool_calls': count}
