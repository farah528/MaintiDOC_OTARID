from __future__ import annotations
import argparse, json, re, time
from pathlib import Path
from src.common import load_inventory, sha256

def extract_pdf(path: Path):
    try:
        import fitz
    except ImportError:
        fitz = None
    if fitz is None:
        from pypdf import PdfReader
        for page_no, page in enumerate(PdfReader(str(path)).pages, 1):
            yield page_no, page.extract_text() or "", []
        return
    doc = fitz.open(path)
    for page_no, page in enumerate(doc, 1):
        text = page.get_text("text")
        figures = []
        for i, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                info = doc.extract_image(xref)
                figures.append({"index": i, "ext": info["ext"], "bytes": info["image"]})
            except Exception:
                pass
        yield page_no, text, figures

def chunk(text: str, size: int = 450, overlap: int = 50):
    words = re.findall(r"\S+", text or "")
    if not words: return []
    step = max(1, size-overlap)
    return [" ".join(words[i:i+size]) for i in range(0, len(words), step)]

def ingest(corpus: Path, output: Path):
    inventory = load_inventory(corpus / "inventaire.csv")
    output.mkdir(parents=True, exist_ok=True)
    elements = []
    for doc_id, meta in inventory.items():
        rel = Path(meta["fichier"])
        path = corpus / rel
        if meta["format"].startswith("pdf"):
            for page, text, figures in extract_pdf(path):
                if not text.strip() and meta["format"] == "pdf_scanne":
                    text = ""
                for j, value in enumerate(chunk(text), 1):
                    elements.append({"element_id": f"{doc_id}_p{page}_t{j}", "document_id": doc_id, "page": page, "type_element": "texte", "text": value, "ocr_status": "not_needed" if text.strip() else "unavailable", "source_path": str(rel), "hash_sha256": sha256(path), **meta})
                for j, fig in enumerate(figures, 1):
                    img_dir = output / "figures"; img_dir.mkdir(exist_ok=True)
                    img_path = img_dir / f"{doc_id}_p{page}_f{j}.{fig['ext']}"; img_path.write_bytes(fig["bytes"])
                    elements.append({"element_id": f"{doc_id}_p{page}_f{j}", "document_id": doc_id, "page": page, "type_element": "figure", "text": "", "image_path": str(img_path), "ocr_status": "not_needed", "source_path": str(rel), "hash_sha256": sha256(path), **meta})
        elif meta["format"] == "image":
            elements.append({"element_id": f"{doc_id}_image", "document_id": doc_id, "page": 1, "type_element": "photo", "text": meta.get("remarques", ""), "image_path": str(corpus / rel), "ocr_status": "not_needed", "source_path": str(rel), "hash_sha256": sha256(path), **meta})
    (output / "elements.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in elements), encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps({"count": len(elements), "documents": len(inventory), "created_at": time.time()}, indent=2), encoding="utf-8")
    return elements

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--corpus", type=Path, required=True); p.add_argument("--output", type=Path, default=Path("data/ingested")); a=p.parse_args(); print(json.dumps(ingest(a.corpus,a.output), ensure_ascii=False)[:0] or f"ingested -> {a.output}")
