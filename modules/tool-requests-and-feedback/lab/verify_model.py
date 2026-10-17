"""Observe the prepared baseline with a private, automatically stopped CPU server.

API/containment assertions are distinct from task_passed. A model failing the
task remains a recorded observation, not an assertion hidden by a retry.
"""
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
from prepare import CONFIG, MODEL, SERVER, model_ready


def verify() -> dict:
    if not SERVER.is_file() or not model_ready():
        raise ValueError('prepare the pinned runtime/model using the generation setup first')
    with socket.socket() as available:
        available.bind(('127.0.0.1', 0))
        port = available.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='tool-feedback-smoke-') as temp:
        root = Path(temp)
        with (root / 'server.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen([str(SERVER), '-m', str(MODEL), '--alias', 'smollm2-135m-instruct-q8',
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
                for name, constrained, without_tool, tokens in [
                    ('ordinary', False, False, 128), ('constrained', True, False, 128),
                    ('no_tool', True, True, 128), ('output_limit', True, False, 1),
                ]:
                    output = root / name
                    report = exercise(output, 'live', endpoint, constrained, without_tool, tokens)
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
                    'model': CONFIG['model'], 'gguf_sha256': CONFIG['gguf_sha256'],
                    'runtime_revision': CONFIG['runtime_revision'], 'threads': 2, 'context': 1024,
                    'runs': runs}
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
