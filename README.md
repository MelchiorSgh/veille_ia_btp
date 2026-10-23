# Veille Technologique : L'IA dans le BTP et l'Architecture

Dispositif automatisé de veille technologique pour surveiller, filtrer et analyser les innovations de l'intelligence artificielle appliquée au secteur du BTP et de l'architecture.

---

## 🏗️ Architecture du Projet

Le pipeline exécute un traitement modulaire en 5 étapes :
`Collecte RSS ➔ Filtrage lexical (Regex) ➔ Dédoublonnage vectoriel ➔ Analyse critique LLM (Gemini) ➔ Scoring pondéré & Restitution`

| Fichier | Rôle |
|---|---|
| `sources.json` | Configuration des flux RSS surveillés avec évaluation CRAAP |
| `collecte.py` | Parseur RSS/Atom avec sanitisation XML robuste |
| `filtre.py` | Filtrage lexical strict par expressions régulières (Regex) |
| `gemini.py` | Client API Google Gemini avec gestion de basculement |
| `embeddings.py` | Vectorisation sémantique (`gemini-embedding-001`) |
| `base_vectorielle.py` | Index vectoriel JSON persistant et calcul de similarité cosinus |
| `doublons.py` | Dédoublonnage par normalisation d'URL et similarité vectorielle |
| `llm.py` | Analyse sémantique : phase du bâtiment, maturité TRL, impact, pertinence, synthèse FR |
| `scoring.py` | Formule multicritère pondérée sur 10 |
| `serveur.py` | Serveur web local interactif pour le pilotage et le repêchage |
| `sortie.py` | Export Excel (.xlsx), CSV cumulatif et rapport Markdown |
| `dashboard.py` | Générateur du tableau de bord web interactif (`docs/index.html`) |
| `valider_rejet.py` | Module de vérification humaine et repêchage (Human-in-the-Loop) |
| `alertes.py` | Notification par Webhook Discord pour les signaux prioritaires |
| `.github/workflows/veille.yml` | Automatisation quotidienne GitHub Actions planifiée chaque matin |

---

## 🚀 Utilisation

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Exécuter les tests unitaires (20 tests automatisés)
```bash
python -m unittest discover -s tests
```

### 3. Tester en mode Démo (hors-ligne)
```bash
python main.py --demo
```
Génère le rapport dans `data/demo_rapport.md` et le tableau de bord dans `docs/demo_index.html`.

### 4. Lancer la veille complète
```bash
python main.py
```
Lit toutes les sources actives de `sources.json`, filtre, dédoublonne, note et génère les exports Excel, CSV et le tableau de bord.

### 5. Lancer l'interface web locale
```bash
python serveur.py
```
Ouvre le centre de pilotage interactif sur `http://localhost:8000`.

---

## ⚙️ Déploiement & Automatisation GitHub

1. **Variables secrètes** (dans **Settings > Secrets and variables > Actions**) :
   - `GEMINI_API_KEY` : Clé API Google AI Studio.
   - `DISCORD_WEBHOOK` : (Facultatif) Webhook Discord pour les alertes prioritaires.
2. **Tableau de bord en ligne (GitHub Pages)** :
   - Dans **Settings > Pages**, définir Source = `Deploy from a branch`, Branche = `main`, Dossier = `/docs`.
