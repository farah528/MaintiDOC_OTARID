from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

ROOT = Path(__file__).parents[1]
OUT = ROOT / "L2_MaintiDoc_OTARID_Rapport.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=25, leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#17365D"), spaceAfter=18))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=14, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#365F91"), spaceAfter=10))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading1"], fontSize=17, leading=21, textColor=colors.HexColor("#17365D"), spaceBefore=0, spaceAfter=12))
styles.add(ParagraphStyle(name="Sub", parent=styles["Heading2"], fontSize=11.5, leading=15, textColor=colors.HexColor("#365F91"), spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontSize=9.6, leading=13.2, spaceAfter=8))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontSize=10, leading=14, leftIndent=10, rightIndent=10, borderColor=colors.HexColor("#9CC2E5"), borderWidth=0.7, borderPadding=8, backColor=colors.HexColor("#EAF3F8"), spaceBefore=6, spaceAfter=10))

def P(text, style="Body"):
    return Paragraph(text, styles[style])

def table(data, widths):
    t = Table([[P(str(x), "Small") for x in row] for row in data], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9EADBA")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#D9E2F3")); canvas.line(2*cm, 1.45*cm, 19*cm, 1.45*cm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#5B6573")); canvas.drawString(2*cm, 0.9*cm, "MAINTiDOC | Livrable 2 | Équipe OTARID")
    canvas.drawRightString(19*cm, 0.9*cm, f"Page {doc.page}"); canvas.restoreState()

def page(title, subtitle=None):
    out = [P(title, "Section")]
    if subtitle: out.append(P(subtitle, "Callout"))
    return out

story = []
# Page 1
story += [Spacer(1, 3.2*cm), P("MAINTiDOC", "CoverTitle"), P("Rapport du Livrable 2", "CoverSub"), P("RAG multimodal : ingestion, recherche et contrôle d'accès", "CoverSub"), Spacer(1, 1.1*cm), P("Équipe OTARID", "CoverSub"), P("Module IA générative multimodale - EMSI - 2026-2027", "CoverSub"), Spacer(1, 2*cm), P("Version structurée du travail effectivement réalisé", "CoverSub"), PageBreak()]
# Page 2
story += page("Résumé exécutif")
story += [P("Le livrable 2 avait pour objectif de transformer le corpus du livrable 1 en un premier système de recherche documentaire multimodale. Le travail réalisé couvre l'ingestion, la conservation des métadonnées, la préparation de l'indexation, la recherche textuelle, la recherche visuelle, la fusion des résultats, le contrôle d'accès et l'évaluation sur 20 questions."), P("L'exécution locale a permis d'ingérer 40 documents et de produire 612 éléments traçables. Une évaluation reproductible a été exécutée sur 20 questions, avec comparaison texte seul et texte-images. Trois scénarios de contrôle d'accès ont été testés directement et réussis sur l'index local de repli."), P("Certaines validations restent bloquées par l'environnement : le daemon Docker et qdrant-client ne sont pas disponibles, les modèles BGE-M3/CLIP ne sont pas chargés et les moteurs OCR comparés ne sont pas installés. Ces limites sont signalées dans la matrice de conformité, dans les CSV et dans ce rapport."), table([["Indicateur", "Résultat vérifié"],["Documents traités", "40"],["Éléments produits", "612"],["Questions évaluées", "20"],["Tests RBAC", "3 scénarios réussis"],["Rapport / veille", "9 pages / 4 pages"]],[7*cm,9*cm]), PageBreak()]
# Page 3
story += page("1. Contexte, objectifs et périmètre")
story += [P("MAINTiDOC est un assistant documentaire destiné aux techniciens de maintenance. Le L2 se concentre sur la récupération de preuves documentaires : passages, tableaux, figures et photos. La génération d'une réponse par un modèle vision-langage n'est pas incluse, conformément aux consignes du livrable."), P("Les deux familles du corpus sont conservées : compresseurs industriels (C01-C20) et centrales de détection incendie (F01-F20). Les documents contradictoires C17/C18 et F17/F18, ainsi que les documents de test d'accès et d'injection, sont conservés dans leur emplacement L1."), P("Les objectifs opérationnels sont :"), P("- extraire le texte, les images et les métadonnées ;<br/>- découper les contenus en éléments recherchables ;<br/>- préparer deux index Qdrant, texte et images ;<br/>- filtrer les résultats selon les groupes autorisés avant la recherche ;<br/>- comparer deux configurations sur 20 questions ;<br/>- documenter honnêtement les résultats et les limites."), P("Le L1 n'a pas été modifié. Le nouveau travail est regroupé dans L2_MaintiDoc_OTARID.") ,PageBreak()]
# Page 4
story += page("2. Architecture mise en œuvre")
story += [P("L'architecture suit quatre couches : ingestion, représentation, recherche et évaluation. Les métadonnées de l'inventaire L1 sont propagées dans chaque élément afin de permettre la traçabilité et le contrôle d'accès."), table([["Couche", "Réalisation", "État"],["Ingestion", "PyMuPDF prévu, extraction texte/images, découpage, SHA-256", "612 éléments produits ; PyMuPDF non disponible localement"],["Représentation", "BGE-M3 pour le texte, encodeur CLIP compatible pour les images", "Fallback hash exécuté ; modèles conformes non chargés"],["Stockage", "Qdrant, collections texte/images, payload filtrable", "Prévu dans Docker Compose ; non vérifié faute de daemon"],["Recherche", "Texte, visuel, photo et fusion RRF", "Smoke test local exécuté"],["Interface", "Point d'entrée Streamlit prévu", "Non capturé dans cet environnement"]],[3.5*cm,9*cm,3.5*cm]), P("Le code est organisé dans src/ingestion, src/indexation, src/recherche et src/acces. Les scripts d'exécution sont regroupés dans scripts et les données d'évaluation dans eval et resultats."), PageBreak()]
# Page 5
story += page("3. Chaîne d'ingestion documentaire")
story += [P("L'ingestion lit l'inventaire CSV du L1 et associe chaque fichier à ses propriétés : document_id, version, équipement, famille, type de document, format et groupes d'accès. Pour les PDF, chaque page est convertie en éléments textuels et figures lorsque cela est possible. Pour les photos isolées, un élément photo est créé avec son chemin source."), P("Le découpage retenu vise des passages d'environ 450 mots avec un recouvrement de 50 mots. Les figures et les tableaux sont conservés comme éléments distincts afin de ne pas perdre leur identité lors de la recherche et de permettre leur transmission ultérieure au module de la semaine 3."), table([["Élément de traçabilité", "Conservation"],["Document source", "document_id, fichier, hash_sha256"],["Localisation", "page, element_id"],["Nature", "type_element : texte, figure ou photo"],["Contexte métier", "equipement_id, famille_equipement, version"],["Sécurité", "groupes_acces"],["OCR", "ocr_status explicite si la couche texte est absente"]],[5*cm,11*cm]), P("Résultat mesuré : 40 documents parcourus et 612 éléments écrits dans elements.jsonl. C17 et F17 sont identifiés comme PDF scannés sans couche texte. Leur passage OCR est conservé comme indisponible plutôt que simulé."), PageBreak()]
# Page 6
story += page("4. Benchmarking des outils")
story += [P("Le cahier des charges exige un benchmarking lorsque l'outil n'est pas fixé. L'OCR devait comparer au moins deux solutions et l'encodeur texte-image au moins deux modèles, avec qualité, temps, mémoire et licence."), table([["Composant", "Options prévues", "Résultat dans l'environnement"],["OCR", "Tesseract / PaddleOCR", "Non mesuré : moteurs absents"],["Encodeur texte-image", "Deux modèles compatibles CLIP", "Non mesuré : transformers et poids absents"],["Embeddings texte", "BGE-M3 imposé", "Non chargé ; fallback hash utilisé pour smoke test"],["Qdrant", "Service imposé", "Non vérifié : daemon Docker absent"]],[4*cm,7*cm,5*cm]), P("Le fichier benchmark_outils.csv conserve ces statuts sans inventer de temps, de mémoire ou de scores. Le choix cible reste BGE-M3 pour le texte et un encodeur multilingue compatible CLIP pour les images, mais la décision expérimentale devra être confirmée dans un environnement équipé."), P("Cette séparation entre cible architecturale, mesure exécutée et blocage d'environnement est importante : les résultats locaux présentés dans la suite ne doivent pas être interprétés comme un benchmark des modèles imposés."), PageBreak()]
# Page 7
story += page("5. Indexation et recherche multimodale")
story += [P("L'indexation prévoit deux collections Qdrant : maintidoc_text pour les passages et tableaux, et maintidoc_images pour les figures et photos. Chaque point doit conserver un payload complet, incluant les groupes d'accès. Le filtre de sécurité doit être appliqué avant la recherche."), P("Trois modes sont représentés dans le code : recherche textuelle, recherche visuelle à partir d'une question et recherche par photo. La fusion utilise un Reciprocal Rank Fusion simplifié, qui additionne des contributions liées au rang dans les listes retournées. Aucun reranking ni génération VLM n'est réalisé."), table([["Mode", "Entrée", "Sortie"],["Texte", "Question française", "Passages classés"],["Visuel", "Question et éléments image", "Figures/photos classées"],["Photo", "Chemin d'une image", "Images similaires prévues"],["Fusion", "Listes texte et image", "Top 5 consolidé"],["Traçabilité", "Payload", "Document, page, élément, score"]],[3*cm,6*cm,7*cm]), P("Lorsque Qdrant et les modèles ne sont pas disponibles, le projet produit un index local déterministe et signale explicitement fallback-hash et qdrant_unavailable. Cette voie a servi uniquement à vérifier la chaîne et le filtrage.") ,PageBreak()]
# Page 8
story += page("6. Contrôle d'accès et tests")
story += [P("Le modèle de permissions reprend les groupes du L1. Trois utilisateurs fictifs sont configurés : tech_compresseurs, tech_incendie et responsable. Un élément est candidat uniquement si l'intersection entre ses groupes d'accès et les groupes de l'utilisateur n'est pas vide."), P("Le filtrage est effectué avant le classement et avant la fusion. Ainsi, un document interdit ne peut pas influencer la liste visible de l'utilisateur autorisé. Les tests couvrent l'accès positif, l'absence d'accès entre familles et la tentative de contournement par la fusion multimodale."), table([["Test", "Scénario", "Résultat"],["Autorisé", "Un technicien compresseurs recherche un élément compresseur", "Passé"],["Interdit", "Un technicien incendie cible un document compresseur", "Passé"],["Fusion", "Une photo et une question ciblent une autre famille", "Passé"],["Qdrant réel", "Filtre dans le service vectoriel", "À refaire quand le daemon sera disponible"]],[3*cm,10*cm,3*cm]), P("Les tests directs du fichier tests/test_acces.py ont été exécutés sur l'index local. La preuve d'isolation est donc vérifiée pour le chemin local, mais reste à confirmer sur Qdrant réel.") ,PageBreak()]
# Page 9
story += page("7. Évaluation expérimentale")
story += [P("Le jeu contient 20 questions : 5 avec photo, plusieurs questions textuelles, les paires contradictoires C17/C18 et F17/F18, ainsi que des cas d'accès refusé. Chaque question conserve les éléments attendus et l'utilisateur associé."), table([["Configuration", "Recall@5", "MRR@10", "Interprétation"],["A - texte seul", "0,7500", "0,6333", "Résultat du moteur local de repli"],["B - texte et images", "0,8000", "0,5083", "Résultat du moteur local de repli"]],[4*cm,3*cm,3*cm,6*cm]), P("La configuration B récupère davantage de questions avec un élément attendu dans les cinq premiers résultats, mais son MRR@10 est inférieur dans cette exécution, ce qui signifie que le premier résultat pertinent apparaît en moyenne plus bas. Cette observation ne permet pas de conclure sur BGE-M3 ou CLIP, car les modèles n'ont pas été chargés."), P("Les résultats complets sont conservés dans resultats/resultats_evaluation.csv. Les trois captures produites correspondent à des sorties locales de test et sont identifiées comme telles."), PageBreak()]
# Page 10
story += page("8. Reproductibilité, limites et conclusion")
story += [P("Le README décrit l'installation, l'ingestion, l'indexation, les tests, l'évaluation et le calcul des métriques. Le fichier .env.example ne contient aucun secret. Le ZIP final a été créé sous un dossier racine unique et vérifié par ouverture et lecture de son contenu."), P("Les limites restantes sont : démarrage réel de Qdrant, installation et exécution de PyMuPDF dans l'environnement cible, comparaison OCR, chargement BGE-M3 et CLIP, captures Streamlit et validation d'un clone neuf. Elles sont inscrites comme bloquées ou partiellement réalisées dans la matrice de conformité."), P("Conclusion", "Sub"), P("Le L2 est structuré, documenté et reproductible pour le chemin local de démonstration. L'ingestion, la traçabilité, l'évaluation et les tests RBAC sont effectivement réalisés. La validation complète des composants imposés dépend d'un environnement disposant de Docker, Qdrant, des moteurs OCR et des poids de modèles. Le rapport ne présente donc pas ces éléments comme terminés."), P("Fichiers de référence", "Sub"), table([["Livrable", "Emplacement"],["Rapport principal", "L2_MaintiDoc_OTARID_Rapport.pdf"],["Veille RAG", "L2_MaintiDoc_OTARID_Veille.pdf"],["Matrice", "evaluation/matrice_conformite.md"],["Résultats", "resultats/"],["Archive", "L2_MaintiDoc_OTARID.zip"]],[5*cm,11*cm])]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
