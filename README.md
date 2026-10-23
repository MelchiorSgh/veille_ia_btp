# Veille Technologique : L'IA dans le BTP et l'Architecture
**Projet IFRI — Licence en Intelligence Artificielle**  
*Cours : Veille Technologique & Intelligence Économique (Mme Marianne A. O. BALOGOUN, Ing. Msc.)*

Système de veille hybride automatisé combinant **Veille Passive (Push)** via flux RSS/Atom et **Veille Active (Pull)** via requêtes booléennes ciblées sur arXiv, Google Scholar et bases de brevets.

---

## 🏗️ Architecture Modulaire

Le pipeline exécute un traitement en 5 étapes conforme au cycle de veille du cours :
`Collecte ➔ Filtrage lexical ➔ Dédoublonnage sémantique vectoriel ➔ Analyse critique LLM ➔ Scoring pondéré & Multi-diffusion`

| Fichier | Rôle dans le dispositif de veille |
|---|---|
| `sources.json` | Configuration des sources avec métadonnées **CRAAP** (1-5) et typologie (*Information Blanche*) |
| `collecte.py` | Parseur RSS/Atom avec sanitisation XML robuste (gère entités illégales et encodages) |
| `filtre.py` | Filtrage bi-dimensionnel strict par expressions régulières : intersection `[Mots IA] ∩ [Mots BTP]` |
| `gemini.py` | Client API Google Gemini résilient avec basculement automatique sur modèles de secours en cas de 404/indisponibilité |
| `embeddings.py` | Modélisation sémantique en vecteurs 256 dimensions (`gemini-embedding-001`) |
| `base_vectorielle.py` | Index vectoriel JSON persistant avec calcul de similarité cosinus |
| `doublons.py` | Double barrière anti-doublon : normalisation d'URL + similarité sémantique (seuil 0.93) |
| `llm.py` | Analyse critique sans hallucination (consigne Slide 43) : phase, maturité TRL, impact, pertinence, synthèse FR |
| `scoring.py` | Formule décisionnelle pondérée sur 10 intégrant la note CRAAP et la décroissance de fraîcheur |
| `veille_active.py` | **Module de Veille Active (Pull)** : interrogation ciblée à la demande sur arXiv API + liens Scholar & Brevets |
| `sortie.py` | Export tableur CSV cumulatif (`data/veille.csv`) et rapport Markdown quotidien (`data/rapport.md`) |
| `dashboard.py` | Générateur du **Tableau de Bord interactif** (`docs/index.html`) avec KPI, recherche et filtres |
| `alertes.py` | Notification instantanée par Webhook Discord pour les innovations prioritaires ($\ge 7.0/10$) |
| `.github/workflows/veille.yml` | Workflow GitHub Actions planifié chaque matin à 07:00 UTC (08:00 Bénin) |

---

## 🚀 Guide d'Utilisation

### 1. Exécuter les tests unitaires (20 tests automatisés)
```bash
python -m unittest discover -s tests
```

### 2. Tester en mode Démo (Sans Internet, données de test)
```bash
python main.py --demo
```
Génère le rapport dans `data/demo_rapport.md` et le tableau de bord dans `docs/demo_index.html`.

### 3. Lancer la Veille Passive complète (Push)
```bash
python main.py
```
Lit toutes les sources actives de `sources.json`, filtre, dédoublonne, note et publie les résultats.

### 4. Lancer une session de Veille Active ciblée (Pull)
```bash
# Investigation par thématique prédéfinie
python veille_active.py --theme conception      # BIM, IA générative, Scan-to-BIM
python veille_active.py --theme chantier        # Sécurité, vision par ordinateur, robots
python veille_active.py --theme exploitation    # Jumeaux numériques, maintenance prédictive
python veille_active.py --theme afrique         # Résilience climatique, voirie, matériaux locaux

# Investigation par requête booléenne libre
python veille_active.py --query "digital twin building machine learning" --max 5
```

---

## 📚 Dossiers & Supports d'Évaluation de l'Exposé

Tous les documents requis pour la notation sont disponibles dans le dossier `docs/` :
- **[Guide Complet de l'Exposé Oral & Soutenance](docs/EXPOSE_SOUTENANCE.md) :** Plan diapo par diapo avec minutage (15 min), script oratoire intégral mot pour mot, et 5 questions/réponses pièges du jury.
- **[Dossier de Veille Technologique](docs/DOSSIER_VEILLE_TECHNO.md) :** Rapport écrit officiel exhaustif (Cadrage AFNOR, matrice CRAAP/AACODS, cadre légal APDP / Code du numérique, et les 3 piliers de l'IE selon Martre 1994).
- **[Guide des Mots-Clés & Chaînes de Recherche](docs/GUIDE_CHAINE_RECHERCHE.md) :** Recueil des équations booléennes, opérateurs avancés Google, Scholar, arXiv et Brevets.

---

## ⚙️ Configuration Cloud & Déploiement
1. Déposer le dépôt sur GitHub.
2. Ajouter les secrets dans **Settings > Secrets and variables > Actions** :
   - `GEMINI_API_KEY` : Clé API Google AI Studio (gratuite).
   - `DISCORD_WEBHOOK` : (Facultatif) URL du webhook du salon Discord.
3. Activer GitHub Pages dans **Settings > Pages** : Source = `Deploy from a branch`, Branche = `main`, Dossier = `/docs`.
