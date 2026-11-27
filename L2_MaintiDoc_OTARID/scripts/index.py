from src.indexation.index import *
if __name__ == "__main__":
    import argparse, json
    p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,required=True); p.add_argument("--qdrant-url",default="http://localhost:6333"); a=p.parse_args()
    print(json.dumps(index(a.input,a.qdrant_url), ensure_ascii=False))
