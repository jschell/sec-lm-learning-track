"""Read JSONL as data; never evaluate content as Python or shell."""
import json
from pathlib import Path
import sys
if len(sys.argv)!=2:
    raise SystemExit('Usage: inspect_trace.py PATH/trace.jsonl')
for line in Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
    row=json.loads(line)
    extra=''
    if row['event']=='tool':
        extra=f" {row['call']['id']} {row['call']['name']} is_error={row['result']['is_error']}"
        extra+=' result='+json.dumps(row['result']['content'][:240],ensure_ascii=False)
    if row['event']=='response':
        text=' '.join(b.get('text','') for b in row['response'].get('content',[]) if b.get('type')=='text')
        if text: extra=' text='+json.dumps(text[:240],ensure_ascii=False)
    if row['event']=='stop': extra=' '+row['status']
    if row['event']=='error': extra=' '+row['error_type']+': '+row['message']
    print(f"{row['seq']:02d} {row['event']}{extra}")
