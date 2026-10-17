"""Read JSONL as data; never evaluate content as Python or shell."""
import json
from pathlib import Path
import sys
if len(sys.argv)!=2:
    raise SystemExit('Usage: inspect_trace.py PATH/trace.jsonl')
for line in Path(sys.argv[1]).read_text().splitlines():
    row=json.loads(line)
    extra=''
    if row['event']=='tool':
        extra=f" {row['call']['id']} {row['call']['name']} is_error={row['result']['is_error']}"
    if row['event']=='stop': extra=' '+row['status']
    if row['event']=='error': extra=' '+row['error_type']+': '+row['message']
    print(f"{row['seq']:02d} {row['event']}{extra}")
