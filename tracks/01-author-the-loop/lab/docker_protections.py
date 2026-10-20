"""Bounded actual-runtime assertions for this lab; not escape-resistance proof.

Docker option semantics: https://docs.docker.com/engine/containers/run/
Original project checks. Invoked only by the explicit Docker integration route.
"""
import json
import os
import subprocess
import uuid
from unittest.mock import patch

CREDENTIALS = {'ANTHROPIC_API_KEY': 'synthetic-host-anthropic-not-a-key',
               'OPENROUTER_API_KEY': 'synthetic-host-openrouter-not-a-key'}

# Runs inside the container; never opens an external connection.
PROBE = r'''
import json, os, pathlib, subprocess
status = dict(line.split(':', 1) for line in pathlib.Path('/proc/self/status').read_text().splitlines())
mounts = [line.split() for line in pathlib.Path('/proc/mounts').read_text().splitlines()]
options = lambda target: next(set(row[3].split(',')) for row in mounts if row[1] == target)
def denied(path):
    try:
        with open(path, 'a'): pass
    except OSError: return True
    return False
script = pathlib.Path('/tmp/noexec-probe')
script.write_text('#!/bin/sh\nexit 0\n'); script.chmod(0o700)
try:
    subprocess.run([str(script)], check=True, timeout=2)
    noexec = False
except PermissionError:
    noexec = True
print(json.dumps({'uid':os.geteuid(), 'no_new_privs':status['NoNewPrivs'].strip(),
 'cap_eff':status['CapEff'].strip(), 'interfaces':sorted(os.listdir('/sys/class/net')),
 'root_readonly':'ro' in options('/'), 'grader_readonly':'ro' in options('/grader'),
 'grader_write_denied':denied('/grader/check.py'), 'tmp_options':sorted(options('/tmp')),
 'tmp_noexec':noexec, 'environment':dict(os.environ)}))
'''


def failures(config: dict, observed: dict) -> set[str]:
    """Name failed protections using inspect data plus in-container observations."""
    host = config['HostConfig']
    checks = {
        'non_root': config['Config']['User'] == '65534:65534' and observed['uid'] == 65534,
        'no_new_privileges': observed['no_new_privs'] == '1',
        'capabilities': 'ALL' in (host.get('CapDrop') or []) and int(observed['cap_eff'], 16) == 0,
        'readonly_root': host['ReadonlyRootfs'] and observed['root_readonly'],
        'readonly_grader': observed['grader_readonly'] and observed['grader_write_denied'],
        'network': host['NetworkMode'] == 'none' and observed['interfaces'] == ['lo'],
        'tmpfs': {'rw','nosuid','nodev','noexec'}.issubset(observed['tmp_options'])
                 and observed['tmp_noexec'] and 'size=8m' in host['Tmpfs'].get('/tmp', ''),
        'resources': host['PidsLimit'] == 32 and host['Memory'] == 128*1024*1024
                     and host['MemorySwap'] == 128*1024*1024 and host['NanoCpus'] == 500000000,
        'credentials': all(name not in observed['environment'] for name in CREDENTIALS)
             and all(value not in json.dumps(observed) for value in CREDENTIALS.values()),
    }
    return {name for name, passed in checks.items() if not passed}


def observe(executor, mutation: str | None = None) -> tuple[dict, dict]:
    """Inspect one disposable container, always remove it, bound every CLI wait."""
    name = 'loop-lab-protection-' + uuid.uuid4().hex
    args = executor.argv('sleep 60', name)
    args[args.index('--rm')] = '--detach'
    removals = {'non_root': ('--user', '65534:65534'),
                'no_new_privileges': ('--security-opt=no-new-privileges',),
                'capabilities': ('--cap-drop=ALL',),
                'readonly_root': ('--read-only',), 'network': ('--network=none',)}
    for item in removals.get(mutation, ()):
        args.remove(item)
    if mutation == 'tmpfs':
        index = args.index('/tmp:rw,nosuid,nodev,noexec,size=8m')
        args[index] = '/tmp:rw,nosuid,nodev,size=8m'
    if mutation == 'readonly_grader':
        index = args.index(f'type=bind,src={executor.grader},dst=/grader,readonly')
        args[index] = f'type=bind,src={executor.grader},dst=/grader'
    # Deliberately seed host-only synthetic credentials, restored immediately.
    with patch.dict(os.environ, CREDENTIALS):
        try:
            subprocess.run(args, check=True, capture_output=True, timeout=20)
            config = json.loads(subprocess.run(['docker','inspect',name], check=True,
                capture_output=True, text=True, timeout=10).stdout)[0]
            result = subprocess.run(['docker','exec',name,'python','-c',PROBE], check=True,
                capture_output=True, text=True, timeout=10)
            return config, json.loads(result.stdout)
        finally:
            subprocess.run(['docker','rm','-f',name],check=True,capture_output=True,timeout=10)


def verify(executor) -> None:
    """Check effective protections, then prove targeted removals are detected."""
    found = failures(*observe(executor))
    assert not found, f'effective protection check failed: {sorted(found)}'
    for protection in ('non_root','no_new_privileges','capabilities','readonly_root',
                       'readonly_grader','network','tmpfs'):
        found = failures(*observe(executor, protection))
        assert protection in found, f'removal of {protection} was not detected: {found}'
    print('PASS: effective Docker protections, two seeded host credentials, seven removal probes')
