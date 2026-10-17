"""Original math and server-contract tests; synthetic responses are not model runs."""
import copy
from contextlib import redirect_stdout
import io
import json
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

LAB=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(LAB))
import observe
from observe import LocalServer, observe as run_observation, summarize
from sampling import example, probabilities


def response(sampled=False):
    selected={'id':7,'token':'OK'}
    other={'id':9,'token':'Yes'}
    if sampled:
        selected.update(prob=0.6,top_probs=[{'id':7,'token':'OK','prob':0.6},
                                          {**other,'prob':0.2}])
    else:
        selected.update(logprob=math.log(0.6),top_logprobs=[
            {'id':7,'token':'OK','logprob':math.log(0.6)}, {**other,'logprob':math.log(0.2)}])
    return {'model':'synthetic-contract-response','content':'OK','tokens':[7],
            'completion_probabilities':[selected], 'stop_type':'eos', 'truncated':False}


class RecordingServer:
    base_url='http://127.0.0.1:8080'
    def __init__(self):self.calls=[]
    def post(self,path,data):
        self.calls.append((path,copy.deepcopy(data)))
        if path=='/apply-template':return {'prompt':'<user>Reply OK</user><assistant>'}
        if path=='/tokenize':return {'tokens':[1,2,3]}
        return response(data['post_sampling_probs'])


class GenerationChecks(unittest.TestCase):
    def test_softmax_is_stable_and_temperature_changes_concentration(self):
        base=probabilities([1002,1001,1000,999])
        self.assertAlmostEqual(sum(base),1.0)
        self.assertAlmostEqual(base[0],0.6439142598879724)
        self.assertGreater(probabilities([2,1,0,-1],0.5)[0],base[0])
        self.assertLess(probabilities([2,1,0,-1],1.5)[0],base[0])
        self.assertEqual(base,probabilities([2,1,0,-1]))

    def test_top_k_zero_preserves_distribution_and_two_removes_tail(self):
        self.assertEqual(probabilities([2,1,0,-1],top_k=0),probabilities([2,1,0,-1]))
        selected=probabilities([2,1,0,-1],top_k=2)
        self.assertEqual(selected[2:],[0.0,0.0])
        self.assertAlmostEqual(selected[0],0.7310585786300049)
        self.assertEqual(probabilities([1,1,0],top_k=1),[1.0,0.0,0.0])

    def test_invalid_math_inputs_are_explained(self):
        for scores,temp,k in [([],1,0),([math.nan],1,0),([1],0,0),([1],math.inf,0),([1],1,-1)]:
            with self.subTest(args=(scores,temp,k)), self.assertRaises(ValueError):
                probabilities(scores,temp,k)

    def test_seeded_example_is_repeatable_and_explicitly_authored(self):
        self.assertEqual(example(7),example(7))
        self.assertIn('no model inference',example()['source'])
        self.assertNotEqual(example(7)['rows'][1]['ten_samples'],example(8)['rows'][1]['ten_samples'])

    def test_request_formats_and_tokenizes_before_inference(self):
        server=RecordingServer()
        result=run_observation(server,'Reply OK.')
        self.assertEqual([path for path,_ in server.calls],['/apply-template','/tokenize','/completion'])
        sent=server.calls[-1][1]
        self.assertEqual(sent['prompt'],[1,2,3])
        self.assertEqual(sent['n_predict'],8)
        self.assertEqual(sent['temperature'],-1.0)
        self.assertTrue(sent['return_tokens'])
        self.assertFalse(sent['post_sampling_probs'])
        self.assertFalse(sent['cache_prompt'])
        self.assertEqual(result['observation']['generated_ids'],[7])
        self.assertEqual(result['observation']['stop_type'],'eos')

    def test_sample_controls_and_probability_stage_are_explicit(self):
        server=RecordingServer()
        result=run_observation(server,'Reply OK.',mode='sample',temperature=0.5,top_k=5,seed=12)
        sent=server.calls[-1][1]
        self.assertEqual(sent['samplers'],['top_k','temperature'])
        self.assertEqual((sent['temperature'],sent['top_k'],sent['seed']),(0.5,5,12))
        self.assertTrue(sent['post_sampling_probs'])
        self.assertEqual(result['probability_stage'],'after sampling chain')

    def test_top_n_mass_is_not_silently_renormalized(self):
        for sampled in (False,True):
            value=summarize(response(sampled))['token_records'][0]
            self.assertAlmostEqual(value['reported_mass'],0.8)
            self.assertAlmostEqual(value['unreported_mass'],0.2)
            self.assertAlmostEqual(value['top_candidates'][0]['probability'],0.6)

    def test_stop_reason_and_incompatible_schema_are_not_hidden(self):
        value=response();value['stop_type']='limit'
        self.assertEqual(summarize(value)['stop_type'],'limit')
        for field in ('completion_probabilities','tokens','stop_type'):
            value=response();del value[field]
            with self.subTest(field=field),self.assertRaises(ValueError):summarize(value)

    def test_local_endpoint_and_bounded_prompts(self):
        for url in ('https://example.invalid','http://127.0.0.1:8080/path','http://user:key@localhost:8080'):
            with self.subTest(url=url),self.assertRaises(ValueError):LocalServer(url)
        server=RecordingServer()
        with self.assertRaises(ValueError):run_observation(server,'x'*2001)
        self.assertEqual(server.calls,[])

    def test_model_hash_and_missing_setup_are_observable(self):
        import hashlib
        import tempfile
        from prepare import CONFIG, model_ready
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'fixture.gguf'
            path.write_bytes(b'synthetic')
            with patch.dict(CONFIG,{'gguf_bytes':9,'gguf_sha256':hashlib.sha256(b'synthetic').hexdigest()}):
                self.assertTrue(model_ready(path))
                path.write_bytes(b'different')
                self.assertFalse(model_ready(path))
                self.assertFalse(model_ready(Path(temp)/'missing'))

    def test_example_entry_never_constructs_a_server(self):
        with patch.object(sys,'argv',['observe.py','--example']),patch.object(observe,'LocalServer') as server:
            output=io.StringIO()
            with redirect_stdout(output):self.assertEqual(observe.main(),0)
            server.assert_not_called()
            self.assertIn('authored',json.loads(output.getvalue())['source'])

    def test_transport_serializes_json_and_reads_real_wire_shape(self):
        with patch('observe.urllib.request.build_opener') as factory:
            handle=factory.return_value.open.return_value.__enter__.return_value
            handle.read.return_value=json.dumps(response()).encode('utf-8')
            client=LocalServer()
            result=client.post('/completion',{'prompt':[1,2],'n_predict':1})
            request=factory.return_value.open.call_args.args[0]
            self.assertEqual(request.full_url,'http://127.0.0.1:8080/completion')
            self.assertEqual(json.loads(request.data),{'prompt':[1,2],'n_predict':1})
            self.assertEqual(result['content'],'OK')
