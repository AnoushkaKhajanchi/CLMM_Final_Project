"""CPU-only final SEMANTIC-memory exact-presence proxies; not a semantic truth judge.
Usage: python week_3/scripts/audit_memory.py RUN/example_id
Supports source_fact_id annotations. Never used by the writer or retriever.
"""
import json,re,sys
from pathlib import Path
from collections import defaultdict,Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'week_2/scripts'))
from count_conflicts import split_fact

def normalize(s):
 s=re.sub(r'^\s*\[source_fact_id=\d+\]\s*','',s)
 s=re.sub(r'^\s*\d+\.\s*','',s)
 return s.strip(" .'\"").lower()

def audit(folder):
 folder=Path(folder)
 state=json.loads((folder/'memory_final.json').read_text())
 context=''.join(json.loads((folder/'chunks.json').read_text()))
 source={int(i):fact for i,fact in re.findall(r'^(\d+)\. (.+)$',context,re.M)}
 lines=[line for e in state['semantic'] for text in e.values() for line in text.splitlines() if line.strip()]
 stored={normalize(line) for line in lines}
 groups=defaultdict(list);unparsed=[];provenance=[]
 for number,fact in source.items():
  parsed=split_fact(fact)
  if parsed:groups[parsed[0]].append((number,fact,parsed[1]))
  else:unparsed.append(number)
 for line in lines:
  m=re.match(r'^\s*\[source_fact_id=(\d+)\]\s*(.*)',line)
  if not m:status='missing_marker'
  elif int(m[1]) not in source:status='unknown_source_id'
  elif normalize(m[2])==normalize(source[int(m[1])]):status='exact_source_match'
  else:status='wording_differs_review_required'
  provenance.append({'line':line,'status':status})
 conflicts=[];nonconflicting=[]
 for key,facts in groups.items():
  facts.sort();latest=facts[-1]
  if len({f[2] for f in facts})==1:
   nonconflicting.append({'key':key,'retained_exactly':normalize(latest[1]) in stored});continue
  old=[f for f in facts[:-1] if f[2]!=latest[2]]
  old_kept=any(normalize(f[1]) in stored for f in old);new_kept=normalize(latest[1]) in stored
  conflicts.append({'key':key,'old_numbers':[f[0] for f in old],'latest_number':latest[0],
   'old_present_exactly':old_kept,'new_present_exactly':new_kept,
   'outcome':{(True,True):'both',(True,False):'only_old',(False,True):'only_new',(False,False):'neither'}[(old_kept,new_kept)]})
 return {'scope':'final semantic memory only; exact-wording proxies, not active-stale truth labels',
  'conflict_groups':len(conflicts),'outcomes':dict(Counter(c['outcome'] for c in conflicts)),
  'old_present_count':sum(c['old_present_exactly'] for c in conflicts),
  'latest_present_count':sum(c['new_present_exactly'] for c in conflicts),
  'nonconflicting_relation_groups':len(nonconflicting),
  'nonconflicting_retained_exactly':sum(c['retained_exactly'] for c in nonconflicting),
  'unparsed_source_ids':unparsed,'provenance_counts':dict(Counter(p['status'] for p in provenance)),
  'conflicts':conflicts,'nonconflicting':nonconflicting,'provenance':provenance,
  'warning':'Paraphrases and explicit historical labels require manual review. An only_new outcome alone does not prove an old fact was removed; inspect the before/after trace. Core and episodic content are not scored here.'}
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2))
