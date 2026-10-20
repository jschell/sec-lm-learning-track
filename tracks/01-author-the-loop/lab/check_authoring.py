"""Run bounded behavioral checks against a learner implementation."""
import argparse
from pathlib import Path
import sys
import subprocess
from run_support import load_implementation, RunDirectory
from loop import Trace, safe_diagnostic

from authoring_checks import check_stage


def main() -> int:
    parser = argparse.ArgumentParser(prog='learn.py check', description=__doc__)
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--stage', type=int, choices=[0, 1, 2, 3], required=True,
                        help='0 checks a Part 0 run_conversation; 1-3 check the worked stages')
    parser.add_argument('--guards', action='store_true', help='Stage 3 extension: verify truncation and call-budget guards')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--output', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.guards and args.stage != 3:
        parser.error('--guards applies only to stage 3')
    if not args.worker:
        run = RunDirectory('check-stage-' + str(args.stage))
        work = run.root / 'work'
        work.mkdir(mode=0o700)
        trace = Trace(run.trace)
        code = 1
        try:
            trace.write('start', mode='synthetic learner checks', stage=args.stage)
            completed = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                '--file', str(args.file.resolve()), '--stage', str(args.stage), '--worker', '--output', str(work),
                *(['--guards'] if args.guards else [])],
                capture_output=True, text=True, encoding='utf-8', timeout=10)
            print(safe_diagnostic(completed.stdout), end='')
            print(safe_diagnostic(completed.stderr), end='', file=sys.stderr)
            code = completed.returncode
        except subprocess.TimeoutExpired:
            print('NOT VERIFIED: learner check exceeded 10 seconds; inspect termination logic.', file=sys.stderr)
        finally:
            status = 'verified' if code == 0 else 'not_verified'
            trace.write('stop', status=status, tool_calls=None,
                        scope='behavior checks; per-case traces are in work/')
            trace.close()
        run.finish({'mode': 'synthetic learner checks', 'status': status, 'tool_calls': None,
                    'guards_checked': args.guards, 'learner_file': str(args.file.resolve())})
        print('Run: ' + str(run.root))
        print('Summary: ' + str(run.result))
        print('Trace: ' + str(run.trace))
        return code
    try:
        module = load_implementation(args.file, 'learner_exercise')
        passed = check_stage(module, args.stage, guards=args.guards, output=args.output)
    except Exception as exc:
        # Isolated learner-worker boundary; common edits must not produce raw tracebacks.
        print(f'NOT VERIFIED stage {args.stage}: {type(exc).__name__}: {safe_diagnostic(exc)}', file=sys.stderr)
        return 1
    for observation in passed:
        print('VERIFIED: ' + observation)
    print(f'Stage {args.stage}: core request/feedback behavior verified with a synthetic model.')
    if args.stage == 3:
        print('Guard extension: verified.' if args.guards else 'Guard extension: not checked; explore learn.py guards, then add --guards to this command.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
