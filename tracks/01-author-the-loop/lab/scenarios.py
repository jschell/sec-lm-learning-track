"""Synthetic command observations for replay. No command or candidate code runs."""
class ScriptedExecutor:
    def __init__(self):
        self.calls = 0

    def run(self, command):
        if command != 'python -I /grader/check.py':
            raise ValueError('scripted executor only recognizes the fixed grading command')
        self.calls += 1
        if self.calls == 1:
            return {'exit_code': 1, 'timed_out': False, 'truncated': False,
                    'output': 'SCRIPTED OBSERVATION: FAIL n=15: actual fifteenth value Fizz'}
        if self.calls == 2:
            return {'exit_code': 0, 'timed_out': False, 'truncated': False,
                    'output': 'SCRIPTED OBSERVATION: PASS: fixed grader checked n=0,1,5,15,30'}
        raise ValueError('scripted command observations exhausted')
