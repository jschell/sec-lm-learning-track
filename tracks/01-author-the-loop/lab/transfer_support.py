"""Visible registration/dispatch for the optional count_lines transfer task."""
from collections.abc import Callable

from loop import Tools, Workspace, schema


class CountLinesTools(Tools):
    """Read-only tools; inject the learner's actual count implementation."""
    def __init__(self, workspace: Workspace, count: Callable[[Workspace, str], int]) -> None:
        super().__init__(workspace)
        self.definitions = [schema('count_lines',
            'Count text lines in a UTF-8 workspace file using Python splitlines semantics. '
            'The operation is read-only; blank lines count and an empty file has zero lines.', ('path',))]
        self.count = count
        self.observed: list[dict] = []

    def dispatch(self, call: dict) -> dict:
        if call.get('name') != 'count_lines':
            return self.result(call, {'error':'unknown or disabled tool'}, error=True)
        args = call.get('input')
        if not isinstance(args, dict) or set(args) != {'path'} or not isinstance(args['path'], str):
            return self.result(call, {'error':'exactly one string path is required'}, error=True)
        try:
            lines = self.count(self.workspace, args['path'])
            if type(lines) is not int or lines < 0:
                raise ValueError('count_lines must return a nonnegative integer')
            value = {'path':args['path'], 'lines':lines}
            self.observed.append(value)
            return self.result(call, value)
        except (ValueError, OSError, UnicodeError) as exc:
            return self.result(call, {'error':str(exc)}, error=True)
