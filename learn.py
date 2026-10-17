"""Short entry point for Track 1. All paths are relative to this file."""
from pathlib import Path
import runpy
import sys

LAB = Path(__file__).resolve().parent / 'tracks/01-author-the-loop/lab'


def main() -> None:
    """Run a stage, check, transfer exercise, full scenario, or trace inspection."""
    sys.path.insert(0, str(LAB))
    commands = {'trace':'inspect_trace.py', 'stage':'stage_demo.py',
                'check':'check_authoring.py', 'transfer':'run_transfer.py'}
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command in commands:
        target = LAB / commands[command]
        sys.argv = [str(target), *sys.argv[2:]]
    else:
        target = LAB / 'cli.py'
    runpy.run_path(str(target), run_name='__main__')


if __name__ == '__main__':
    main()
