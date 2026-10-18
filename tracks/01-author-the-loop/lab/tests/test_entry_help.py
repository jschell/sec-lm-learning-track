"""The documented entry point must expose the route and preserve old invocations."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]


class EntryHelpTests(unittest.TestCase):
    def invoke(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(ROOT / 'learn.py'), *args],
                              cwd=ROOT, capture_output=True, text=True, check=True)

    def test_top_level_help_lists_routes(self):
        for flag in ('--help', '-h'):
            text = self.invoke(flag).stdout
            for command in ('stage', 'trace', 'transfer', 'check', 'guards', '--scenario'):
                self.assertIn(command, text)

    def test_command_help_still_delegates(self):
        for command in ('stage', 'trace', 'transfer', 'check', 'guards'):
            text = self.invoke(command, '--help').stdout
            self.assertIn('usage:', text.lower())

    def test_existing_scenario_route_still_runs(self):
        output = json.loads(self.invoke('--scenario', 'multi', '--max-calls', '1').stdout)
        self.assertEqual(output['status'], 'tool_limit')
        self.assertEqual(output['tool_calls'], 0)


if __name__ == '__main__':
    unittest.main()
