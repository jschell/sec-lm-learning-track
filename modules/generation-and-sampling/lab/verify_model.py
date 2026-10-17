"""Actual prepared-model smoke checks, distinct from synthetic contract tests.

Starts/stops a dedicated server on an ephemeral loopback port. No model setup
is performed here. Outputs are observations, not claims about Pi performance.
"""
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from observe import LocalServer, observe
from prepare import CONFIG, MODEL, SERVER, model_ready


def verify() -> None:
    if not SERVER.is_file() or not model_ready():
        raise ValueError('prepare the pinned runtime/model before actual smoke checks')
    with socket.socket() as available:
        available.bind(('127.0.0.1',0))
        port=available.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix='generation-smoke-') as temp:
        log_path=Path(temp)/'server.log'
        with log_path.open('w',encoding='utf-8') as log:
            process=subprocess.Popen([str(SERVER),'-m',str(MODEL),'--alias','smollm2-135m-instruct-q8',
                '--host','127.0.0.1','--port',str(port),'-t','2','-c','1024','-np','1','-ngl','0'],
                stdout=log,stderr=subprocess.STDOUT)
            try:
                endpoint=f'http://127.0.0.1:{port}'
                deadline=time.monotonic()+90
                while True:
                    if process.poll() is not None:
                        raise RuntimeError('server exited: '+log_path.read_text(encoding='utf-8')[-3000:])
                    try:
                        with urllib.request.urlopen(endpoint+'/health',timeout=1) as response:
                            if response.status==200:break
                    except (urllib.error.URLError,TimeoutError):pass
                    if time.monotonic()>=deadline:raise RuntimeError('prepared server startup timed out')
                    time.sleep(0.2)
                server=LocalServer(endpoint)
                prompts=json.loads((Path(__file__).parent/'prompts.json').read_text(encoding='utf-8'))
                experiments={}
                for name in ('reply','extract','rewrite','opposite'):
                    experiments[name]=observe(server,prompts[name]['prompt'],max_tokens=32)
                experiments['limit']=observe(server,prompts['rewrite']['prompt'],max_tokens=1)
                for temperature in (0.5,1.5):
                    experiments[f'temperature_{temperature}']=observe(server,prompts['rewrite']['prompt'],
                        mode='sample',temperature=temperature,max_tokens=8)
                for k in (0,5):
                    experiments[f'top_k_{k}']=observe(server,prompts['rewrite']['prompt'],mode='sample',top_k=k,max_tokens=8)
                repeats=[observe(server,prompts['reply']['prompt'],mode='sample',max_tokens=8) for _ in range(2)]
                for run in experiments.values():
                    assert run['observation']['token_records'],'model probabilities unavailable'
                    assert not run['observation']['context_truncated'],'unexpected context truncation'
                assert experiments['limit']['observation']['stop_type']=='limit','output cap not observed'
                result={'model':CONFIG['model'],'gguf_sha256':CONFIG['gguf_sha256'],
                    'runtime_revision':CONFIG['runtime_revision'],
                    'task_checks':{'reply_exact':experiments['reply']['observation']['content'].strip()=='OK',
                        'extract_exact':experiments['extract']['observation']['content'].strip()=='denied',
                        'opposite_contains_cold':'cold' in experiments['opposite']['observation']['content'].lower()},
                    'sampled_repeat_ids_equal':repeats[0]['observation']['generated_ids']==repeats[1]['observation']['generated_ids'],
                    'experiments':experiments}
                print(json.dumps(result,ensure_ascii=False,indent=2))
            finally:
                process.terminate()
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


if __name__=='__main__':
    verify()
