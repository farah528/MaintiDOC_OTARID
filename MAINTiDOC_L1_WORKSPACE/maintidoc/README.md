# MAINTiDOC — Assistant Documentaire Multimodal et Agentique pour la Maintenance

**Module :** IA Générative Multimodale  
**Établissement :** École Marocaine des Sciences de l'Ingénieur (EMSI) — Année Universitaire 2026-2027  
**Encadrante :** Pr. Mariam CHERRABI  
**Équipe :** OTARID  
**Membres de l'équipe :**
- Farah OTARID (Étudiante)
- `[A_COMPLETER si binôme]`

---

## 1. Présentation et Objectif du Projet

**MAINTiDOC** est un assistant intelligent d'aide à la maintenance industrielle destiné aux techniciens d'intervention et aux responsables de maintenance. Exploitant les avancées récentes du **RAG multimodal** (Retrieval-Augmented Generation) et des **architectures agentiques**, le système répond à des interrogations techniques en français, appuyées par des citations documentaires formellement vérifiables (document, page, figure ou tableau).

### Capacités Clés du Système
1. **Recherche Multimodale Intelligente :** Interrogation simultanée par question textuelle et photographie de terrain (vue d'un panneau de commande, voyant allumé, plaque signalétique).
2. **Preuves Documentaires Vérifiables :** Restitution d'extraits exacts issus des manuels constructeurs, schémas électriques, circuits pneumatiques et tableaux d'alarmes, sans hallucination.
3. **Contrôle d'Accès Granulaire (RBAC) :** Cloisonnement strict des documents selon le groupe d'appartenance de l'utilisateur (`techniciens_compresseurs`, `techniciens_incendie`, `responsables_maintenance`).
4. **Intégration Outil Externe MCP (Model Context Protocol) :** Consultation sécurisée de l'historique des pannes passées et des tickets ouverts.
5. **Préparation et Création de Ticket avec Approbation Humaine :** Génération d'un brouillon de ticket structuré dans l'interface, avec soumission effective sur le serveur de maintenance uniquement après validation explicite du technicien (Human-in-the-Loop et protection anti-doublon par clé d'idempotence).

> **Avertissement de sécurité :** MAINTiDOC est un système d'assistance documentaire d'aide à la décision. Il ne pilote aucun équipement physique, ne garantit aucun diagnostic autonome et ne se substitue en aucun cas aux habilitations professionnelles ni aux consignes de sécurité en vigueur.

---

## 2. Familles d'Équipements Étudiées

Le corpus documentaire et les scénarios d'évaluation se concentrent sur deux familles industrielles critiques :
1. **Famille 1 — Compresseurs d'Air Industriels :** Compresseurs rotatifs à vis lubrifiée et à spirale (Sullair LS-20, Scroll Air, Bauer Mariner, modèle de référence AEROCOMP-VSD-45). Circuit thermodynamique, lubrification, schémas de démarrage étoile-triangle et régulation de pression.
2. **Famille 2 — Centrales de Détection Incendie (SSI) :** Systèmes de Détection Incendie (SDI) et Centralisateurs de Mise en Sécurité Incendie (CMSI) adressables et conventionnels (gammes UTC/Edwards 2X-F, Mx-4000, Panasonic EBL512, modèle de référence IGNIS-PRO-800). Boucles rebouclées classe A, asservissements DAS clapets et évacuation.

---

## 3. Contenu du Dossier de Livraison (Livrable 1)

Conformément aux consignes officielles du Livrable 1, ce dossier contient rigoureusement les quatre éléments requis :

```text
L1_MaintiDoc_OTARID/
│
├── L1_MaintiDoc_OTARID_Rapport.pdf      # Rapport académique complet (10 à 15 pages, 6 parties obligatoires)
├── L1_MaintiDoc_OTARID_LienGitHub.txt    # Fichier contenant l'URL du dépôt GitHub officiel de l'équipe
├── README.md                             # Synthèse du projet, équipe, corpus et organisation
│
└── L1_MaintiDoc_OTARID_Corpus/           # Dossier complet du corpus documentaire (40 documents)
    ├── inventaire.csv                    # Registre officiel UTF-8 (20 colonnes, 40 documents vérifiés)
    ├── prompts_corpus.md                 # Traçabilité exhaustive des prompts IA et analyse critique
    │
    ├── documents/
    │   ├── famille_1/                    # 19 documents PDF de la Famille 1 (C01 à C11, C13 à C20)
    │   │   ├── C01.pdf à C11.pdf         # Documents réels et schémas normés
    │   │   ├── C13.pdf à C16.pdf         # Documents synthétiques et historique GMAO
    │   │   ├── C17.pdf                   # Version v1 contradictoire — PDF SCANNÉ SANS COUCHE TEXTE (test OCR)
    │   │   ├── C18.pdf                   # Version v2 contradictoire rectifiée — PDF texte
    │   │   ├── C19.pdf                   # Document piégé avec tentative d'injection de prompt
    │   │   └── C20.pdf                   # Cas de diagnostic d'incident de surchauffe
    │   │
    │   └── famille_2/                    # 19 documents PDF de la Famille 2 (F01 à F11, F13 à F20)
    │       ├── F01.pdf à F11.pdf         # Documents réels et schémas boucle/CMSI
    │       ├── F13.pdf à F16.pdf         # Documents synthétiques et registre SSI
    │       ├── F17.pdf                   # Version v1 contradictoire — PDF SCANNÉ SANS COUCHE TEXTE (test OCR)
    │       ├── F18.pdf                   # Version v2 contradictoire rectifiée — PDF texte
    │       ├── F19.pdf                   # Document piégé avec tentative d'injection de prompt
    │       └── F20.pdf                   # Cas de diagnostic de défaut de terre
    │
    └── images/                           # Photographies documentaires réelles
        ├── C12.jpg                       # Panneau réel avec manomètres de compresseur (Wikimedia CC0)
        └── F12.jpg                       # Écran réel pupitre centrale incendie SMS Senator (Wikimedia CC0)
```

---

## 4. Organisation du Dépôt GitHub (`maintidoc/`)

Le code source, les configurations reproductibles et les sources des diagrammes sont structurés au sein du dépôt Git local :

```text
maintidoc/
├── README.md                             # Documentation du dépôt Git
├── .gitignore                            # Exclusion des secrets (.env), caches (__pycache__) et venv
│
├── docs/
│   └── diagrammes/                       # Sources éditables et rendus haute résolution
│       ├── architecture_globale.mmd      # Source Mermaid architecture globale
│       ├── architecture_globale.png / svg
│       ├── flux_ingestion.mmd / png / svg
│       ├── flux_requete.mmd / png / svg
│       ├── flux_ticket_mcp.mmd / png / svg
│       ├── modele_acces_securite.mmd / png / svg
│       ├── schema_electrique_compresseur.png / svg
│       ├── schema_pneumatique_compresseur.png / svg
│       ├── schema_boucle_incendie.png / svg
│       └── schema_cablage_peripheriques.png / svg
│
└── corpus/                               # Réplique miroir du corpus documentaire validé
    ├── inventaire.csv
    ├── prompts_corpus.md
    ├── documents/
    │   ├── famille_1/
    │   └── famille_2/
    └── images/
```

---

## 5. Points Forts et Conformité du Livrable 1

- **Respect rigoureux de la grille d'évaluation :** Rapport complet en 6 parties ordonnées, 40 documents documentés à la ligne près, traçabilité des prompts IA avec analyse critique d'une demi-page.
- **Diversité documentaire :** Manuels constructeurs volumineux (jusqu'à 160 pages), schémas vectoriels haute résolution, fiches de sécurité réglementaires, historiques exploitables par MCP.
- **Préparation active de l'évaluation (Semaine 5) :** Deux paires de documents contradictoires (C17/C18 sur le couple et l'huile ; F17/F18 sur les temporisations d'alarme) et deux documents piégés d'injection de prompt (C19 et F19).
- **Test effectif de l'OCR :** Présence de deux documents scannés réels (C17 et F17) dépourvus de toute couche textuelle, obligeant le moteur d'ingestion à utiliser la reconnaissance optique de caractères.
