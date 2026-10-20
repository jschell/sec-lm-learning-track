"""Run progressively complete read-only stages, with optional live inference."""
import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

from loop import run_loop as guarded_loop, safe_diagnostic, MessagesHTTP, Replay, Tools, Trace, Workspace, system_for_task

from run_support import record_failure, RunDirectory, ObservedDispatch, accounting, print_run_paths

HERE = Path(__file__).resolve().parent


def changed_read_replay(run_root: Path, work: Path, path: str) -> Path:
    """Write a run-local copy of read.json whose first call requests ``path``.

    The source fixture is never edited. The expected result follows the copied workspace:
    an existing regular file must succeed; anything else must return is_error=true.
    """
    replay = json.loads((HERE / 'replay' / 'read.json').read_text(encoding='utf-8'))
    replay['turns'][0]['response']['content'][0]['input']['path'] = path
    try:
        expect_error = not Workspace(work).path(path).is_file()
    except ValueError:
        expect_error = True
    replay['turns'][0]['checks'] = [{'id': 'read-1', 'is_error': expect_error}]
    target = run_root / 'read-replay.json'
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
        json.dump(replay, stream, indent=2)
        stream.write('\n')
    return target


def main() -> int:
    parser = argparse.ArgumentParser(prog='learn.py stage', description=__doc__)
    parser.add_argument('stage', type=int, choices=[1, 2, 3])
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--provider', choices=['anthropic', 'openrouter'], default='anthropic')
    parser.add_argument('--model')
    parser.add_argument('--replay-file', type=Path, help='Use your edited synthetic response fixture')
    parser.add_argument('--read', metavar='PATH',
                        help='Stage 2 only: change the path the scripted first response requests')
    parser.add_argument('--json', action='store_true',
                        help='Stages 1/2: print the full response/history instead of a summary')
    args = parser.parse_args()
    if args.read is not None and args.stage != 2:
        parser.error('--read applies only to stage 2')
    if args.read is not None and (args.replay_file or args.live):
        parser.error('--read cannot be combined with --replay-file or --live')
    if args.live and args.stage < 3:
        parser.error('live stages 1/2 are unsupported; use stage 3 --live or learn.py --live --read-only')
    if args.live and args.replay_file:
        parser.error('--replay-file cannot be combined with --live')
    if args.live and not args.model:
        parser.error('--live requires --model')
    run = RunDirectory('stage-' + str(args.stage))
    trace = None
    tools = None
    transport = None
    result = {'status': 'error', 'tool_calls': 0, 'completed_tool_calls': 0,
              'dispatch_attempts': 0, 'dispatch_uncertain': False}
    mode = 'live' if args.live else 'synthetic-replay'
    json_output = args.json or args.stage == 3
    try:
        trace = Trace(run.trace)
        trace.write('start', stage=args.stage, mode=mode, max_turns=6, max_calls=24,
                    **({'read_path': args.read} if args.read is not None else {}))
        work = run.copy_fixtures(HERE / 'fixtures')
        if args.read is not None:
            args.replay_file = changed_read_replay(run.root, work, args.read)
        raw_tools = Tools(Workspace(work))
        raw_tools.definitions = [d for d in raw_tools.definitions if d['name'] in {'read_file', 'list_files'}]
        tools = ObservedDispatch(raw_tools)
        source = HERE / 'solutions/stages.py'
        spec = importlib.util.spec_from_file_location('worked_stages', source)
        stages = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stages)
        replay = {1:'inference', 2:'read', 3:'recover'}[args.stage]
        transport = MessagesHTTP(args.model, args.provider) if args.live else Replay(args.replay_file or HERE / 'replay' / (replay + '.json'))
        prompt = 'Read notes.txt and report the fifteenth value. Use only the provided read-only tools.'
        class RecordedModel:
            def __init__(self) -> None:
                self.turn = 0
            def complete(self, request: dict) -> dict:
                self.turn += 1
                trace.write('request', turn=self.turn, request=request)
                response = transport.complete(request)
                trace.write('response', turn=self.turn, response=response)
                return response
        if args.stage < 3:
            model = RecordedModel()
            if args.stage == 1:
                response = stages.infer_once(model, 'Explain what a controller supplies in one inference request.')
                payload = response
            else:
                response, history = stages.exchange(model, tools, prompt)
                trace.write('history', messages=history)
                payload = {'history': history, 'response': response}
            if not isinstance(response, dict) or response.get('stop_reason') != 'end_turn':
                raise ValueError('short exchange expects a final end_turn response; inspect the replay file')
            result = {'status': 'completed', **tools.counts()}
            if args.json:
                print(json.dumps(payload, indent=2))
            else:
                # Summary only: the trace viewer is where the exchange is inspected.
                print(f'Stage {args.stage} ({mode}): completed')
                print(f'Inference requests: {model.turn}')
                print(f'Completed tool calls (error results included): {tools.counts()["completed_tool_calls"]}')
                if args.read is not None:
                    print(f'Requested path changed to: {args.read}')
                print('Full JSON instead of this summary: add --json')
        else:
            controller = guarded_loop if args.live else stages.run_loop
            result = controller(transport, tools, prompt, trace, max_turns=6, system=system_for_task('inspect'))
            print(json.dumps(result, indent=2))
    except Exception as exc:
        result = {'status': 'error', **(tools.counts() if tools else result),
                  'message': safe_diagnostic(exc, transport)}
        result['status'] = 'error'
        result['trace_incomplete'] = not record_failure(trace, type(exc).__name__, result['message'], result)
        json_output = True
        print(json.dumps(result, indent=2))
    finally:
        if trace is not None:
            trace.close()
    try:
        run.finish({'stage': args.stage, 'mode': mode, 'status': result['status'],
                    **accounting(result), 'trace_incomplete': result.get('trace_incomplete', False),
                    **({'message': result['message']} if 'message' in result else {})})
    except OSError as exc:
        print('Cannot save run summary: ' + safe_diagnostic(exc) + '; inspect ' + str(run.root), file=sys.stderr)
        return 1
    # JSON output keeps stdout a single JSON document; paths go to stderr.
    print_run_paths(run, sys.stderr if json_output else sys.stdout)
    return int(result['status'] != 'completed')


if __name__ == '__main__':
    raise SystemExit(main())
