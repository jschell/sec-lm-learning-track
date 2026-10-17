"""Short entry point for Track 1. All paths are relative to this file."""
from pathlib import Path
import runpy
import sys

LAB = Path(__file__).resolve().parent / 'tracks/01-author-the-loop/lab'


def main() -> None:
    """Run a fresh exercise, or inspect a trace with `learn.py trace PATH`."""
    sys.path.insert(0, str(LAB))
    if sys.argv[1:2] == ['trace']:
        sys.argv = [str(LAB / 'inspect_trace.py'), *sys.argv[2:]]
        runpy.run_path(str(LAB / 'inspect_trace.py'), run_name='__main__')
    else:
        runpy.run_path(str(LAB / 'cli.py'), run_name='__main__')


if __name__ == '__main__':
    main()
