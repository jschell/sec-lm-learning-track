"""Original worked answers for lessons 1 and 2. See ../SOURCES.md."""
from loop import SYSTEM


def infer_once(model, prompt):
    return model.complete({'system': SYSTEM, 'messages': [{'role': 'user', 'content': prompt}],
                           'tools': [], 'max_tokens': 1024})


def exchange(model, tools, prompt):
    messages = [{'role': 'user', 'content': prompt}]
    request = {'system': SYSTEM, 'messages': messages,
               'tools': tools.definitions, 'max_tokens': 1024}
    first = model.complete(request)
    messages.append({'role': 'assistant', 'content': first['content']})
    results = [tools.dispatch(b) for b in first['content'] if b['type'] == 'tool_use']
    messages.append({'role': 'user', 'content': results})
    return model.complete(request), messages
