# Matrice de conformite L2

| Référence | Exigence | Action à réaliser | Fichier concerné | Statut | Vérification |
|---|---|---|---|---|---|
| 2.1 | Extraction PDF PyMuPDF | Extraction texte/images, fallback explicite | src/ingestion/ingest.py | Partiellement réalisé | 40 docs/612 éléments; PyMuPDF absent localement |
| 2.1 | OCR sur C17/F17 | Comparer 2 moteurs | scripts/benchmark_outils.py; eval/benchmark_outils.csv | Bloqué | moteurs non installés |
| 2.1 | Chunking/metadonnées/traçabilité | 450 mots, chevauchement, inventaire L1 | src/ingestion/ingest.py | Réalisé | manifest.json et elements.jsonl |
| 2.2 | BGE-M3 texte | Embeddings et collection texte Qdrant | src/indexation/index.py | Partiellement réalisé | fallback hash faute de modèle |
| 2.2 | Encodeur CLIP multilingue | Comparaison de deux options | eval/benchmark_outils.csv | Bloqué | modèles non installés |
| 2.2 | Qdrant texte/images | Deux collections et payload | src/indexation/index.py; docker-compose.yml | Partiellement réalisé | client/daemon indisponibles |
| 2.3 | Recherche texte | Top 5 sourcé | src/recherche/search.py | Réalisé | évaluation exécutée |
| 2.3 | Recherche visuelle/photo/fusion | RRF et photo | src/recherche/search.py | Partiellement réalisé | fusion locale; encodeur image non disponible |
| 2.4 | RBAC avant recherche | Filtrage par groupes | src/recherche/search.py; config/utilisateurs.yaml | Réalisé | 3 tests directs passent |
| 2.4 | Accès page/image | Réutiliser contrôle d'accès | src/recherche/search.py | Partiellement réalisé | API de restitution à compléter |
| 2.5 | 20 questions, 5 photos, 3 ambigus | Jeu et résultats réels | eval/questions_test.csv; resultats/ | Réalisé | 20 questions, 40 lignes de résultats |
| 2.5 | Analyse de 3 échecs | Rapport | rapport/ | Partiellement réalisé | à finaliser après modèles conformes |
| Bonus | Recall@5/MRR@10 | Script et sortie | scripts/calculer_metriques.py | Réalisé | métriques calculées sur 20 questions |
| 2.6 | Veille 3-4 pages, 5 sources | Document séparé et CSV | docs/veille/ | Réalisé | 5 URLs vérifiées le 27/11/2026 |
| 2.7 | Rapport PDF 8-12 pages | Rapport français et captures | rapport/ | Partiellement réalisé | contenu en préparation |
| 3 | ZIP exact | Package OTARID | scripts/package.py | À faire | après validation finale |
| 3 | Git tag v0.2-L2 | Commit/tag/push | LienGitHub.txt | À faire | push non autorisé/exécuté |
