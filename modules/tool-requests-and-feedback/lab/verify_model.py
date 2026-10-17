"""Observe the prepared baseline with a private, automatically stopped CPU server.

API/containment assertions are distinct from task_passed. A model failing the
task remains a recorded observation, not an assertion hidden by a retry.
"""
import argparse
import json
from pathlib import Path
import platform
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from bridge import exercise
from prepare import SERVER, model_ready, model_setup


def verify(model_name: str = '135m') -> dict:
    config,model=model_setup(model_name)
    if not SERVER.is_file() or not model_ready(model,config):
        raise ValueError('prepare the pinned runtime/model using the generation setup first')
    with socket.socket() as available:
        available.bind(('127.0.0.1', 0))
        port = available.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='tool-feedback-smoke-') as temp:
        root = Path(temp)
        with (root / 'server.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen([str(SERVER), '-m', str(model), '--alias', f'smollm2-{model_name}-instruct-q8',
                '--host', '127.0.0.1', '--port', str(port), '-t', '2', '-c', '1024', '-np', '1', '-ngl', '0'],
                stdout=log, stderr=subprocess.STDOUT)
            try:
                endpoint = f'http://127.0.0.1:{port}'
                deadline = time.monotonic() + 90
                while True:
                    if process.poll() is not None:
                        raise RuntimeError('server exited; inspect prepared runtime compatibility')
                    try:
                        with urllib.request.urlopen(endpoint + '/health', timeout=1) as response:
                            if response.status == 200:
                                break
                    except (urllib.error.URLError, TimeoutError):
                        pass
                    if time.monotonic() >= deadline:
                        raise RuntimeError('prepared server startup timed out')
                    time.sleep(0.2)
                runs = {}
                conditions = [
                    ('ordinary', False, False, 128, 'baseline'),
                    ('constrained', True, False, 128, 'baseline'),
                    ('no_tool', True, True, 128, 'baseline'),
                    ('output_limit', True, False, 1, 'baseline'),
                ]
                # Small observed comparison, not a benchmark or automatic prompt search.
                conditions += [(f'{style}_{suffix}_{trial}', constrained, False, 128, style)
                    for style in ('example', 'copy-line')
                    for suffix, constrained in [('ordinary', False), ('constrained', True)]
                    for trial in range(1, 4)]
                for name, constrained, without_tool, tokens, prompt_style in conditions:
                    output = root / name
                    report = exercise(output, 'live', endpoint, constrained, without_tool, tokens, prompt_style)
                    events = [json.loads(line) for line in (output / 'trace.jsonl').read_text(encoding='utf-8').splitlines()]
                    responses = [e['response'] for e in events if e['event'] == 'local_response']
                    assert responses, 'no actual completion was observed'
                    assert not any(r.get('truncated') for r in responses), 'input context was truncated'
                    if name == 'no_tool':
                        assert report['successful_reads'] == 0, 'omitted tool dispatched successfully'
                    if name == 'output_limit':
                        assert report['loop_status'] == 'model_stop:max_tokens', 'output cap was not mapped'
                        assert report['successful_reads'] == 0, 'partial reply executed'
                    runs[name] = {'report': report, 'events': events}
                return {'source': 'actual CPU model run, not replay', 'platform': platform.platform(),
                    'machine': platform.machine(), 'python': platform.python_version(),
                    'model': config['model'], 'gguf_sha256': config['gguf_sha256'],
                    'runtime_revision': config['runtime_revision'], 'threads': 2, 'context': 1024,
                    'runs': runs}
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


def example_task_check(record: dict) -> dict:
    """Optional recipe regression check, independent of the API smoke assertions."""
    cases = {name: record['runs'].get(name, {}).get('report', {}).get('task_passed') is True
             for name in (f'example_ordinary_{trial}' for trial in range(1, 4))}
    return {'condition': 'example prompt, ordinary generation, three fresh tasks',
            'cases': cases, 'passed': all(cases.values())}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',choices=['135m','360m'],default='135m')
    parser.add_argument('--require-example-task',action='store_true',
                        help='also require the three ordinary/example tasks to pass; records still printed on failure')
    args=parser.parse_args()
    record=verify(args.model)
    required=example_task_check(record) if args.require_example_task else None
    record['required_task_check']=required
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 1 if required is not None and not required['passed'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
