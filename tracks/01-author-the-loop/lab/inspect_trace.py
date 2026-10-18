"""Summarize JSONL data without executing it; full requests stay in the source trace."""
import json
from pathlib import Path
import sys


def excerpt(value: object) -> str:
    """Escape embedded newlines/control characters and bound a display excerpt."""
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 240 else text[:240] + '...'


def summary(row: dict) -> str:
    """Keep permission decisions, simulations and observed effects distinct."""
    event = row['event']
    extra = ''
    if event == 'tool':
        extra = f" {row['call']['id']} {row['call']['name']} is_error={row['result']['is_error']}"
        extra += ' result=' + excerpt(row['result']['content'])
    elif event == 'response':
        text = ' '.join(b.get('text', '') for b in row['response'].get('content', []) if b.get('type') == 'text')
        if text:
            extra = ' text=' + excerpt(text)
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
    if len(sys.argv) != 2:
        raise SystemExit('Usage: inspect_trace.py PATH/trace.jsonl')
    for line in Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
        print(summary(json.loads(line)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
