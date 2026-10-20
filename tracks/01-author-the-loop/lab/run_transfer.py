"""Exercise a new read-only tool through the real harness, replay or live."""
import argparse
import json
import sys
from pathlib import Path

from loop import MessagesHTTP, Replay, Trace, Workspace, run_loop, system_for_task
from transfer_support import CountLinesTools

from run_support import record_failure, load_implementation, RunDirectory, accounting
from loop import safe_diagnostic

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(prog='learn.py transfer', description=__doc__)
    parser.add_argument('--file', type=Path, default=HERE / 'solutions/transfer.py')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--provider', choices=['anthropic', 'openrouter'], default='anthropic')
    parser.add_argument('--model')
    args = parser.parse_args()
    if args.live and not args.model:
        parser.error('--live requires --model')
    run = RunDirectory('transfer')
    trace = None
    observed = []
    verified = False
    not_implemented: list[bool] = []
    result = {'status': 'error', 'tool_calls': 0, 'completed_tool_calls': 0,
              'dispatch_attempts': 0, 'dispatch_uncertain': False}
    mode = 'live' if args.live else 'synthetic-replay'
    try:
        trace = Trace(run.trace)
        work = run.copy_fixtures(HERE / 'fixtures')
        module = load_implementation(args.file, 'transfer_implementation')

        def count(workspace: Workspace, path: str) -> int:
            try:
                return module.count_lines(workspace, path)
            except NotImplementedError:
                not_implemented.append(True)
                raise

        tools = CountLinesTools(Workspace(work), count)
        observed = tools.observed
        model = MessagesHTTP(args.model, args.provider) if args.live else Replay(HERE / 'replay' / 'transfer.json')
        result = {'status': 'error', 'tool_calls': None, 'completed_tool_calls': None,
                  'dispatch_attempts': None, 'dispatch_uncertain': True}
        result = run_loop(model, tools, 'Use count_lines to count notes.txt; report the observed count.',
                          trace, max_turns=4, max_calls=4, system=system_for_task('transfer'))
        verified = result['status'] == 'completed' and {'path':'notes.txt','lines':2} in observed
    except Exception as exc:
        result['message'] = safe_diagnostic(exc)
        result['trace_incomplete'] = not record_failure(trace, type(exc).__name__, result['message'], result)
    finally:
        if trace is not None:
            trace.close()
    report = {'mode': mode, 'status': result['status'], 'observed': observed,
              'wiring_verified': verified, 'trace_incomplete': result.get('trace_incomplete', False), **accounting(result)}
    if 'message' in result:
        report['message'] = result['message']
    if not_implemented:
        report['learner_status'] = 'count_lines not implemented'
    try:
        print(json.dumps(run.finish(report), indent=2))
    except OSError as exc:
        print('Cannot save run summary: ' + safe_diagnostic(exc) + '; inspect ' + str(run.root), file=sys.stderr)
        return 1
    # Verdicts and paths go to stderr so stdout stays a single JSON document.
    print('Inspect: uv run --frozen --offline python learn.py trace ' + str(run.root), file=sys.stderr)
    if not_implemented:
        print(f'NOT VERIFIED: count_lines is not implemented yet. Edit {args.file} '
              '(Lesson 6, "Make one change"); the worked version is lab/solutions/transfer.py.', file=sys.stderr)
        return 1
    if not verified:
        print('NOT VERIFIED: expected an actual count_lines dispatch reporting two lines; inspect the run trace.',
              file=sys.stderr)
        return 1
    print('VERIFIED: new read-only tool dispatched; matching result returned to the loop.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
