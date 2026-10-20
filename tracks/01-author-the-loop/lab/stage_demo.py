"""Run progressively complete read-only stages, with optional live inference."""
import argparse
import importlib.util
import json
from pathlib import Path

from loop import run_loop as guarded_loop, safe_diagnostic, MessagesHTTP, Replay, Tools, Trace, Workspace, system_for_task

from run_support import record_failure, RunDirectory, ObservedDispatch, accounting

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', type=int, choices=[1, 2, 3])
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--provider', choices=['anthropic', 'openrouter'], default='anthropic')
    parser.add_argument('--model')
    parser.add_argument('--replay-file', type=Path, help='Use your edited synthetic response fixture')
    args = parser.parse_args()
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
    try:
        trace = Trace(run.trace)
        trace.write('start', stage=args.stage, mode=mode, max_turns=6, max_calls=24)
        work = run.copy_fixtures(HERE / 'fixtures')
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
            print(json.dumps(payload, indent=2))
        else:
            controller = guarded_loop if args.live else stages.run_loop
            result = controller(transport, tools, prompt, trace, max_turns=6, system=system_for_task('inspect'))
            print(json.dumps(result, indent=2))
    except Exception as exc:
        result = {'status': 'error', **(tools.counts() if tools else result),
                  'message': safe_diagnostic(exc, transport)}
        result['status'] = 'error'
        result['trace_incomplete'] = not record_failure(trace, type(exc).__name__, result['message'], result)
        print(json.dumps(result, indent=2))
    finally:
        if trace is not None:
            trace.close()
    try:
        run.finish({'stage': args.stage, 'mode': mode, 'status': result['status'],
                    **accounting(result), 'trace_incomplete': result.get('trace_incomplete', False),
                    **({'message': result['message']} if 'message' in result else {})})
    except OSError as exc:
        print('Cannot save run summary: ' + safe_diagnostic(exc) + '; inspect ' + str(run.root))
        return 1
    print('Run: ' + str(run.root))
    print('Summary: ' + str(run.result))
    print('Trace: ' + str(run.trace))
    return int(result['status'] != 'completed')


if __name__ == '__main__':
    raise SystemExit(main())
