from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import cm

ROOT=Path(__file__).parents[1]
OUT=ROOT/'rapport'; OUT.mkdir(exist_ok=True)
st=getSampleStyleSheet(); st.add(ParagraphStyle(name='Cover',parent=st['Title'],alignment=TA_CENTER,fontSize=21,leading=27,spaceAfter=24)); st.add(ParagraphStyle(name='H',parent=st['Heading1'],textColor=colors.HexColor('#1f4e79'),spaceBefore=10,spaceAfter=7))
def P(t,s='BodyText'): return Paragraph(t,st[s])
def footer(c,d): c.saveState(); c.setFont('Helvetica',8); c.drawString(2*cm,1*cm,'MAINTiDOC - L2 - OTARID'); c.drawRightString(19*cm,1*cm,str(d.page)); c.restoreState()
def common(title, body, out):
    d=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=2*cm,leftMargin=2*cm,topMargin=1.8*cm,bottomMargin=1.7*cm)
    story=[P(title,'Cover'),P('MAINTiDOC - equipe OTARID','Cover')]
    for heading,text in body:
        story += [P(heading,'H'),P(text),Spacer(1,.25*cm)]
        if 'Rapport' in out.name: story.append(PageBreak())
        elif heading.startswith(('2.','4.','6.')): story.append(PageBreak())
    d.build(story,onFirstPage=footer,onLaterPages=footer); return out
def report():
    body=[
('1. Contexte et périmètre','Le livrable 2 transforme le corpus du livrable 1 en une chaîne de recherche multimodale. Le périmètre couvre ingestion, métadonnées, indexation, recherche texte, recherche image, fusion, contrôle d’accès et évaluation. La génération par VLM est explicitement reportée à la semaine 3 et n’est pas implémentée.'),
('2. Architecture et écarts au L1','Le corpus original reste inchangé dans L1_MaintiDoc_OTARID_Corpus. Le nouveau dossier sépare ingestion, indexation, recherche et évaluation. Qdrant est prévu par Docker Compose avec deux collections. Dans l’environnement de réalisation, Docker et qdrant-client ne sont pas disponibles; un index local de repli est produit et son statut reste non conforme à la validation Qdrant finale.'),
('3. Ingestion documentaire','L’inventaire L1 fournit les métadonnées. Chaque élément conserve document_id, version, page, element_id, type, équipement, famille, groupes d’accès, chemin source et SHA-256. Le découpage vise 450 mots avec 50 mots de recouvrement. L’exécution locale a produit 612 éléments sur 40 documents. C17 et F17 sont détectés comme PDF scannés sans couche texte; leur OCR comparatif reste à exécuter.'),
('4. Benchmarking','Le cahier des charges impose deux moteurs OCR et deux encodeurs texte-image. Les scripts et le CSV existent, mais Tesseract, PaddleOCR, transformers et sentence-transformers ne sont pas disponibles localement et le réseau Python est bloqué. Les cellules sont donc marquées unavailable; aucun score fictif n’est présenté.'),
('5. Indexation et recherche','Le code prépare les vecteurs, payloads et filtres Qdrant. Faute de modèles, le smoke test utilise un vecteur de hachage déterministe explicitement marqué fallback-hash. Les résultats gardent document, page, élément, extrait, type et score. La fusion est RRF; reranking et VLM sont absents.'),
('6. Contrôle d’accès','Trois utilisateurs sont configurés : tech_compresseurs, tech_incendie et responsable. Le filtre par intersection des groupes est appliqué avant classement. Les trois scénarios obligatoires sont couverts : accès autorisé, accès interdit et absence de contournement par fusion. Les trois tests directs passent; la validation Qdrant réelle reste à refaire.'),
('7. Évaluation sur 20 questions','Le jeu contient 20 questions, 5 photos et les contradictions C17/C18 et F17/F18. Deux configurations ont été exécutées sur le moteur local : texte seul : Recall@5 0,7500 et MRR@10 0,6333; texte-images : Recall@5 0,8000 et MRR@10 0,5083. Ces valeurs décrivent le fallback lexical, pas BGE-M3/CLIP.'),
('8. Limites et perspectives','Les limites vérifiées sont l’absence de Qdrant démarré, de modèles, d’OCR comparatif et de captures Streamlit. La prochaine action est d’installer les dépendances dans un environnement réseau autorisé, démarrer Compose, relancer ingestion et benchmarks, puis régénérer résultats et captures. La matrice distingue ces éléments sans les déclarer terminés.'),
('9. Reproductibilité et répartition','Les commandes sont dans README.md, les scripts locaux sont déterministes et aucun secret n’est inclus. L’équipe OTARID et Farah OTARID sont reprises du L1; aucun binôme n’est inventé. Le tag v0.2-L2 et le push GitHub nécessitent encore une action de dépôt et ne sont pas revendiqués.'),
]
    return common('Livrable 2 - RAG multimodal : ingestion, recherche et contrôle d’accès',body,OUT/'L2_MaintiDoc_OTARID_OTARID_Rapport.pdf')
def veille():
    body=[('1. Méthode','Veille réalisée le 27 novembre 2026 à partir de cinq sources ouvertes et vérifiées : documentations Qdrant et PyMuPDF, article BGE-M3 et article CLIP. Les questions portent sur qualité des données, recherche multimodale et absence de fuite RBAC.'),('2. Découpage et extraction','PyMuPDF permet d’extraire texte et images. Un découpage par unités techniques, avec page et identifiant, rend les citations vérifiables. MAINTiDOC retient 450 mots avec 50 mots de recouvrement; tableaux et figures sont isolés.'),('3. Embeddings et recherche multimodale','BGE-M3 est retenu pour le texte multilingue. Un encodeur compatible CLIP relie requêtes françaises et figures. Les espaces sont séparés puis fusionnés par RRF. La discrimination de voyants proches doit être mesurée sur le même jeu.'),('4. Métadonnées et contrôle d’accès','Les payloads Qdrant conservent document, page, élément et groupes autorisés. Le filtre est appliqué avant chaque recherche et avant la fusion. C’est la décision de sécurité centrale du L2.'),('5. Évaluation et traçabilité','Le jeu de 20 questions conserve attendus et résultats réels. Recall@5 et MRR@10 sont produits par script. Les valeurs fallback restent identifiées comme telles et ne remplacent pas les mesures BGE-M3/CLIP.'),('6. Synthèse','Appliquées : découpage structuré, payload riche, filtrage pré-recherche, scripts d’évaluation. À mesurer : comparaison OCR et encodeurs image. Reportée : génération VLM en semaine 3.'),('7. Sources','S1 Qdrant Filtering - https://qdrant.tech/documentation/search/filtering/<br/>S2 Qdrant Payload - https://qdrant.tech/documentation/manage-data/payload/<br/>S3 BGE-M3 - https://arxiv.org/abs/2402.03216<br/>S4 CLIP - https://proceedings.mlr.press/v139/radford21a.html<br/>S5 PyMuPDF - https://pymupdf.readthedocs.io/en/latest/recipes-text.html')]
    return common('Veille sur les bonnes pratiques RAG multimodal',body,OUT/'L2_MaintiDoc_OTARID_OTARID_Veille.pdf')
if __name__=='__main__': print(report()); print(veille())
