"""Run the read-only bridge: default scripted comparison, explicit live generation."""
import argparse
import json
from pathlib import Path

from bridge import exercise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['replay', 'live'], default='replay')
    parser.add_argument('--output', type=Path, required=True, help='new directory; never overwritten')
    parser.add_argument('--base-url', default='http://127.0.0.1:8080')
    parser.add_argument('--constrain', action='store_true', help='constrain live output with JSON Schema')
    parser.add_argument('--without-tool', action='store_true')
    parser.add_argument('--max-tokens', type=int, default=128)
    parser.add_argument('--prompt-style', choices=['baseline', 'example', 'copy-line'], default='baseline')
    args = parser.parse_args()
    try:
        report = exercise(args.output, args.mode, args.base_url, args.constrain,
                          args.without_tool, args.max_tokens, args.prompt_style)
    except (ValueError, OSError, RuntimeError) as exc:
        print(json.dumps({'setup_error': str(exc)}))
        return 2
    print(json.dumps(report, indent=2))
    # Failed model observations are preserved; never presented as passing tasks.
    return 0 if report['task_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
