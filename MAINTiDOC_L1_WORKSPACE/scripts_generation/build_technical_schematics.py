import os
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath("MAINTiDOC_L1_WORKSPACE/maintidoc/docs/diagrammes")
os.makedirs(output_dir, exist_ok=True)

# 1. Schéma Électrique de Commande Compresseur (Star-Delta Starter & Interlocks)
svg_elec = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial; font-size: 18px; font-weight: bold; fill: #0d47a1; }
      .subtitle { font-family: 'Segoe UI', Arial; font-size: 12px; fill: #546e7a; }
      .label { font-family: 'Segoe UI', Arial; font-size: 11px; fill: #263238; }
      .wire { stroke: #263238; stroke-width: 2; fill: none; }
      .wire-neutral { stroke: #0288d1; stroke-width: 2; fill: none; }
      .wire-safety { stroke: #d32f2f; stroke-width: 2; fill: none; }
      .component { fill: #ffffff; stroke: #1565c0; stroke-width: 1.5; }
      .relay { fill: #e3f2fd; stroke: #0d47a1; stroke-width: 1.5; }
      .terminal { fill: #263238; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="1000" height="650" fill="#ffffff" stroke="#cfd8dc" stroke-width="2"/>
  <rect x="15" y="15" width="970" height="620" fill="none" stroke="#90a4ae" stroke-width="1" stroke-dasharray="4"/>

  <!-- Header block -->
  <rect x="30" y="30" width="940" height="60" fill="#f5f7fa" stroke="#b0bec5" stroke-width="1"/>
  <text x="50" y="55" class="title">SCHÉMA ÉLECTRIQUE DE COMMANDE — COMPRESSEUR INDUSTRIEL (REF: C09 / ELEC-COMP-VSD)</text>
  <text x="50" y="75" class="subtitle">Circuit 230V AC Commande / Démarrage Étoile-Triangle &amp; Chaîne de Sécurité Intrinsèque (Arrêt d'Urgence, Pressostat, Klixon)</text>

  <!-- Rails 230V & Neutre -->
  <line x1="80" y1="130" x2="920" y2="130" stroke="#d32f2f" stroke-width="3"/>
  <text x="890" y="120" font-family="Segoe UI" font-size="12" font-weight="bold" fill="#d32f2f">L1 (230V AC)</text>

  <line x1="80" y1="560" x2="920" y2="560" stroke="#0288d1" stroke-width="3"/>
  <text x="890" y="580" font-family="Segoe UI" font-size="12" font-weight="bold" fill="#0288d1">N (Neutre)</text>

  <!-- Ligne 1: Chaîne de sécurité -->
  <!-- Sectionneur Q1 -->
  <line x1="120" y1="130" x2="120" y2="160" class="wire"/>
  <rect x="105" y="160" width="30" height="30" class="component"/>
  <text x="110" y="180" class="label">Q1</text>
  <text x="145" y="180" class="label">Disjoncteur Q1 (4A)</text>
  <line x1="120" y1="190" x2="120" y2="220" class="wire"/>

  <!-- Arrêt d'urgence AU1 -->
  <circle cx="120" cy="235" r="14" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="113" y="240" font-family="Segoe UI" font-size="12" font-weight="bold" fill="#d32f2f">AU</text>
  <text x="145" y="240" class="label">Arrêt d'Urgence (NF, coupure coup de poing)</text>
  <line x1="120" y1="250" x2="120" y2="280" class="wire-safety"/>

  <!-- Sécurité Thermique F2 -->
  <rect x="105" y="280" width="30" height="30" class="component"/>
  <text x="110" y="300" class="label">F2</text>
  <text x="145" y="300" class="label">Relais Thermique Moteur F2 (Contact NF 95-96)</text>
  <line x1="120" y1="310" x2="120" y2="340" class="wire"/>

  <!-- Sécurité Pression Max Pressostat PS_MAX -->
  <rect x="105" y="340" width="30" height="30" class="component"/>
  <text x="108" y="360" class="label">PS1</text>
  <text x="145" y="360" class="label">Pressostat Sécurité Pression Haute (NF P &lt; 13 bar)</text>
  <line x1="120" y1="370" x2="120" y2="400" class="wire"/>

  <!-- Sonde Température Klixon TS1 -->
  <rect x="105" y="400" width="30" height="30" class="component"/>
  <text x="108" y="420" class="label">TS1</text>
  <text x="145" y="420" class="label">Thermostat Huile Éléments (NF T &lt; 110°C)</text>
  <line x1="120" y1="430" x2="120" y2="480" class="wire"/>

  <!-- Bobine Relais Sécurité KA1 -->
  <rect x="100" y="480" width="40" height="40" class="relay"/>
  <text x="107" y="505" font-weight="bold" class="label">KA1</text>
  <text x="145" y="505" class="label">Relais Maître de Sécurité Sécurité OK</text>
  <line x1="120" y1="520" x2="120" y2="560" class="wire-neutral"/>

  <!-- Ligne 2: Boutons Marche / Arrêt & Maintien -->
  <line x1="420" y1="130" x2="420" y2="180" class="wire"/>
  <!-- Contact KA1 -->
  <line x1="410" y1="180" x2="430" y2="180" class="wire"/>
  <line x1="410" y1="195" x2="430" y2="195" class="wire"/>
  <line x1="420" y1="180" x2="420" y2="195" class="wire"/>
  <text x="440" y="190" class="label">Contact KA1 (Sécurité OK)</text>
  <line x1="420" y1="195" x2="420" y2="230" class="wire"/>

  <!-- Bouton Arrêt S0 (NF) -->
  <circle cx="420" cy="245" r="10" fill="#fff" stroke="#d32f2f" stroke-width="1.5"/>
  <text x="440" y="250" class="label">Bouton Arrêt S0 (NF)</text>
  <line x1="420" y1="255" x2="420" y2="290" class="wire"/>

  <!-- Bouton Marche S1 (NO) en // avec KM1 maintien -->
  <line x1="420" y1="290" x2="380" y2="290" class="wire"/>
  <line x1="420" y1="290" x2="460" y2="290" class="wire"/>
  <line x1="380" y1="290" x2="380" y2="310" class="wire"/>
  <circle cx="380" cy="320" r="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="345" y="345" class="label">S1 (Marche)</text>
  <line x1="380" y1="330" x2="380" y2="350" class="wire"/>

  <line x1="460" y1="290" x2="460" y2="310" class="wire"/>
  <rect x="448" y="310" width="24" height="20" class="component"/>
  <text x="449" y="325" font-size="10" class="label">KM1</text>
  <text x="480" y="325" class="label">Auto-maintien KM1</text>
  <line x1="460" y1="330" x2="460" y2="350" class="wire"/>

  <line x1="380" y1="350" x2="460" y2="350" class="wire"/>
  <line x1="420" y1="350" x2="420" y2="400" class="wire"/>

  <!-- Contact Pressostat Régulation Reg_P -->
  <rect x="405" y="400" width="30" height="25" class="component"/>
  <text x="410" y="418" class="label">P_REG</text>
  <text x="445" y="418" class="label">Pressostat Régulation En Charge / À Vide (7-10 bar)</text>
  <line x1="420" y1="425" x2="420" y2="480" class="wire"/>

  <!-- Bobine Contacteur Ligne KM1 -->
  <rect x="400" y="480" width="40" height="40" class="relay"/>
  <text x="407" y="505" font-weight="bold" class="label">KM1</text>
  <text x="445" y="505" class="label">Contacteur Principal de Ligne KM1</text>
  <line x1="420" y1="520" x2="420" y2="560" class="wire-neutral"/>

  <!-- Ligne 3: Temporisateur et Contacteur Étoile KM2 / Triangle KM3 -->
  <line x1="720" y1="130" x2="720" y2="350" class="wire"/>
  <line x1="420" y1="350" x2="720" y2="350" class="wire"/>
  
  <!-- Relais Temporisé KT1 (0-10s) -->
  <line x1="660" y1="350" x2="660" y2="480" class="wire"/>
  <rect x="640" y="480" width="40" height="40" class="relay"/>
  <text x="647" y="505" font-weight="bold" class="label">KT1</text>
  <text x="615" y="535" class="label">Temporisateur (6s)</text>
  <line x1="660" y1="520" x2="660" y2="560" class="wire-neutral"/>

  <!-- Contacteur Étoile KM2 (Démarrage) -->
  <line x1="760" y1="350" x2="760" y2="390" class="wire"/>
  <rect x="748" y="390" width="24" height="20" class="component"/>
  <text x="750" y="405" font-size="9" class="label">KT1_NF</text>
  <line x1="760" y1="410" x2="760" y2="430" class="wire"/>
  <rect x="748" y="430" width="24" height="20" class="component"/>
  <text x="750" y="445" font-size="9" class="label">KM3_NF</text>
  <text x="780" y="445" class="label">Verrouillage élec.</text>
  <line x1="760" y1="450" x2="760" y2="480" class="wire"/>
  <rect x="740" y="480" width="40" height="40" class="relay"/>
  <text x="747" y="505" font-weight="bold" class="label">KM2</text>
  <text x="735" y="535" class="label">Contacteur Étoile</text>
  <line x1="760" y1="520" x2="760" y2="560" class="wire-neutral"/>

  <!-- Contacteur Triangle KM3 (Régime nominal) -->
  <line x1="860" y1="350" x2="860" y2="390" class="wire"/>
  <rect x="848" y="390" width="24" height="20" class="component"/>
  <text x="850" y="405" font-size="9" class="label">KT1_NO</text>
  <line x1="860" y1="410" x2="860" y2="430" class="wire"/>
  <rect x="848" y="430" width="24" height="20" class="component"/>
  <text x="850" y="445" font-size="9" class="label">KM2_NF</text>
  <text x="880" y="445" class="label">Verrouillage élec.</text>
  <line x1="860" y1="450" x2="860" y2="480" class="wire"/>
  <rect x="840" y="480" width="40" height="40" class="relay"/>
  <text x="847" y="505" font-weight="bold" class="label">KM3</text>
  <text x="830" y="535" class="label">Contacteur Triangle</text>
  <line x1="860" y1="520" x2="860" y2="560" class="wire-neutral"/>

  <!-- Footer metadata -->
  <text x="50" y="615" font-family="Segoe UI" font-size="11" fill="#78909c">Projet MAINTiDOC — Assistant Documentaire Multimodal — Document C09 Schéma Électrique Conforme Norme NF EN 60204-1</text>
</svg>"""

# 2. Schéma Pneumatique Compresseur à Vis
svg_pneu = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial; font-size: 18px; font-weight: bold; fill: #0d47a1; }
      .subtitle { font-family: 'Segoe UI', Arial; font-size: 12px; fill: #546e7a; }
      .label { font-family: 'Segoe UI', Arial; font-size: 11px; fill: #263238; font-weight: bold; }
      .desc { font-family: 'Segoe UI', Arial; font-size: 10px; fill: #455a64; }
      .air-line { stroke: #0288d1; stroke-width: 3; fill: none; }
      .oil-line { stroke: #e65100; stroke-width: 2.5; stroke-dasharray: 6,3; fill: none; }
      .control-line { stroke: #7b1fa2; stroke-width: 1.5; stroke-dasharray: 3,3; fill: none; }
      .tank { fill: #e1f5fe; stroke: #0277bd; stroke-width: 2; }
      .cooler { fill: #f1f8e9; stroke: #33691e; stroke-width: 1.5; }
      .block { fill: #eceff1; stroke: #37474f; stroke-width: 2; }
    </style>
  </defs>

  <rect width="1000" height="650" fill="#ffffff" stroke="#cfd8dc" stroke-width="2"/>
  <rect x="15" y="15" width="970" height="620" fill="none" stroke="#90a4ae" stroke-width="1" stroke-dasharray="4"/>

  <!-- Header -->
  <rect x="30" y="30" width="940" height="60" fill="#f5f7fa" stroke="#b0bec5" stroke-width="1"/>
  <text x="50" y="55" class="title">SCHÉMA DU CIRCUIT PNEUMATIQUE ET D'HUILE — COMPRESSEUR À VIS (REF: C10)</text>
  <text x="50" y="75" class="subtitle">Circuit d'Aspiration, Compression bi-vis lubrifiée, Séparation Air/Huile, Régulation MPV et Réfrigérant final (ISO 1219)</text>

  <!-- Légende en haut à droite -->
  <rect x="700" y="105" width="260" height="65" fill="#fafafa" stroke="#cfd8dc" stroke-width="1"/>
  <line x1="715" y1="120" x2="745" y2="120" class="air-line"/>
  <text x="755" y="123" class="desc">Circuit Air Comprimé</text>
  <line x1="715" y1="138" x2="745" y2="138" class="oil-line"/>
  <text x="755" y="141" class="desc">Circuit Huile d'Injection</text>
  <line x1="715" y1="155" x2="745" y2="155" class="control-line"/>
  <text x="755" y="158" class="desc">Ligne de Commande / Décharge</text>

  <!-- Étape 1: Filtre à air d'aspiration -->
  <rect x="60" y="240" width="70" height="60" rx="5" class="block"/>
  <text x="72" y="265" class="label">FILTRE AIR</text>
  <text x="68" y="285" class="desc">Filtre 3 µm (AF1)</text>
  <line x1="30" y1="270" x2="60" y2="270" class="air-line"/>
  <text x="32" y="260" class="desc">Air ambiant</text>

  <!-- Liaison Filtre vers Vanne d'admission -->
  <line x1="130" y1="270" x2="180" y2="270" class="air-line"/>

  <!-- Vanne d'admission / Régulateur (Unloader Valve) -->
  <polygon points="180,250 220,270 180,290" fill="#b0bec5" stroke="#37474f" stroke-width="1.5"/>
  <polygon points="220,250 180,270 220,290" fill="#b0bec5" stroke="#37474f" stroke-width="1.5"/>
  <text x="175" y="240" class="label">VANNE ASPIRATION</text>
  <text x="170" y="310" class="desc">Régulation Tout/Rien (UV1)</text>

  <!-- Ligne vers Élément Compresseur -->
  <line x1="220" y1="270" x2="280" y2="270" class="air-line"/>

  <!-- Élément Compresseur à Vis (Airend) -->
  <rect x="280" y="220" width="110" height="100" rx="8" fill="#cfd8dc" stroke="#263238" stroke-width="2.5"/>
  <circle cx="320" cy="270" r="22" fill="#eceff1" stroke="#37474f" stroke-width="1.5"/>
  <circle cx="355" cy="270" r="16" fill="#eceff1" stroke="#37474f" stroke-width="1.5"/>
  <text x="295" y="245" class="label">BLOC VIS</text>
  <text x="295" y="305" class="desc">Vis Mâle + Femelle</text>

  <!-- Refoulement Mélange Air + Huile -->
  <line x1="390" y1="270" x2="480" y2="270" stroke="#8d6e63" stroke-width="4"/>
  <text x="400" y="260" class="desc" font-weight="bold">Mélange Air/Huile (85°C, 9 bar)</text>

  <!-- Réservoir Séparateur Air / Huile -->
  <rect x="480" y="180" width="120" height="230" rx="20" class="tank"/>
  <text x="495" y="210" class="label">RÉSERVOIR</text>
  <text x="495" y="225" class="label">SÉPARATEUR</text>
  <text x="495" y="240" class="desc">(Cuve sous pression)</text>

  <!-- Cartouche séparatrice interne -->
  <rect x="500" y="260" width="80" height="70" stroke="#f57f17" stroke-width="2" fill="#fffde7" stroke-dasharray="4"/>
  <text x="508" y="295" font-size="9" class="label" fill="#f57f17">Cartouche Déshuileuse</text>

  <!-- Sortie Huile en bas de cuve -->
  <line x1="540" y1="410" x2="540" y2="480" class="oil-line"/>
  
  <!-- Thermostat d'Huile / Vanne Thermostatique -->
  <polygon points="530,480 550,480 540,495" fill="#e65100"/>
  <circle cx="540" cy="495" r="15" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5"/>
  <text x="565" y="495" class="label">VANNE THERMOSTATIQUE</text>
  <text x="565" y="510" class="desc">Bypass Réfrigérant si T &lt; 71°C</text>

  <!-- Vers Réfrigérant d'huile -->
  <line x1="540" y1="510" x2="540" y2="550" class="oil-line"/>
  <line x1="540" y1="550" x2="420" y2="550" class="oil-line"/>
  <rect x="330" y="530" width="90" height="40" class="cooler"/>
  <text x="340" y="555" class="label">AÉRORÉFRIGÉRANT</text>
  <line x1="330" y1="550" x2="250" y2="550" class="oil-line"/>

  <!-- Filtre à Huile (OF1) -->
  <circle cx="230" cy="550" r="18" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="218" y="555" class="label">OF1</text>
  <text x="180" y="585" class="desc">Filtre à Huile (10 µm)</text>

  <!-- Retour Huile vers Bloc Vis pour lubrification et étanchéité -->
  <line x1="230" y1="532" x2="230" y2="350" class="oil-line"/>
  <line x1="230" y1="350" x2="330" y2="350" class="oil-line"/>
  <line x1="330" y1="350" x2="330" y2="320" class="oil-line"/>
  <text x="235" y="370" class="desc" fill="#e65100">Injection Huile Lubrifiée</text>

  <!-- Sortie Air Propre Déshuilé (Haut de cuve) -->
  <line x1="540" y1="180" x2="540" y2="140" class="air-line"/>
  
  <!-- Soupape de Pression Minimale (MPV) -->
  <polygon points="530,140 550,140 540,125" fill="#0288d1"/>
  <circle cx="540" cy="120" r="14" fill="#e1f5fe" stroke="#0288d1" stroke-width="1.5"/>
  <text x="560" y="125" class="label">SOUPAPE PRESSION MINIMALE (MPV)</text>
  <text x="560" y="140" class="desc">Maintient P &gt; 4.5 bar pour lubrification &amp; Clapet Anti-retour</text>

  <!-- Liaison vers Réfrigérant Final d'Air -->
  <line x1="554" y1="120" x2="720" y2="120" class="air-line"/>
  <line x1="720" y1="120" x2="720" y2="240" class="air-line"/>

  <!-- Réfrigérant Final (Aftercooler) -->
  <rect x="670" y="240" width="100" height="60" class="cooler"/>
  <text x="682" y="265" class="label">AFTERCOOLER</text>
  <text x="680" y="285" class="desc">Refroidisseur Air</text>

  <!-- Sortie Air vers Séparateur de Condensats -->
  <line x1="770" y1="270" x2="840" y2="270" class="air-line"/>
  
  <!-- Séparateur Condensat & Purgeur -->
  <rect x="840" y="245" width="50" height="50" rx="5" fill="#e0f7fa" stroke="#00838f" stroke-width="1.5"/>
  <text x="845" y="268" class="label">PURGE</text>
  <text x="845" y="285" class="desc">Auto</text>

  <!-- Sortie Réseau Utilisateur -->
  <line x1="890" y1="270" x2="950" y2="270" class="air-line"/>
  <polygon points="950,265 965,270 950,275" fill="#0288d1"/>
  <text x="895" y="260" class="label" fill="#0288d1">SORTIE AIR RÉSEAU</text>
  <text x="895" y="295" class="desc">Vers Sécheur / Cuve Usine</text>

  <!-- Soupape de sécurité sur cuve -->
  <line x1="600" y1="230" x2="630" y2="230" stroke="#d32f2f" stroke-width="2"/>
  <circle cx="640" cy="230" r="10" fill="#ffebee" stroke="#d32f2f" stroke-width="1.5"/>
  <text x="655" y="235" class="label" fill="#d32f2f">Soupape Sécurité (14 bar)</text>

  <text x="50" y="615" font-family="Segoe UI" font-size="11" fill="#78909c">Projet MAINTiDOC — Assistant Documentaire Multimodal — Document C10 Schéma Pneumatique ISO 1219</text>
</svg>"""

# 3. Schéma Boucle Détection Incendie Adressable
svg_fire_loop = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial; font-size: 18px; font-weight: bold; fill: #b71c1c; }
      .subtitle { font-family: 'Segoe UI', Arial; font-size: 12px; fill: #546e7a; }
      .label { font-family: 'Segoe UI', Arial; font-size: 11px; fill: #263238; font-weight: bold; }
      .desc { font-family: 'Segoe UI', Arial; font-size: 10px; fill: #455a64; }
      .loop-out { stroke: #d32f2f; stroke-width: 3; fill: none; }
      .loop-in { stroke: #c2185b; stroke-width: 3; stroke-dasharray: 6,3; fill: none; }
      .panel { fill: #fbe9e7; stroke: #b71c1c; stroke-width: 2.5; }
      .device { fill: #ffffff; stroke: #c62828; stroke-width: 1.5; }
      .isolator { fill: #fff8e1; stroke: #f57f17; stroke-width: 2; }
    </style>
  </defs>

  <rect width="1000" height="650" fill="#ffffff" stroke="#cfd8dc" stroke-width="2"/>
  <rect x="15" y="15" width="970" height="620" fill="none" stroke="#90a4ae" stroke-width="1" stroke-dasharray="4"/>

  <!-- Header -->
  <rect x="30" y="30" width="940" height="60" fill="#fff5f5" stroke="#ffcdd2" stroke-width="1"/>
  <text x="50" y="55" class="title">SCHÉMA DE RACCORDEMENT BOUCLE ADRESSABLE — CENTRALE INCENDIE (REF: F09)</text>
  <text x="50" y="75" class="subtitle">Architecture Rebouclée Classe A / Style 7 avec Isolateurs de Court-Circuit Intégrés (Norme NF S 61-970 &amp; EN 54-2)</text>

  <!-- Centrale Incendie ECS/CMSI à gauche -->
  <rect x="50" y="130" width="180" height="420" rx="10" class="panel"/>
  <text x="70" y="165" class="title" font-size="15">CENTRALE ECS</text>
  <text x="70" y="185" class="desc" font-weight="bold">Équipement de Contrôle<br/>et de Signalisation</text>
  
  <!-- Borniers Départ / Retour Boucle -->
  <rect x="160" y="220" width="60" height="40" fill="#ffffff" stroke="#b71c1c" stroke-width="1.5"/>
  <text x="165" y="240" font-size="10" font-weight="bold" fill="#b71c1c">DÉPART</text>
  <text x="165" y="253" font-size="9" class="desc">L1+ / L1-</text>

  <rect x="160" y="440" width="60" height="40" fill="#ffffff" stroke="#b71c1c" stroke-width="1.5"/>
  <text x="165" y="460" font-size="10" font-weight="bold" fill="#b71c1c">RETOUR</text>
  <text x="165" y="473" font-size="9" class="desc">L1+ / L1-</text>

  <text x="70" y="320" class="label">Alimentation 24V CC</text>
  <text x="70" y="340" class="desc">Batteries de secours</text>
  <text x="70" y="360" class="desc">Autonomie 72h + 30m</text>

  <!-- Ligne Départ Boucle -->
  <line x1="220" y1="240" x2="300" y2="240" class="loop-out"/>
  
  <!-- Isolateur 1 (ISO-01) -->
  <rect x="300" y="220" width="45" height="40" rx="4" class="isolator"/>
  <text x="306" y="245" font-size="10" font-weight="bold" fill="#f57f17">ISO 1</text>
  <line x1="345" y1="240" x2="400" y2="240" class="loop-out"/>

  <!-- Périphérique 1: Détecteur Optique de Fumée (D01) -->
  <circle cx="430" cy="240" r="25" class="device"/>
  <text x="415" y="242" class="label">DA-01</text>
  <text x="412" y="255" font-size="8" class="desc">Optique</text>
  <text x="400" y="200" class="desc">Zone 1 : Hall Accueil</text>
  <line x1="455" y1="240" x2="520" y2="240" class="loop-out"/>

  <!-- Périphérique 2: Détecteur Thermovélocimétrique (D02) -->
  <circle cx="550" cy="240" r="25" class="device"/>
  <text x="535" y="242" class="label">DT-02</text>
  <text x="535" y="255" font-size="8" class="desc">Thermique</text>
  <text x="520" y="200" class="desc">Zone 2 : Chaufferie</text>
  <line x1="575" y1="240" x2="640" y2="240" class="loop-out"/>

  <!-- Périphérique 3: Déclencheur Manuel DM-01 -->
  <rect x="640" y="218" width="44" height="44" rx="4" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="646" y="242" font-size="10" font-weight="bold" fill="#b71c1c">DM 1</text>
  <text x="646" y="255" font-size="8" class="desc">Manuel</text>
  <text x="630" y="200" class="desc">Issue de Secours</text>
  <line x1="684" y1="240" x2="760" y2="240" class="loop-out"/>

  <!-- Isolateur 2 (ISO-02) -->
  <rect x="760" y="220" width="45" height="40" rx="4" class="isolator"/>
  <text x="766" y="245" font-size="10" font-weight="bold" fill="#f57f17">ISO 2</text>
  <line x1="805" y1="240" x2="880" y2="240" class="loop-out"/>

  <!-- Courbe de retour de boucle (Descente vers bas) -->
  <line x1="880" y1="240" x2="880" y2="460" class="loop-in"/>
  <text x="895" y="350" font-size="11" font-weight="bold" fill="#c2185b" transform="rotate(90,895,350)">Câble Résistant au Feu CR1 (2x1.5 mm² blindé)</text>

  <!-- Périphérique 4: Détecteur Optique Fumée (D03) -->
  <line x1="880" y1="460" x2="800" y2="460" class="loop-in"/>
  <circle cx="775" cy="460" r="25" class="device"/>
  <text x="760" y="462" class="label">DA-03</text>
  <text x="758" y="475" font-size="8" class="desc">Optique</text>
  <text x="745" y="505" class="desc">Zone 3 : Bureau R&amp;D</text>

  <!-- Périphérique 5: Module d'Entrée/Sortie (Asservissement DAS Clapets) -->
  <line x1="750" y1="460" x2="680" y2="460" class="loop-in"/>
  <rect x="635" y="438" width="45" height="44" rx="4" fill="#e8eaf6" stroke="#283593" stroke-width="1.5"/>
  <text x="640" y="462" font-size="10" font-weight="bold" fill="#283593">M-ES</text>
  <text x="638" y="475" font-size="8" class="desc">Relais</text>
  <text x="615" y="505" class="desc">Asservissement DAS</text>

  <!-- Périphérique 6: Diffuseur Sonore Adressable (DS-01) -->
  <line x1="635" y1="460" x2="560" y2="460" class="loop-in"/>
  <polygon points="535,440 560,460 535,480" fill="#fff9c4" stroke="#fbc02d" stroke-width="1.5"/>
  <rect x="515" y="445" width="20" height="30" fill="#fff9c4" stroke="#fbc02d" stroke-width="1.5"/>
  <text x="510" y="505" class="desc">Sirène 90 dB (DS-01)</text>

  <!-- Isolateur 3 (ISO-03) -->
  <line x1="515" y1="460" x2="440" y2="460" class="loop-in"/>
  <rect x="395" y="440" width="45" height="40" rx="4" class="isolator"/>
  <text x="401" y="465" font-size="10" font-weight="bold" fill="#f57f17">ISO 3</text>

  <!-- Retour final à la centrale -->
  <line x1="395" y1="460" x2="220" y2="460" class="loop-in"/>

  <!-- Explication de la tolérance aux pannes Style 7 -->
  <rect x="260" y="300" width="400" height="85" fill="#f9fbe7" stroke="#c0ca33" stroke-width="1"/>
  <text x="275" y="320" font-weight="bold" font-size="11" fill="#827717">Avantage de la boucle rebouclée fermée (Classe A / Style 7) :</text>
  <text x="275" y="340" font-size="10" fill="#33691e">• En cas de coupure unique : la centrale alimente les deux côtés (départ et retour).</text>
  <text x="275" y="355" font-size="10" fill="#33691e">• En cas de court-circuit : les isolateurs encadrants s'ouvrent immédiatement,</text>
  <text x="275" y="370" font-size="10" fill="#33691e">  isolant le tronçon défaillant sans perte d'aucun autre point du bâtiment.</text>

  <text x="50" y="615" font-family="Segoe UI" font-size="11" fill="#78909c">Projet MAINTiDOC — Assistant Documentaire Multimodal — Document F09 Schéma Boucle Rebouclée NF S 61-970</text>
</svg>"""

# 4. Schéma Câblage Périphériques Incendie
svg_cabling = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial; font-size: 18px; font-weight: bold; fill: #b71c1c; }
      .subtitle { font-family: 'Segoe UI', Arial; font-size: 12px; fill: #546e7a; }
      .label { font-family: 'Segoe UI', Arial; font-size: 11px; fill: #263238; font-weight: bold; }
      .desc { font-family: 'Segoe UI', Arial; font-size: 10px; fill: #455a64; }
      .wire-pwr { stroke: #d32f2f; stroke-width: 2.5; fill: none; }
      .wire-gnd { stroke: #263238; stroke-width: 2.5; fill: none; }
      .wire-sig { stroke: #1976d2; stroke-width: 2; fill: none; }
      .wire-relay { stroke: #388e3c; stroke-width: 2; stroke-dasharray: 4,3; fill: none; }
      .box { fill: #ffffff; stroke: #455a64; stroke-width: 1.5; }
    </style>
  </defs>

  <rect width="1000" height="650" fill="#ffffff" stroke="#cfd8dc" stroke-width="2"/>
  <rect x="15" y="15" width="970" height="620" fill="none" stroke="#90a4ae" stroke-width="1" stroke-dasharray="4"/>

  <!-- Header -->
  <rect x="30" y="30" width="940" height="60" fill="#fff5f5" stroke="#ffcdd2" stroke-width="1"/>
  <text x="50" y="55" class="title">SCHÉMA DE CÂBLAGE DES PÉRIPHÉRIQUES ET ASSERVISSEMENTS — CMSI (REF: F10)</text>
  <text x="50" y="75" class="subtitle">Raccordement Relais d'Alarme, Lignes Diffuseurs Sonores/Flashs Évacuation et Lignes DAS (Clapets Coupe-Feu / Désenfumage)</text>

  <!-- Bloc Central ECS/CMSI -->
  <rect x="60" y="120" width="240" height="460" rx="8" fill="#fbe9e7" stroke="#b71c1c" stroke-width="2"/>
  <text x="80" y="155" class="title" font-size="16">BORNIERS CMSI</text>
  <text x="80" y="175" class="desc" font-weight="bold">Système de Mise en Sécurité Incendie</text>

  <!-- Bornier 1: Sortie Ligne Sirènes (SND1) -->
  <rect x="200" y="210" width="80" height="50" class="box"/>
  <text x="210" y="230" font-size="10" font-weight="bold" fill="#d32f2f">SND 1 (+ / -)</text>
  <text x="210" y="245" font-size="9" class="desc">24V / Ligne surveillée</text>

  <!-- Bornier 2: Sortie Contact Sec Alarme Feu Général (RL1) -->
  <rect x="200" y="290" width="80" height="50" class="box"/>
  <text x="210" y="310" font-size="10" font-weight="bold" fill="#388e3c">RELAIS FEU</text>
  <text x="210" y="325" font-size="9" class="desc">C / NO / NC (2A)</text>

  <!-- Bornier 3: Sortie Contact Sec Dérangement / Défaut (RL2) -->
  <rect x="200" y="370" width="80" height="50" class="box"/>
  <text x="210" y="390" font-size="10" font-weight="bold" fill="#f57f17">RELAIS DÉFAUT</text>
  <text x="210" y="405" font-size="9" class="desc">C / NO / NC (Failsafe)</text>

  <!-- Bornier 4: Ligne Télécommande DAS Clapets Coupe-feu -->
  <rect x="200" y="450" width="80" height="50" class="box"/>
  <text x="210" y="470" font-size="10" font-weight="bold" fill="#1976d2">DAS LIGNE 1</text>
  <text x="210" y="485" font-size="9" class="desc">Émission de courant (24V)</text>

  <!-- Connexions Ligne Sirène -->
  <line x1="280" y1="225" x2="420" y2="225" class="wire-pwr"/>
  <line x1="280" y1="245" x2="420" y2="245" class="wire-gnd"/>

  <!-- Sirène 1 -->
  <rect x="420" y="210" width="70" height="50" rx="4" fill="#fff9c4" stroke="#fbc02d" stroke-width="1.5"/>
  <text x="430" y="235" class="label">SIRÈNE 1</text>
  <text x="430" y="250" font-size="9" class="desc">NFS 32-001</text>

  <line x1="490" y1="225" x2="590" y2="225" class="wire-pwr"/>
  <line x1="490" y1="245" x2="590" y2="245" class="wire-gnd"/>

  <!-- Diffuseur Lumineux Flash 2 -->
  <rect x="590" y="210" width="70" height="50" rx="4" fill="#e1f5fe" stroke="#0288d1" stroke-width="1.5"/>
  <text x="600" y="235" class="label">FLASH 2</text>
  <text x="600" y="250" font-size="9" class="desc">EN 54-23</text>

  <line x1="660" y1="225" x2="760" y2="225" class="wire-pwr"/>
  <line x1="660" y1="245" x2="760" y2="245" class="wire-gnd"/>

  <!-- Résistance de Fin de Ligne (EOL) -->
  <rect x="760" y="220" width="50" height="30" fill="#efebe9" stroke="#5d4037" stroke-width="1.5"/>
  <text x="767" y="240" font-size="9" font-weight="bold">R_EOL</text>
  <line x1="760" y1="225" x2="760" y2="245" stroke="#5d4037" stroke-width="2"/>
  <text x="825" y="238" class="desc">R = 4.7 kΩ (Surveillance boucle ouverte/court-circuit)</text>

  <!-- Connexions Relais Feu -> Transmetteur Téléphonique / GTC -->
  <line x1="280" y1="315" x2="450" y2="315" class="wire-relay"/>
  <rect x="450" y="295" width="160" height="45" rx="5" fill="#f1f8e9" stroke="#33691e" stroke-width="1.5"/>
  <text x="460" y="315" class="label">TRANSMETTEUR D'ALARME</text>
  <text x="460" y="330" font-size="9" class="desc">Renvoi PC Sécurité / Télésurveillance</text>

  <!-- Connexions Relais Défaut -> Supervision Technique GTB -->
  <line x1="280" y1="395" x2="450" y2="395" class="wire-relay"/>
  <rect x="450" y="375" width="160" height="45" rx="5" fill="#fffde7" stroke="#f57f17" stroke-width="1.5"/>
  <text x="460" y="395" class="label">SUPERVISION GTC / GTB</text>
  <text x="460" y="410" font-size="9" class="desc">Report Défaut Technique / Batterie</text>

  <!-- Connexions Ligne DAS Clapets Coupe-Feu -->
  <line x1="280" y1="475" x2="450" y2="475" class="wire-sig"/>
  <rect x="450" y="455" width="130" height="45" rx="5" fill="#ede7f6" stroke="#512da8" stroke-width="1.5"/>
  <text x="460" y="475" class="label">DÉCLENCHEUR DAS</text>
  <text x="460" y="490" font-size="9" class="desc">Ventouse électromagnétique</text>

  <line x1="580" y1="475" x2="650" y2="475" class="wire-sig"/>
  <rect x="650" y="455" width="140" height="45" rx="5" fill="#fce4ec" stroke="#c2185b" stroke-width="1.5"/>
  <text x="660" y="475" class="label">CLAPET COUPE-FEU</text>
  <text x="660" y="490" font-size="9" class="desc">Fermeture étanchéité gaine</text>

  <!-- Contact de position clapet (FDC) -->
  <line x1="790" y1="475" x2="850" y2="475" stroke="#7b1fa2" stroke-width="1.5" stroke-dasharray="3,3"/>
  <rect x="850" y="460" width="70" height="30" class="box"/>
  <text x="855" y="480" font-size="9" class="label">FDC Clapet</text>
  <text x="830" y="515" class="desc">Retour position d'attente / sécurité</text>

  <text x="50" y="615" font-family="Segoe UI" font-size="11" fill="#78909c">Projet MAINTiDOC — Assistant Documentaire Multimodal — Document F10 Schéma Câblage Périphériques NF S 61-932</text>
</svg>"""

schematics = {
    "schema_electrique_compresseur": svg_elec,
    "schema_pneumatique_compresseur": svg_pneu,
    "schema_boucle_incendie": svg_fire_loop,
    "schema_cablage_peripheriques": svg_cabling
}

print("Rendering technical schematics to SVG and PNG...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1100, "height": 750, "device_scale_factor": 2})

    for name, svg_code in schematics.items():
        svg_path = os.path.join(output_dir, f"{name}.svg")
        png_path = os.path.join(output_dir, f"{name}.png")

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)

        temp_html = os.path.join(output_dir, f"temp_{name}.html")
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(f"<!DOCTYPE html><html><body style='margin:0;padding:10px;background:#fff;'>{svg_code}</body></html>")

        page.goto(f"file:///{temp_html}")
        page.wait_for_selector("svg")
        svg_el = page.query_selector("svg")
        svg_el.screenshot(path=png_path)
        print(f"Rendered {svg_path} and {png_path}")

        os.remove(temp_html)

    browser.close()

print("All technical schematics created successfully!")
