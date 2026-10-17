"""Exercise a new read-only tool through the real harness, replay or live."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

from loop import MessagesHTTP, Replay, Trace, Workspace, run_loop, system_for_task
from transfer_support import CountLinesTools

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
    spec = importlib.util.spec_from_file_location('transfer_implementation', args.file.resolve())
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = Path(tempfile.mkdtemp(prefix='loop-transfer-'))
    shutil.copytree(HERE / 'fixtures', root / 'work')
    tools = CountLinesTools(Workspace(root / 'work'), module.count_lines)
    model = MessagesHTTP(args.model, args.provider) if args.live else Replay(HERE / 'replay' / 'transfer.json')
    trace = Trace(root / 'trace.jsonl')
    try:
        result = run_loop(model, tools, 'Use count_lines to count notes.txt; report the observed count.',
                          trace, max_turns=4, max_calls=4, system=system_for_task("transfer"))
    finally:
        trace.close()
    print(json.dumps({'mode':'live' if args.live else 'synthetic-replay',
                      'status':result['status'], 'observed':tools.observed,
                      'trace':str(root / 'trace.jsonl')}, indent=2))
    if result['status'] != 'completed' or {'path':'notes.txt','lines':2} not in tools.observed:
        print('NOT VERIFIED: expected an actual count_lines dispatch reporting two lines.')
        return 1
    print('VERIFIED: new read-only tool dispatched; matching result returned to the loop.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
