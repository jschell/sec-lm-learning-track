"""Behavioral checks against the pinned tokenizer and its real chat template."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from assets import checked_assets
from inspect_input import encode, inspect, load, render


class ModelInputChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer, cls.template = load()
        cls.fixture = json.loads((LAB/'fixtures.json').read_text(encoding='utf-8'))

    def test_original_text_roundtrips_and_pinned_ids(self):
        expected = {'prose':6, 'code':11, 'log':16, 'unicode':4}
        for name,text in self.fixture['texts'].items():
            with self.subTest(name=name):
                value = encode(self.tokenizer,text)
                self.assertEqual(value['decoded'],text)
                self.assertEqual(value['count'],expected[name])
        self.assertEqual(encode(self.tokenizer,self.fixture['texts']['prose'])['ids'],
                         [33876,63956,18511,1841,21853,13])

    def test_role_markers_are_special_tokens_and_decode_is_explicit(self):
        marker = '<|im_start|>'
        value = encode(self.tokenizer,marker)
        self.assertEqual(value['ids'],[151644])
        self.assertEqual(value['decoded'],marker)
        self.assertEqual(self.tokenizer.decode(value['ids'],skip_special_tokens=True),'')
        self.assertEqual(self.tokenizer.token_to_id('<|im_end|>'),151645)

    def test_plain_render_and_generation_suffix(self):
        messages = self.fixture['messages'][:2]
        complete = render(self.template,messages,[],False)
        next_turn = render(self.template,messages,[],True)
        self.assertEqual(next_turn, complete + '<|im_start|>assistant\n')
        self.assertTrue(complete.startswith('<|im_start|>system\n'))
        self.assertIn('<|im_start|>user\nCount lines in notes.txt.',complete)
        self.assertNotIn('<tools>',complete)
        self.assertEqual(encode(self.tokenizer,next_turn)['count'],28)

    def test_tool_definition_call_and_result_survive_rendering(self):
        value = inspect('tool')
        text = value['rendered']['text']
        self.assertIn('<tools>\n',text)
        self.assertIn('"name": "count_lines"',text)
        self.assertIn('<tool_call>\n',text)
        self.assertIn('<tool_response>\n{"path":"notes.txt","lines":2}',text)
        self.assertEqual(text,value['rendered']['decoded'])

    def test_omission_removes_feedback_but_retains_tool_definition(self):
        full, omitted, plain = (inspect(v) for v in ('tool','omitted','plain'))
        self.assertIn('<tools>',omitted['rendered']['text'])
        self.assertNotIn('<tool_response>',omitted['rendered']['text'])
        self.assertNotIn('"lines":2',omitted['rendered']['text'])
        self.assertGreater(full['rendered']['count'],omitted['rendered']['count'])
        self.assertGreater(omitted['rendered']['count'],plain['rendered']['count'])

    def test_missing_or_altered_asset_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            with self.assertRaisesRegex(ValueError,'Missing or altered'):
                checked_assets(path)
            (path/'tokenizer.json').write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Missing or altered tokenizer.json'):
                checked_assets(path)
