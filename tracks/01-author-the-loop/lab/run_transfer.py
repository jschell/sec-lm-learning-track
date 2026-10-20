"""Exercise a new read-only tool through the real harness, replay or live."""
import argparse
import json
from pathlib import Path

from loop import MessagesHTTP, Replay, Trace, Workspace, run_loop, system_for_task
from transfer_support import CountLinesTools

from run_support import record_failure, load_implementation, RunDirectory, accounting
from loop import safe_diagnostic

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
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
    result = {'status': 'error', 'tool_calls': 0, 'completed_tool_calls': 0,
              'dispatch_attempts': 0, 'dispatch_uncertain': False}
    mode = 'live' if args.live else 'synthetic-replay'
    try:
        trace = Trace(run.trace)
        work = run.copy_fixtures(HERE / 'fixtures')
        module = load_implementation(args.file, 'transfer_implementation')
        tools = CountLinesTools(Workspace(work), module.count_lines)
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
    try:
        print(json.dumps(run.finish(report), indent=2))
    except OSError as exc:
        print('Cannot save run summary: ' + safe_diagnostic(exc) + '; inspect ' + str(run.root))
        return 1
    if not verified:
        print('NOT VERIFIED: expected an actual count_lines dispatch reporting two lines; inspect the run trace.')
        return 1
    print('VERIFIED: new read-only tool dispatched; matching result returned to the loop.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
