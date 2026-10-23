import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas

pdf_path = "docs/PLAN_EXPOSE_POWERPOINT.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 30, "Veille Technologique IA x BTP & Architecture - Licence IA (IFRI)")
        self.drawRightString(A4[0] - 54, 30, f"Page {self._pageNumber} sur {page_count}")
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=50
)

styles = getSampleStyleSheet()
primary_color = colors.HexColor("#1e3a8a")
secondary_color = colors.HexColor("#0f172a")
accent_color = colors.HexColor("#f59e0b")
text_dark = colors.HexColor("#1e293b")

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=22,
    textColor=primary_color,
    alignment=1
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor("#475569"),
    alignment=1
)

h1_style = ParagraphStyle(
    "SectionH1",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=15,
    textColor=primary_color,
    spaceBefore=10,
    spaceAfter=4
)

h2_style = ParagraphStyle(
    "SlideH2",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=13,
    textColor=secondary_color,
    spaceBefore=6,
    spaceAfter=2
)

body_style = ParagraphStyle(
    "DocBody",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=11.5,
    textColor=text_dark
)

callout_style = ParagraphStyle(
    "DocCallout",
    parent=body_style,
    fontName="Helvetica-Oblique",
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor("#0c4a6e")
)

table_header_style = ParagraphStyle(
    "TH",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=10,
    textColor=colors.white,
    alignment=1
)

table_cell_style = ParagraphStyle(
    "TD",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=9.5,
    textColor=text_dark
)

story = []

story.append(Paragraph("PLAN OFFICIEL DE L'EXPOSÉ POWERPOINT", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Veille Technologique : L'Intelligence Artificielle dans le BTP et l'Architecture</b><br/>Formation : Licence en Intelligence Artificielle (IFRI / UAC) - Enseignante : Mme Marianne A. O. BALOGOUN, Ing. Msc.", subtitle_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=2, color=accent_color, spaceBefore=2, spaceAfter=8))

# Synthèse Barème
story.append(Paragraph("1. Synthèse du Barème &amp; Critères d'Évaluation Couverts", h1_style))
data_bareme = [
    [Paragraph("Critère d'évaluation", table_header_style), Paragraph("Diapositives", table_header_style), Paragraph("Éléments méthodologiques valorisés", table_header_style)],
    [Paragraph("<b>1. Mots-clés</b>", table_cell_style), Paragraph("Slide 4 &amp; 5", table_cell_style), Paragraph("Délimitation en 4 sous-axes métiers, justification du cycle de vie de l'ouvrage, matrice bilingue FR/EN.", table_cell_style)],
    [Paragraph("<b>2. Chaînes de recherche</b>", table_cell_style), Paragraph("Slide 6", table_cell_style), Paragraph("Opérateurs booléens universels (AND, OR, NOT), guillemets, requêtes transposables Google/arXiv/Brevets.", table_cell_style)],
    [Paragraph("<b>3. Automatisation</b>", table_cell_style), Paragraph("Slide 8, 9 &amp; 10", table_cell_style), Paragraph("Approche hybride Push/Pull, pipeline Python, dédoublonnage sémantique (Embeddings), GitHub Actions, Discord.", table_cell_style)],
    [Paragraph("<b>4. Esprit critique</b>", table_cell_style), Paragraph("Slide 7, 8, 11 &amp; 12", table_cell_style), Paragraph("Grille CRAAP avec formule /10, TRL (1-9), anti-hallucination, Code du numérique (APDP), <b>repêchage en 1 clic</b>.", table_cell_style)]
]
t_bareme = Table(data_bareme, colWidths=[110, 70, 335])
t_bareme.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), primary_color),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
    ("PADDING", (0,0), (-1,-1), 3),
]))
story.append(t_bareme)
story.append(Spacer(1, 8))

# ACTE 1
story.append(Paragraph("ACTE 1 : Cadrage Métier &amp; Problématique", h1_style))
story.append(Paragraph("📌 Diapositive 1 : Titre &amp; Introduction Générale", h2_style))
story.append(Paragraph("Présentation de l'équipe, cadrage académique IFRI, annonce de la problématique de rupture technologique dans le secteur de la construction.", body_style))

story.append(Paragraph("📌 Diapositive 2 : Définitions Métiers &amp; Complémentarité BTP / Architecture", h2_style))
box_def = [
    [Paragraph("<b>Architecture :</b> Art et science de concevoir, agencer et modéliser des espaces bâtis conciliant esthétique, fonctionnalité, calcul de résistance et normes.<br/>"
               "<b>BTP (Bâtiment et Travaux Publics) :</b> Secteur industriel qui matérialise physiquement ces projets (bâtiments tertiaires/résidentiels et grands travaux : routes, ponts, réseaux).<br/>"
               "<b>Pourquoi les lier ?</b> Ils forment une chaîne continue : l'architecte conçoit le modèle numérique, le BTP le construit, et le gestionnaire l'exploite. L'IA est la passerelle numérique entre maquette et chantier réel.", callout_style)]
]
t_def = Table(box_def, colWidths=[515])
t_def.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f0f9ff")),
    ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
    ("PADDING", (0,0), (-1,-1), 5)
]))
story.append(t_def)

story.append(Paragraph("📌 Diapositive 3 : Pourquoi faire une veille sur l'IA dans ce secteur ?", h2_style))
story.append(Paragraph("Enjeux : Secteur pesant ~10% du PIB mondial et 37% des émissions de CO2. Risque d'obsolescence (leçons Nokia/Yahoo) pour les bureaux d'études ignorant l'IA face à des concurrents concevant 10 fois plus vite.", body_style))

story.append(Paragraph("📌 Diapositive 4 : Découpage Thématique en 4 Sous-Axes &amp; Justifications", h2_style))
story.append(Paragraph("Justifications : 1. Élimination du bruit documentaire (le mot BTP seul est trop large). 2. Respect du cycle de vie de l'ouvrage (algorithmes distincts par étape). 3. Ancrage territorial africain (matériaux bio-sourcés, climat tropical, inondations de Cotonou).<br/>"
                       "Les 4 axes : 1. Conception &amp; BIM | 2. Chantier &amp; Sécurité | 3. Exploitation &amp; Jumeaux numériques | 4. Contexte Afrique &amp; Résilience.", body_style))
story.append(Spacer(1, 8))

# ACTE 2
story.append(Paragraph("ACTE 2 : La Stratégie de Recherche", h1_style))
story.append(Paragraph("📌 Diapositive 5 : Matrice des Mots-Clés Bilingues (FR / EN)", h2_style))
data_mots = [
    [Paragraph("Sous-Axe", table_header_style), Paragraph("Mots-clés Français", table_header_style), Paragraph("Mots-clés Anglais", table_header_style), Paragraph("Algorithmes IA", table_header_style)],
    [Paragraph("Conception", table_cell_style), Paragraph("Architecture générative, BIM, Scan-to-BIM, optimisation structurelle", table_cell_style), Paragraph("Generative design, BIM, Text-to-BIM, point cloud", table_cell_style), Paragraph("Modèles de diffusion, LLM multimodaux", table_cell_style)],
    [Paragraph("Chantier", table_cell_style), Paragraph("Sécurité chantier, détection EPI (casques), engins autonomes", table_cell_style), Paragraph("Construction site safety, PPE detection, autonomous excavator", table_cell_style), Paragraph("Vision par ordinateur (YOLO), Reinforcement Learning", table_cell_style)],
    [Paragraph("Exploitation", table_cell_style), Paragraph("Jumeau numérique bâtiment, maintenance prédictive, GTB/BEMS", table_cell_style), Paragraph("Digital twin building, predictive maintenance, SHM", table_cell_style), Paragraph("Séries temporelles (LSTM, Transformers), PINN", table_cell_style)],
    [Paragraph("Afrique", table_cell_style), Paragraph("Architecture tropicale, terre stabilisée, résilience inondations", table_cell_style), Paragraph("Tropical architecture, compressed earth blocks, flood resilience", table_cell_style), Paragraph("Télédétection satellitaire, Edge AI", table_cell_style)]
]
t_mots = Table(data_mots, colWidths=[65, 150, 160, 140])
t_mots.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), primary_color),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
    ("PADDING", (0,0), (-1,-1), 2.5),
]))
story.append(t_mots)

story.append(Paragraph("📌 Diapositive 6 : Chaînes de Recherche Booléennes &amp; Opérateurs Avancés", h2_style))
story.append(Paragraph("• <b>Google Alerts (Presse/Actualités) :</b> <code>\"intelligence artificielle\" (BTP OR architecture OR \"génie civil\" OR chantier) -crypto -jeux</code><br/>"
                       "• <b>arXiv API (Scientifique) :</b> <code>((all:\"building information modeling\" OR all:\"generative design\") OR (all:\"digital twin\" AND all:building)) AND cat:cs.AI</code><br/>"
                       "• <b>Brevets (Lens.org / Google Patents) :</b> <code>(\"autonomous excavator\" OR \"construction robot\") AND (\"deep learning\" OR \"computer vision\")</code>", body_style))
story.append(Spacer(1, 8))

# ACTE 3
story.append(Paragraph("ACTE 3 : Sources, Notation &amp; Automatisation", h1_style))
story.append(Paragraph("📌 Diapositive 7 : Sélection des Sources &amp; Grille d'Évaluation CRAAP", h2_style))
data_craap = [
    [Paragraph("Source", table_header_style), Paragraph("Type", table_header_style), Paragraph("C", table_header_style), Paragraph("R", table_header_style), Paragraph("A", table_header_style), Paragraph("A", table_header_style), Paragraph("P", table_header_style), Paragraph("Note /10", table_header_style), Paragraph("Biais critique identifié", table_header_style)],
    [Paragraph("AEC Magazine", table_cell_style), Paragraph("RSS", table_cell_style), Paragraph("5", table_cell_style), Paragraph("5", table_cell_style), Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("<b>9.2</b>", table_cell_style), Paragraph("Presse tech indépendante, référence mondiale.", table_cell_style)],
    [Paragraph("Construction Dive", table_cell_style), Paragraph("RSS", table_cell_style), Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("<b>8.8</b>", table_cell_style), Paragraph("Presse métier chantiers et sécurité ouvriers.", table_cell_style)],
    [Paragraph("arXiv (cs.AI/CV)", table_cell_style), Paragraph("Atom", table_cell_style), Paragraph("5", table_cell_style), Paragraph("5", table_cell_style), Paragraph("3", table_cell_style), Paragraph("3", table_cell_style), Paragraph("4", table_cell_style), Paragraph("<b>8.0</b>", table_cell_style), Paragraph("Pointe scientifique, mais prépublications sans relecture.", table_cell_style)],
    [Paragraph("ArchDaily", table_cell_style), Paragraph("RSS", table_cell_style), Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("3", table_cell_style), Paragraph("<b>8.0</b>", table_cell_style), Paragraph("Portail mondial, fort biais visuel/marketing.", table_cell_style)],
    [Paragraph("Google News FR/EN", table_cell_style), Paragraph("RSS", table_cell_style), Paragraph("5", table_cell_style), Paragraph("4", table_cell_style), Paragraph("3", table_cell_style), Paragraph("4", table_cell_style), Paragraph("3", table_cell_style), Paragraph("<b>7.6</b>", table_cell_style), Paragraph("Signaux faibles, quelques publi-reportages.", table_cell_style)],
    [Paragraph("Graphisoft (Archicad)", table_cell_style), Paragraph("RSS", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("4", table_cell_style), Paragraph("<b>1</b>", table_cell_style), Paragraph("<b>6.8</b>", table_cell_style), Paragraph("<b>Biais commercial pur (P=1) : vente de logiciels.</b>", table_cell_style)]
]
t_craap = Table(data_craap, colWidths=[85, 25, 15, 15, 15, 15, 15, 40, 290])
t_craap.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), primary_color),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
    ("PADDING", (0,0), (-1,-1), 2),
]))
story.append(t_craap)
story.append(Paragraph("<i>Formule de calcul : Note Source (/10) = (Somme des 5 critères CRAAP sur 5 / 5) * 2.</i>", subtitle_style))

story.append(Paragraph("📌 Diapositive 8 : Grille de Notation des Articles &amp; Échelle TRL", h2_style))
box_trl = [
    [Paragraph("<b>Définition du TRL (Technology Readiness Level) :</b> Échelle de maturité technologique créée par la <b>NASA</b> et adoptée par l'UE. Mesure l'avancement d'une innovation de 1 à 9 :<br/>"
               "• <b>TRL 1 à 3 :</b> Concept théorique et laboratoire | • <b>TRL 4 à 6 :</b> Prototype et simulation | • <b>TRL 7 à 9 :</b> Déploiement opérationnel réel sur chantier.<br/>"
               "<b>Formule de Score Article (/10) :</b> <code>Score = 0.35*Pertinence + 0.20*Impact + 0.20*CRAAP_Source + 0.15*(TRL/9*10) + 0.10*Fraîcheur</code>.<br/>"
               "Seuil d'innovation prioritaire fixé à <b>7.0 / 10</b> (déclenche alerte Discord et cloche).", callout_style)]
]
t_trl = Table(box_trl, colWidths=[515])
t_trl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#fefce8")),
    ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#fef08a")),
    ("PADDING", (0,0), (-1,-1), 5)
]))
story.append(t_trl)

story.append(Paragraph("📌 Diapositive 9 : Méthode Hybride : Veille Passive (Push) vs Veille Active (Pull)", h2_style))
story.append(Paragraph("Push (Passif) : flux RSS continus programmés chaque matin. Pull (Actif) : requêtage ciblé à la demande via <code>veille_active.py</code> sur arXiv, Scholar et brevets pour approfondir un signal faible.", body_style))

story.append(Paragraph("📌 Diapositive 10 : Architecture du Système Automatisé veille-light", h2_style))
story.append(Paragraph("Pipeline 5 étapes : Collecte -> Filtre lexical -> Dédoublonnage vectoriel (Embeddings 256 dim, cosinus &gt; 0.93) -> Analyse LLM -> Multi-diffusion (GitHub Pages, Discord, CSV Excel).", body_style))
story.append(Spacer(1, 8))

# ACTE 4
story.append(Paragraph("ACTE 4 : Esprit Critique, Démonstration &amp; Bilan", h1_style))
story.append(Paragraph("📌 Diapositive 11 : Esprit Critique, Éthique &amp; Repêchage Humain en 1 Clic", h2_style))
story.append(Paragraph("Garde-fous anti-hallucination IA (température 0.2, faits prouvés). Respect du Code du numérique béninois (APDP). Fichier Excel des rejets (<code>rejets.csv</code>) et <b>repêchage interactif en 1 clic</b> depuis le tableau de bord web via <code>serveur.py</code>.", body_style))

story.append(Paragraph("📌 Diapositive 12 : Démonstration Live, Tendances Lourdes &amp; Conclusion", h2_style))
story.append(Paragraph("Démonstration en direct du Dashboard et test du repêchage en 1 clic. 3 signaux faibles : 1. Drones Edge AI sur chantiers isolés. 2. Bétons bas-carbone (-20% clinker). 3. Text-to-BIM.", body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print("PDF genere avec succes.")
