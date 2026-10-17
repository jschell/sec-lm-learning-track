"""Observe an already-running local llama.cpp model; no setup or model download.

Protocol target and limits: ../SOURCES.md. Outputs contain synthetic prompts only.
"""
import argparse
import json
import math
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

from sampling import example

HERE = Path(__file__).resolve().parent


class LocalServer:
    """JSON client for a user-configured loopback llama.cpp server, without retries."""
    def __init__(self, base_url: str = 'http://127.0.0.1:8080') -> None:
        url = urllib.parse.urlsplit(base_url)
        if url.scheme != 'http' or url.hostname not in {'127.0.0.1','localhost','::1'}:
            raise ValueError('use an already-configured HTTP loopback llama.cpp server')
        if url.username or url.password or url.path not in {'','/'} or url.query or url.fragment:
            raise ValueError('base URL must contain only the local host and port')
        self.base_url = base_url.rstrip('/')
        self.opener = urllib.request.build_opener(NoRedirect())

    def post(self, path: str, data: dict) -> dict:
        request = urllib.request.Request(self.base_url + path,
            data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'}, method='POST')
        try:
            with self.opener.open(request, timeout=60) as response:
                raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError('server response exceeded the observation limit')
            value = json.loads(raw)
            if not isinstance(value,dict):
                raise ValueError('server response must be a JSON object')
            return value
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f'Local server HTTP {exc.code}; check the native endpoint/build. No retry.') from None
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError('Local server unavailable or timed out; see setup assumptions in the lesson.') from None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def probability(row: dict) -> float:
    """Convert the endpoint's explicit probability or natural-log probability."""
    if 'prob' in row:
        value = row['prob']
    elif 'logprob' in row and isinstance(row['logprob'], (int,float)) and row['logprob'] <= 0:
        value = math.exp(row['logprob'])
    else:
        raise ValueError('missing/invalid prob or logprob; incompatible server response')
    if not isinstance(value,(int,float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('invalid token probability')
    return float(value)


def summarize(response: dict) -> dict:
    """Retain reported IDs/stop reason and show top-N mass without renormalizing."""
    records = response.get('completion_probabilities')
    if not isinstance(records,list) or not records:
        raise ValueError('completion_probabilities missing/empty; inspect server compatibility')
    rows = []
    for index, record in enumerate(records):
        candidates = record.get('top_probs',record.get('top_logprobs'))
        if not isinstance(candidates,list):
            raise ValueError('top_probs/top_logprobs missing; incompatible server response')
        top = [{'id':item['id'], 'token':item['token'], 'probability':probability(item)}
               for item in candidates]
        mass = sum(item['probability'] for item in top)
        if mass > 1.0001:
            raise ValueError('returned candidate mass exceeds one')
        rows.append({'step':index + 1, 'selected_id':record['id'],
                     'selected_piece':record['token'], 'selected_probability':probability(record),
                     'top_candidates':top, 'reported_mass':mass,
                     'unreported_mass':max(0.0,1.0 - mass)})
    if response.get('stop_type') not in {'eos','limit','word'}:
        raise ValueError('missing/unsupported terminal stop_type; inspect server build')
    if not isinstance(response.get('tokens'),list) or any(type(x) is not int for x in response['tokens']):
        raise ValueError('generated token IDs unavailable; requires return_tokens support')
    return {'reported_model':response.get('model'), 'content':response['content'],
            'generated_ids':response['tokens'], 'token_records':rows,
            'stop_type':response['stop_type'], 'context_truncated':response.get('truncated'),
            'timings':response.get('timings'), 'generation_settings':response.get('generation_settings')}


def observe(server: LocalServer, prompt: str, mode: str = 'greedy', temperature: float = 1.0,
            top_k: int = 0, seed: int = 7, max_tokens: int = 8) -> dict:
    """Format the same synthetic input, then request one bounded completion."""
    if mode not in {'greedy','sample'} or not 1 <= max_tokens <= 64:
        raise ValueError('choose greedy/sample and 1–64 generated tokens')
    if not math.isfinite(temperature) or not 0.05 <= temperature <= 2 or not 0 <= top_k <= 100:
        raise ValueError('temperature must be 0.05–2; top_k must be 0–100')
    if mode == 'greedy' and top_k != 0:
        raise ValueError('top_k variation belongs to sample mode in this lesson')
    if not prompt or len(prompt) > 2000:
        raise ValueError('use a nonempty synthetic prompt up to 2000 characters')
    formatted = server.post('/apply-template', {'messages':[{'role':'user','content':prompt}]})['prompt']
    tokenized = server.post('/tokenize', {'content':formatted,'add_special':False,'parse_special':True})['tokens']
    if not tokenized or len(tokenized) > 256:
        raise ValueError('use a formatted prompt of at most 256 tokens')
    request = {'prompt':tokenized, 'n_predict':max_tokens, 'stream':False,
               'return_tokens':True, 'n_probs':8, 'seed':seed, 'cache_prompt':False,
               'temperature':-1.0 if mode == 'greedy' else temperature,
               'top_k':top_k, 'samplers':['top_k','temperature'],
               'post_sampling_probs':mode == 'sample'}
    started = time.perf_counter()
    response = server.post('/completion',request)
    return {'source':'local server response; model identity/suitability require validation',
            'expected_model':'SmolLM2-135M-Instruct', 'endpoint':server.base_url,
            'prompt':prompt, 'formatted_prompt':formatted, 'prompt_ids':tokenized,
            'mode':mode, 'probability_stage':'after sampling chain' if mode == 'sample' else 'greedy request; simple softmax scores',
            'request':request, 'wall_seconds':time.perf_counter() - started,
            'observation':summarize(response)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default='http://127.0.0.1:8080')
    parser.add_argument('--task',choices=['reply','extract','rewrite','opposite'],default='reply')
    parser.add_argument('--mode',choices=['greedy','sample'],default='greedy')
    parser.add_argument('--temperature',type=float,default=1.0)
    parser.add_argument('--top-k',type=int,default=0)
    parser.add_argument('--seed',type=int,default=7)
    parser.add_argument('--max-tokens',type=int,default=8)
    parser.add_argument('--repeat',type=int,choices=[1,2],default=1)
    parser.add_argument('--example',action='store_true',help='Calculate an authored score vector; no server call')
    args = parser.parse_args()
    if args.example:
        print(json.dumps(example(args.seed),indent=2))
        return 0
    prompts = json.loads((HERE/'prompts.json').read_text(encoding='utf-8'))
    server = LocalServer(args.base_url)
    try:
        runs = [observe(server,prompts[args.task]['prompt'],args.mode,args.temperature,
                        args.top_k,args.seed,args.max_tokens) for _ in range(args.repeat)]
    except (ValueError,RuntimeError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'observation unavailable','message':str(exc)}))
        return 1
    print(json.dumps({'task':args.task, 'task_check':prompts[args.task]['check'], 'runs':runs,
        'repeated_ids_equal':runs[0]['observation']['generated_ids']==runs[1]['observation']['generated_ids']
                            if len(runs)==2 else None},ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
