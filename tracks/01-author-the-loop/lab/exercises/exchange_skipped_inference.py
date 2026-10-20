"""Fix exercise: one tool exchange that answers without asking the model again.

Check with the command printed by `learn.py fix exchange-skipped-inference`.
"""
from loop import system_for_task


def exchange(model, tools, prompt: str, system: str | None = None) -> tuple[dict, list]:
    system = system or system_for_task("inspect")
    messages = [{'role': 'user', 'content': prompt}]
    first_request = {'system': system, 'messages': messages,
                     'tools': tools.definitions, 'max_tokens': 1024}
    first = model.complete(first_request)
    messages.append({'role': 'assistant', 'content': first['content']})
    results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
    messages.append({'role': 'user', 'content': results})
    second_request = {'system': system, 'messages': messages,
                      'tools': tools.definitions, 'max_tokens': 1024}
    # TODO: Fix the returned response; change only the two lines below.
    final = {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'The file was read.'}]}
    return final, messages
