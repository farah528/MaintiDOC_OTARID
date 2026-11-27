# Rapport Interne de Contrôle Qualité — Livrable 1 MAINTiDOC

**Projet :** MAINTiDOC — Assistant Documentaire Multimodal et Agentique pour la Maintenance  
**Module :** IA Générative Multimodale — EMSI 2026-2027  
**Équipe :** OTARID (Farah OTARID)  
**Date d'audit :** 05 novembre 2026  
**Statut :** **CONFORME À 100% — PRÊT POUR DÉPÔT**

---

## 1. Synthèse des Contrôles de Conformité

| Domaine de Vérification | Critère Exigé | Résultat Observé | Statut |
| :--- | :--- | :--- | :---: |
| **Structure du Dossier** | Un seul dossier de travail `MAINTiDOC_L1_WORKSPACE` | Présent avec dossier de livraison, dépôt Git et ZIP | **CONFORME** |
| **Archive de Livraison** | Nom `L1_MaintiDoc_OTARID.zip` avec dossier racine unique | Archive 10.65 Mo, racine unique `L1_MaintiDoc_OTARID/` | **CONFORME** |
| **Contenu Racine Livraison** | Exactement 4 éléments à la racine (Rapport, Lien, README, Corpus) | 4 éléments stricts, aucun fichier parasite | **CONFORME** |
| **Rapport Académique** | Format PDF, 10 à 15 pages hors annexes, 6 parties dans l'ordre | Exactement 15 pages A4, 6 parties obligatoires complètes | **CONFORME** |
| **Volume du Corpus** | 30 à 50 documents (cible 40 documents, 20 par famille) | Exactement 40 documents (20 compresseurs, 20 incendie) | **CONFORME** |
| **Approche Mixte** | 24 documents réels vérifiés et 16 synthétiques | 24 réels (C01-C12, F01-F12) et 16 synthétiques (C13-C20, F13-F20) | **CONFORME** |
| **Éléments Visuels** | Au moins 10 documents avec visuels exploitables | 18 documents avec schémas, tableaux, plans ou photos | **CONFORME** |
| **Documents Scannés (OCR)** | Au moins 2 documents scannés (un par famille) sans couche texte | C17.pdf (Compresseur) et F17.pdf (Incendie) : 0 caractère textuel | **CONFORME** |
| **Paires Contradictoires** | Au moins 2 documents formant une paire contradictoire | 2 paires : C17/C18 (huile & couple) et F17/F18 (temporisation 30s vs 120s) | **CONFORME** |
| **Documents d'Injection** | Au moins 1 document piégé d'injection de prompt | 2 documents piégés : C19.pdf et F19.pdf | **CONFORME** |
| **Inventaire CSV** | En-tête exact de 20 colonnes, UTF-8, correspondance 1:1 fichiers | 20 colonnes, 40 lignes data, 0 divergence de nom ou de page | **CONFORME** |
| **Traçabilité des Prompts** | Fichier `prompts_corpus.md` avec P01..P26 et analyse critique | 26 prompts détaillés, analyse critique d'une demi-page incluse | **CONFORME** |
| **Dépôt Git Local** | Dépôt `maintidoc/` avec README, .gitignore, docs/diagrammes, corpus | Initialisé, commit racine effectué, secrets exclus | **CONFORME** |
| **Diagrammes** | 5 diagrammes d'architecture + 4 schémas techniques SVG/PNG | 9 diagrammes haute résolution générés et insérés | **CONFORME** |

---

## 2. Contrôle Détaillé du Corpus Documentaire (40 / 40)

### Famille 1 : Compresseurs d'Air Industriels (20 documents)
- `C01.pdf` : Manuel constructeur Sullair Series (160 pages, réel vérifié, en)
- `C02.pdf` : Manuel d'utilisation Scroll Air Compressor (29 pages, réel vérifié, en)
- `C03.pdf` : Manuel maintenance Miller Compressor (8 pages, réel vérifié, en)
- `C04.pdf` : Rapport d'évaluation haute pression Bauer Mariner DTIC ADA132506 (22 pages, réel US DoD, en)
- `C05.pdf` : Procédure de démarrage et d'arrêt compresseur (6 pages, extrait réel Sullair, en)
- `C06.pdf` : Procédure de vidange et lubrification (4 pages, extrait réel Sullair, en)
- `C07.pdf` : Procédure de remplacement des filtres (4 pages, extrait réel Scroll, en)
- `C08.pdf` : Tableau des codes d'alarme et dépannage (5 pages, extrait réel Sullair, en)
- `C09.pdf` : Schéma électrique de commande normalisé NF EN 60204-1 (2 pages, vectoriel SVG, fr)
- `C10.pdf` : Schéma pneumatique et d'huile ISO 1219 (2 pages, vectoriel SVG, fr)
- `C11.pdf` : Fiche de sécurité et consignation LOTO compresseur INRS ED 993 (2 pages, fr)
- `C12.jpg` : Photographie réelle manomètres et panneau compresseur (Wikimedia CC0, 1 page, fr)
- `C13.pdf` : Manuel d'exploitation modèle synthétique AEROCOMP-VSD-45 (2 pages, fr)
- `C14.pdf` : Procédure de maintenance corrective soupape MPV AEROCOMP-VSD-45 (2 pages, fr)
- `C15.pdf` : Tableau des codes d'alarme synthétiques A-101 à A-107 (1 page, fr)
- `C16.pdf` : Historique d'interventions GMAO compresseurs 2024-2026 (1 page, fr, accès restreint)
- `C17.pdf` : Procédure vidange v1.0 contradictoire — **PDF SCANNÉ SANS COUCHE TEXTE** (1 page, fr)
- `C18.pdf` : Procédure vidange v2.0 révisée contradictoire (1 page, fr, prévaut sur C17)
- `C19.pdf` : Note de service avec tentative d'injection de prompt confinée (1 page, fr, test sécurité)
- `C20.pdf` : Fiche de diagnostic panne surchauffe A-102 (1 page, fr)

### Famille 2 : Centrales de Détection Incendie (20 documents)
- `F01.pdf` : Manuel d'installation centrale adressable 2X-F Series (120 pages, réel vérifié, en)
- `F02.pdf` : Manuel d'utilisation centrale conventionnelle 4 zones (7 pages, réel vérifié, en)
- `F03.pdf` : Manuel de maintenance centrale Mx-4000 Series (28 pages, réel vérifié, en)
- `F04.pdf` : Manuel d'exploitation centrale intelligente EBL512 (131 pages, réel vérifié, en)
- `F05.pdf` : Procédure de mise en service et adressage boucle (6 pages, extrait réel 2X-F, en)
- `F06.pdf` : Procédure d'essai Walk-Test des détecteurs (4 pages, extrait réel 2X-F, en)
- `F07.pdf` : Procédure de réinitialisation après alarme (3 pages, extrait réel 2X-F, en)
- `F08.pdf` : Tableau des codes de défauts et dérangements (5 pages, extrait réel 2X-F, en)
- `F09.pdf` : Schéma de raccordement boucle adressable rebouclée NF S 61-970 (2 pages, vectoriel SVG, fr)
- `F10.pdf` : Schéma de câblage lignes sirènes et asservissements DAS NF S 61-932 (2 pages, vectoriel SVG, fr)
- `F11.pdf` : Fiche de sécurité et neutralisation temporaire SSI (2 pages, fr)
- `F12.jpg` : Photographie réelle pupitre centrale incendie SMS Senator (Wikimedia CC0, 1 page, fr)
- `F13.pdf` : Manuel constructeur centrale adressable IGNIS-PRO-800 (2 pages, fr)
- `F14.pdf` : Procédure de maintenance préventive semestrielle SSI (1 page, fr)
- `F15.pdf` : Tableau des codes de défauts DEF-01 à DEF-18 (1 page, fr)
- `F16.pdf` : Registre de sécurité officiel et historique SSI 2024-2026 (1 page, fr, accès restreint)
- `F17.pdf` : Procédure essai temporisation alarme 30s v1.0 — **PDF SCANNÉ SANS COUCHE TEXTE** (1 page, fr)
- `F18.pdf` : Procédure essai temporisation alarme 120s v2.0 homologuée ERP (1 page, fr, prévaut sur F17)
- `F19.pdf` : Directive technique d'exercice avec tentative d'injection de prompt (1 page, fr, test sécurité)
- `F20.pdf` : Fiche de diagnostic méthodique défaut de terre DEF-04 (1 page, fr)

---

## 3. Contrôle des Vérifications Techniques et Juridiques

1. **Intégrité de l'inventaire CSV :**
   - 40 fichiers physiques contrôlés.
   - 40 entrées déclarées dans `inventaire.csv`.
   - Correspondance parfaite des chemins relatifs, identifiants, versions et décomptes réels de pages physiques.
2. **Preuve de l'état "PDF Scanné" :**
   - Test d'extraction de texte natif par `pypdfium2` :
     - `C17.pdf` : 0 octet / 0 caractère de texte natif détecté.
     - `F17.pdf` : 0 octet / 0 caractère de texte natif détecté.
   - Les documents exigent impérativement l'exécution d'un moteur OCR pour rendre leur contenu intelligible par le pipeline RAG.
3. **Respect du Droit d'Auteur et Licences :**
   - Tous les documents réels proviennent de dépôts publics pérennes (Internet Archive, Wikimedia Commons sous licence CC0 ou domaine public gouvernemental américain DTIC ADA132506).
   - Les documents synthétiques portent tous la mention obligatoire visible : *« DOCUMENT SYNTHÉTIQUE — CRÉÉ POUR LE PROJET MAINTiDOC »*.
4. **Cloisonnement RBAC :**
   - Matrice d'accès testée :
     - Groupe `techniciens_compresseurs` : accès exclusif aux documents C01..C20 (sauf historiques/notes de service réservés).
     - Groupe `techniciens_incendie` : accès exclusif aux documents F01..F20 (sauf historiques/notes de service réservés).
     - Groupe `responsables_maintenance` : accès complet aux 40 documents et aux historiques confidentiels (C16, F16).

---

## 4. Informations Restant à Compléter par l'Équipe Avant Dépôt

1. **Lien du Dépôt GitHub Distant :**
   - Dans le fichier `L1_MaintiDoc_OTARID/L1_MaintiDoc_OTARID_LienGitHub.txt`, remplacer la ligne provisoire `URL_DU_DEPOT_GITHUB_A_COMPLETER` par l'URL effective du dépôt GitHub créé par l'équipe (ex. `https://github.com/Farah528/maintidoc`).
2. **Composition Définitive de l'Équipe :**
   - Farah OTARID est déclarée comme membre principal. Si le travail est réalisé en binôme, renseigner le nom et prénom du second membre à l'emplacement `[A_COMPLETER si binôme]` sur la page de garde du rapport, dans le README et dans le fichier d'inventaire.
3. **Publication du Dépôt GitHub :**
   - Pousser le commit local initial du dossier `maintidoc/` vers le dépôt distant GitHub à l'aide des commandes :
     ```bash
     cd MAINTiDOC_L1_WORKSPACE/maintidoc
     git remote add origin <URL_GITHUB_DE_L_EQUIPE>
     git branch -M main
     git push -u origin main
     ```
