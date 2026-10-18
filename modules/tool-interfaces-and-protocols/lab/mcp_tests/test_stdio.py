"""Real SDK/subprocess integration; fixed calls, no model."""
import asyncio
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from direct import run as direct_run
from mcp_demo import run as mcp_run


class StdioTests(unittest.TestCase):
    def test_stdio_matches_direct_and_wire_results_match_request_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            direct = direct_run(root / 'direct')
            mcp = asyncio.run(asyncio.wait_for(mcp_run(root / 'mcp'), timeout=20))
            self.assertEqual([r['outcome'] for r in direct['calls']], [r['outcome'] for r in mcp['calls']])
            self.assertEqual(mcp['execution_count'], 3)
            self.assertEqual(mcp['connection']['protocol_version'], '2026-07-28')
            messages = [json.loads(line) for line in (root / 'mcp/messages.jsonl').read_text(encoding='utf-8').splitlines()]
            sent = {row['message']['id']: row['message'] for row in messages
                    if row['direction'] == 'client_to_server' and 'id' in row['message']}
            received = {row['message']['id']: row['message'] for row in messages
                        if row['direction'] == 'server_to_client' and 'id' in row['message']}
            self.assertEqual(set(sent), set(received))
            methods = [message['method'] for message in sent.values()]
            self.assertIn('server/discover', methods)
            self.assertIn('tools/list', methods)
            wire_calls = [received[key]['result'] for key, request in sent.items() if request['method'] == 'tools/call']
            self.assertEqual(len(wire_calls), 6)
            self.assertEqual([r['isError'] for r in wire_calls], [False, True, True, False, True, True])
            self.assertEqual(wire_calls[0]['structuredContent'], mcp['calls'][0]['outcome'])
            discovered = json.loads((root / 'mcp/discovered-tools.json').read_text(encoding='utf-8'))
            self.assertEqual(len(discovered['tools']), 1)
            self.assertEqual(discovered['tools'][0]['inputSchema'], direct['definition']['inputSchema'])
            audit = [json.loads(line) for line in (root / 'mcp/executions.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual([r['event_id'] for r in audit], ['E001', 'E999', 'E500'])
            self.assertTrue((root / 'mcp/feedback-example.json').is_file())


if __name__ == '__main__':
    unittest.main()
