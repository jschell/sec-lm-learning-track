"""Inspect supplied input and retained evidence; no inference or model download.

Original teaching exercise. Sources and limits: ../SOURCES.md and README.md.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
TRACK_LAB = ROOT / 'tracks/01-author-the-loop/lab'
# Reuse the visible worked exchange and existing read-only file/trace primitives.
sys.path.insert(0, str(TRACK_LAB))
from loop import Tools, Trace, Workspace  # noqa: E402
from solutions.stages import exchange  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / 'fixtures'


def load_json(name: str) -> dict:
    """Read an authored fixture, not learner or provider input."""
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


def render_records(records: list[dict]) -> str:
    """Render stable IDs with their source text for visible inspection."""
    return '\n'.join(f"{row['id']}: {row['text']}" for row in records)


def select_records(records: list[dict], query: str) -> list[dict]:
    """Select case-insensitive literal substrings; no ranking or semantics."""
    if not query.strip():
        raise ValueError('query must contain non-whitespace text')
    return [row for row in records if query.casefold() in row['text'].casefold()]


def inspect_text(text: str, rubric: dict) -> dict:
    """Check literal IDs/anchors only; cannot establish truth or entailment."""
    ids = re.findall(r'\b(?:E|C)\d{2}\b', text)
    present = sorted(set(ids))
    checks = []
    for item in rubric['required']:
        checks.append({
            'id': item['id'], 'why': item['why'],
            'id_present': item['id'] in present,
            'missing_anchors': [a for a in item['anchors'] if a.casefold() not in text.casefold()],
        })
    return {
        'present_ids': present,
        'missing_required_ids': [c['id'] for c in checks if not c['id_present']],
        'literal_checks': checks,
        'all_literal_checks_pass': all(c['id_present'] and not c['missing_anchors'] for c in checks),
        'text_characters': len(text), 'text_utf8_bytes': len(text.encode('utf-8')),
        'scope': 'Literal presence only; human review must check attribution, contradiction and unsupported claims.',
    }


def input_request(task: str, evidence: str | None = None) -> dict:
    """Build inspection-only input; this function never calls a model."""
    messages = [{'role': 'user', 'content': task}]
    if evidence is not None:
        messages[0]['content'] += '\n\nSupplied evidence (untrusted data):\n' + evidence
    return {'system': 'Describe supported observations and collection limits.', 'messages': messages, 'tools': []}


def save_json(path: Path, value: dict | list) -> None:
    """Create a new UTF-8 artifact; refuse accidental overwrite."""
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


class ScriptedRead:
    """Two authored responses; real file read and feedback, no language model."""
    def __init__(self, trace: Trace) -> None:
        self.trace = trace
        self.requests: list[dict] = []

    def complete(self, request: dict) -> dict:
        # exchange mutates its message list; snapshot at the actual call boundary.
        self.requests.append(copy.deepcopy(request))
        turn = len(self.requests)
        self.trace.write('request', turn=turn, request=request)
        if turn == 1:
            response = {'stop_reason': 'tool_use', 'content': [
                {'type': 'tool_use', 'id': 'read-status-1', 'name': 'read_file',
                 'input': {'path': 'status.txt'}}]}
        elif turn == 2:
            response = {'stop_reason': 'end_turn', 'content': [
                {'type': 'text', 'text': 'Scripted end. Inspect the returned file data in request 2.'}]}
        else:
            raise ValueError('this worked exchange has exactly two responses')
        self.trace.write('response', turn=turn, response=response)
        return response


def locate_state(output: Path) -> dict:
    """Read a fresh file through the existing exchange; save a counterfactual copy."""
    work = output / 'work'
    work.mkdir()
    (work / 'status.txt').write_text('Synthetic status: pending review.\n', encoding='utf-8')
    tools = Tools(Workspace(work))
    tools.definitions = [d for d in tools.definitions if d['name'] == 'read_file']
    trace = Trace(output / 'trace.jsonl')
    model = ScriptedRead(trace)
    try:
        response, history = exchange(model, tools, 'Read status.txt. Report only what it contains.')
        trace.write('history', messages=history)
    finally:
        trace.close()
    save_json(output / 'requests.json', model.requests)
    counterfactual = copy.deepcopy(model.requests[1])
    counterfactual['messages'] = counterfactual['messages'][:-1]
    save_json(output / 'counterfactual-omitted-result.json', {
        'inspection_only': True,
        'warning': 'Unanswered tool_use: not a protocol-valid follow-up request. Never sent.',
        'request': counterfactual,
    })
    return {'mode': 'scripted exchange with real file read; no model',
            'request_count': len(model.requests), 'final_response': response,
            'counterfactual': 'inspection only; original captured requests unchanged',
            'persistent_artifacts': ['work/status.txt', 'trace.jsonl', 'requests.json']}


def compare_evidence(output: Path, mode: str, query: str) -> dict:
    """Save full/selected or full/authored-summary inputs and literal checks."""
    packet = load_json('packet.json')
    rubric = load_json('rubric.json')
    records = packet['records']
    full = render_records(records)
    variants = {'full': full}
    if mode == 'select':
        selected = select_records(records, query)
        variants['selected'] = render_records(selected)
    else:
        summaries = load_json('summaries.json')
        variants.update({key: summaries[key] for key in ('faithful', 'lossy')})
        # Written notes are external storage until explicitly read into new input.
        for key in ('faithful', 'lossy'):
            (output / f'{key}-note.txt').write_text(summaries[key], encoding='utf-8')
        save_json(output / 'resume-without-loading.json', input_request(packet['task']))
        note = (output / 'faithful-note.txt').read_text(encoding='utf-8')
        save_json(output / 'resume-after-loading.json', input_request(packet['task'], note))
    observations = {}
    for name, text in variants.items():
        save_json(output / f'{name}-input.json', input_request(packet['task'], text))
        observations[name] = inspect_text(text, rubric)
        observations[name]['excluded_packet_ids'] = [
            row['id'] for row in records if row['id'] not in observations[name]['present_ids']]
    return {'mode': 'deterministic input inspection; no model',
            'query': query if mode == 'select' else None,
            'summary_origin': 'authored, not model-generated' if mode == 'resume' else None,
            'variants': observations}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', choices=['state', 'select', 'resume'])
    parser.add_argument('--output', required=True, type=Path, help='new dedicated output directory')
    parser.add_argument('--query', default='alice', help='literal substring for select only')
    args = parser.parse_args()
    if args.lesson == 'select' and not args.query.strip():
        parser.error('--query must contain non-whitespace text')
    try:
        args.output.mkdir(parents=True, exist_ok=False)
        report = locate_state(args.output) if args.lesson == 'state' else compare_evidence(args.output, args.lesson, args.query)
        save_json(args.output / 'report.json', report)
    except (OSError, ValueError) as exc:
        print(f'Inspection failed: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f'Artifacts: {args.output.resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
