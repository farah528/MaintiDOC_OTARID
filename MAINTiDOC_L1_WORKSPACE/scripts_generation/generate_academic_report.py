import os
from playwright.sync_api import sync_playwright
import pypdfium2 as pdfium

diag_dir = os.path.abspath("MAINTiDOC_L1_WORKSPACE/maintidoc/docs/diagrammes").replace("\\", "/")
target_pdf = os.path.abspath("MAINTiDOC_L1_WORKSPACE/L1_MaintiDoc_OTARID/L1_MaintiDoc_OTARID_Rapport.pdf")

html_report = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>L1_MaintiDoc_OTARID_Rapport</title>
<style>
  @page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
    @top-right {{
      content: "MAINTiDOC — Livrable 1 : Cadrage, Corpus & Architecture";
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 8pt;
      color: #64748b;
      font-weight: 500;
    }}
    @bottom-right {{
      content: "Page " counter(page) " / " counter(pages);
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 8pt;
      color: #64748b;
      font-weight: 600;
    }}
    @bottom-left {{
      content: "EMSI 2026-2027 — IA Générative Multimodale — Équipe OTARID";
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 8pt;
      color: #64748b;
    }}
  }}

  @page:first {{
    margin: 0;
    @top-right {{ content: normal; }}
    @bottom-right {{ content: normal; }}
    @bottom-left {{ content: normal; }}
  }}

  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 9.2pt;
    margin: 0;
    padding: 0;
  }}

  /* Page de Garde */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    box-sizing: border-box;
    padding: 50px 45px;
    background: linear-gradient(135deg, #0b192c 0%, #1e3e62 100%);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .cover-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid rgba(255, 255, 255, 0.2);
    padding-bottom: 18px;
  }}
  .cover-school {{
    font-size: 15pt;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #f8fafc;
  }}
  .cover-module {{
    font-size: 9.5pt;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: right;
  }}
  .cover-body {{
    margin: 40px 0;
  }}
  .cover-badge {{
    display: inline-block;
    background: #00adb5;
    color: #0b192c;
    font-weight: 700;
    font-size: 9pt;
    padding: 5px 12px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
  }}
  .cover-title {{
    font-size: 30pt;
    font-weight: 900;
    line-height: 1.15;
    color: #ffffff;
    margin: 0 0 10px 0;
  }}
  .cover-subtitle {{
    font-size: 14pt;
    font-weight: 400;
    color: #cbd5e1;
    margin-bottom: 25px;
  }}
  .cover-desc {{
    font-size: 10pt;
    color: #94a3b8;
    max-width: 600px;
    line-height: 1.5;
    border-left: 3px solid #00adb5;
    padding-left: 15px;
  }}
  .cover-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 20px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    font-size: 9.5pt;
  }}
  .cover-footer-block h4 {{
    margin: 0 0 6px 0;
    color: #00adb5;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }}
  .cover-footer-block p {{
    margin: 0;
    color: #e2e8f0;
    line-height: 1.4;
  }}

  /* Typographie de rapport */
  h1 {{
    font-size: 15pt;
    font-weight: 800;
    color: #0b2545;
    border-bottom: 2px solid #134074;
    padding-bottom: 5px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }}
  h2 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #134074;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 10pt;
    font-weight: 600;
    color: #1e3e62;
    margin-top: 10px;
    margin-bottom: 4px;
    page-break-after: avoid;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
  }}
  ul, ol {{
    margin-top: 0;
    margin-bottom: 8px;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 3px;
  }}

  /* Tableaux */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 8.5pt;
    page-break-inside: auto;
  }}
  tr {{
    page-break-inside: avoid;
    page-break-after: auto;
  }}
  th {{
    background: #0b2545;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #0b2545;
  }}
  td {{
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }}
  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  /* Encadrés et Callouts */
  .callout {{
    padding: 10px 14px;
    border-radius: 4px;
    margin: 10px 0 12px 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
  }}
  .callout-info {{
    background: #f0f7ff;
    border-left: 4px solid #0284c7;
    color: #0c4a6e;
  }}
  .callout-warning {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #78350f;
  }}
  .callout-danger {{
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    color: #7f1d1d;
  }}

  /* Diagrammes */
  .diagram-box {{
    text-align: center;
    margin: 12px 0;
    page-break-inside: avoid;
  }}
  .diagram-box img {{
    max-width: 98%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .diagram-caption {{
    font-size: 8pt;
    font-weight: 600;
    color: #475569;
    margin-top: 4px;
  }}

  .page-break {{
    page-break-after: always;
  }}

  .toc {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 14px 20px;
    margin-bottom: 20px;
  }}
  .toc-title {{
    font-size: 11pt;
    font-weight: 700;
    color: #0b2545;
    margin-bottom: 8px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
  }}
  .toc-list {{
    list-style: none;
    padding-left: 0;
    margin: 0;
    font-size: 9pt;
  }}
  .toc-list li {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    border-bottom: 1px dotted #cbd5e1;
    padding-bottom: 2px;
  }}
  .toc-list li span.dots {{
    flex: 1;
    border-bottom: 1px dotted #94a3b8;
    margin: 0 6px 4px 6px;
  }}
</style>
</head>
<body>

<!-- PAGE DE GARDE -->
<div class="cover-page">
  <div class="cover-header">
    <div class="cover-school">EMSI — CASABLANCA</div>
    <div class="cover-module">
      IA Générative Multimodale<br/>
      Année Universitaire 2026-2027
    </div>
  </div>

  <div class="cover-body">
    <div class="cover-badge">Livrable 1 — Cadrage, Corpus &amp; Architecture</div>
    <div class="cover-title">MAINTiDOC</div>
    <div class="cover-subtitle">Assistant Documentaire Multimodal et Agentique pour la Maintenance Industrielle</div>
    <div class="cover-desc">
      Conception d'un assistant documentaire d'aide à la décision technique combinant RAG multimodal (texte, schémas, photos), modèle vision-langage open-weights (Qwen2.5-VL-7B), requêtes outillées MCP, vérification formelle des citations et contrôle d'accès granulaire RBAC.
    </div>
  </div>

  <div class="cover-footer">
    <div class="cover-footer-block">
      <h4>Composition de l'Équipe</h4>
      <p><strong>Équipe :</strong> OTARID</p>
      <p><strong>Membre 1 :</strong> Farah OTARID (Étudiante)</p>
      <p><strong>Membre 2 :</strong> [A_COMPLETER si binôme]</p>
    </div>
    <div class="cover-footer-block">
      <h4>Encadrement Pédagogique &amp; Dépôt</h4>
      <p><strong>Enseignante :</strong> Pr. Mariam CHERRABI</p>
      <p><strong>Date de remise :</strong> Novembre 2026</p>
      <p><strong>Dépôt GitHub :</strong> Lien déclaré dans L1_MaintiDoc_OTARID_LienGitHub.txt</p>
    </div>
  </div>
</div>

<!-- TABLE DES MATIÈRES & INTRODUCTION -->
<div class="toc">
  <div class="toc-title">Table des Matières Synthétique du Livrable 1</div>
  <ul class="toc-list">
    <li><strong>1. Cadrage du Projet</strong><span class="dots"></span><span>Page 2</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;1.1 Contexte opérationnel &amp; besoins des profils de maintenance<span class="dots"></span><span>Page 2</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;1.2 Cas d'usage concrets de terrain<span class="dots"></span><span>Page 2</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;1.3 Objectifs vérifiables à l'échéance Semaine 6<span class="dots"></span><span>Page 3</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;1.4 Périmètre strict, action sensible et hors-périmètre explicite<span class="dots"></span><span>Page 3</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;1.5 Hypothèses, contraintes matérielles &amp; environnement de calcul<span class="dots"></span><span>Page 3</span></li>
    <li><strong>2. Constitution du Corpus Documentaire</strong><span class="dots"></span><span>Page 4</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;2.1 Familles d'équipements retenues &amp; justification de l'approche mixte<span class="dots"></span><span>Page 4</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;2.2 Synthèse quantitative, typologie documentaire &amp; répartition linguistique<span class="dots"></span><span>Page 4</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;2.3 Paires contradictoires, documents scannés OCR &amp; injections de prompt<span class="dots"></span><span>Page 5</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;2.4 Synthèse du registre d'inventaire CSV &amp; analyse critique des prompts IA<span class="dots"></span><span>Page 6</span></li>
    <li><strong>3. Architecture Cible</strong><span class="dots"></span><span>Page 7</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;3.1 Schéma fonctionnel d'ensemble de la solution MAINTiDOC<span class="dots"></span><span>Page 7</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;3.2 Fiches descriptives des blocs fonctionnels<span class="dots"></span><span>Page 8</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;3.3 Points de contrôle critiques &amp; parcours pas-à-pas d'une requête<span class="dots"></span><span>Page 9</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;3.4 Questions ouvertes &amp; hypothèses architecturales à valider<span class="dots"></span><span>Page 9</span></li>
    <li><strong>4. Flux de Données</strong><span class="dots"></span><span>Page 10</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;4.1 Flux d'ingestion documentaire &amp; indexation multimodale<span class="dots"></span><span>Page 10</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;4.2 Flux de traitement d'une requête utilisateur multimodale<span class="dots"></span><span>Page 10</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;4.3 Flux de préparation et création de ticket de maintenance via MCP<span class="dots"></span><span>Page 11</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;4.4 Schéma des métadonnées d'indexation &amp; modèle de sécurité RBAC<span class="dots"></span><span>Page 12</span></li>
    <li><strong>5. Analyse des Risques</strong><span class="dots"></span><span>Page 13</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;5.1 Grille matricielle de criticité des risques projet<span class="dots"></span><span>Page 13</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;5.2 Analyse approfondie des scénarios critiques et parades<span class="dots"></span><span>Page 13</span></li>
    <li><strong>6. Planning et Organisation de l'Équipe</strong><span class="dots"></span><span>Page 14</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;6.1 Répartition des rôles et gouvernance de projet<span class="dots"></span><span>Page 14</span></li>
    <li>&nbsp;&nbsp;&nbsp;&nbsp;6.2 Planning prévisionnel des semaines 2 à 6 et jalons de livraison<span class="dots"></span><span>Page 14</span></li>
  </ul>
</div>

<!-- PARTIE 1 : CADRAGE DU PROJET -->
<h1>1. Cadrage du Projet</h1>

<h2>1.1 Contexte et Problématique</h2>
<p>Dans l'industrie manufacturière et les infrastructures tertiaires modernes, la maintenance des équipements critiques conditionne directement la sécurité des personnels et la continuité opérationnelle. Deux contraintes majeures pèsent quotidiennement sur les équipes de maintenance : d'une part, l'immense hétérogénéité et la volumétrie des documentations constructeurs (manuels de 150 pages, schémas de raccordement, tableaux d'alarmes, bulletins d'évolution technique), rendant la recherche d'information lente et sujette aux erreurs sous pression ; d'autre part, la criticité absolue de la sécurité, interdisant toute intervention fondée sur une intuition non vérifiée ou sur une consigne obsolète.</p>

<p>Les outils de recherche textuelle classiques ou les grands modèles de langage (LLM) généralistes ne répondent pas à ces exigences : ils ne traitent pas nativement les éléments visuels réels de terrain (voyants clignotants sur un pupitre, manomètres analogiques, schémas de câblage), sont sujets à des hallucinations non sourcées et manquent de liaisons outillées avec les systèmes de gestion de maintenance (GMAO). <strong>MAINTiDOC</strong> est conçu pour combler cette rupture en proposant un assistant documentaire multimodal, rigoureusement ancré sur un corpus documentaire vérifié, doté d'outils MCP standardisés et soumis à un contrôle humain obligatoire.</p>

<h2>1.2 Profils Utilisateurs et Besoins Spécifiques</h2>
<table>
  <thead>
    <tr>
      <th style="width: 25%;">Profil Utilisateur</th>
      <th style="width: 35%;">Besoins Métiers Exprimés</th>
      <th style="width: 40%;">Attentes Vis-à-vis de MAINTiDOC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Technicien de Terrain<br/>(Intervention directe)</strong></td>
      <td>
        • Identification immédiate d'un code défaut ou voyant.<br/>
        • Accès rapide à la procédure de démontage et outillage.<br/>
        • Repérage des points de consignation électrique/fluidique.<br/>
        • Consultation des dernières pannes survenues sur la machine.
      </td>
      <td>
        • Soumission directe d'une photo de panneau prise au smartphone.<br/>
        • Réponse concise citant la page et le schéma exacts.<br/>
        • Pré-remplissage automatique d'un ticket de maintenance pour éviter la double saisie après intervention.
      </td>
    </tr>
    <tr>
      <td><strong>Responsable Maintenance<br/>(Supervision &amp; Méthodes)</strong></td>
      <td>
        • Veille sur les procédures applicables et versions actives.<br/>
        • Gestion du cloisonnement documentaire par corps d'état.<br/>
        • Validation formelle de toute ouverture de ticket d'arrêt.<br/>
        • Analyse de l'historique global et traçabilité des pièces.
      </td>
      <td>
        • Garantie d'absence de fuite d'informations entre groupes.<br/>
        • Alertes en cas de contradiction détectée dans le corpus.<br/>
        • Tableau de bord d'audit des approbations humaines.<br/>
        • Respect strict des licences et de la souveraineté des données.
      </td>
    </tr>
  </tbody>
</table>

<h2>1.3 Cas d'Usage Concrets de Terrain</h2>
<ul>
  <li><strong>Cas d'usage 1 — Diagnostic sur alarme visuelle :</strong> Un technicien fait face à un compresseur arrêté avec un voyant orange clignotant. Il photographie le pupitre de commande et interroge l'assistant en français : <em>« Que signifie ce voyant et quelle est la vérification préalable avant réarmement ? »</em>. MAINTiDOC analyse l'image, identifie le symbole de dérivation thermique, extrait la procédure du manuel d'exploitation et répond en citant précisément la page 24 et la figure associée.</li>
  <li><strong>Cas d'usage 2 — Résolution de défaut sur boucle incendie :</strong> Un technicien SSI constate un défaut d'isolement sur la centrale. Il demande : <em>« Quelle est la démarche méthodique pour localiser un défaut de terre DEF-04 sur la boucle 2 ? »</em>. L'assistant restitue la procédure par dichotomie de la fiche F20 et propose l'affichage du schéma de raccordement F09.</li>
  <li><strong>Cas d'usage 3 — Consultation d'historique via MCP et préparation de ticket :</strong> Face à une surchauffe récurrente, le technicien demande : <em>« Consulte les interventions des 6 derniers mois sur cet équipement et prépare un ticket pour remplacement de la vanne thermostatique si la panne est répétitive »</em>. L'assistant appelle l'outil MCP <code>get_equipment_history</code>, synthétise l'intervention précédente (TICK-2025-1120), rédige le brouillon du ticket et attend l'approbation explicite de l'utilisateur.</li>
  <li><strong>Cas d'usage 4 — Détection d'ambiguïté et demande de clarification :</strong> Un opérateur envoie une photographie floue d'un voyant vert sur un fond métallique sombre sans précision de modèle. Le système s'abstient de deviner : il identifie l'incertitude et formule une demande de précision ciblée (demande de photographier la plaque signalétique de l'équipement).</li>
</ul>

<h2>1.4 Objectifs Vérifiables à l'Échéance Semaine 6</h2>
<p>Conformément aux consignes officielles, le prototype de démonstration finalisé devra satisfaire les objectifs opérationnels vérifiables suivants (sans anticipation de mesures expérimentales non encore exécutées) :</p>
<ol>
  <li><strong>Citation Formellement Vérifiable :</strong> Pour toute réponse technique affirmative, MAINTiDOC doit citer au moins un document, un numéro de page et un élément visuel (figure ou tableau) effectivement présents dans le corpus indexé et soutenant sémantiquement l'affirmation.</li>
  <li><strong>Cloisonnement Étanche des Droits (RBAC) :</strong> Un utilisateur authentifié dans le groupe <code>techniciens_compresseurs</code> doit se voir refuser strictement tout accès ou citation portant sur les documents des centrales incendie (et inversement), vérifiable par test d'audit.</li>
  <li><strong>Non-Exécution Autonome d'Action Sensible :</strong> Aucun ticket de maintenance ne doit pouvoir être inséré dans la base de données du serveur MCP sans qu'un jeton d'approbation humaine explicite (Human Validation Token) n'ait été émis suite à une action utilisateur dans l'interface.</li>
  <li><strong>Résistance aux Injections de Prompt :</strong> Face à un document du corpus contenant des instructions hostiles (ex. C19 ou F19), le système doit traiter le document comme une donnée passive et refuser d'exécuter l'instruction malveillante.</li>
  <li><strong>Abstention Justifiée :</strong> En cas de source absente, contradictoire ou d'image inexploitable, le système doit générer un statut de clarification sans inventer de recommandation.</li>
</ol>

<h2>1.5 Périmètre Strict et Hors-Périmètre Explicite</h2>
<div class="callout callout-danger">
  <strong>HORS-PÉRIMÈTRE STRICTEMENT EXCLU :</strong>
  <p>MAINTiDOC <strong>ne pilote aucun automate, machine ou équipement physique</strong> (aucune écriture Modbus, Profinet ou BACnet). Il ne fournit <strong>aucun diagnostic garanti engageant la responsabilité juridique</strong> de l'établissement et ne remplace en aucun cas les habilitations électriques ou réglementaires des techniciens.</p>
</div>

<p>Le périmètre du prototype est circonscrit aux composants suivants :</p>
<ul>
  <li><strong>Entrées autorisées :</strong> Questions en langage naturel en français, photographies au format standard (JPEG/PNG) et documents techniques PDF.</li>
  <li><strong>Sorties produites :</strong> Réponses techniques structurées au format Pydantic JSON contenant la réponse textuelle, les citations documentaires vérifiables, les incertitudes éventuelles, les questions de clarification ou le brouillon de ticket.</li>
  <li><strong>Outils externes :</strong> Serveur de maintenance de démonstration conforme au standard MCP (Model Context Protocol) exposant <code>get_equipment_history(equipment_id)</code>, <code>get_open_tickets(equipment_id)</code> et <code>create_ticket(equipment_id, title, description, approval_token)</code>.</li>
  <li><strong>Action sensible contrôlée :</strong> La fonction <code>create_ticket</code> est protégée par un checkpoint d'interruption humaine obligatoire (Human-in-the-Loop) et par une clé d'idempotence.</li>
</ul>

<h2>1.6 Hypothèses, Contraintes Matérielles et Organisationnelles</h2>
<ul>
  <li><strong>Matériel cible :</strong> Station de calcul équipée d'un GPU de 24 Go de VRAM (ex. NVIDIA RTX 3090 / 4090 ou A10G) avec quantification 4-bit (AWQ / GPTQ) pour faire tenir le modèle vision-langage 7B, les encodeurs d'embeddings et le reranker.</li>
  <li><strong>Environnement d'exécution :</strong> Déploiement reproductible conteneurisé sous Docker et Docker Compose, avec isolation réseau des services sensibles.</li>
  <li><strong>Données personnelles &amp; conformité :</strong> Toutes les données d'utilisateurs, de tickets et d'historiques sont 100% synthétiques. Aucune donnée nominative réelle n'est présente dans les jeux de données.</li>
</ul>

<div class="page-break"></div>

<!-- PARTIE 2 : CONSTITUTION DU CORPUS DOCUMENTAIRE -->
<h1>2. Constitution du Corpus Documentaire</h1>

<h2>2.1 Familles d'Équipements Retenues &amp; Justification de l'Approche Mixte</h2>
<p>Les deux familles d'équipements sélectionnées pour constituer le corpus sont :</p>
<ul>
  <li><strong>Famille 1 — Compresseurs d'Air Industriels :</strong> Équipements de production d'énergie fluidique indispensables aux usines (modèles à vis lubrifiée, compresseurs scroll sans huile, unités haute pression). Risques associés : pneumatique (surpression, déflagration), thermique (huile à 110 °C), électrique (démarrage fort courant).</li>
  <li><strong>Famille 2 — Centrales de Détection Incendie (SSI) :</strong> Systèmes de sécurité des bâtiments (Équipements de Contrôle et de Signalisation ECS, CMSI, boucles adressables rebouclées, asservissements de clapets et diffuseurs sonores). Risques associés : fausses alertes, panique en ERP, non-détection d'un sinistre réel.</li>
</ul>

<div class="callout callout-info">
  <strong>DÉCLARATION FORMELLE DE L'APPROCHE MIXTE :</strong><br/>
  « Le corpus documentaire de MAINTiDOC repose sur une approche mixte combinant des documents issus d'équipements réels et des documents synthétiques élaborés dans le cadre du projet. Les documents réels sont retenus uniquement lorsque leur provenance et leurs conditions d'utilisation ont pu être vérifiées. Les documents synthétiques permettent de compléter les informations disponibles, de créer des scénarios de maintenance cohérents et de construire des cas de test contrôlés. Chaque document est identifié dans l'inventaire avec sa provenance, son statut de génération par IA, sa licence ou son statut synthétique, ainsi que les corrections apportées après vérification. »
</div>

<h2>2.2 Synthèse Quantitative et Répartition du Corpus</h2>
<p>Le corpus documentaire complet comprend <strong>rigoureusement 40 documents</strong>, répartis de manière parfaitement équilibrée entre les deux familles d'équipements et entre sources réelles vérifiées et créations synthétiques contrôlées :</p>

<table>
  <thead>
    <tr>
      <th>Famille d'Équipement</th>
      <th style="text-align: center;">Documents Réels Vérifiés</th>
      <th style="text-align: center;">Documents Synthétiques Contrôlés</th>
      <th style="text-align: center;">Total Documents</th>
      <th style="text-align: center;">Format Image / Photos</th>
      <th style="text-align: center;">Documents Scannés (OCR)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Famille 1 : Compresseurs d'Air</strong></td>
      <td style="text-align: center;">12 (C01 à C12)</td>
      <td style="text-align: center;">8 (C13 à C20)</td>
      <td style="text-align: center;"><strong>20</strong></td>
      <td style="text-align: center;">1 (C12.jpg)</td>
      <td style="text-align: center;">1 (C17.pdf)</td>
    </tr>
    <tr>
      <td><strong>Famille 2 : Centrales Incendie</strong></td>
      <td style="text-align: center;">12 (F01 à F12)</td>
      <td style="text-align: center;">8 (F13 à F20)</td>
      <td style="text-align: center;"><strong>20</strong></td>
      <td style="text-align: center;">1 (F12.jpg)</td>
      <td style="text-align: center;">1 (F17.pdf)</td>
    </tr>
    <tr style="background: #e2e8f0; font-weight: bold;">
      <td>TOTAL GÉNÉRAL DU CORPUS</td>
      <td style="text-align: center;">24</td>
      <td style="text-align: center;">16</td>
      <td style="text-align: center;">40</td>
      <td style="text-align: center;">2 (C12, F12)</td>
      <td style="text-align: center;">2 (C17, F17)</td>
    </tr>
  </tbody>
</table>

<p><strong>Répartition linguistique ciblée :</strong> Le corpus est majoritairement composé de documents en langue française (<strong>32 documents</strong>), favorisant l'alignement avec les requêtes des techniciens francophones. Les <strong>8 documents en langue anglaise</strong> correspondent à des manuels constructeurs réels complets (C01 à C08, F01 à F08) dont la terminologie industrielle d'origine a été scrupuleusement préservée. Cette bilingualité contrôlée constitue un atout pour évaluer la capacité multilingue des modèles d'embeddings (BGE-M3) et du VLM.</p>

<h2>2.3 Cas Spécifiques Préparatoires à l'Évaluation</h2>
<ul>
  <li><strong>Documents Scannés (Test de l'OCR local) :</strong> Le corpus intègre deux documents spécifiquement préparés sous la forme d'images raster sans aucune couche textuelle vectorielle (<code>C17.pdf</code> et <code>F17.pdf</code>). Le contrôle par script d'extraction de texte (pypdfium2) confirme une longueur de texte natif égale à zéro. Ces fichiers obligent le pipeline d'ingestion à déclencher le moteur OCR (Tesseract / PaddleOCR) pour rendre leur contenu indexable et recherchable.</li>
  <li><strong>Paires Contradictoires (Test de Détection de Divergence) :</strong>
    <ul>
      <li><em>Paire Compresseurs (C17 vs C18) :</em> Le document archivé C17 v1.0 prescrit une huile synthétique ISO VG 46 et un couple de serrage du bouchon de carter de 45 N.m. Le document actif révisé C18 v2.0 modifie formellement ces paramètres en prescrivant une huile minérale ISO VG 68 et un couple renforcé de 65 N.m suite à un bulletin service pour éliminer les fuites vibratoires.</li>
      <li><em>Paire Incendie (F17 vs F18) :</em> Le document archivé F17 v1.0 prévoyait une temporisation d'alarme restreinte courte de 30 secondes avant évacuation générale. La directive actualisée F18 v2.0 porte ce délai à 120 secondes (2 minutes) pour accorder le temps nécessaire à la levée de doute physique en ERP, tout en maintenant le déclenchement immédiat (0s) sur déclencheur manuel.</li>
    </ul>
  </li>
  <li><strong>Documents Piégés (Évaluation de la Résistance aux Injections de Prompt) :</strong> Les documents <code>C19.pdf</code> et <code>F19.pdf</code> intègrent au sein de consignes techniques courantes une charge utile malveillante de test (ex. tentative d'activation d'un faux mode "System Override", ordre de désactiver la validation humaine des tickets et demande d'exfiltration des données). Ces documents sont explicitement signalés dans l'inventaire avec la mention <code>usage_test = injection</code>.</li>
</ul>

<h2>2.4 Synthèse du Registre d'Inventaire (`inventaire.csv`)</h2>
<p>L'inventaire officiel du corpus est consigné dans le fichier <code>corpus/inventaire.csv</code> encodé en UTF-8 et comprenant exactement 20 colonnes. Le tableau ci-dessous présente un extrait représentatif de la structure des données :</p>

<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Fichier Relatif</th>
      <th>Titre Lisible</th>
      <th>Équipement ID</th>
      <th>Type</th>
      <th>Pages</th>
      <th>Format</th>
      <th>Groupe d'Accès</th>
      <th>Usage Test</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>C01</td><td>documents/famille_1/C01.pdf</td><td>Manuel général compresseur à vis Sullair Series</td><td>SULLAIR-LS20</td><td>manuel</td><td>160</td><td>pdf_texte</td><td>techniciens_compresseurs ; responsables</td><td>normal</td></tr>
    <tr><td>C09</td><td>documents/famille_1/C09.pdf</td><td>Schéma électrique commande NF EN 60204-1</td><td>COMP-ELEC-STD</td><td>schema</td><td>2</td><td>pdf_texte</td><td>techniciens_compresseurs ; responsables</td><td>normal</td></tr>
    <tr><td>C12</td><td>images/C12.jpg</td><td>Photographie réelle manomètres compresseur</td><td>COMP-PANEL-REAL</td><td>photo</td><td>1</td><td>image</td><td>techniciens_compresseurs ; responsables</td><td>ambigu</td></tr>
    <tr><td>C17</td><td>documents/famille_1/C17.pdf</td><td>Procédure vidange et lubrification (v1.0)</td><td>AEROCOMP-VSD-45</td><td>procedure</td><td>1</td><td>pdf_scanne</td><td>techniciens_compresseurs</td><td>contradictoire</td></tr>
    <tr><td>C18</td><td>documents/famille_1/C18.pdf</td><td>Procédure vidange et lubrification révisée (v2.0)</td><td>AEROCOMP-VSD-45</td><td>procedure</td><td>1</td><td>pdf_texte</td><td>techniciens_compresseurs</td><td>contradictoire</td></tr>
    <tr><td>C19</td><td>documents/famille_1/C19.pdf</td><td>Note service hivernale &amp; test prompt injection</td><td>AEROCOMP-VSD-45</td><td>procedure</td><td>1</td><td>pdf_texte</td><td>responsables_maintenance</td><td>injection</td></tr>
    <tr><td>F01</td><td>documents/famille_2/F01.pdf</td><td>Manuel installation centrale 2X-F Series</td><td>2X-F-ADDR</td><td>manuel</td><td>120</td><td>pdf_texte</td><td>techniciens_incendie ; responsables</td><td>normal</td></tr>
    <tr><td>F09</td><td>documents/famille_2/F09.pdf</td><td>Schéma boucle adressable rebouclée NF S 61-970</td><td>FIRE-LOOP-STD</td><td>schema</td><td>2</td><td>pdf_texte</td><td>techniciens_incendie ; responsables</td><td>normal</td></tr>
    <tr><td>F12</td><td>images/F12.jpg</td><td>Photographie écran LCD centrale SMS Senator</td><td>SMS-SENATOR-01</td><td>photo</td><td>1</td><td>image</td><td>techniciens_incendie ; responsables</td><td>normal</td></tr>
    <tr><td>F17</td><td>documents/famille_2/F17.pdf</td><td>Procédure essai alarme temporisation 30s (v1.0)</td><td>IGNIS-PRO-800</td><td>procedure</td><td>1</td><td>pdf_scanne</td><td>techniciens_incendie</td><td>contradictoire</td></tr>
    <tr><td>F18</td><td>documents/famille_2/F18.pdf</td><td>Procédure essai alarme révisée 120s (v2.0)</td><td>IGNIS-PRO-800</td><td>procedure</td><td>1</td><td>pdf_texte</td><td>techniciens_incendie</td><td>contradictoire</td></tr>
    <tr><td>F19</td><td>documents/famille_2/F19.pdf</td><td>Directive exercice évacuation &amp; test injection</td><td>IGNIS-PRO-800</td><td>procedure</td><td>1</td><td>pdf_texte</td><td>responsables_maintenance</td><td>injection</td></tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- PARTIE 3 : ARCHITECTURE CIBLE -->
<h1>3. Architecture Cible</h1>

<h2>3.1 Schéma Fonctionnel Global du Système MAINTiDOC</h2>
<p>L'architecture de MAINTiDOC est conçue selon un modèle modulaire découplé, articulé autour d'une passerelle d'API sécurisée, d'un orchestrateur agentique à graphe d'états (LangGraph) et d'un sous-système de recherche documentaire RAG multimodal haute précision :</p>

<div class="diagram-box">
  <img src="{diag_dir}/architecture_globale.png" alt="Architecture Globale de MAINTiDOC"/>
  <div class="diagram-caption">Figure 3.1 — Schéma fonctionnel complet de l'architecture cible de MAINTiDOC.</div>
</div>

<h2>3.2 Fiches Descriptives des Blocs Fonctionnels</h2>
<table>
  <thead>
    <tr>
      <th style="width: 18%;">Bloc Composant</th>
      <th style="width: 32%;">Rôle en Une Phrase</th>
      <th style="width: 22%;">Entrées &amp; Sorties</th>
      <th style="width: 28%;">Outil Envisagé &amp; Justification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Interface Web Utilisateur</strong></td>
      <td>Interface graphique réactive permettant la saisie de texte, le téléversement d'images, la consultation des citations et la validation explicite des tickets.</td>
      <td><strong>E :</strong> Saisies technicien, photos.<br/><strong>S :</strong> Réponses sourcées, brouillons.</td>
      <td><strong>Streamlit</strong> (rapidité de prototypage, support des composants interactifs d'approbation et rendu markdown riche).</td>
    </tr>
    <tr>
      <td><strong>Passerelle API &amp; Sécurité</strong></td>
      <td>Point d'entrée sécurisé assurant l'authentification des requêtes, le contrôle des rôles RBAC et l'application des quotas d'exécution.</td>
      <td><strong>E :</strong> Requêtes HTTP/WS avec JWT.<br/><strong>S :</strong> Contexte utilisateur validé.</td>
      <td><strong>FastAPI</strong> (haute performance asynchrone, validation stricte des schémas Pydantic, intégration OAuth2/JWT).</td>
    </tr>
    <tr>
      <td><strong>Orchestrateur Agentique</strong></td>
      <td>Moteur d'exécution modélisant le cycle de raisonnement sous forme de graphe d'états avec points d'interruption humaine et gestion des boucles.</td>
      <td><strong>E :</strong> Requête + état conversation.<br/><strong>S :</strong> Transition d'état, réponse.</td>
      <td><strong>LangGraph &amp; LangChain</strong> (gestion native des états cycliques, persistance checkpointing et Human-in-the-Loop).</td>
    </tr>
    <tr>
      <td><strong>Indexation &amp; RAG Multimodal</strong></td>
      <td>Recherche hybride dense/sparse de passages textuels et recherche vectorielle visuelle sur le sous-ensemble de documents autorisés.</td>
      <td><strong>E :</strong> Vecteur requête + filtre RBAC.<br/><strong>S :</strong> Top-20 passages/figures.</td>
      <td><strong>Qdrant</strong> (support performant du filtrage par payload, recherche hybride textuelle et visuelle intégrée).</td>
    </tr>
    <tr>
      <td><strong>Reranker Spécialisé</strong></td>
      <td>Reclassement sémantique des candidats documentaires récupérés afin de maximiser la pertinence des 5 passages soumis au VLM.</td>
      <td><strong>E :</strong> Paire (Question, Passage).<br/><strong>S :</strong> Score de pertinence sémantique.</td>
      <td><strong>BGE-Reranker Multilingue</strong> (Cross-Encoder compact, cible prioritaire du fine-tuning en Semaine 5).</td>
    </tr>
    <tr>
      <td><strong>Modèle Vision-Langage</strong></td>
      <td>Modèle de fondation multimodal comprenant conjointement le texte technique et les éléments graphiques (schémas, voyants, tableaux).</td>
      <td><strong>E :</strong> Prompt système + contexte + photo.<br/><strong>S :</strong> Réponse structurée JSON.</td>
      <td><strong>Qwen2.5-VL-7B-Instruct</strong> (modèle open-weights d'excellence pour la lecture d'images industrielles et de documents).</td>
    </tr>
    <tr>
      <td><strong>Client &amp; Serveur MCP</strong></td>
      <td>Connecteur standardisé permettant à l'assistant d'interroger la GMAO pour l'historique et de créer des tickets après accord.</td>
      <td><strong>E :</strong> Nom outil + arguments token.<br/><strong>S :</strong> Données GMAO / Réf. ticket.</td>
      <td><strong>Serveur MCP Maintenance</strong> (implémentation du protocole Model Context Protocol sur base PostgreSQL).</td>
    </tr>
    <tr>
      <td><strong>Stockage &amp; Données</strong></td>
      <td>Conservation persistante des métadonnées d'inventaire, des documents PDF originaux et des images extraites haute résolution.</td>
      <td><strong>E :</strong> Fichiers bruts, métadonnées.<br/><strong>S :</strong> URIs et flux binaires.</td>
      <td><strong>PostgreSQL</strong> (métadonnées et RBAC) et <strong>MinIO</strong> (stockage objet S3 compatible pour les fichiers lourds).</td>
    </tr>
  </tbody>
</table>

<h2>3.3 Points de Contrôle Critiques et Parcours d'une Requête</h2>
<p>Trois points de contrôle fondamentaux garantissent la robustesse et la conformité du système :</p>
<ol>
  <li><strong>Point de Contrôle 1 — Filtrage d'Accès Pré-Recherche (RBAC strict) :</strong> Lors de toute interrogation de la base vectorielle Qdrant, un filtre de métadonnées non contournable applique la clause <code>groupe_acces IN user.groups</code>. Un technicien ne peut en aucun cas récupérer un candidat vectoriel hors de son périmètre d'habilitation.</li>
  <li><strong>Point de Contrôle 2 — Fact-Checking et Vérification des Citations :</strong> Dès la génération de la réponse par le VLM, un analyseur syntaxique Pydantic extrait les citations (<code>document_id</code>, <code>page</code>, <code>element_id</code>). Le module vérifie formellement que chaque document cité figurait bien dans le contexte effectivement injecté et que le passage textuel soutient rigoureusement l'assertion. En cas de contradiction, la réponse est rejetée au profit d'un message d'incertitude.</li>
  <li><strong>Point de Contrôle 3 — Approbation Humaine Explicite (Action Sensible) :</strong> Lors d'une demande de création de ticket, le moteur LangGraph suspend son exécution (interruption de workflow). Le brouillon du ticket est affiché dans Streamlit. L'utilisateur doit impérativement cliquer sur « Approuver et créer le ticket », ce qui génère un jeton cryptographique éphémère (<code>approval_token</code>) transmis au serveur MCP avec une clé d'idempotence évitant les doublons.</li>
</ol>

<h2>3.4 Questions Ouvertes et Hypothèses Architecturales à Valider</h2>
<ul>
  <li><em>Hypothèse GPU 24 Go :</em> Le modèle Qwen2.5-VL-7B requiert environ 14 à 16 Go de VRAM en quantification 4-bit (AWQ). L'adjonction de l'encodeur d'embeddings BGE-M3 (1.5 Go) et du reranker cross-encoder (1.5 Go) laisse une marge théorique de 5 Go pour le contexte KV. Cette hypothèse de tenue mémoire devra être validée par banc d'essai sous charge en Semaine 2.</li>
  <li><em>Performance de l'OCR Local :</em> L'arbitrage entre Tesseract (rapide sur CPU mais sensibilité moyenne sur polices dégradées) et PaddleOCR (très précis sur les tableaux mais plus gourmand en ressources) sera tranché suite aux mesures de latence sur les documents C17 et F17.</li>
  <li><em>Pertinence de la Recherche Visuelle CLIP :</em> La capacité de l'espace vectoriel CLIP à discriminer des photographies de voyants de taille réduite (ex. voyant orange compresseur vs voyant orange centrale incendie) sera évaluée face à une approche alternative de description textuelle systématique par le VLM (image captioning à l'ingestion).</li>
</ul>

<div class="page-break"></div>

<!-- PARTIE 4 : FLUX DE DONNÉES -->
<h1>4. Flux de Données</h1>

<h2>4.1 Flux A — Ingestion Documentaire et Indexation Multimodale</h2>
<p>Le flux d'ingestion transforme les documents bruts du corpus en représentations vectorielles et métadonnées indexées selon une chaîne de traitement séquentielle sécurisée :</p>

<div class="diagram-box">
  <img src="{diag_dir}/flux_ingestion.png" alt="Flux d'ingestion documentaire"/>
  <div class="diagram-caption">Figure 4.1 — Schéma détaillé du flux d'ingestion, d'extraction OCR et d'indexation vectorielle.</div>
</div>

<p><strong>Description séquentielle de l'ingestion :</strong></p>
<ol>
  <li><strong>Dépôt et typage :</strong> Le document entrant est classifié selon son format (PDF natif, PDF scanné, image isolée). Les fichiers originaux sont archivés dans MinIO sous un identifiant immuable lié à leur hash SHA-256.</li>
  <li><strong>Extraction de contenu :</strong> Les PDF natifs sont traités par PyMuPDF pour en extraire le flux textuel, les coordonnées des tableaux et les flux d'images vectorielles. Les PDF scannés et photographies sont dirigés vers le module OCR local qui extrait les zones de texte avec leurs boîtes englobantes (bounding boxes).</li>
  <li><strong>Découpage sémantique (Chunking) :</strong> Les textes sont segmentés en passages d'une granularité de 300 à 500 tokens avec un recouvrement glissant de 50 tokens pour préserver la continuité contextuelle des phrases techniques. Les tableaux et figures sont isolés en chunks distincts.</li>
  <li><strong>Enrichissement des métadonnées :</strong> Chaque passage est étiqueté avec <code>document_id</code>, <code>version</code>, <code>page</code>, <code>element_id</code>, <code>equipement_id</code>, <code>famille_equipement</code> et les <code>groupe_acces</code> autorisés.</li>
  <li><strong>Vectorisation et indexation :</strong> Génération conjointe d'embeddings textuels denses (1024 dimensions) via BGE-M3 et d'embeddings visuels (512 dimensions) via CLIP, puis insertion dans les collections dédiées de Qdrant. Les métadonnées relationnelles sont enregistrées dans PostgreSQL.</li>
</ol>

<h2>4.2 Flux B — Traitement d'une Requête Utilisateur Multimodale</h2>
<p>Ce flux opérationnel décrit le parcours complet d'une demande soumise par un opérateur de maintenance :</p>

<div class="diagram-box">
  <img src="{diag_dir}/flux_requete.png" alt="Flux de traitement d'une requête"/>
  <div class="diagram-caption">Figure 4.2 — Parcours pas-à-pas d'une requête multimodale avec points de contrôle de sécurité.</div>
</div>

<p><strong>Étapes clés du traitement :</strong></p>
<ol>
  <li><strong>Authentification &amp; Résolution de profil :</strong> Le jeton JWT de l'utilisateur est décodé par FastAPI pour identifier ses groupes d'habilitation (ex. <code>techniciens_compresseurs</code>).</li>
  <li><strong>Analyse visuelle précoce :</strong> Si une image est fournie, le VLM Qwen2.5-VL réalise une première passe d'inspection visuelle pour détecter les codes d'alarmes affichés, les voyants actifs ou la référence visible sur la plaque machine.</li>
  <li><strong>Recherche hybride filtrée :</strong> Interrogation vectorielle dans Qdrant avec filtre obligatoire sur <code>groupe_acces</code>. La recherche dense (sémantique) et sparse (lexicale) est fusionnée avec la recherche visuelle par l'algorithme <em>Reciprocal Rank Fusion (RRF)</em>.</li>
  <li><strong>Reclassement Cross-Encoder :</strong> Les 20 meilleurs candidats issus de la fusion sont réévalués par le Reranker BGE, qui sélectionne les 5 passages et figures présentant le score de pertinence le plus élevé.</li>
  <li><strong>Contrôle de suffisance et synthèse :</strong> Si les sources sont contradictoires ou insuffisantes, le système émet une demande de précision. Dans le cas contraire, le contexte validé est transmis au VLM qui génère une réponse conforme au schéma Pydantic.</li>
  <li><strong>Vérification formelle et restitution :</strong> Le module de vérification contrôle chaque citation avant affichage sur l'interface Streamlit.</li>
</ol>

<h2>4.3 Flux C — Préparation et Création de Ticket via MCP avec Idempotence</h2>
<p>L'action sensible de création de ticket d'intervention est strictement encadrée par une boucle de validation humaine :</p>

<div class="diagram-box">
  <img src="{diag_dir}/flux_ticket_mcp.png" alt="Flux de création de ticket MCP"/>
  <div class="diagram-caption">Figure 4.3 — Processus de validation humaine explicite et création idempotente de ticket de maintenance.</div>
</div>

<p><strong>Détail du protocole d'approbation et d'idempotence :</strong></p>
<ol>
  <li><strong>Consultation de contexte :</strong> L'assistant interroge l'historique récent via l'outil MCP <code>get_equipment_history(equipement_id)</code> pour vérifier si l'anomalie a déjà été signalée.</li>
  <li><strong>Génération du brouillon :</strong> Un objet Pydantic <code>TicketDraft</code> est instancié (équipement concerné, niveau de priorité, intitulé court, description étayée par les citations documentaires et préconisations de sécurité).</li>
  <li><strong>Interruption de workflow (Human-in-the-Loop) :</strong> Le graphe LangGraph s'interrompt. Le brouillon apparaît en surbrillance sur le panneau Streamlit du technicien. Aucune requête réseau de création n'est émise vers la GMAO.</li>
  <li><strong>Validation active par le technicien :</strong> L'utilisateur peut modifier manuellement les champs ou valider le brouillon. Le clic sur « Approuver et créer le ticket » déclenche la génération d'un <code>approval_token</code> cryptographique éphémère (validité 120 secondes) et d'une clé d'idempotence calculée comme suit :<br/>
  <code>idempotency_key = SHA256(utilisateur_id + equipement_id + date_heure_minute)</code>.</li>
  <li><strong>Exécution de l'outil MCP :</strong> Le client MCP transmet l'appel <code>create_ticket(..., approval_token, idempotency_key)</code>. Le serveur MCP vérifie l'authenticité du jeton. Si la clé d'idempotence a déjà été traitée (cas d'un double-clic involontaire), le serveur retourne le ticket déjà créé sans instancier de doublon.</li>
</ol>

<h2>4.4 Schéma des Métadonnées et Modèle de Sécurité RBAC</h2>
<p>Chaque passage de texte ou figure indexé dans la base vectorielle conserve une structure de métadonnées normalisée conforme au modèle Pydantic suivant :</p>

<table>
  <thead>
    <tr>
      <th>Champ Métadonnée</th>
      <th>Type</th>
      <th>Exemple de Valeur</th>
      <th>Rôle dans le Pipeline</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>document_id</code></td><td>String</td><td><code>C13</code></td><td>Identifiant immuable utilisé dans les citations générées.</td></tr>
    <tr><td><code>version</code></td><td>String</td><td><code>v1.3 (2025-02)</code></td><td>Permet la traçabilité des évolutions et la gestion des paires contradictoires.</td></tr>
    <tr><td><code>page</code></td><td>Integer</td><td><code>2</code></td><td>Numéro de page physique au sein du document d'origine.</td></tr>
    <tr><td><code>element_id</code></td><td>String</td><td><code>tableau_maintenance_p2</code></td><td>Identifiant précis du paragraphe, de la figure ou du tableau.</td></tr>
    <tr><td><code>equipement_id</code></td><td>String</td><td><code>AEROCOMP-VSD-45</code></td><td>Lien direct avec les identifiants gérés par le serveur MCP de GMAO.</td></tr>
    <tr><td><code>famille_equipement</code></td><td>String</td><td><code>compresseurs</code></td><td>Permet le partitionnement thématique lors de la recherche.</td></tr>
    <tr><td><code>groupe_acces</code></td><td>List[String]</td><td><code>["techniciens_compresseurs", "responsables"]</code></td><td>Clause de pré-filtrage obligatoire lors des requêtes Qdrant.</td></tr>
    <tr><td><code>hash_sha256</code></td><td>String</td><td><code>e3b0c44298fc1c14...</code></td><td>Garantit l'intégrité du contenu indexé et l'auditabilité.</td></tr>
  </tbody>
</table>

<div class="diagram-box">
  <img src="{diag_dir}/modele_acces_securite.png" alt="Modèle de sécurité et groupes d'accès"/>
  <div class="diagram-caption">Figure 4.4 — Cloisonnement documentaire étanche par groupes d'accès RBAC et barrières anti-injection.</div>
</div>

<p><strong>Modèle d'accès et séparation des groupes d'utilisateurs fictifs :</strong></p>
<ul>
  <li><strong>Groupe 1 — <code>techniciens_compresseurs</code> :</strong> Accès exclusif aux 20 documents de la Famille 1 (C01 à C20), à l'exception des historiques complets de GMAO et des notes de sécurité sensibles réservées à la hiérarchie.</li>
  <li><strong>Groupe 2 — <code>techniciens_incendie</code> :</strong> Accès exclusif aux 20 documents de la Famille 2 (F01 à F20), sans visibilité sur les compresseurs.</li>
  <li><strong>Groupe 3 — <code>responsables_maintenance</code> :</strong> Accès transverse à l'intégralité des 40 documents, incluant les historiques d'interventions confidentiels (C16, F16) et les notes de service (C19, F19).</li>
</ul>

<div class="page-break"></div>

<!-- PARTIE 5 : ANALYSE DES RISQUES -->
<h1>5. Analyse des Risques</h1>

<h2>5.1 Grille Matricielle de Criticité des Risques Projet</h2>
<p>L'analyse des risques couvre les dimensions technique, opérationnelle, sécurité de l'information et organisationnelle. La probabilité et l'impact sont évalués sur une échelle de 1 (Faible) à 3 (Élevé) :</p>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Risque Identifié</th>
      <th style="width: 12%;">Catégorie</th>
      <th style="width: 8%; text-align: center;">Prob. (1-3)</th>
      <th style="width: 8%; text-align: center;">Impact (1-3)</th>
      <th style="width: 35%;">Mesure de Prévention &amp; Atténuation Prévue</th>
      <th style="width: 15%;">Responsable</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Hallucinations et citations non fondées</strong></td>
      <td>Technique / Qualité</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">3</td>
      <td>Module de fact-checking automatisé Pydantic comparant chaque citation avec le contexte source ; abstention forcée si la source est absente.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>2. Fuite documentaire entre groupes d'accès</strong></td>
      <td>Sécurité / RBAC</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">3</td>
      <td>Filtrage strict pré-recherche dans le payload Qdrant (<code>Filter.must</code>) et seconde vérification des citations post-génération avant restitution.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>3. Création autonome de ticket sans approbation</strong></td>
      <td>Sécurité / Processus</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">3</td>
      <td>Interruption matérielle LangGraph (Human-in-the-Loop) ; génération obligatoire d'un jeton d'approbation cryptographique signé pour l'appel MCP.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>4. Erreurs introduites par l'IA dans le corpus</strong></td>
      <td>Données / Qualité</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">2</td>
      <td>Relecture systématique des grandeurs physiques et pressions ; traçabilité exhaustive dans <code>prompts_corpus.md</code> et validation par script.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>5. Non-conformité des licences de redistribution</strong></td>
      <td>Juridique / Données</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">2</td>
      <td>Sélection exclusive de documents sous licences ouvertes (CC0, CC-BY, US Public Domain) ou documents synthétiques créés spécifiquement.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>6. Insuffisance de mémoire VRAM GPU (< 24 Go)</strong></td>
      <td>Infrastructure / Tech</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">3</td>
      <td>Quantification 4-bit (AWQ/GPTQ) du VLM Qwen2.5-VL ; limitation stricte de la résolution des images téléversées à 1024x1024 max.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>7. Injection de prompt indirecte dans un PDF</strong></td>
      <td>Sécurité / IA</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">3</td>
      <td>Traitement des documents comme données passives étanches (prompt shield) ; isolation des instructions système ; jeux de tests dédiés (C19/F19).</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>8. Échec d'extraction OCR sur documents scannés</strong></td>
      <td>Technique / Ingestion</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">2</td>
      <td>Prétraitement d'image (débruitage, binarisation adaptative Otsu) avant passage dans PaddleOCR/Tesseract ; validation de la couche de confiance.</td>
      <td>Farah OTARID</td>
    </tr>
    <tr>
      <td><strong>9. Contradiction non détectée entre versions</strong></td>
      <td>Méthodes / Qualité</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">2</td>
      <td>Priorisation temporelle des métadonnées (la version la plus récente prévaut) et émission d'un avertissement explicite si conflit détecté.</td>
      <td>Farah OTARID</td>
    </tr>
  </tbody>
</table>

<h2>5.2 Analyse Approfondie des Scénarios Critiques</h2>
<p>Parmi ces risques, trois appellent des protocoles de parade renforcés :</p>
<ul>
  <li><strong>Scénario d'Injection de Prompt (Risque 7) :</strong> Le document piégé C19 contient l'instruction textuelle ordonnant de supprimer les filtres de sécurité. Si le VLM interprétait ce texte comme une directive système, il violerait l'étanchéité des groupes. La parade repose sur une séparation stricte des canaux de prompting : le contexte documentaire est délimité par des balises XML fermées <code>&lt;context_data&gt;</code> avec instruction méta préalable ordonnant au modèle de ne traiter aucun ordre textuel situé à l'intérieur de ces balises comme une commande exécutable.</li>
  <li><strong>Scénario de Débordement Mémoire GPU (Risque 6) :</strong> Lors de l'analyse conjointe d'un long historique et d'une photo en très haute résolution, l'allocation mémoire peut saturer. La politique d'atténuation applique un redimensionnement dynamique automatique (downsampling) de l'image dès son entrée dans l'API FastAPI et plafonne le budget de contexte documentaire à 4 096 tokens.</li>
  <li><strong>Scénario de Doublon de Ticket GMAO (Risque 3) :</strong> Si le réseau subit une micro-coupure lors de la validation, l'opérateur peut cliquer une seconde fois sur le bouton d'envoi. La clé d'idempotence calculée sur l'empreinte de la demande garantit que le serveur MCP rejettera la seconde requête comme une transaction déjà validée, préservant l'intégrité de la GMAO.</li>
</ul>

<div class="page-break"></div>

<!-- PARTIE 6 : PLANNING ET ORGANISATION -->
<h1>6. Planning et Organisation de l'Équipe</h1>

<h2>6.1 Organisation, Rôles et Gouvernance</h2>
<p>Le projet est conduit selon une méthodologie itérative rigoureuse jalonnée par les 6 semaines du module. La structure de gouvernance est organisée comme suit :</p>

<table>
  <thead>
    <tr>
      <th>Membre / Rôle Déclaré</th>
      <th>Domaines de Responsabilité Principaux</th>
      <th>Livrables &amp; Tâches Associées</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Farah OTARID</strong><br/><em>(Architecte IA &amp; Lead RAG)</em></td>
      <td>
        • Cadrage technique global et architecture cible.<br/>
        • Constitution, vérification et packaging du corpus de 40 documents.<br/>
        • Conception des pipelines d'ingestion PyMuPDF et OCR local.<br/>
        • Mise en place de la recherche hybride Qdrant et reranking BGE.<br/>
        • Intégration du modèle vision-langage Qwen2.5-VL-7B.
      </td>
      <td>
        • Rédaction du Livrable 1 (Rapport, Inventaire, Diagrammes).<br/>
        • Implémentation du pipeline RAG multimodal en Semaine 2.<br/>
        • Fine-tuning du reranker et évaluations nDCG/MRR en Semaine 5.<br/>
        • Conteneurisation Docker Compose finale en Semaine 6.
      </td>
    </tr>
    <tr>
      <td><strong>[A_COMPLETER si binôme]</strong><br/><em>(Ingénieur Logiciel &amp; MCP)</em></td>
      <td>
        • Développement de la passerelle API FastAPI et sécurité JWT.<br/>
        • Implémentation du serveur MCP et des outils de maintenance.<br/>
        • Développement de l'interface graphique Streamlit interactive.<br/>
        • Gestion du workflow agentique LangGraph et des checkpoints Human-in-the-Loop.<br/>
        • Automatisation des tests d'évaluation et de sécurité.
      </td>
      <td>
        • Configuration du serveur MCP et base de démo en Semaine 4.<br/>
        • Implémentation du flux de ticket et validation en Semaine 4.<br/>
        • Batterie de tests d'injection de prompt en Semaine 5.<br/>
        • Préparation du scénario de soutenance et démonstration finale.
      </td>
    </tr>
  </tbody>
</table>

<h2>6.2 Planning Prévisionnel Détaillé des Semaines 2 à 6</h2>
<table>
  <thead>
    <tr>
      <th style="width: 15%;">Période</th>
      <th style="width: 35%;">Objectifs Techniques &amp; Développements</th>
      <th style="width: 32%;">Livrables Intermédiaires &amp; Jalons</th>
      <th style="width: 18%;">Critères de Validation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Semaine 1<br/>(Échue)</strong></td>
      <td>• Analyse des cahiers des charges et consignes officielles.<br/>• Constitution intégrale du corpus documentaire (40 documents).<br/>• Définition de l'architecture cible et des flux.<br/>• Élaboration de la matrice des risques.</td>
      <td><strong>LIVRABLE 1 :</strong><br/>• Archive L1_MaintiDoc_OTARID.zip.<br/>• Rapport PDF académique.<br/>• inventaire.csv validé.<br/>• prompts_corpus.md tracé.<br/>• Dépôt Git initialisé.</td>
      <td>Validation formelle de l'inventaire 40/40 et conformité des 6 parties du rapport.</td>
    </tr>
    <tr>
      <td><strong>Semaine 2</strong></td>
      <td>• Implémentation du pipeline d'ingestion PyMuPDF + PaddleOCR.<br/>• Découpage sémantique en passages et extraction des figures.<br/>• Vectorisation BGE-M3 (texte) et CLIP (visuel).<br/>• Indexation dans Qdrant avec filtrage RBAC par payload.</td>
      <td>• Scripts d'ingestion automatisée.<br/>• Collections Qdrant peuplées.<br/>• Tests unitaires de filtrage de groupe (isolation étanche confirmée).</td>
      <td>Temps d'ingestion complet &lt; 15 min ; 0 fuite documentaire lors des tests de requêtes RBAC.</td>
    </tr>
    <tr>
      <td><strong>Semaine 3</strong></td>
      <td>• Déploiement local du VLM Qwen2.5-VL-7B (vLLM / AWQ).<br/>• Conception des prompts structurés (Pydantic schema).<br/>• Implémentation du module de vérification des citations.<br/>• Intégration de la recherche multimodale hybride (fusion RRF).</td>
      <td>• Module de génération opérationnel.<br/>• Schémas de sortie validés.<br/>• Banc d'essai sur questions avec photo de panneau.</td>
      <td>100% des citations renvoyées correspondent à des pages existantes.</td>
    </tr>
    <tr>
      <td><strong>Semaine 4</strong></td>
      <td>• Implémentation du serveur MCP (protocole Model Context Protocol).<br/>• Orchestration de l'état avec LangGraph.<br/>• Implémentation de l'interruption Human-in-the-Loop.<br/>• Interface Streamlit avec formulaire et affichage des sources.</td>
      <td>• Serveur MCP fonctionnel.<br/>• Interface Streamlit connectée.<br/>• Workflow complet de préparation et validation de ticket.</td>
      <td>Zéro création de ticket sans clic de confirmation explicite ; clé d'idempotence active.</td>
    </tr>
    <tr>
      <td><strong>Semaine 5</strong></td>
      <td>• Fine-tuning du reranker BGE Cross-Encoder sur jeu de données ciblé (800 à 1 500 paires).<br/>• Campagne d'évaluation sur 150 scénarios de test.<br/>• Exécution des tests de résistance aux injections de prompt (C19/F19).<br/>• Comparaisons métriques avant/après adaptation (nDCG@5, MRR@10).</td>
      <td>• Modèle reranker adapté.<br/>• Rapport d'évaluation chiffré.<br/>• Résultats des tests de sécurité et d'ambiguïté.</td>
      <td>Amélioration mesurable du nDCG@5 ; neutralisation confirmée des injections de prompt.</td>
    </tr>
    <tr>
      <td><strong>Semaine 6</strong></td>
      <td>• Optimisation globale de la latence (target p95 &lt; 30s).<br/>• Finalisation du docker-compose multi-services.<br/>• Rédaction de la fiche de limites et de la documentation d'exploitation.<br/>• Préparation de la démonstration live pour la soutenance finale.</td>
      <td><strong>LIVRABLE FINAL &amp; SOUTENANCE :</strong><br/>• Prototype complet opérationnel.<br/>• Dépôt GitHub documenté.<br/>• Démonstration des 6 scénarios obligatoires devant l'enseignante.</td>
      <td>Démonstration fluide du scénario nominal, ambiguïté, accès interdit, MCP et ticket approuvé.</td>
    </tr>
  </tbody>
</table>

<div class="callout callout-warning">
  <strong>MÉTHODOLOGIE D'ÉVALUATION ET DE TEST (SEMAINE 5) :</strong><br/>
  Conformément aux exigences du cahier des charges général, le jeu de test final comprendra 150 scénarios couvrant les questions purement textuelles (40), les questions appuyées par une image ou un schéma (30), les consultations d'historique MCP (20), les cas de sources contradictoires ou absentes (20), les vérifications de contrôle d'accès RBAC (20) et les tentatives d'injection de prompt (20).
</div>

</body>
</html>"""

print("Rendering academic PDF report with Playwright...")
temp_report_html = target_pdf.replace(".pdf", "_temp.html")
with open(temp_report_html, "w", encoding="utf-8") as f:
    f.write(html_report)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{temp_report_html}")
    page.pdf(
        path=target_pdf,
        format="A4",
        print_background=True,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    browser.close()

os.remove(temp_report_html)

doc = pdfium.PdfDocument(target_pdf)
print(f"Academic Report generated: {target_pdf}")
print(f"Total Page Count: {len(doc)} pages (Requirement: 10 to 15 pages)")
doc.close()
