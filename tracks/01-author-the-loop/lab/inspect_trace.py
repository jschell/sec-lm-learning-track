"""Summarize JSONL data without executing it; full requests stay in the source trace."""
import argparse
import json
import re
import sys
from loop import safe_diagnostic
from pathlib import Path


def excerpt(value: object) -> str:
    """Escape embedded newlines/control characters and bound a display excerpt."""
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 240 else text[:240] + '...'


def label(value: object) -> str:
    """Keep normal event labels readable while escaping untrusted controls."""
    return value if isinstance(value, str) and len(value) <= 240 and re.fullmatch(r'[A-Za-z0-9_.:-]+', value) else excerpt(value)


def message_snapshot(messages: list, label: str, offset: int = 0, cumulative: bool = True) -> str:
    """Show bounded cumulative input/history, never infer a fresh dispatch."""
    blocks = []
    for index, message in enumerate(messages, start=offset + 1):
        content = message.get('content', [])
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get('type') == 'tool_use':
                blocks.append(('call', index, {'id': block.get('id'), 'name': block.get('name'),
                                               'input': block.get('input')}))
            elif block.get('type') == 'tool_result':
                blocks.append(('result', index, {'tool_use_id': block.get('tool_use_id'),
                                                 'is_error': block.get('is_error'),
                                                 'content': block.get('content')}))
    shown = blocks[-8:]
    kind = "cumulative" if cumulative else "new input; not dispatch"
    extra = f" {label}({kind}; messages={len(messages)}; tool_blocks={len(blocks)}; omitted={len(blocks)-len(shown)})"
    for kind, index, value in shown:
        extra += f" {kind}[message={index}]=" + excerpt(value)
    return extra


def summary(row: dict, previous: list | None = None, cumulative: bool = True, limits: dict | None = None) -> str:
    """Keep permission decisions, simulations and observed effects distinct."""
    event = row['event']
    extra = ''
    if event == 'request':
        messages = row['request'].get('messages', [])
        if cumulative:
            extra = message_snapshot(messages, 'input_snapshot')
        elif previous is None or messages[:len(previous)] == previous:
            offset = len(previous) if previous is not None else 0
            extra = message_snapshot(messages[offset:], 'input_added', offset, cumulative=False)
        else:
            extra = ' input_reset(history changed; not an append)'
            extra += message_snapshot(messages, 'input_snapshot')
    elif event == 'history':
        extra = (message_snapshot(row.get('messages', []), 'history_snapshot') if cumulative
                 else ' history retained; use --cumulative or raw JSONL for the snapshot')
    elif event == 'tool':
        extra = f" {label(row['call']['id'])} {label(row['call']['name'])} is_error={row['result']['is_error']}"
        extra += ' result=' + excerpt(row['result']['content'])
    elif event == 'response':
        calls = [b for b in row['response'].get('content', []) if b.get('type') == 'tool_use']
        for call in calls[:8]:
            extra += ' proposed_call=' + excerpt({key: call.get(key) for key in ('id', 'name', 'input')})
        if len(calls) > 8:
            extra += f' omitted_proposals={len(calls)-8}'
        text = ' '.join(b.get('text', '') for b in row['response'].get('content', []) if b.get('type') == 'text')
        if text:
            extra += ' text=' + excerpt(text)
    elif event == 'stop':
        extra = ' ' + label(row['status'])
        extra += ' limits=' + excerpt(limits or {})
        extra += ' accounting=' + excerpt({key: row.get(key) for key in
            ('tool_calls', 'completed_tool_calls', 'dispatch_attempts', 'dispatch_uncertain')})
    elif event == 'error':
        extra = ' ' + label(row['error_type']) + ': ' + excerpt(row['message'])
    elif event == 'comparison':
        extra = ' recording_only=' + excerpt(row.get('observation'))
    elif event == 'proposal':
        proposal = row.get('proposal', {})
        extra = ' proposed=' + excerpt({'label': proposal.get('label'), 'call': proposal.get('call'),
                                        'origin': row.get('origin')})
    elif event == 'decision':
        extra = ' permission=' + excerpt({'decision': row.get('decision'), 'call': row.get('call'),
                                          'reason': row.get('reason')})
    elif event == 'recording_only_decision':
        extra = ' simulation=' + excerpt({'label': row.get('label'), 'decision': row.get('decision'),
                                          'executed': row.get('executed'), 'scope': row.get('scope')})
    elif event == 'effect':
        extra = ' observed_effect=' + excerpt({key: row[key] for key in
            ('operation', 'path', 'characters_returned') if key in row})
    return f"{row['seq']:02d} {label(event)}{extra}"


def main() -> int:
    parser = argparse.ArgumentParser(prog='learn.py trace', description=__doc__)
    parser.add_argument('path', type=Path, help='Run directory or saved JSONL trace')
    parser.add_argument('--cumulative', action='store_true', help='Show bounded cumulative input/history instead of newly added input')
    args = parser.parse_args()
    path = args.path / 'trace.jsonl' if args.path.is_dir() else args.path
    rows = []
    errors = False
    previous = None
    limits = {}
    last_sequence = 0
    try:
        with path.open(encoding='utf-8') as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if (not isinstance(row, dict) or not isinstance(row.get('seq'), int)
                            or isinstance(row.get('seq'), bool) or row['seq'] <= last_sequence
                            or not isinstance(row.get('event'), str)):
                        raise ValueError('expected increasing integer seq and string event')
                    if row['event'] == 'start':
                        limits.update({key: row[key] for key in ('max_calls', 'max_turns') if key in row})
                    print(summary(row, previous, args.cumulative, limits))
                    if row['event'] == 'request':
                        previous = row['request'].get('messages', [])
                    rows.append(row)
                    last_sequence = row['seq']
                except (ValueError, KeyError, TypeError, AttributeError) as exc:
                    errors = True
                    print(f'{path}:{line_number}: invalid/incomplete record: {type(exc).__name__}: {excerpt(safe_diagnostic(exc))}; inspect raw JSONL', file=sys.stderr)
    except (OSError, UnicodeError) as exc:
        print(f'{path}: cannot read trace ({type(exc).__name__}); supply a run directory or trace file', file=sys.stderr)
        return 2
    if not rows:
        print(f'{path}: empty trace; no completion evidence', file=sys.stderr)
        return 2
    if errors:
        print('INCOMPLETE/INVALID TRACE: completion cannot be established.')
        return 2
    terminal = rows[-1]['event'] == 'stop'
    stage = next((row.get('stage') for row in rows if row['event'] == 'start' and 'stage' in row), None)
    responses = [row for row in rows if row['event'] == 'response']
    short_complete = (stage in (1, 2) and len(responses) == stage
                      and sum(row['event'] == 'request' for row in rows) == stage
                      and not any(row['event'] == 'error' for row in rows)
                      and responses[-1]['response'].get('stop_reason') == 'end_turn'
                      and rows[-1]['event'] == ('response' if stage == 1 else 'history'))
    if terminal or short_complete:
        print('Trace terminal record present.' if terminal else 'Short-stage response/history complete; no stop event required.')
        return 0
    if any(row['event'] in ('start', 'request', 'response') for row in rows):
        print('INCOMPLETE TRACE: no terminal stop or complete short-stage response/history.')
        return 1
    print('Completion not established: event log has no controller lifecycle records.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
