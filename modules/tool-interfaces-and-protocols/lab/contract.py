"""Original read-only teaching contract shared by direct and MCP adapters.

No model generates these proposals. Concept sources: ../SOURCES.md.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
DEFINITION = {
    'name': 'lookup_event',
    'description': 'Look up one synthetic event by ID. Returns found/not_found; E500 simulates a backend fault.',
    'inputSchema': {'type': 'object', 'properties': {'event_id': {'type': 'string', 'pattern': '^E[0-9]{3}$'}},
                    'required': ['event_id'], 'additionalProperties': False},
}


def load_calls() -> list[dict]:
    """Load six authored proposals; this is not model selection."""
    return json.loads((HERE / 'calls.json').read_text(encoding='utf-8'))


def write_json(path: Path, data: object) -> None:
    """Create an artifact; fail if it already exists."""
    with path.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


class BackendUnavailable(Exception):
    """The deliberately seeded E500 fixture fault."""


class EventLookup:
    """Same lookup implementation in both processes; audit actual entry, even on error."""
    def __init__(self, audit: Path) -> None:
        self.events = json.loads((HERE / 'events.json').read_text(encoding='utf-8'))
        self.audit = audit
        self.execution_count = 0
        # Create immediately: an empty audit is meaningful if no call executed.
        self.audit.open('x', encoding='utf-8').close()

    def lookup_event(self, event_id: str) -> dict:
        """Return a fixture result; raise BackendUnavailable for the seeded fault."""
        self.execution_count += 1
        with self.audit.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps({'execution': self.execution_count, 'event_id': event_id}) + '\n')
        if event_id == 'E500':
            raise BackendUnavailable('synthetic backend unavailable')
        if event_id not in self.events:
            return {'status': 'not_found', 'event_id': event_id}
        return {'status': 'found', 'event': self.events[event_id]}


def dispatch(lookup: EventLookup, name: str, arguments: object) -> dict:
    """Enforce this small schema explicitly; invalid proposals never enter lookup_event.

    This validator implements only the displayed one-argument teaching contract,
    not a general JSON Schema engine. Unexpected defects propagate to the runner.
    """
    if name != 'lookup_event':
        return {'status': 'unknown_tool', 'executed': False, 'error': 'unknown tool name'}
    if (not isinstance(arguments, dict) or set(arguments) != {'event_id'}
            or not isinstance(arguments['event_id'], str)
            or re.fullmatch(r'E[0-9]{3}', arguments['event_id']) is None):
        return {'status': 'invalid_arguments', 'executed': False,
                'error': 'require exactly event_id: string matching E followed by three digits'}
    accepted = {'event_id': arguments['event_id']}
    try:
        data = lookup.lookup_event(**accepted)
    except BackendUnavailable as exc:
        return {'status': 'execution_error', 'executed': True, 'accepted_arguments': accepted, 'error': str(exc)}
    return {'status': data['status'], 'executed': True, 'accepted_arguments': accepted, 'data': data}


def feedback_example(proposal: dict, outcome: dict) -> dict:
    """Show a possible model-facing adapter, never sent to inference.

    The proposal ID is distinct from an MCP JSON-RPC request ID.
    """
    return {'inspection_only': True, 'assistant': {'role': 'assistant', 'content': [
        {'type': 'tool_use', 'id': proposal['id'], 'name': proposal['name'], 'input': proposal['arguments']}]},
        'feedback': {'role': 'user', 'content': [
            {'type': 'tool_result', 'tool_use_id': proposal['id'],
             'is_error': outcome['status'] in {'invalid_arguments', 'unknown_tool', 'execution_error'},
             'content': json.dumps(outcome)}]}}
