import os
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath("MAINTiDOC_L1_WORKSPACE/maintidoc/docs/diagrammes")
os.makedirs(output_dir, exist_ok=True)

html_template = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #ffffff;
    margin: 0;
    padding: 30px;
    display: inline-block;
  }
  .mermaid {
    background: #ffffff;
  }
</style>
</head>
<body>
<div class="mermaid">
{mermaid_code}
</div>
<script>
mermaid.initialize({
  startOnLoad: true,
  theme: 'neutral',
  themeVariables: {
    fontFamily: 'Segoe UI',
    fontSize: '14px',
    primaryColor: '#e3f2fd',
    primaryBorderColor: '#0d47a1',
    primaryTextColor: '#0d47a1',
    lineColor: '#1565c0',
    secondaryColor: '#f1f8e9',
    secondaryBorderColor: '#33691e',
    secondaryTextColor: '#1b5e20',
    tertiaryColor: '#fffde7',
    tertiaryBorderColor: '#f57f17',
    tertiaryTextColor: '#e65100',
    edgeLabelBackground: '#ffffff'
  }
});
</script>
</body>
</html>"""

diagrams = {
    "architecture_globale": {
        "title": "Architecture Globale Cible de MAINTiDOC",
        "code": """flowchart TB
    subgraph UI ["Interface Utilisateur"]
        direction TB
        Streamlit["Application Web Streamlit<br/>- Formulaire Question & Photo<br/>- Visualisation Citations & Sources<br/>- Approbation Explicite de Ticket"]
    end

    subgraph Gateway ["Passerelle API & Sécurité"]
        FastAPI["API FastAPI<br/>- Authentification JWT & RBAC<br/>- Validation Schémas Pydantic<br/>- Quotas & Rate Limiting (60s)"]
    end

    subgraph Orchestration ["Orchestration Agentique (LangGraph)"]
        LG["Moteur de Workflow LangGraph<br/>- Gestionnaire d'État & Transitions<br/>- Plafond de Boucle (max 6 itérations)<br/>- Point d'Interruption Humaine (Human-in-the-Loop)"]
    end

    subgraph RAG ["Sous-système RAG Multimodal (LangChain)"]
        direction TB
        subgraph Ret ["Recherche Documentaire Hybride"]
            BGE["Recherche Dense & Sparse (BGE-M3)"]
            CLIP["Recherche Visuelle (CLIP Multilingue)"]
            RRF["Fusion RRF (Reciprocal Rank Fusion)"]
        end
        Reranker["Reranker BGE Cross-Encoder<br/>(Fine-tuné Semaine 5)"]
        Filter["Contrôle d'Accès Pré-filtrage<br/>(Filtrage strict par groupe_acces)"]
        CiteCheck["Module de Vérification des Citations<br/>(Fact-Checking & Validation des Sources)"]
    end

    subgraph VLM ["Modèle Vision-Langage"]
        Qwen["Qwen2.5-VL-7B-Instruct<br/>(Inférence Transformers / vLLM, GPU 24 Go)"]
    end

    subgraph MCP ["Écosystème MCP Maintenance"]
        MCPClient["Client MCP LangChain"]
        MCPServer["Serveur MCP Maintenance (Démonstration)<br/>- get_equipment_history()<br/>- get_open_tickets()<br/>- create_ticket(approval_token, idempotency_key)"]
    end

    subgraph Stockage ["Infrastructures de Données"]
        Qdrant[("Base Vectorielle Qdrant<br/>- Index Passages Textuels<br/>- Index Éléments Visuels")]
        Postgres[("Base PostgreSQL<br/>- Métadonnées Inventaire & RBAC<br/>- Journaux d'Audit & Historique")]
        MinIO[("Stockage Objet MinIO<br/>- Documents PDF Originaux<br/>- Images Haute Résolution")]
    end

    subgraph Ops ["Observabilité & Déploiement"]
        MLflow["MLflow Tracking & Logging"]
        Docker["Déploiement Docker Compose"]
    end

    Streamlit <-->|"Requêtes HTTPS / Websockets"| FastAPI
    FastAPI <-->|"State & Context"| LG
    LG <-->|"Filtrage & Requête Hybride"| Ret
    Filter -.->|"Application RBAC"| Ret
    BGE <-->|"Recherche Vectorielle"| Qdrant
    CLIP <-->|"Recherche Visuelle"| Qdrant
    Ret -->|"Top-20 Candidats"| RRF
    RRF -->|"Fusion"| Reranker
    Reranker -->|"Top-5 Passages & Figures"| LG
    LG <-->|"Prompt Contexte + Image"| Qwen
    Qwen -->|"Réponse Brute JSON"| CiteCheck
    CiteCheck -->|"Vérification Factuelle"| LG
    LG <-->|"Historique & Brouillon Ticket"| MCPClient
    MCPClient <-->|"Protocole Standard MCP"| MCPServer
    MCPServer <-->|"Données Tickets"| Postgres
    FastAPI -.->|"Fichiers & Images"| MinIO
    FastAPI -.->|"Métadonnées & Utilisateurs"| Postgres
    LG -.->|"Métriques & Traces"| MLflow
"""
    },

    "flux_ingestion": {
        "title": "Flux d'Ingestion Documentaire et Indexation Multimodale",
        "code": """flowchart TD
    DocIn["Documents Sources du Corpus<br/>(PDF Textuels, PDF Scannés, Photographies)"] --> TypeCheck{"Type de Fichier & Format ?"}
    
    TypeCheck -->|"PDF Scanné / Image"| OCRProc["OCR Local (Tesseract / PaddleOCR)<br/>- Détection zones de texte<br/>- Extraction bboxes & confiance"]
    TypeCheck -->|"PDF Textuel Natif"| PyMu["PyMuPDF (fitz)<br/>- Extraction flux texte natif<br/>- Extraction figures & tableaux"]
    
    OCRProc --> Normal["Normalisation du Contenu Textuel"]
    PyMu --> Normal
    PyMu --> VisualExt["Extraction des Éléments Visuels<br/>(Schémas, Tableaux, Diagrammes)"]

    Normal --> Chunking["Découpage Sémantique (Chunking)<br/>- Passages de 300 à 500 tokens<br/>- Chevauchement de 50 tokens"]
    
    Chunking --> BGEEmb["Génération Embeddings Textuels<br/>- Modèle BGE-M3 (Dense 1024-dim + Sparse Lexical)"]
    VisualExt --> CLIPEmb["Génération Embeddings Visuels<br/>- Encodeur CLIP Multilingue (512-dim)"]

    Chunking --> MetaAssign["Attribution des Métadonnées Enrichies<br/>- document_id, version, page, element_id<br/>- equipement_id, famille_equipement<br/>- groupe_acces, hash_sha256"]
    VisualExt --> MetaAssign

    BGEEmb --> QdrantIndex[("Indexation Qdrant<br/>Collection Textuelle")]
    CLIPEmb --> QdrantIndexVis[("Indexation Qdrant<br/>Collection Visuelle")]
    MetaAssign --> QdrantIndex
    MetaAssign --> QdrantIndexVis
    MetaAssign --> PostgresIndex[("PostgreSQL<br/>Métadonnées & Registre")]
    DocIn --> MinIOStore[("MinIO Object Storage<br/>Stockage Fichiers Bruts")]
"""
    },

    "flux_requete": {
        "title": "Flux de Traitement d'une Requête Utilisateur",
        "code": """flowchart TD
    UserQ["Technicien : Question Textuelle + Photo optionnelle"] --> API["FastAPI : Authentification JWT"]
    API --> CheckPerm["Résolution des Droits Utilisateur<br/>- Récupération user_groups (ex: techniciens_compresseurs)"]
    
    CheckPerm --> ImgCheck{"Image fournie dans la requête ?"}
    ImgCheck -->|"Oui"| VLMPre["Analyse Visuelle VLM (Qwen2.5-VL)<br/>- Identification visuelle équipement<br/>- Détection codes voyants / afficheur"]
    ImgCheck -->|"Non"| QueryPrep["Formulation de la Requête de Recherche"]
    VLMPre --> QueryPrep

    QueryPrep --> SearchExec["Recherche Multimodale Hybride dans Qdrant<br/>[POINT DE CONTRÔLE 1 : Filtre strict groupe_acces]"]
    SearchExec --> RetText["Recherche Dense + Lexicale (BGE-M3)"]
    SearchExec --> RetVis["Recherche Visuelle (CLIP)"]
    
    RetText --> RRF["Fusion Reciprocal Rank Fusion (RRF)"]
    RetVis --> RRF
    RRF --> CrossRank["Reclassement Reranker Cross-Encoder BGE<br/>(Top-5 passages & figures retenus)"]

    CrossRank --> CheckSuff{"Preuves documentaires<br/>suffisantes et concordantes ?"}
    CheckSuff -->|"Ambiguïté / Absence / Contradiction"| Clarif["Génération Demande de Clarification<br/>(status: needs_clarification)"]
    CheckSuff -->|"Preuves Solides"| GenVLM["Génération de Réponse Sourcée (VLM)<br/>Format Pydantic JSON validé"]

    GenVLM --> CiteVerify["[POINT DE CONTRÔLE 2 : Vérification Citations]<br/>- Existence effective des pages/figures<br/>- Support sémantique de l'affirmation"]
    CiteVerify --> ResponseOut["Restitution Réponse Sourcée à l'Utilisateur<br/>(Citations exactes document, page, figure)"]
    Clarif --> ResponseOut
"""
    },

    "flux_ticket_mcp": {
        "title": "Processus de Préparation et Création de Ticket avec Approbation Humaine",
        "code": """flowchart TD
    Demand["Technicien / Assistant : Détection d'un incident justifiant un ticket"] --> HistCheck["LangGraph : Appel MCP get_equipment_history(equipement_id)"]
    HistCheck --> HistResp["Serveur MCP : Retour des 5 dernières interventions & tickets ouverts"]
    
    HistResp --> DraftPrep["Génération Brouillon de Ticket (Pydantic TicketDraft)<br/>- Équipement concerné (ex: COMP-B-02)<br/>- Titre, Gravité & Description détaillée de l'incident<br/>- Citations documentaires justificatives (manuel, page)<br/>- Recommandations techniques"]

    DraftPrep --> Checkpoint["[POINT DE CONTRÔLE : Interruption Humaine LangGraph]<br/>Affichage du Brouillon dans l'interface Streamlit"]
    
    Checkpoint --> UserDecision{"Validation Humaine par le Technicien"}
    UserDecision -->|"Refus / Annulation"| CancelTicket["Workflow Interrompu : Aucun ticket créé"]
    UserDecision -->|"Modification souhaitée"| EditDraft["Édition manuelle des champs du ticket"]
    EditDraft --> Checkpoint
    UserDecision -->|"Approbation Explicite"| TokenGen["Génération Token d'Approbation Cryptographique<br/>+ Clé d'Idempotence sha256(user+equip+timestamp)"]

    TokenGen --> MCPCall["Client MCP : create_ticket(approval_token, idempotency_key, ticket_data)"]
    
    MCPCall --> ServerCheck{"Serveur MCP : Contrôle du Token et de l'Idempotence"}
    ServerCheck -->|"Token Invalide / Absent"| Reject["Rejet Strict 403 : Action Non Autorisée"]
    ServerCheck -->|"Déjà Traité (Idempotence)"| ReturnExisting["Retour du Ticket existant sans doublon"]
    ServerCheck -->|"Valide & Inédit"| InsertDB["Insertion Ticket dans la Base de Maintenance"]

    InsertDB --> SuccessNotif["Confirmation Succès : Numéro Ticket généré (TICK-2026-XXXX)<br/>Affichage sur l'interface technicien"]
    ReturnExisting --> SuccessNotif
"""
    },

    "modele_acces_securite": {
        "title": "Modèle de Sécurité, Cloisonnement RBAC et Protection Anti-Injection",
        "code": """flowchart TD
    subgraph Users ["Utilisateurs & Profils Déclarés"]
        TechC["Technicien Compresseurs<br/>(Groupe: techniciens_compresseurs)"]
        TechI["Technicien Incendie<br/>(Groupe: techniciens_incendie)"]
        RespM["Responsable Maintenance<br/>(Groupe: responsables_maintenance)"]
    end

    subgraph SecurityLayer ["Couche de Contrôle d'Accès (API & RAG)"]
        JWTEval["Contrôleur JWT & Décodeur de Rôles"]
        QdrantFilter["Filtre Pré-Recherche Qdrant<br/>Filter.must: groupe_acces IN user.groups"]
        Sanitize["Barrière Anti-Injection (Prompt Shield)<br/>Documents traités comme données passives"]
    end

    subgraph CorpusSplits ["Cloisonnement du Corpus Documentaire"]
        DocsComp["Famille 1 : Compresseurs d'Air Industriels<br/>(20 documents C01-C20)<br/>Accessible: techniciens_compresseurs, responsables"]
        DocsInc["Famille 2 : Centrales Détection Incendie<br/>(20 documents F01-F20)<br/>Accessible: techniciens_incendie, responsables"]
        DocsSensibles["Documents Restreints / Historiques Globaux<br/>(C16, F16, notes internes)<br/>Accessible: UNIQUEMENT responsables_maintenance"]
    end

    subgraph OutIsolation ["Isolation des Réponses & Outils MCP"]
        RespFilter["Vérification Post-Génération : Zéro fuite de citation hors groupe"]
        MCPAccess["Serveur MCP : Autorisation granulaire sur create_ticket & history"]
    end

    TechC --> JWTEval
    TechI --> JWTEval
    RespM --> JWTEval

    JWTEval --> QdrantFilter
    QdrantFilter --> DocsComp
    QdrantFilter --> DocsInc
    QdrantFilter --> DocsSensibles

    Sanitize -.->|"Neutralisation tentatives injection (C19, F19)"| QdrantFilter
    DocsComp --> RespFilter
    DocsInc --> RespFilter
    DocsSensibles --> RespFilter
    RespFilter --> MCPAccess
"""
    }
}

print("Launching Playwright to render all Mermaid diagrams...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 1000, "device_scale_factor": 2})

    for name, data in diagrams.items():
        mmd_path = os.path.join(output_dir, f"{name}.mmd")
        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(data["code"])
        print(f"Saved Mermaid source: {mmd_path}")

        html_content = html_template.replace("{mermaid_code}", data["code"])
        temp_html = os.path.join(output_dir, f"temp_{name}.html")
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        page.goto(f"file:///{temp_html}")
        page.wait_for_selector("svg", timeout=15000)
        svg_el = page.query_selector("svg")

        png_path = os.path.join(output_dir, f"{name}.png")
        svg_path = os.path.join(output_dir, f"{name}.svg")

        # Save SVG
        svg_html = page.evaluate("el => el.outerHTML", svg_el)
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_html)

        # Save high-res PNG
        svg_el.screenshot(path=png_path)
        print(f"Rendered {png_path} and {svg_path}")

        os.remove(temp_html)

    browser.close()

print("All architectural diagrams generated successfully!")
