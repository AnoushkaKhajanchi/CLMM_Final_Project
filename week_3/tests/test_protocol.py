import unittest,sys,json,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from protocol import strict_calls,retrieve_entries,writer_suffix,diagnostic_cases
ROOT=Path(__file__).resolve().parents[1]
class ProtocolTests(unittest.TestCase):
 def test_reject_truncated_json(self):
  good={'name':'new_memory_insert','arguments':'{"memory_type":"semantic_memory","content":"a"}'}
  bad={'name':'new_memory_insert','arguments':'{"memory_type":"semantic_memory","content":"Urs'}
  a,r=strict_calls([{'function_call':good},{'function_call':bad}])
  self.assertEqual(len(a),1);self.assertEqual(len(r),1)
 def test_hidden_retrieval_preserves_whole_note(self):
  state={'core':'','semantic':[{'old':'[source_fact_id=1] Ada lives in Paris.\n[source_fact_id=2] Ben likes chess.'}]+[{str(i):f'Person{i} likes gardening.'} for i in range(8)],'episodic':[]}
  found=retrieve_entries(state,'20. Ada now lives in Rome.')
  self.assertEqual(found[0]['memory_id'],'old');self.assertIn('Ben likes chess',found[0]['content'])
  suffix,c=writer_suffix(state,'20. Ada now lives in Rome.','baseline');self.assertEqual(c,[])
 def test_split(self):
  s=json.loads((ROOT/'docs/question_split.json').read_text())
  self.assertIn('uncertain',s['exposure_status'])
  for task in s['tasks'].values():
   d,f=map(set,(task['development'],task['reserved_final']))
   self.assertEqual(len(d),20);self.assertEqual(len(f),80)
   self.assertFalse(d&f);self.assertEqual(d|f,set(range(100)));self.assertTrue(set(range(5))<=d)
 def test_notebooks(self):
  protocol=(ROOT/'scripts/protocol.py').read_text()
  for p in (ROOT/'notebooks').glob('*.ipynb'):
   n=json.loads(p.read_text());code='\n'.join(c['source'] for c in n['cells'] if c['cell_type']=='code')
   for c in n['cells']:
    if c['cell_type']=='code':ast.parse(c['source']);self.assertEqual(c['outputs'],[])
   self.assertIn('MAX_INPUT_PLUS_OUTPUT = 16384',code)
   self.assertIn('revisions = dict(PINNED_REVISIONS)',code)
   self.assertNotIn("['reserved_final']\n",code)
   assignments=[node for c in n['cells'] if c['cell_type']=='code' for node in ast.parse(c['source']).body if isinstance(node,ast.Assign)]
   embedded=next(ast.literal_eval(a.value) for a in assignments if any(isinstance(t,ast.Name) and t.id=='PROTOCOL_SOURCE' for t in a.targets))
   self.assertEqual(embedded,protocol)
 def test_diagnostic_matrix(self):
  cases=diagnostic_cases();self.assertEqual(len(cases),6)
  hidden=next(c for c in cases if c['id']=='hidden')
  self.assertNotIn('Ada',' '.join(hidden['seed'][-5:]))
if __name__=='__main__':unittest.main()
