"""Run bounded behavioral checks against a learner implementation."""
import argparse
import importlib.util
from pathlib import Path
import sys
import subprocess

from authoring_checks import check_stage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--stage', type=int, choices=[1, 2, 3], required=True)
    parser.add_argument('--guards', action='store_true', help='Stage 3 extension: verify truncation and call-budget guards')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.guards and args.stage != 3:
        parser.error('--guards applies only to stage 3')
    if not args.worker:
        try:
            completed = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                '--file', str(args.file.resolve()), '--stage', str(args.stage), '--worker',
                *(['--guards'] if args.guards else [])],
                capture_output=True, text=True, encoding='utf-8', timeout=10)
        except subprocess.TimeoutExpired:
            print('NOT VERIFIED: learner check exceeded 10 seconds; inspect termination logic.', file=sys.stderr)
            return 1
        print(completed.stdout, end='')
        print(completed.stderr, end='', file=sys.stderr)
        return completed.returncode
    spec = importlib.util.spec_from_file_location('learner_exercise', args.file.resolve())
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        passed = check_stage(module, args.stage, guards=args.guards)
    except (AssertionError, NotImplementedError, AttributeError, KeyError, TypeError, ValueError) as exc:
        print(f'NOT VERIFIED stage {args.stage}: {exc}', file=sys.stderr)
        return 1
    for observation in passed:
        print('VERIFIED: ' + observation)
    print(f'Stage {args.stage}: core request/feedback behavior verified with a synthetic model.')
    if args.stage == 3:
        print('Guard extension: verified.' if args.guards else 'Guard extension: not checked; explore learn.py guards, then add --guards to this command.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
