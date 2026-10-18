"""Run fixed proposals directly; standard library only, no inference."""
import argparse
from pathlib import Path

from contract import DEFINITION, EventLookup, dispatch, feedback_example, load_calls, write_json


def run(output: Path) -> dict:
    """Write direct-call observations to a new dedicated output directory."""
    output.mkdir(parents=True, exist_ok=False)
    lookup = EventLookup(output / 'executions.jsonl')
    calls = load_calls()
    rows = []
    for proposal in calls:
        outcome = dispatch(lookup, proposal['name'], proposal['arguments'])
        rows.append({'proposal': proposal, 'outcome': outcome})
    report = {'mode': 'direct fixed calls; no model', 'definition': DEFINITION,
              'calls': rows, 'execution_count': lookup.execution_count}
    write_json(output / 'report.json', report)
    write_json(output / 'feedback-example.json', feedback_example(calls[0], rows[0]['outcome']))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run(args.output)
    except (OSError, ValueError) as exc:
        print(f'Direct lab failed: {exc}')
        return 2
    print(f"{len(report['calls'])} proposals; {report['execution_count']} function entries. Artifacts: {args.output.resolve()}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
