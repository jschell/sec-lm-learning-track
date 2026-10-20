"""List, copy or hint the optional fix exercises; each copy is a fresh retained run.

The broken-file format adapts Rustlings' exercise/hint pattern; see ../SOURCES.md.
"""
import argparse
import json
import os
from pathlib import Path
import sys

from loop import Trace
from run_support import REPOSITORY, RunDirectory

HERE = Path(__file__).resolve().parent
EXERCISES = HERE / 'exercises'


def load_manifest() -> dict:
    """Read the exercise manifest supplied with the lab."""
    return json.loads((EXERCISES / 'exercises.json').read_text(encoding='utf-8'))


def copy_exercise(name: str, entry: dict) -> tuple[RunDirectory, Path]:
    """Copy one exercise into a new private run; the source file is never edited."""
    run = RunDirectory('fix-' + name)
    trace = Trace(run.trace)
    try:
        trace.write('start', mode='fix exercise copy', exercise=name, stage=entry['stage'])
        work = run.root / 'work'
        work.mkdir(mode=0o700)
        target = work / entry['file']
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            stream.write((EXERCISES / entry['file']).read_text(encoding='utf-8'))
        trace.write('stop', status='copied', tool_calls=None, scope='no inference or dispatch; copy only')
    finally:
        trace.close()
    run.finish({'mode': 'fix exercise copy', 'status': 'copied', 'exercise': name,
                'stage': entry['stage'], 'tool_calls': None, 'exercise_file': str(target)})
    return run, target


def main() -> int:
    manifest = load_manifest()
    parser = argparse.ArgumentParser(prog='learn.py fix', description=__doc__)
    parser.add_argument('name', nargs='?', help='exercise to copy; omit to list exercises')
    parser.add_argument('--hint', type=int, metavar='N', help='print hint N instead of copying')
    args = parser.parse_args()
    if args.name is None:
        if args.hint is not None:
            parser.error('--hint needs an exercise name')
        print('Optional fix exercises (outside the core route and pilot assessment):')
        for name, entry in manifest.items():
            print(f'  {name:<28} stage {entry["stage"]}  {entry["summary"]}')
        print('Start one with: uv run --frozen --offline python learn.py fix NAME')
        return 0
    if args.name not in manifest:
        parser.error(f'unknown exercise {args.name!r}; choose one of: ' + ', '.join(manifest))
    entry = manifest[args.name]
    if args.hint is not None:
        if not 1 <= args.hint <= len(entry['hints']):
            parser.error(f'{args.name} has hints 1-{len(entry["hints"])}')
        print(f'Hint {args.hint}/{len(entry["hints"])}: {entry["hints"][args.hint - 1]}')
        return 0
    run, target = copy_exercise(args.name, entry)
    solution = (EXERCISES / entry['solution']).relative_to(REPOSITORY)
    print(f'Exercise: {args.name} (stage {entry["stage"]}): {entry["summary"]}')
    print(f'Constraint: {entry["constraint"]} Look for the TODO.')
    print(f'Edit: {target}')
    print(f'Check: uv run --frozen --offline python learn.py check --file {target} --stage {entry["stage"]}')
    print(f'Hint:  uv run --frozen --offline python learn.py fix {args.name} --hint 1')
    print(f'Compare after trying: {solution}')
    print('Fresh copy: run this command again; earlier copies are retained.')
    print('Run: ' + str(run.root))
    print('Summary: ' + str(run.result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
