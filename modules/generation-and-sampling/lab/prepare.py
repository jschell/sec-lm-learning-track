"""Prepare a pinned CPU server and GGUF from a blank Linux/64-bit Pi setup.

Original setup code; upstream source, quantizer attribution and licenses in
../SOURCES.md. No server is started and no output is installed system-wide.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CONFIG=json.loads((HERE/'setup.json').read_text(encoding='utf-8'))
CACHE=ROOT/'.cache/generation'
SOURCE=CACHE/'llama.cpp'
MODEL=CACHE/CONFIG['gguf_file']
SERVER=SOURCE/'build/bin/llama-server'


def model_setup(name: str = '135m') -> tuple[dict, Path]:
    """Explicit choice only; the default baseline is never automatically replaced."""
    if name not in {'135m','360m'}:
        raise ValueError('choose 135m or the explicit 360m comparison')
    config = CONFIG if name == '135m' else json.loads((HERE/'setup-360m.json').read_text(encoding='utf-8'))
    return config, CACHE/config['gguf_file']


def digest(path: Path) -> str:
    """Hash large model files without holding all bytes in memory."""
    with path.open('rb') as handle:
        return hashlib.file_digest(handle,'sha256').hexdigest()


def model_ready(path: Path = MODEL, config: dict = CONFIG) -> bool:
    return (path.is_file() and path.stat().st_size==config['gguf_bytes']
            and digest(path)==config['gguf_sha256'])


def download_model(config: dict = CONFIG, model: Path = MODEL) -> None:
    """Stream exact pinned GGUF bytes; refuse a hash/length mismatch."""
    if model_ready(model,config):
        print('Verified cached GGUF.',flush=True)
        return
    url=(f"https://huggingface.co/{config['gguf_repository']}/resolve/"
         f"{config['gguf_revision']}/{config['gguf_file']}")
    temporary=model.with_suffix('.download')
    total=0
    with urllib.request.urlopen(url,timeout=60) as response,temporary.open('wb') as handle:
        while chunk:=response.read(1024*1024):
            total+=len(chunk)
            if total>config['gguf_bytes']:
                raise ValueError('model download exceeded its pinned size')
            handle.write(chunk)
    if not model_ready(temporary,config):
        raise ValueError('model download hash/size mismatch; original cached model not replaced')
    temporary.replace(model)
    print(f'Verified GGUF: {total} bytes.',flush=True)


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command,cwd=cwd,check=True)


def prepare(jobs: int = 2, model_name: str = '135m') -> None:
    config, model = model_setup(model_name)
    if not 1<=jobs<=4:
        raise ValueError('choose 1–4 build jobs; start with 1 on a small Pi')
    for program in ('git','cmake','c++'):
        if shutil.which(program) is None:
            raise ValueError(f'{program} unavailable; follow the lesson setup prerequisites')
    CACHE.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter()
    if not (SOURCE/'.git').is_dir():
        SOURCE.mkdir(exist_ok=True)
        run(['git','init',str(SOURCE)])
        run(['git','remote','add','origin',config['runtime_repository']],SOURCE)
    current=subprocess.run(['git','rev-parse','HEAD'],cwd=SOURCE,capture_output=True,
                           text=True,encoding='utf-8')
    if current.returncode or current.stdout.strip()!=config['runtime_revision']:
        run(['git','fetch','--depth','1','origin',config['runtime_revision']],SOURCE)
        run(['git','checkout','--detach',config['runtime_revision']],SOURCE)
    # Runtime source retains its own LICENSE and third-party notices.
    run(['cmake','-S',str(SOURCE),'-B',str(SOURCE/'build'),'-DCMAKE_BUILD_TYPE=Release',
         '-DGGML_NATIVE=ON','-DLLAMA_BUILD_TESTS=OFF','-DLLAMA_BUILD_EXAMPLES=OFF',
         '-DLLAMA_BUILD_APP=OFF','-DLLAMA_BUILD_UI=OFF','-DLLAMA_USE_PREBUILT_UI=OFF',
         '-DLLAMA_BUILD_SERVER=ON','-DLLAMA_OPENSSL=OFF'])
    run(['cmake','--build',str(SOURCE/'build'),'--target','llama-server','--parallel',str(jobs)])
    download_model(config,model)
    notice_name = 'MODEL' if model_name == '135m' else 'MODEL-360M'
    notices={
        notice_name+'-README.md':f"https://huggingface.co/{config['gguf_repository']}/resolve/{config['gguf_revision']}/README.md",
        'MODEL-LICENSE-Apache-2.0.txt':'https://www.apache.org/licenses/LICENSE-2.0.txt',
    }
    for name,url in notices.items():
        path=CACHE/name
        if not path.is_file():
            with urllib.request.urlopen(url,timeout=30) as response:data=response.read(100_001)
            if len(data)>100_000:
                raise ValueError('unexpected notice length')
            path.write_bytes(data)
    print(json.dumps({'runtime_revision':config['runtime_revision'],
        'model':config['model'],'gguf_sha256':digest(model),
        'elapsed_seconds':time.perf_counter()-started,'server':str(SERVER),'model_file':str(model)},indent=2))
    print('Next: uv run --frozen --offline python modules/generation-and-sampling/lab/serve.py --model '+model_name,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=2)
    parser.add_argument('--model',choices=['135m','360m'],default='135m')
    args=parser.parse_args()
    prepare(args.jobs,args.model)
