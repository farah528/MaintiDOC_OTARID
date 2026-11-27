# Veille sur les bonnes pratiques RAG multimodal

## 1. Methode

La veille a ete realisee le 27 novembre 2026 a partir des documentations officielles de Qdrant et PyMuPDF et des articles fondateurs sur BGE-M3 et CLIP. Les pages ont ete ouvertes et verifiees avant inscription dans `sources_veille.csv`. La question directrice est : quelles pratiques reduisent le risque de perte de contexte, de mauvais classement et de fuite documentaire dans le prototype MAINTiDOC ?

## 2. Fiches thematiques

### Decoupage et extraction documentaire

Le decoupage doit preserver l'unite technique d'un passage et la provenance de chaque element. PyMuPDF fournit une extraction de texte et une voie de recuperation des images de page [S5]. Un bloc fixe trop long melange des procedures; un bloc trop court perd les conditions et les exceptions. Pour MAINTiDOC, l'ingestion distingue texte, tableau, figure et page, puis conserve document, page et identifiant d'element. Les passages textuels utilisent une cible de 450 mots avec recouvrement de 50 mots; les tableaux et figures restent des elements autonomes. Cette decision est appliquee dans `src/ingestion/ingest.py`.

### Embeddings et recherche multimodale

BGE-M3 a ete concu pour des langues et granularites multiples et pour plusieurs fonctions de recherche [S3]. CLIP apprend un espace commun texte-image qui permet d'interroger des concepts visuels par le langage [S4]. Ces avantages ne garantissent pas une bonne discrimination de deux voyants proches : il faut donc comparer plusieurs modeles dans les memes conditions. MAINTiDOC reserve une collection Qdrant aux textes et une autre aux figures/photos, avec une fusion RRF. Le reranking et la generation VLM restent hors perimetre du L2.

### Metadonnees et controle d'acces

Qdrant permet de stocker un payload JSON avec chaque vecteur [S2] et d'appliquer des conditions au moment de la recherche [S1]. Le filtrage doit donc porter sur `groupes_acces` avant la recherche, et non sur l'affichage final. Le code transmet le groupe de l'utilisateur a chaque mode et la fusion ne recoit que les resultats filtres. Les ouvertures de page ou d'image doivent reutiliser la meme fonction d'autorisation. La limite actuelle est l'absence de serveur Qdrant demarre dans l'environnement de production de ce livrable; le test local de repli verifie la meme propriete sur les candidats.

### Evaluation et tracabilite

Une evaluation utile separe le jeu de questions, les elements attendus et le resultat reel. Le prototype conserve pour chaque resultat le document, la page, l'element et le score. Le jeu comporte 20 questions, 5 questions avec photo et 3 cas contradictoires ou d'acces. Recall@5 et MRR@10 sont calcules par script sur les CSV produits. Les limites sont signalees lorsque le moteur ou les modeles ne sont pas disponibles; aucune valeur de remplacement n'est interpretee comme une mesure.

### Synthese des decisions

| Bonne pratique | Sources | Decision | Justification MAINTiDOC |
|---|---|---|---|
| Decouper selon la structure et conserver la page | [S5] | appliquee | citations et figures recuperables |
| Conserver un payload riche | [S2] | appliquee | document, page, element et RBAC |
| Filtrer avant la recherche | [S1] | appliquee | aucune fuite entre familles |
| Utiliser BGE-M3 pour le texte | [S3] | appliquee sous reserve du telechargement | francais et corpus multilingue |
| Comparer deux encodeurs image | [S4] | a mesurer | modele non fixe par l'enseignant |
| Calculer Recall@5 et MRR@10 | [S3] | appliquee | metriques reproductibles du L2 |
| Generer avec un VLM | - | reportee semaine 3 | explicitement hors perimetre |

## 3. Sources

Les cinq sources ouvertes et verifiees sont listees dans `sources_veille.csv`. Les URLs sont conservees pour permettre un controle exterieur et ne sont pas remplacees par des references inventees.
