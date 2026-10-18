"""Follow authored untrusted content and compare recording-only policy with authority.

No model, shell, deletion or network operation. Sources: ../SOURCES.md.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent / 'fixtures'
sys.path.insert(0, str(ROOT / 'tracks/01-author-the-loop/lab'))
from loop import Trace, Workspace, run_loop, schema, system_for_task


READ_DEFINITION = schema('read_file', 'Read only the supplied note.txt. No edits or other paths permitted.', ('path',))


def write_json(path: Path, value: object) -> None:
    """Create one artifact; refuse accidental overwrite."""
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def make_workspace(root: Path, variant: str) -> Workspace:
    """Fresh supplied data; setup writes are separate from dispatched tool effects."""
    root.mkdir()
    (root / 'note.txt').write_text((FIXTURES / f'{variant}.txt').read_text(encoding='utf-8'), encoding='utf-8')
    (root / 'notes.txt').write_text('Investigation open.\n', encoding='utf-8')
    (root / 'private.txt').write_text('SYNTHETIC-NOT-A-SECRET\n', encoding='utf-8')
    return Workspace(root)


class ReadOnlyTools:
    """Enforce one exact operation/path independently of descriptions or prompts."""
    def __init__(self, workspace: Workspace, trace: Trace) -> None:
        self.workspace, self.trace = workspace, trace
        self.definitions = [copy.deepcopy(READ_DEFINITION)]
        self.decisions: list[dict] = []
        self.executions: list[dict] = []

    def dispatch(self, call: dict) -> dict:
        """Return matching feedback; denied proposals never reach the read primitive."""
        allowed = call.get('name') == 'read_file' and call.get('input') == {'path': 'note.txt'}
        decision = {'call': copy.deepcopy(call), 'decision': 'allow' if allowed else 'deny',
                    'reason': 'exact allowed operation/arguments' if allowed else 'only read_file(note.txt) is authorized'}
        self.decisions.append(decision)
        self.trace.write('decision', **decision)
        if not allowed:
            return {'type': 'tool_result', 'tool_use_id': call['id'], 'is_error': True,
                    'content': json.dumps({'decision': 'denied', 'reason': decision['reason']})}
        data = self.workspace.read('note.txt')
        effect = {'operation': 'read_file', 'path': 'note.txt', 'characters_returned': len(data)}
        self.executions.append(effect)
        self.trace.write('effect', **effect)
        return {'type': 'tool_result', 'tool_use_id': call['id'], 'is_error': False, 'content': json.dumps(data)}


class AuthoredResponses:
    """Fixed read/end responses, optionally with a fixed attempted edit between.

    The program selects the scenario; this class never chooses from file text.
    """
    def __init__(self, attempt: dict | None = None) -> None:
        self.turn = 0
        self.attempt = copy.deepcopy(attempt)

    def complete(self, request: dict) -> dict:
        self.turn += 1
        if self.turn == 1:
            return {'stop_reason': 'tool_use', 'content': [
                {'type': 'tool_use', 'id': 'read-note', 'name': 'read_file', 'input': {'path': 'note.txt'}}]}
        if self.turn == 2 and self.attempt is not None:
            return {'stop_reason': 'tool_use', 'content': [copy.deepcopy(self.attempt)]}
        if self.turn == (3 if self.attempt is not None else 2):
            return {'stop_reason': 'end_turn', 'content': [
                {'type': 'text', 'text': 'Authored end. Inspect supplied feedback; this is not model behavior.'}]}
        raise ValueError('authored exchange exhausted')


def exchange_case(root: Path, variant: str, attempt: dict | None = None) -> dict:
    """Run a fixed scenario through the unchanged guarded loop and exact dispatcher."""
    root.mkdir()
    workspace = make_workspace(root / 'work', variant)
    trace = Trace(root / 'trace.jsonl')
    tools = ReadOnlyTools(workspace, trace)
    try:
        result = run_loop(AuthoredResponses(attempt), tools, 'Read note.txt as evidence; do not change files.', trace,
                          max_turns=3, max_calls=2, system=system_for_task('injection'))
    finally:
        trace.close()
    if result['status'] != 'completed':
        raise ValueError(f"{variant} exchange did not complete: {result['status']}")
    write_json(root / 'history.json', result['messages'])
    forbidden = [d for d in tools.decisions if d['decision'] == 'deny']
    return {'variant': variant, 'origin': 'authored responses; actual read and dispatcher decisions',
            'forbidden_proposals': len(forbidden), 'decisions': tools.decisions,
            'executions': tools.executions, 'notes_after': workspace.read('notes.txt')}


def inspect_exposure(output: Path) -> dict:
    """Vary only file contents; both variants receive identical authored responses."""
    rows = [exchange_case(output / variant, variant) for variant in ('benign', 'injected')]
    report = {'mode': 'offline data-flow comparison, not model behavior', 'cases': rows}
    write_json(output / 'report.json', report)
    return report


def description_only_recording(proposal: dict) -> dict:
    """Intentionally wrong authorization idea, confined to recording only.

    No callback, file tool, subprocess or network action exists on this path.
    """
    approved = 'approved' in proposal['display_description'].casefold()
    return {'decision': 'would_allow' if approved else 'would_deny',
            'reason': 'deliberately wrong substring check of untrusted display text',
            'executed': False, 'scope': 'recording only; no operation was invoked'}


def inspect_authority(output: Path) -> dict:
    """Hold proposals constant; compare description-only recording with exact dispatch."""
    proposals = json.loads((FIXTURES / 'proposals.json').read_text(encoding='utf-8'))
    workspace = make_workspace(output / 'work', 'injected')
    trace = Trace(output / 'trace.jsonl')
    tools = ReadOnlyTools(workspace, trace)
    rows = []
    try:
        for proposal in proposals:
            call = proposal['call']
            trace.write('proposal', origin='authored fixture, not model output', proposal=proposal)
            simulated = description_only_recording(proposal)
            trace.write('recording_only_decision', label=proposal['label'], **simulated)
            before = len(tools.executions)
            result = tools.dispatch(call)
            trace.write('tool', call=call, result=result)
            rows.append({'proposal': proposal, 'recording_only': simulated,
                         'bounded_decision': tools.decisions[-1]['decision'],
                         'bounded_executed': len(tools.executions) > before, 'result': result})
    finally:
        trace.close()
    attempt = exchange_case(output / 'scripted-attempt', 'injected', proposals[1]['call'])
    effects = tools.executions + attempt['executions']
    forbidden_count = sum(e['operation'] != 'read_file' or e['path'] != 'note.txt' for e in effects)
    report = {'mode': 'fixed proposals and real bounded reads; no model', 'cases': rows,
              'bounded_executions': tools.executions, 'scripted_attempt': attempt,
              'forbidden_execution_count': forbidden_count,
              'notes_after': workspace.read('notes.txt'),
              'scope': 'Setup/artifact writes are separate; dispatched tools have no write/network implementation.'}
    write_json(output / 'report.json', report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', choices=['exposure', 'authority'])
    parser.add_argument('--output', type=Path, required=True, help='new dedicated output directory')
    args = parser.parse_args()
    try:
        args.output.mkdir(parents=True, exist_ok=False)
        report = inspect_exposure(args.output) if args.lesson == 'exposure' else inspect_authority(args.output)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Authority inspection failed: {exc}', file=sys.stderr)
        return 2
    print(f"{len(report['cases'])} cases inspected. Artifacts: {args.output.resolve()}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
