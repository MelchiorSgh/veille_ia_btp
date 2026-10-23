# Rapport Exécutif de Veille Technologique — 15/10/2026

> **Dispositif de Veille :** Observatoire automatisé (IFRI - Licence IA)
> **Thématique :** L'intelligence artificielle dans le BTP et l'architecture

---

## 1. Synthèse Décisionnelle & Indicateurs Clés

| Indicateur Clé | Valeur | Description & Impact |
| :--- | :---: | :--- |
| **Flux mondiaux surveillés (bruts)** | **8** | Volume total d'articles collectés via les flux RSS/Atom |
| **Innovations validées en base** | **6** | Fiches qualifiées par le double filtrage IA et stockées |
| **Signaux prioritaires (Score >= 7.0/10)** | **5** | Innovations majeures à fort impact opérationnel immédiat |
| **Articles écartés (Quarantaine)** | **2** | Rejets conservés pour audit et vérification humaine |

---

## 2. Top Signaux & Innovations Prioritaires (Score >= 7.0/10)

### [Graphisoft launches AI plugin for Archicad that generates facade layouts](https://example.org/a1)
- **Phase :** Conception | **Source :** ArchDaily | **Score :** 8.4/10 | **Maturité :** TRL 8.0/9
- **Synthèse :** Graphisoft lance un assistant IA sous forme de plugin pour Archicad, utilisant la conception générative pour proposer des agencements de façades. Cet outil vise à réduire le temps de conception et l'impact carbone pour les architectes.

### [Digital twin and predictive maintenance pilot cuts building energy use](https://example.org/c1)
- **Phase :** Exploitation | **Source :** Canadian Architect | **Score :** 8.4/10 | **Maturité :** TRL 8.0/9
- **Synthèse :** Un projet pilote déploie un jumeau numérique couplé au machine learning pour assurer la maintenance prédictive d'un bâtiment commercial. Cette approche permet un suivi énergétique précis et génère une réduction des coûts de 18 pour cent.

### [Computer vision for construction site safety: detecting missing helmets with drones](https://example.org/x2)
- **Phase :** Chantier | **Source :** arXiv (IA x construction) | **Score :** 8.1/10 | **Maturité :** TRL 5.0/9
- **Synthèse :** Cet article présente un modèle de vision par ordinateur embarqué sur des drones pour surveiller la sécurité sur les chantiers. Il détecte automatiquement le manque d'équipements de protection individuelle, spécifiquement les casques.

### [Machine learning predicts concrete strength for 3D printing of structures](https://example.org/n1)
- **Phase :** Conception | **Source :** Nature (Engineering) | **Score :** 8.0/10 | **Maturité :** TRL 4.0/9
- **Synthèse :** Des chercheurs ont développé un modèle de machine learning pour prédire la résistance des mélanges de béton utilisés en impression 3D. Cette innovation améliore la sécurité structurelle tout en réduisant l'empreinte carbone de la construction.

### [Reinforcement learning for autonomous excavator scheduling on construction sites](https://example.org/x1)
- **Phase :** Chantier | **Source :** arXiv (IA x construction) | **Score :** 7.4/10 | **Maturité :** TRL 4.0/9
- **Synthèse :** Cet article présente un nouveau cadre basé sur l'apprentissage par renforcement pour optimiser l'ordonnancement d'excavatrices autonomes sur les chantiers. Des simulations démontrent des gains de productivité significatifs grâce à cette approche robotique.

---

## 3. Répartition des Innovations par Cycle de Vie du Bâtiment

### Phase 1 : Conception & Modélisation BIM (3 fiches)

- **[Graphisoft launches AI plugin for Archicad that generates facade layouts](https://example.org/a1)** (ArchDaily, Score 8.4/10, TRL 8.0) — *Graphisoft lance un assistant IA sous forme de plugin pour Archicad, utilisant la conception générative pour proposer des agencements de faç...*
- **[Machine learning predicts concrete strength for 3D printing of structures](https://example.org/n1)** (Nature (Engineering), Score 8.0/10, TRL 4.0) — *Des chercheurs ont développé un modèle de machine learning pour prédire la résistance des mélanges de béton utilisés en impression 3D. Cette...*
- **[Why architects are skeptical of AI-generated renderings](https://example.org/e1)** (Common Edge, Score 6.3/10, TRL 6.0) — *Cet article explore le scepticisme des architectes face aux outils de rendu générés par l'intelligence artificielle. Il met en lumière les l...*

### Phase 2 : Chantier, Robotique & Sécurité Ouvrière (2 fiches)

- **[Computer vision for construction site safety: detecting missing helmets with drones](https://example.org/x2)** (arXiv (IA x construction), Score 8.1/10, TRL 5.0) — *Cet article présente un modèle de vision par ordinateur embarqué sur des drones pour surveiller la sécurité sur les chantiers. Il détecte au...*
- **[Reinforcement learning for autonomous excavator scheduling on construction sites](https://example.org/x1)** (arXiv (IA x construction), Score 7.4/10, TRL 4.0) — *Cet article présente un nouveau cadre basé sur l'apprentissage par renforcement pour optimiser l'ordonnancement d'excavatrices autonomes sur...*

### Phase 3 : Exploitation, Maintenance & Jumeaux Numériques (1 fiches)

- **[Digital twin and predictive maintenance pilot cuts building energy use](https://example.org/c1)** (Canadian Architect, Score 8.4/10, TRL 8.0) — *Un projet pilote déploie un jumeau numérique couplé au machine learning pour assurer la maintenance prédictive d'un bâtiment commercial. Cet...*

---

## 4. Bilan Qualité, Filtrage & Esprit Critique (Human-in-the-Loop)

Afin de garantir l'absence d'hallucinations et de neutraliser les faux positifs, le pipeline applique un filtrage strict à 3 niveaux :

| Motif d'exclusion | Nombre | Justification méthodologique |
| :--- | :---: | :--- |
| **Filtre lexical (hors-sujet)** | 1 | Absence des mots-clés bilingues du domaine dans le titre et le résumé |
| **Doublons sémantiques / URL** | 1 | Articles déjà connus ou clones de communiqués de presse (similarité >= 85%) |
| **Refus sémantique LLM (Gemini)** | 0 | Mots-clés présents mais faux amis (ex: architecture informatique, campus sans IA) |
| **Total articles en quarantaine** | **2** | Consultables et repêchables directement dans l'onglet Rejetés |

---

## 5. Recommandations Opérationnelles pour les Équipes

1. **Accélération BIM/IA :** Prioriser l'expérimentation des agents d'automatisation des maquettes Revit/IFC pour réduire les temps de pré-construction.
2. **Sécurité sur chantier :** Évaluer les systèmes de vision par ordinateur (détection de casques et EPI) pour réduire les risques d'accidents du travail.
3. **Conformité & Éthique :** Veiller au respect du cadre légal (Code du numérique béninois et APDP) concernant le traitement d'images d'ouvriers sur chantier.
