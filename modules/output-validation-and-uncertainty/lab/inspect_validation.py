"""Inspect independent outcome checks and prepare a claim-review worksheet.

Original bounded teaching exercise, no inference. Sources: ../SOURCES.md.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'modules/tool-requests-and-feedback/lab'))
# Reuse the exact existing wire parser and feedback grader. Importing these
# standard-library modules does not start prepare.py, a server or an inference.
# Import this verifier first: bridge then prepends a generation-lab path that
# contains a different verify_model.py. No module is executed as a CLI here.
from verify_model import example_feedback_check
from bridge import decode_wire

PACKET = ROOT / 'modules/context-and-state/lab/fixtures/packet.json'


def read_json(path: Path) -> dict | list:
    """Read a supplied local fixture; no external retrieval."""
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data: object) -> None:
    """Create a new artifact; refuse overwrite."""
    with path.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def recorded_observation() -> tuple[dict, dict]:
    """Verify the retained source bytes before referencing authentic observations."""
    provenance = read_json(LAB / 'observation-source.json')
    path = ROOT / provenance['path']
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != provenance['sha256']:
        raise ValueError('retained observation changed; review source provenance before updating the manifest')
    return json.loads(data), provenance


def grade_case(case: dict, matching_feedback: bool) -> dict:
    """Recheck recorded raw answers/reads/stops, not the saved success label.

    Task grade follows the existing exact-answer/read/completed rule; feedback
    integration is separate. Neither establishes private reasoning or reliability.
    """
    report, events = case['report'], case['events']
    native = [e['response'] for e in events if e['event'] == 'local_response']
    decoded = []
    wire_valid = bool(native)
    for response in native:
        try:
            decoded.append(decode_wire(response['content'], 'inspection-only'))
        except (KeyError, ValueError, TypeError):
            wire_valid = False
            decoded.append(None)
    last = decoded[-1] if decoded else None
    answer = (last['content'][0]['text'] if last and last['stop_reason'] == 'end_turn' else None)
    read_observed = False
    for event in events:
        if event['event'] != 'tool':
            continue
        call, result = event['call'], event['result']
        try:
            value = json.loads(result['content'])
        except (KeyError, ValueError, TypeError):
            continue
        if (call['name'] == 'read_file' and call['input'] == {'path': 'status.txt'}
                and result.get('is_error') is False and isinstance(value, str)
                and value.strip() == report['expected_code']):
            read_observed = True
    stops = [e['status'] for e in events if e['event'] == 'stop']
    completed = bool(stops) and stops[-1] == 'completed'
    exact = answer == report['expected_code']
    return {'wire_format_valid': wire_valid, 'successful_read_observed': read_observed,
            'matching_feedback': matching_feedback, 'loop_completed': completed,
            'answer': answer, 'expected': report['expected_code'], 'exact_answer': exact,
            'task_passed': read_observed and exact and completed,
            'recorded_task_passed': report['task_passed'],
            'scope': 'Rechecks this recorded trace; not a new trial, semantic grader or reliability estimate.'}


def broken_feedback(record: dict) -> dict:
    """One explicitly synthetic mutation: change only the next canonical result ID."""
    changed = copy.deepcopy(record)
    events = changed['runs']['example_ordinary_2']['events']
    tool_index = next(i for i, event in enumerate(events) if event['event'] == 'tool')
    request = next(e['request'] for e in events[tool_index + 1:] if e['event'] == 'request')
    request['messages'][-1]['content'][0]['tool_use_id'] = 'synthetic-wrong-feedback-id'
    return changed


def inspect_outcomes(output: Path) -> dict:
    """Compare three authentic cases and one labelled derived copy; preserve source."""
    record, provenance = recorded_observation()
    feedback = example_feedback_check(record)['cases']
    rows = [{'case': name, 'origin': 'retained actual model observation',
             **grade_case(case, feedback[name])} for name, case in record['runs'].items()]
    changed = broken_feedback(record)
    name = 'example_ordinary_2'
    altered_case = changed['runs'][name]
    write_json(output / 'synthetic-broken-feedback.json', {
        'origin': 'Synthetic mutation of retained case 2; no new inference',
        'change': 'Only next canonical tool_result.tool_use_id changed; raw model output preserved.',
        'source': provenance, 'case': altered_case})
    rows.append({'case': 'synthetic-broken-feedback', 'origin': 'synthetic mutation, not a model observation',
                 **grade_case(altered_case, example_feedback_check(changed)['cases'][name])})
    result = {'source': provenance, 'cases': rows}
    write_json(output / 'report.json', result)
    return result


def check_references(claim: object, evidence_ids: set[str]) -> dict:
    """Check a narrow object shape and resolvable IDs, never semantic support."""
    valid = (isinstance(claim, dict) and set(claim) == {'claim_id', 'text', 'evidence_ids'}
             and isinstance(claim['claim_id'], str) and bool(claim['claim_id'])
             and isinstance(claim['text'], str) and bool(claim['text'])
             and isinstance(claim['evidence_ids'], list) and bool(claim['evidence_ids'])
             and all(isinstance(value, str) for value in claim['evidence_ids']))
    ids = claim['evidence_ids'] if valid else []
    missing = [value for value in ids if value not in evidence_ids]
    return {'object_shape_valid': valid, 'unresolved_ids': missing,
            'references_resolve': valid and not missing,
            'semantic_support': 'not graded; review evidence with the authored rubric'}


def inspect_claims(output: Path, claims_path: Path) -> dict:
    """Save structural checks and blank review prompts; never auto-approve claims."""
    packet = read_json(PACKET)
    claims = read_json(claims_path)
    if not isinstance(claims, list) or not 1 <= len(claims) <= 20:
        raise ValueError('claims fixture must be a list of 1–20 objects')
    known = {row['id'] for row in packet['records']}
    rows = [{'claim': claim, **check_references(claim, known)} for claim in claims]
    write_json(output / 'evidence.json', packet)
    write_json(output / 'report.json', {'origin': 'authored claims; structural checks only', 'claims': rows})
    notes = ['# Claim review', '', 'Fill before reading lab/rubric.json. No model or semantic grader ran.', '']
    for index, row in enumerate(rows, 1):
        notes.extend([f'## Item {index}', '', json.dumps(row['claim'], ensure_ascii=False), '',
                      f"Reference check: {row['references_resolve']}", '',
                      'Judgment:', 'Supporting/conflicting evidence and collection limits:',
                      'Revision or missing evidence needed:', ''])
    (output / 'claim-review.md').write_text('\n'.join(notes), encoding='utf-8')
    return {'claims': rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', choices=['outcomes', 'claims'])
    parser.add_argument('--output', type=Path, required=True, help='new dedicated output directory')
    parser.add_argument('--claims', type=Path, default=LAB / 'claims.json', help='local synthetic claims for claims lesson')
    args = parser.parse_args()
    try:
        args.output.mkdir(parents=True, exist_ok=False)
        if args.lesson == 'outcomes':
            result = inspect_outcomes(args.output)
            for row in result['cases']:
                print(f"{row['case']}: feedback={row['matching_feedback']} exact={row['exact_answer']} task={row['task_passed']}")
        else:
            result = inspect_claims(args.output, args.claims)
            print(f"{len(result['claims'])} claims structurally inspected; fill claim-review.md before opening the authored rubric.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Validation inspection failed: {exc}', file=sys.stderr)
        return 2
    print(f'Artifacts: {args.output.resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
