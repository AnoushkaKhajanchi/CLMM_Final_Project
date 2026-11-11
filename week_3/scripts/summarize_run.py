"""CPU-only summary of a Week 3 exported run. Usage: python summarize_run.py RUN_DIR"""
import json
import sys
from pathlib import Path
from protocol import numbered_lines

def summarize(root):
    root=Path(root)
    manifest=json.loads((root/'manifest.json').read_text())
    groups={}
    for p in sorted(root.rglob('*.json')):
        if p.name=='manifest.json':continue
        obj=json.loads(p.read_text())
        if not isinstance(obj,dict):continue
        if 'generation' not in obj:continue
        key=p.parent.relative_to(root).as_posix()
        group=groups.setdefault(key,{'writes':0,'write_seconds':0,'write_output_caps':0,'rejected_calls':0,
                                     'tool_errors':0,'answers':{}})
        if 'before' in obj and 'after' in obj:
            group['writes']+=1;group['write_seconds']+=obj['wall_seconds']
            group['write_output_caps']+=int(obj['generation']['hit_output_limit'])
            group['rejected_calls']+=len(obj.get('rejected_calls',[]))
            group['tool_errors']+=sum(c['error'] for c in obj['calls'])
        elif 'exact_match' in obj:
            cond=obj.get('condition','control')
            scores=group['answers'].setdefault(cond,{'n':0,'exact_matches':0,'substring_matches':0,'output_caps':0})
            scores['n']+=1;scores['exact_matches']+=obj['exact_match']
            scores['substring_matches']+=obj.get('substring_exact_match',0)
            scores['output_caps']+=int(obj['generation']['hit_output_limit'])
    provenance={str(p.parent.relative_to(root)):numbered_lines(json.loads(p.read_text())) for p in root.rglob('memory_final.json')}
    return {'settings':manifest['settings'],'groups':groups,'provenance_format_only':provenance,
            'interpretation':'Development results. Presence/format proxies require manual validation; no final-evaluation claim.'}
if __name__=='__main__':print(json.dumps(summarize(sys.argv[1]),indent=2))
