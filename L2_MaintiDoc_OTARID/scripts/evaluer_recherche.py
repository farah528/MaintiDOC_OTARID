from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from src.recherche.search import SearchEngine
from src.acces.rbac import user_groups
def parse_expected(s):
    return {x.split()[0] for x in s.split(';') if x and x != 'aucun'}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--questions',type=Path,required=True); p.add_argument('--input',type=Path,default=Path('data/ingested')); p.add_argument('--output',type=Path,required=True); a=p.parse_args(); e=SearchEngine(a.input); rows=[]
    with a.questions.open(encoding='utf-8-sig',newline='') as f:
        for q in csv.DictReader(f):
            groups=user_groups(q['utilisateur']); expected=parse_expected(q['elements_attendus']);
            for config,results in [('texte_seul',e.text(q['question'],groups)),('texte_images',e.search(q['question'],groups,photo=q['photo'] or None))]:
                ids=[x['document_id'] for x in results]; rows.append({'question_id':q['question_id'],'configuration':config,'attendus':';'.join(sorted(expected)),'resultats':' '.join(ids),'hit_at_5':int(bool(expected & set(ids))), 'top1':ids[0] if ids else ''})
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text('',encoding='utf-8');
    with a.output.open('w',encoding='utf-8',newline='') as f: w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
if __name__=='__main__': main()
