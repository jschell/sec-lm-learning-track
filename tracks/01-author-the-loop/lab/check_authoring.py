"""Small offline protocol checks for lesson 1/2 starter functions."""
import argparse
import importlib.util
from pathlib import Path
import tempfile
from loop import Replay, Tools, Workspace

HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--file', type=Path, required=True)
p.add_argument('--stage', type=int, choices=[1, 2], required=True)
a = p.parse_args()
spec = importlib.util.spec_from_file_location('exercise', a.file.resolve())
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if a.stage == 1:
    result = module.infer_once(Replay(HERE/'replay/inference.json'), 'Explain the exchange.')
    assert result['stop_reason'] == 'end_turn'
    assert result['content'][0]['type'] == 'text'
else:
    with tempfile.TemporaryDirectory() as temp:
        (Path(temp)/'notes.txt').write_text((HERE/'fixtures/notes.txt').read_text())
        result, history = module.exchange(Replay(HERE/'replay/read.json'),
                                         Tools(Workspace(temp)), 'Read notes.txt.')
        assert [m['role'] for m in history] == ['user','assistant','user']
        call = history[1]['content'][0]
        answer = history[2]['content'][0]
        assert answer['tool_use_id'] == call['id']
        assert not answer['is_error']
        assert result['stop_reason'] == 'end_turn'
print(f'PASS lesson {a.stage}: synthetic protocol check (not a live model test)')
