"""Run from any directory; output stays under a fresh temporary lab directory."""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
from loop import MessagesHTTP, DockerExecutor, Replay, Tools, Trace, Workspace, run_loop

HERE = Path(__file__).resolve().parent
PROMPT = ("Inspect fizzbuzz.py and repair its ordering bug. Check it with "
          "python -I /grader/check.py before and after editing if execution is enabled. "
          "If execution is unavailable, explicitly say it was not run.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scenario', choices=['inference', 'read', 'repair', 'recover',
                                        'limit', 'truncated', 'multi'], default='read')
    p.add_argument('--live', action='store_true', help='send synthetic workspace data to the selected provider')
    p.add_argument('--provider', choices=['anthropic', 'openrouter'], default='anthropic',
                   help='live inference destination (default: anthropic)')
    p.add_argument('--model', help='required live model ID; choose one your account can access')
    p.add_argument('--execute', action='store_true', help='enable Docker-only command tool')
    p.add_argument('--max-turns', type=int, default=12)
    p.add_argument('--max-calls', type=int, default=24)
    p.add_argument('--loop-file', type=Path, help='learner loop module exporting run_loop')
    a = p.parse_args()
    if a.max_turns < 1 or a.max_calls < 1:
        p.error('limits must be positive')
    if a.live and not a.model:
        p.error('--live requires --model')
    if not a.live and a.provider != 'anthropic':
        p.error('--provider openrouter requires --live; replay does not call a provider')
    if not a.live and a.execute:
        p.error('replay uses scripted observations; --execute is for live mode only')
    root = Path(tempfile.mkdtemp(prefix='loop-lab-'))
    root.chmod(0o755)
    work = root / 'work'
    shutil.copytree(HERE / 'fixtures', work)
    work.chmod(0o777)  # Disposable ONLY: the container uses UID 65534.
    for f in work.iterdir():
        f.chmod(0o666)
    try:
        executor = DockerExecutor(work, HERE / 'grader') if a.execute else None
        tools = Tools(Workspace(work), executor)
        scenario = a.scenario
        replay_path = HERE / 'replay' / (scenario + '.json')
        if not a.live and scenario == 'repair':
            # Explicitly scripted command observations, never executed on host.
            from scenarios import ScriptedExecutor
            tools = Tools(Workspace(work), ScriptedExecutor())
        model = MessagesHTTP(a.model, provider=a.provider) if a.live else Replay(replay_path)
        fn = run_loop
        if a.loop_file:
            import importlib.util
            spec = importlib.util.spec_from_file_location('learner_loop', a.loop_file.resolve())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            fn = module.run_loop
        trace = Trace(root / 'trace.jsonl')
        try:
            prompt = PROMPT if scenario == 'repair' or a.live else 'Inspect the synthetic exercise.'
            result = fn(model, tools, prompt, trace, max_turns=a.max_turns, max_calls=a.max_calls)
        finally:
            trace.close()
        print(json.dumps({'mode': 'live' if a.live else 'synthetic-replay',
                          'provider': a.provider if a.live else 'synthetic-replay',
                          'command_execution': bool(a.execute), 'directory': str(root),
                          'status': result['status'], 'tool_calls': result['tool_calls']}, indent=2))
        if result['status'] == 'error':
            return 1
        return 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(f'Lab setup failed: {exc}; disposable files: {root}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
