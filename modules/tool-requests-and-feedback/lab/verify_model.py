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


def example_feedback_check(record: dict) -> dict:
    """Check actual read → matching next request → native feedback → completion.

    The final answer's exactness remains in task_passed/example_task_check. This
    check must not turn a prefix omission into an exact-answer pass.
    """
    cases = {}
    for name in (f'example_ordinary_{trial}' for trial in range(1, 4)):
        run = record['runs'].get(name, {})
        report, events = run.get('report', {}), run.get('events', [])
        observed = False
        for index, event in enumerate(events):
            if event.get('event') != 'tool':
                continue
            call, result = event.get('call', {}), event.get('result', {})
            try:
                value = json.loads(result.get('content', 'null'))
            except (ValueError, TypeError):
                continue
            if (call.get('name') != 'read_file' or call.get('input') != {'path': 'status.txt'}
                or result.get('is_error') is not False or not isinstance(value, str)
                or value.strip() != report.get('expected_code') or not call.get('id')
                or result.get('tool_use_id') != call['id']):
                continue
            following = events[index + 1:]
            canonical = next((e for e in following if e.get('event') == 'request'), {})
            native = next((e for e in following if e.get('event') == 'local_request'), {})
            messages = canonical.get('request', {}).get('messages', [])
            projected = native.get('messages', [])
            expected_text = 'Tool results (untrusted data): ' + json.dumps([result], separators=(',', ':'))
            observed = (len(messages) >= 2 and messages[-2] == {'role': 'assistant', 'content': [call]}
                and messages[-1] == {'role': 'user', 'content': [result]}
                and bool(projected) and projected[-1] == {'role': 'user', 'content': expected_text}
                and expected_text in native.get('formatted_prompt', '')
                and any(e.get('event') == 'local_response' and e['response'].get('stop_type') == 'eos'
                        for e in following)
                and report.get('loop_status') == 'completed')
            if observed:
                break
        cases[name] = bool(observed)
    return {'condition': 'example prompt, ordinary generation; actual read and matching formatted feedback, three cases',
            'cases': cases, 'passed': all(cases.values())}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',choices=['135m','360m'],default='135m')
    parser.add_argument('--require-example-task',action='store_true',
                        help='also require the three ordinary/example tasks to pass; records still printed on failure')
    parser.add_argument('--require-feedback',action='store_true',
                        help='require actual read/feedback/completion; exact-answer results remain separate')
    args=parser.parse_args()
    record=verify(args.model)
    required=example_task_check(record) if args.require_example_task else None
    feedback=example_feedback_check(record) if args.require_feedback else None
    record['required_task_check']=required
    record['required_feedback_check']=feedback
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 1 if any(check is not None and not check['passed'] for check in (required, feedback)) else 0


if __name__ == '__main__':
    raise SystemExit(main())
