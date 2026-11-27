import argparse,csv
def main():
 p=argparse.ArgumentParser(); p.add_argument('--input',required=True); a=p.parse_args(); rows=list(csv.DictReader(open(a.input,encoding='utf-8')))
 for cfg in sorted({r['configuration'] for r in rows}):
  rs=[r for r in rows if r['configuration']==cfg]; recall=sum(int(r['hit_at_5']) for r in rs)/len(rs); mrr=0
  for r in rs:
   expected=set(r['attendus'].split(';')) if r['attendus'] else set(); ids=r['resultats'].split(); ranks=[i+1 for i,x in enumerate(ids[:10]) if x in expected]; mrr += 1/ranks[0] if ranks else 0
  print(f'{cfg}: Recall@5={recall:.4f}, MRR@10={mrr/len(rs):.4f}, n={len(rs)}')
if __name__=='__main__': main()
