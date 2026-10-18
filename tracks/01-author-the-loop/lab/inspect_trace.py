"""Summarize JSONL data without executing it; full requests stay in the source trace."""
import argparse
import json
from pathlib import Path


def excerpt(value: object) -> str:
    """Escape embedded newlines/control characters and bound a display excerpt."""
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 240 else text[:240] + '...'


def message_snapshot(messages: list, label: str) -> str:
    """Show bounded cumulative input/history, never infer a fresh dispatch."""
    blocks = []
    for index, message in enumerate(messages, start=1):
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
    extra = f" {label}(cumulative; messages={len(messages)}; tool_blocks={len(blocks)}; omitted={len(blocks)-len(shown)})"
    for kind, index, value in shown:
        extra += f" {kind}[message={index}]=" + excerpt(value)
    return extra


def summary(row: dict) -> str:
    """Keep permission decisions, simulations and observed effects distinct."""
    event = row['event']
    extra = ''
    if event == 'request':
        extra = message_snapshot(row['request'].get('messages', []), 'input_snapshot')
    elif event == 'history':
        extra = message_snapshot(row.get('messages', []), 'history_snapshot')
    elif event == 'tool':
        extra = f" {row['call']['id']} {row['call']['name']} is_error={row['result']['is_error']}"
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
        extra = ' ' + row['status']
    elif event == 'error':
        extra = ' ' + row['error_type'] + ': ' + excerpt(row['message'])
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
    return f"{row['seq']:02d} {event}{extra}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, help='Saved JSONL trace; cumulative snapshots are not fresh execution')
    args = parser.parse_args()
    for line in args.path.read_text(encoding='utf-8').splitlines():
        print(summary(json.loads(line)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
