# MAINTiDOC - Livrable 2

Ce dossier contient l'implementation du RAG multimodal du livrable 2 pour l'equipe OTARID. La generation VLM n'est pas incluse.

## Arborescence

`src/` contient l'ingestion, les embeddings et la recherche; `config/` contient les utilisateurs; `eval/` contient les questions et scripts; `docs/veille/` contient la veille et ses sources; `resultats/` contient les mesures produites.

## Prerequis

Python 3.11+, Docker Compose (Qdrant), et les dependances de `requirements.txt`. Les modeles BGE-M3 et CLIP multilingue sont charges depuis le cache Hugging Face ou telecharges au premier lancement.

## Installation et lancement

```powershell
cd L2_MaintiDoc_OTARID
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
docker compose up -d qdrant
python scripts/ingest.py --corpus ..\L1_MaintiDoc_OTARID_Corpus --output data\ingested
python scripts/index.py --input data\ingested --qdrant-url http://localhost:6333
pytest -q tests
python scripts/evaluer_recherche.py --questions eval/questions_test.csv --output resultats/resultats_evaluation.csv
python scripts/calculer_metriques.py --input resultats/resultats_evaluation.csv
streamlit run src/app.py
```

L'ingestion utilise PyMuPDF pour les PDF, conserve les originaux et reprend l'inventaire L1. Les PDF scannes sont transmis a l'OCR configure; en absence d'un moteur local, l'element est conserve avec `ocr_status=unavailable` et n'est pas presente comme correctement extrait.

La recherche applique le filtre RBAC dans Qdrant avant la recherche. Elle expose recherche texte, recherche texte-image, recherche par photo et fusion RRF. Les cinq premiers resultats retournent document, page, element, extrait et score. Aucun module de generation VLM n'est lance.

## Limites d'execution

Les valeurs de benchmark et d'evaluation sont generees par les scripts a partir des executions locales. Un resultat `blocked` ou `unavailable` est conserve comme tel; il ne constitue pas une mesure inventee. Le rapport distingue les etapes verifiees, partielles et non verifiees.
