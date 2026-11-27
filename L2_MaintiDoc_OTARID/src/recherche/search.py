from __future__ import annotations
import json, math, re
from pathlib import Path
from src.common import allowed, stable_vector

def lexical_score(q, text):
    a=set(re.findall(r"[\wÀ-ÿ]+",q.lower())); b=set(re.findall(r"[\wÀ-ÿ]+",text.lower())); return len(a&b)/(len(a)**0.5*len(b)**0.5 or 1)
def cosine(a,b): return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(y*y for y in b)) or 1)
class SearchEngine:
    def __init__(self, input_dir: Path):
        data=json.loads((input_dir/"local_index.json").read_text(encoding="utf-8")); self.items=data["items"]; self.vecs=data["vectors"]
    def _candidates(self, groups): return [(i,x) for i,x in enumerate(self.items) if allowed(x.get("groupes_acces",[]),groups)]
    def text(self, query, groups, k=5):
        return sorted(({**x,"score":lexical_score(query,x.get("text",x.get("remarques",""))),"modality":"text"} for i,x in self._candidates(groups)), key=lambda x:x["score"], reverse=True)[:k]
    def visual(self, query, groups, k=5):
        return sorted(({**x,"score":lexical_score(query,x.get("remarques",x.get("titre",""))),"modality":"visual"} for i,x in self._candidates(groups) if x["type_element"] in ("figure","photo")), key=lambda x:x["score"], reverse=True)[:k]
    def search(self, query, groups, photo=None, k=5):
        a=self.text(query,groups,k*2); b=self.visual(query,groups,k*2) if photo or query else []
        ranked={}
        for rank,x in enumerate(a,1): ranked.setdefault(x["element_id"], {**x,"score":0})["score"] += 1/(60+rank)
        for rank,x in enumerate(b,1): ranked.setdefault(x["element_id"], {**x,"score":0})["score"] += 1/(60+rank)
        return sorted(ranked.values(),key=lambda x:x["score"],reverse=True)[:k]
