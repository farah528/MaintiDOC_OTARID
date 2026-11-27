from pathlib import Path
from src.ingestion.ingest import ingest
from src.recherche.search import SearchEngine

def engine(tmp_path):
    corpus=Path(__file__).parents[2]/"L1_MaintiDoc_OTARID_Corpus"; out=tmp_path/"ingested"; ingest(corpus,out)
    from src.indexation.index import index
    index(out,"http://localhost:6333")
    return SearchEngine(out)

def test_authorized_group_sees_family(tmp_path):
    e=engine(tmp_path); r=e.text("compresseur huile",["techniciens_compresseurs"]); assert r and all("techniciens_compresseurs" in x["groupes_acces"] for x in r)
def test_unauthorized_group_sees_no_compresseur(tmp_path):
    e=engine(tmp_path); r=e.text("AEROCOMP huile",["techniciens_incendie"]); assert all(x["famille_equipement"] != "compresseurs" for x in r)
def test_fusion_does_not_bypass_access(tmp_path):
    e=engine(tmp_path); r=e.search("panneau compresseur",["techniciens_incendie"],photo="C12.jpg"); assert all("techniciens_compresseurs" not in x["groupes_acces"] for x in r)
