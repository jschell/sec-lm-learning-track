"""Solution: one tool exchange whose feedback cannot be matched to its call.

One-change repair of the matching fix exercise; compare it with your own fix.
"""
from loop import system_for_task


def exchange(model, tools, prompt: str, system: str | None = None) -> tuple[dict, list]:
    system = system or system_for_task("inspect")
    messages = [{'role': 'user', 'content': prompt}]
    first_request = {'system': system, 'messages': messages,
                     'tools': tools.definitions, 'max_tokens': 1024}
    first = model.complete(first_request)
    # Fixed: the assistant message carrying the tool_use must precede its results.
    messages.append({'role': 'assistant', 'content': first['content']})
    results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
    messages.append({'role': 'user', 'content': results})
    second_request = {'system': system, 'messages': messages,
                      'tools': tools.definitions, 'max_tokens': 1024}
    return model.complete(second_request), messages
