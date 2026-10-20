"""Part 0: the whole agent loop, minimal, in Geoffrey Huntley's order. Original Python.

The structure follows Huntley's workshop (an outer loop over user turns, an inner loop
that runs requested tools until the model stops asking); see ../../SOURCES.md. No
upstream code is copied.

This loop is deliberately guard-free, like Huntley's: no stop-reason check, no limits, no
duplicate-ID check. Run it only through `learn.py part0`, which supplies scripted
responses and read-only tools. Later sections add the checks it lacks.
"""
from collections.abc import Callable

from loop import Workspace, schema

SYSTEM = 'You can use the listed read-only tools. Answer from what they return.'


# --- Tools: a definition the model sees, and a function the controller runs ---------

def read_file(workspace: Workspace, args: dict) -> str:
    return workspace.read(args['path'])


def list_files(workspace: Workspace, args: dict) -> str:
    return '\n'.join(sorted(p.name for p in workspace.path(args['path']).iterdir()))


DEFINITIONS = {
    'read_file': schema('read_file', 'Read a text file in the workspace.', ('path',)),
    'list_files': schema('list_files', "List the files in a workspace directory; use '.' for the top.", ('path',)),
}
FUNCTIONS: dict[str, Callable[[Workspace, dict], str]] = {'read_file': read_file, 'list_files': list_files}


class ReadOnlyTools:
    """The definitions sent to the model, and dispatch: look the tool up by name, then run it."""
    def __init__(self, workspace: Workspace, names: list[str]) -> None:
        self.workspace = workspace
        self.definitions = [DEFINITIONS[name] for name in names]
        self.functions = {name: FUNCTIONS[name] for name in names}

    def dispatch(self, call: dict) -> dict:
        function = self.functions.get(call['name'])
        try:
            if function is None:
                raise ValueError(f"tool {call['name']!r} not found")
            content, is_error = function(self.workspace, call['input']), False
        except (ValueError, KeyError, TypeError, OSError, UnicodeError) as exc:
            content, is_error = str(exc), True  # a failure is still a result the model sees
        return {'type': 'tool_result', 'tool_use_id': call['id'], 'content': content, 'is_error': is_error}


# --- The loop ----------------------------------------------------------------------

def request(conversation: list, tools) -> dict:
    """Everything the model receives: instructions, the whole conversation, the tools."""
    return {'system': SYSTEM, 'messages': conversation, 'tools': tools.definitions, 'max_tokens': 1024}


def run_conversation(model, tools, user_turns: list[str], show: Callable[[str, str], None]) -> list:
    conversation = []
    for user_text in user_turns:                                   # outer loop: one user turn
        show('You', user_text)
        conversation.append({'role': 'user', 'content': user_text})
        message = model.complete(request(conversation, tools))
        conversation.append({'role': 'assistant', 'content': message['content']})
        while True:                                                # inner loop: until no tool is requested
            results = []
            for block in message['content']:
                if block['type'] == 'text':
                    show('Model', block['text'])
                elif block['type'] == 'tool_use':
                    show('tool', f"{block['name']}({block['input']})")
                    result = tools.dispatch(block)
                    show('error' if result['is_error'] else 'result', result['content'])
                    results.append(result)
            if not results:
                break
            conversation.append({'role': 'user', 'content': results})  # every result, one message
            message = model.complete(request(conversation, tools))
            conversation.append({'role': 'assistant', 'content': message['content']})
    return conversation
