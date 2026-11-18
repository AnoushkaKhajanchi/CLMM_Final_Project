import unittest,sys,json,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from protocol import strict_calls,retrieve_entries,writer_suffix,diagnostic_cases,reader_messages,require_reader_controls,numbered_lines
ROOT=Path(__file__).resolve().parents[1]
class ProtocolTests(unittest.TestCase):
 def test_reject_truncated_json(self):
  good={'name':'new_memory_insert','arguments':'{"memory_type":"semantic_memory","content":"a"}'}
  bad={'name':'new_memory_insert','arguments':'{"memory_type":"semantic_memory","content":"Urs'}
  a,r,rep=strict_calls([{'function_call':good},{'function_call':bad}])
  self.assertEqual(len(a),1);self.assertEqual(len(r),1);self.assertEqual(rep,[])
 def test_repair_bracket_typo_keeps_every_fact(self):
  # Seen in run week3_dev_memalpha_baseline_locked_r2_01: whole-chunk notes closed with "] not "}.
  typo={'name':'new_memory_insert','arguments':'{"memory_type": "semantic_memory", "content": "1. Ada lives in Rome.\\n2. Ben likes chess."]'}
  a,r,rep=strict_calls([{'function_call':typo}])
  self.assertEqual((len(a),len(r),len(rep)),(1,0,1))
  self.assertEqual(a[0]['arguments']['content'],'1. Ada lives in Rome.\n2. Ben likes chess.')
 def test_retrieval_covers_every_incoming_fact(self):
  # Ten changed facts in one chunk: each old note must be offered (a fixed top-6 could not).
  people=['Ada','Ben','Cy','Dot','Eve','Fay','Gus','Hal','Ivy','Jo']
  state={'core':'','semantic':[{f'id{i}':f'[source_fact_id={i}] {p} lives in Paris.'} for i,p in enumerate(people)]+[{'blk':'\n'.join(f'[source_fact_id={30+i}] Person{i} likes chess.' for i in range(16))}],'episodic':[]}
  chunk='\n'.join(f'{50+i}. {p} lives in Rome.' for i,p in enumerate(people))
  ids={c['memory_id'] for c in retrieve_entries(state,chunk)}
  self.assertTrue({f'id{i}' for i in range(10)}<=ids)
 def test_provenance_tag_anywhere_on_line(self):
  state={'semantic':[{'a':'[source_fact_id=1] Ada lives in Rome.\nBen likes chess. [source_fact_id=2]\nNo tag here.'}]}
  self.assertEqual(numbered_lines(state)['annotated_lines'],2)
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
   n=json.loads(p.read_text())
   for c in n['cells']:c['source']=''.join(c['source'])  # Jupyter allows a string or a list of lines
   code='\n'.join(c['source'] for c in n['cells'] if c['cell_type']=='code')
   for c in n['cells']:
    if c['cell_type']=='code':ast.parse(c['source']);self.assertEqual(c['outputs'],[])
   self.assertIn('MAX_INPUT_PLUS_OUTPUT = 16384',code)
   self.assertIn('revisions = dict(PINNED_REVISIONS)',code)
   self.assertNotIn("['reserved_final']\n",code)
   assignments=[node for c in n['cells'] if c['cell_type']=='code' for node in ast.parse(c['source']).body if isinstance(node,ast.Assign)]
   embedded=next(ast.literal_eval(a.value) for a in assignments if any(isinstance(t,ast.Name) and t.id=='PROTOCOL_SOURCE' for t in a.targets))
   self.assertEqual(embedded,protocol)
 def test_reader_instruction_separation(self):
  messages=reader_messages('1. Ben likes chess.', 'What does Ben like?', 'explicit', 'Question: {question}')
  self.assertIn('<question>\nWhat does Ben like?\n</question>',messages[1]['content'])
  self.assertNotIn('Resolve',messages[1]['content'])
  self.assertIn('NOT its answer',messages[0]['content'])
  original=reader_messages('facts','actual question','original','Question: {question}')
  self.assertTrue(original[1]['content'].endswith('Question: actual question'))
 def test_reader_gate(self):
  good={'exact_match':1,'generation':{'hit_output_limit':False}}
  self.assertTrue(require_reader_controls([good]*4))
  for results in [[],[good]*3,[good]*3+[{'exact_match':0,'generation':{'hit_output_limit':False}}],
                  [good]*3+[{'exact_match':1,'generation':{'hit_output_limit':True}}]]:
   with self.assertRaises(RuntimeError):require_reader_controls(results)
 def test_diagnostic_matrix(self):
  cases=diagnostic_cases();self.assertEqual(len(cases),6)
  hidden=next(c for c in cases if c['id']=='hidden')
  self.assertNotIn('Ada',' '.join(hidden['seed'][-5:]))
if __name__=='__main__':unittest.main()
