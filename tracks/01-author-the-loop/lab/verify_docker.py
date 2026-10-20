"""Genuine Docker integration checks; never executes candidate code on the host."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile
from docker_protections import verify
from loop import DockerExecutor, Workspace, Tools, Trace, Replay, run_loop, COMMAND_OUTPUT_BYTES

HERE = Path(__file__).resolve().parent
if shutil.which('docker') is None:
    raise SystemExit('Docker is required. No host fallback; no integration tests ran.')
subprocess.run(['docker','image','inspect','python:3.12-slim'],check=True,stdout=subprocess.DEVNULL)
with tempfile.TemporaryDirectory(prefix='loop-docker-') as temp:
    root=Path(temp)
    root.chmod(0o755)
    work=root/'work'
    shutil.copytree(HERE/'fixtures',work)
    work.chmod(0o777)
    for f in work.iterdir(): f.chmod(0o666)
    executor=DockerExecutor(work,HERE/'grader')
    verify(executor)
    before=executor.run('python -I /grader/check.py')
    assert before['exit_code'] == 1 and 'FAIL' in before['output'], before
    # Actual read/edit tool calls; only replace scripted command expectations.
    turns=json.loads((HERE/'replay/repair.json').read_text())
    for turn in turns['turns']:
        for check in turn.get('checks',[]):
            check['contains']=check.get('contains','').replace('SCRIPTED OBSERVATION: ','')
    replay_path=root/'actual.json'
    replay_path.write_text(json.dumps(turns))
    trace=Trace(root/'trace.jsonl')
    try:
        result=run_loop(Replay(replay_path),Tools(Workspace(work),executor),
                        'Repair the exercise',trace)
    finally: trace.close()
    assert result['status']=='completed', result
    after=executor.run('python -I /grader/check.py')
    assert after['exit_code']==0 and 'PASS' in after['output'], after
    denied=executor.run("echo changed > /grader/check.py")
    assert denied['exit_code']!=0, denied
    output=executor.run("python -c 'print(\"x\" * 10000)'")
    assert output['truncated'] and len(output['output'])<=4096, output
    unicode_output=executor.run("python -c 'print(chr(0x20ac) * 5000)'")
    # Retain 4096 source bytes; a split UTF-8 character is decoded with replacement.
    assert unicode_output['truncated'], unicode_output
    assert unicode_output['output'] == '€' * (COMMAND_OUTPUT_BYTES // 3) + '\ufffd', unicode_output
    stopped=executor.run("python -c 'import subprocess,time; subprocess.Popen([\"sleep\",\"60\"]); time.sleep(60)'")
    assert stopped['timed_out'], stopped
    running=subprocess.run(['docker','ps','-aq','--filter','name=loop-lab-'],capture_output=True,text=True,check=True)
    assert not running.stdout.strip(), 'Lab containers remain: '+running.stdout
    print('PASS: actual FAIL→edit→PASS, read-only grader, absent credential, bounded output, timeout/child cleanup')
