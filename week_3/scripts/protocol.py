"""CPU-only Week 3 protocol helpers. No benchmark answers enter writer decisions."""
import json
import re
from collections import Counter

PROVENANCE = '''Preserve the original source number on EVERY stored fact line as [source_fact_id=N].
Use only numbers present in the supplied source or existing memory; never invent or renumber them.
Copying or rewriting a fact does not change its source number. A note with several facts needs a number on each fact line.
Operation timestamps and chunk indices are NOT freshness evidence. Preserve these annotations for the answering model.'''
CONFLICT = '''Before writing, check whether incoming facts conflict with existing memory.
For the SAME subject and relation, a larger source fact number supersedes a smaller one.
Update the existing entry to the newer fact when appropriate; identical facts need no duplicate.
Unrelated facts and legitimately coexisting facts must remain. If a note contains several facts,
edit only the conflicting part and preserve all other lines and their original numbers.
Use the actual memory ID for update/delete tools. Do not delete a whole multi-fact note to remove one fact.'''

def strict_calls(messages):
    accepted, rejected = [], []
    for message in messages:
        call = message.get('function_call')
        if not call:
            continue
        try:
            args = call['arguments']
            if isinstance(args, str):
                args = json.loads(args)
            if not isinstance(args, dict):
                raise ValueError('Arguments must be a JSON object')
            if call['name'] not in {'new_memory_insert', 'memory_update', 'memory_delete', 'search_memory'}:
                raise ValueError('Unknown tool')
            accepted.append({'name': call['name'], 'arguments': args})
        except (ValueError, KeyError, TypeError) as error:
            rejected.append({'raw_call': call, 'reason': str(error)})
    return accepted, rejected

def tokens(text):
    return set(re.findall(r'[a-z]+', text.lower())) - {'the','is','in','of','a','an','and','with','to','source','fact','id'}

def retrieve_entries(state, chunk, k=6):
    """Lexical overlap, ranked per incoming line then globally; includes whole notes.
    No gold conflict parser, answers, or future facts are used. Zero-overlap entries are excluded.
    """
    queries = [tokens(line) for line in chunk.splitlines() if line.strip()]
    candidates = []
    for kind in ['semantic', 'episodic']:
        for entry in state[kind]:
            for mid, content in entry.items():
                words = tokens(content)
                score = max((len(q & words) / max(1, len(q)) for q in queries), default=0)
                if score:
                    candidates.append({'memory_type': kind+'_memory', 'memory_id': mid,
                                       'content': content, 'retrieval_score': score})
    return sorted(candidates, key=lambda e: (-e['retrieval_score'], e['memory_type'], e['memory_id']))[:k]

def writer_suffix(state, chunk, condition):
    if condition not in {'baseline','prompted','retrieval'}:
        raise ValueError(condition)
    candidates = retrieve_entries(state, chunk) if condition == 'retrieval' else []
    suffix = '\n\n' + PROVENANCE
    if condition != 'baseline':
        suffix += '\n\n' + CONFLICT
    if candidates:
        suffix += '\n\nExisting candidate notes (not new facts):\n' + json.dumps(candidates, ensure_ascii=False)
    return suffix, candidates

def numbered_lines(state):
    """Diagnostics only: counts IDs and malformed/missing fact-line markers, not semantic correctness."""
    lines = [line for e in state['semantic'] for text in e.values() for line in text.splitlines() if line.strip()]
    annotated = [line for line in lines if re.match(r'^\s*\[source_fact_id=\d+\]', line)]
    return {'semantic_nonempty_lines': len(lines), 'annotated_lines': len(annotated),
            'missing_marker_lines': len(lines)-len(annotated)}

def diagnostic_cases():
    old = '[source_fact_id=1] Ada lives in Paris.'
    unrelated = '[source_fact_id=2] Ben likes chess.'
    fillers = [f'[source_fact_id={i+3}] Person{i} likes gardening.' for i in range(6)]
    return [
        {'id':'visible','seed':[old, unrelated], 'incoming':'20. Ada now lives in Rome.', 'expected_new':'Rome', 'expected_old':'Paris', 'retain':'Ben likes chess'},
        {'id':'hidden','seed':[old, unrelated]+fillers, 'incoming':'20. Ada now lives in Rome.', 'expected_new':'Rome', 'expected_old':'Paris', 'retain':'Ben likes chess'},
        {'id':'block','seed':[old+'\n'+unrelated], 'incoming':'20. Ada now lives in Rome.', 'expected_new':'Rome', 'expected_old':'Paris', 'retain':'Ben likes chess'},
        {'id':'duplicate','seed':[old,unrelated], 'incoming':'1. Ada lives in Paris.', 'expected_new':'Paris','expected_old':None,'retain':'Ben likes chess'},
        {'id':'coexist','seed':['[source_fact_id=1] Ada likes painting.',unrelated], 'incoming':'20. Ada also likes hiking.', 'expected_new':'hiking','expected_old':None,'retain':'Ada likes painting'},
        {'id':'older_arrives_late','seed':['[source_fact_id=20] Ada lives in Rome.',unrelated], 'incoming':'1. Ada lived in Paris at source time 1.', 'expected_new':'Rome','expected_old':None,'retain':'Ben likes chess'},
    ]
