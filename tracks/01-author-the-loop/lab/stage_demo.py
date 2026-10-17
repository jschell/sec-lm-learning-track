"""Run progressively complete read-only stages, with optional live inference."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

from loop import MessagesHTTP, Replay, Tools, Trace, Workspace

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', type=int, choices=[1, 2, 3])
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--provider', choices=['anthropic', 'openrouter'], default='anthropic')
    parser.add_argument('--model')
    parser.add_argument('--replay-file', type=Path, help='Use your edited synthetic response fixture')
    args = parser.parse_args()
    if args.live and args.replay_file:
        parser.error('--replay-file cannot be combined with --live')
    if args.live and not args.model:
        parser.error('--live requires --model')
    root = Path(tempfile.mkdtemp(prefix='loop-stage-'))
    shutil.copytree(HERE / 'fixtures', root / 'work')
    tools = Tools(Workspace(root / 'work'))
    tools.definitions = [d for d in tools.definitions if d['name'] in {'read_file', 'list_files'}]
    source = HERE / 'solutions/stages.py'
    spec = importlib.util.spec_from_file_location('worked_stages', source)
    stages = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stages)
    replay = {1:'inference', 2:'read', 3:'recover'}[args.stage]
    model = MessagesHTTP(args.model, args.provider) if args.live else Replay(args.replay_file or HERE / 'replay' / (replay + '.json'))
    trace = Trace(root / 'trace.jsonl')
    prompt = 'Read notes.txt and report the fifteenth value. Use only the provided read-only tools.'
    # Recording is outside the teaching functions so their control flow stays visible.
    transport = model
    class RecordedModel:
        def complete(self, request: dict) -> dict:
            trace.write('request', request=request)
            response = transport.complete(request)
            trace.write('response', response=response)
            return response
    if args.stage < 3:
        model = RecordedModel()
    if args.stage == 1:
        prompt = 'Explain what a controller supplies in one inference request.'
    trace.write('start', stage=args.stage, mode='live' if args.live else 'synthetic-replay')
    try:
        if args.stage == 1:
            response = stages.infer_once(model, prompt)
            trace.write('response', turn=1, response=response)
            print(json.dumps(response, indent=2))
        elif args.stage == 2:
            response, history = stages.exchange(model, tools, prompt)
            trace.write('history', messages=history)
            trace.write('response', turn=2, response=response)
            print(json.dumps({'history':history, 'response':response}, indent=2))
        else:
            result = stages.run_loop(model, tools, prompt, trace, max_turns=6)
            print(json.dumps(result, indent=2))
            if result['status'] != 'completed':
                return 1
    finally:
        trace.close()
        print('Trace: ' + str(root / 'trace.jsonl'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
