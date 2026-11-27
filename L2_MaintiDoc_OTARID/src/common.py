from __future__ import annotations
import csv, hashlib, json, os, re
from pathlib import Path

def load_inventory(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for row in rows:
        row["groupes_acces"] = [x.strip() for x in row.get("groupe_acces", "").split(";") if x.strip()]
        out[row["document_id"]] = row
    return out

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): h.update(b)
    return h.hexdigest()

def stable_vector(text: str, dim: int = 384) -> list[float]:
    """Deterministic lexical fallback used only when model weights are unavailable."""
    import math
    v = [0.0] * dim
    for token in re.findall(r"[\wÀ-ÿ]+", text.lower()):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        i = int.from_bytes(digest[:4], "big") % dim
        v[i] += 1.0 if digest[4] & 1 else -1.0
    n = math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/n for x in v]

def allowed(groups: list[str], user_groups: list[str]) -> bool:
    return bool(set(groups) & set(user_groups))
