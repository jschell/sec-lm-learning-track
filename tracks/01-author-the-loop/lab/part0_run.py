"""Run one Part 0 step: the minimal loop on scripted replay with read-only tools.

Prints a live transcript (You / Model (scripted) / tool / result / error) and retains the
run under .cache/exercises/track-1/part0-STEP/ so later sections can inspect it.
"""
import argparse
import copy
import json
from pathlib import Path
import sys

from loop import Replay, Trace, Workspace, safe_diagnostic
from part0.minimal_loop import ReadOnlyTools, run_conversation
from run_support import RunDirectory, print_run_paths

HERE = Path(__file__).resolve().parent
STEP_TOOLS = {'chat': [], 'exchange': ['read_file'], 'loop': ['read_file'], 'more-tools': ['read_file', 'list_files']}
SHOW_CHARS = 200


def show(label: str, text: str) -> None:
    """One transcript line; long or multi-line text is shortened for reading, not for evidence."""
    shown = ' / '.join(str(text).splitlines())
    if len(shown) > SHOW_CHARS:
        shown = shown[:SHOW_CHARS] + ' ...'
    print(f"{'Model (scripted)' if label == 'Model' else label}: {shown}")


def show_tools() -> int:
    """Step 2: what the model is told about each tool, and what the controller runs."""
    tools = ReadOnlyTools(Workspace(HERE / 'fixtures'), ['read_file', 'list_files'])
    for definition in tools.definitions:
        function = tools.functions[definition['name']]
        print(f"Tool: {definition['name']}")
        print(f"  description (sent to the model): {definition['description']}")
        print(f"  input schema (sent to the model): {json.dumps(definition['input_schema'])}")
        print(f"  runs (on the controller, looked up by name): {function.__name__}() in lab/part0/minimal_loop.py")
    print('The model only ever sees the definitions. Nothing runs until the controller dispatches a call.')
    return 0


class RecordedModel:
    """Scripted replay that also records each request and response in the run's trace."""
    def __init__(self, replay: Replay, trace: Trace) -> None:
        self.replay, self.trace, self.turn = replay, trace, 0

    def complete(self, request: dict) -> dict:
        self.turn += 1
        self.trace.write('request', turn=self.turn, request=copy.deepcopy(request))
        response = self.replay.complete(request)
        self.trace.write('response', turn=self.turn, response=response)
        return response


def main() -> int:
    parser = argparse.ArgumentParser(prog='learn.py part0', description=__doc__)
    parser.add_argument('step', choices=['chat', 'tools', 'exchange', 'loop', 'more-tools'])
    parser.add_argument('--live', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.live:
        parser.error('Part 0 runs on scripted replay only; for a real model see the optional step in 00-the-loop.md')
    if args.step == 'tools':
        return show_tools()
    replay_path = HERE / 'part0' / 'replay' / (args.step + '.json')
    user_turns = json.loads(replay_path.read_text(encoding='utf-8'))['user_turns']
    run = RunDirectory('part0-' + args.step)
    trace = Trace(run.trace)
    status, message = 'completed', None
    conversation: list = []
    try:
        trace.write('start', mode='part0 scripted replay', step=args.step, tools=STEP_TOOLS[args.step])
        work = run.copy_fixtures(HERE / 'fixtures')
        model = RecordedModel(Replay(replay_path), trace)
        conversation = run_conversation(model, ReadOnlyTools(Workspace(work), STEP_TOOLS[args.step]), user_turns, show)
        trace.write('history', messages=conversation)
    except Exception as exc:
        # Top-level teaching boundary: report a readable failure and keep the partial trace.
        status, message = 'error', f'{type(exc).__name__}: {safe_diagnostic(exc)}'
        print('Part 0 run failed: ' + message, file=sys.stderr)
    calls = sum(1 for m in conversation if m['role'] == 'user' and isinstance(m['content'], list)
                for b in m['content'] if b.get('type') == 'tool_result')
    trace.write('stop', status=status, tool_calls=calls if status == 'completed' else None)
    trace.close()
    run.finish({'mode': 'part0 scripted replay', 'step': args.step, 'status': status, 'tool_calls': calls,
                **({'message': message} if message else {})})
    print()
    print_run_paths(run)
    return int(status != 'completed')


if __name__ == '__main__':
    raise SystemExit(main())
