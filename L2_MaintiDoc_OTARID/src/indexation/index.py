from __future__ import annotations
import argparse, json, os
from pathlib import Path
from src.common import stable_vector

def embed_text(items):
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(os.getenv("TEXT_MODEL", "BAAI/bge-m3"))
        return model.encode([x.get("text", "") for x in items], normalize_embeddings=True).tolist(), "BAAI/bge-m3"
    except Exception as exc:
        return [stable_vector(x.get("text", "")) for x in items], f"fallback-hash ({type(exc).__name__})"

def index(input_dir: Path, qdrant_url: str):
    items = [json.loads(x) for x in (input_dir/"elements.jsonl").read_text(encoding="utf-8").splitlines()]
    vecs, model = embed_text(items)
    try:
        from qdrant_client import QdrantClient, models
        client=QdrantClient(url=qdrant_url); dim=len(vecs[0]);
        for name in ("maintidoc_text", "maintidoc_images"):
            try: client.recreate_collection(name, vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE))
            except Exception: pass
        for i,(item,vec) in enumerate(zip(items,vecs)):
            collection="maintidoc_images" if item["type_element"] in ("figure","photo") else "maintidoc_text"
            client.upsert(collection, [models.PointStruct(id=i, vector=vec, payload=item)])
        return {"status":"verified", "model":model, "points":len(items)}
    except Exception as exc:
        (input_dir/"local_index.json").write_text(json.dumps({"items":items,"vectors":vecs,"model":model},ensure_ascii=False), encoding="utf-8")
        return {"status":"qdrant_unavailable", "model":model, "points":len(items), "reason":str(exc)}

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,required=True); p.add_argument("--qdrant-url",default="http://localhost:6333"); a=p.parse_args(); print(json.dumps(index(a.input,a.qdrant_url),ensure_ascii=False))
