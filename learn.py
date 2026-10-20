"""Short entry point for Track 1. Learner artifacts are anchored to this checkout."""
from pathlib import Path
import runpy
import sys

LAB = Path(__file__).resolve().parent / 'tracks/01-author-the-loop/lab'


def main() -> None:
    """Run a stage, check, transfer or fix exercise, full scenario, or trace inspection."""
    # Bare learn.py shows help; scenarios still run with explicit flags such as --scenario NAME.
    if sys.argv[1:] in ([], ['--help'], ['-h']):
        print("""Usage: learn.py COMMAND [OPTIONS]

Start here (Part 0, the loop):
  part0 STEP       STEP is chat, tools, exchange, loop or more-tools

Core learning commands:
  stage {1,2,3}    Run one inference, one exchange, or repeated feedback
  trace PATH       Summarize a run directory or saved JSONL trace
  transfer         Inspect the supplied count_lines exchange

Further exercises:
  check            Check a learner implementation (guards are optional)
  guards           Compare missing guards with recording-only tools
  fix [NAME]       List or copy an optional broken-file fix exercise

Existing scenario route:
  learn.py --scenario NAME [OPTIONS]
  learn.py --scenario read --help   Show all scenario/provider/limit flags

Use learn.py COMMAND --help for command-specific options.
Start: tracks/01-author-the-loop/README.md""")
        return
    sys.path.insert(0, str(LAB))
    commands = {'trace':'inspect_trace.py', 'stage':'stage_demo.py',
                'check':'check_authoring.py', 'transfer':'run_transfer.py', 'guards':'compare_guards.py',
                'fix':'fix_exercise.py', 'part0':'part0_run.py'}
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command in commands:
        target = LAB / commands[command]
        sys.argv = [str(target), *sys.argv[2:]]
    else:
        target = LAB / 'cli.py'
    try:
        runpy.run_path(str(target), run_name='__main__')
    except (OSError, ValueError, SyntaxError, ImportError, AttributeError) as exc:
        from loop import safe_diagnostic
        print('Lab command failed: ' + safe_diagnostic(exc) +
              '; check the supplied file/path and run setup from the repository root.', file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == '__main__':
    main()
