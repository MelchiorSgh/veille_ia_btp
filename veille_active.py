"""MODULE VEILLE ACTIVE (PULL) - Recherche ciblée et approfondie à la demande.
Conforme au cours d'Intelligence Économique / Veille (IFRI - Slide 26 : Pull vs Push).
Complète la veille passive (flux RSS programmés) par des requêtes booléennes ciblées
sur les bases scientifiques (arXiv), et génère les équations de recherche pour Google Scholar,
IEEE Xplore et les bases de brevets (Google Patents, Lens.org).

Usage :
    python veille_active.py --theme conception
    python veille_active.py --theme chantier
    python veille_active.py --theme exploitation
    python veille_active.py --query "scan-to-bim deep learning"
"""
import sys, os, urllib.request, urllib.parse, argparse
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import filtre, doublons, llm, scoring, sortie
from base_vectorielle import Base
import collecte

# Thématiques ciblées prédéfinies avec équations de recherche booléennes
THEMES_ACTIFS = {
    "conception": {
        "nom": "Conception & Architecture Générative (BIM/IA)",
        "query_arxiv": '((all:"generative design" OR all:"building information modeling" OR all:"scan-to-bim") AND (all:architecture OR all:building)) AND (cat:cs.AI OR cat:cs.CV)',
        "scholar_query": '"generative design" ("BIM" OR architecture) "deep learning"',
        "patents_query": '("generative design" OR "building information modeling") "artificial intelligence"',
    },
    "chantier": {
        "nom": "Chantier & Sécurité / Robotique BTP",
        "query_arxiv": '((all:"construction site" OR all:"construction safety") AND (all:"computer vision" OR all:robot OR all:drone OR all:"reinforcement learning")) AND (cat:cs.CV OR cat:cs.RO OR cat:cs.AI)',
        "scholar_query": '"computer vision" "construction site" (safety OR helmet OR robot)',
        "patents_query": '("autonomous excavator" OR "construction robot") "machine learning"',
    },
    "exploitation": {
        "nom": "Exploitation, Jumeaux Numériques & Maintenance Prédictive",
        "query_arxiv": '((all:"digital twin" OR all:"predictive maintenance" OR all:"building energy") AND (all:building OR all:infrastructure)) AND (cat:cs.AI OR cat:cs.LG)',
        "scholar_query": '"digital twin" "predictive maintenance" building "machine learning"',
        "patents_query": '"digital twin" ("facility management" OR "building") "predictive maintenance"',
    },
    "afrique": {
        "nom": "IA, BTP & Résilience Climatique en Afrique",
        "query_arxiv": '((all:Africa OR all:tropical OR all:climate) AND (all:construction OR all:building OR all:infrastructure) AND (all:"machine learning" OR all:AI))',
        "scholar_query": '("Africa" OR "Bénin" OR "tropical") (construction OR infrastructure) ("artificial intelligence" OR "machine learning")',
        "patents_query": '(Africa OR tropical) construction materials "artificial intelligence"',
    }
}

SOURCE_ACTIVE_CRAAP = {
    "nom": "arXiv API (Veille Active)",
    "type": "active_pull",
    "craap": {"actualite": 5, "pertinence": 5, "autorite": 4, "fiabilite": 4, "objectif": 4}
}


def generer_liens_recherche_externe(terme_recherche):
    """Génère les URLs directes vers les bases scientifiques et de brevets avec syntaxe booléenne."""
    q_enc = urllib.parse.quote_plus(terme_recherche)
    return {
        "Google Scholar": f"https://scholar.google.com/scholar?q={q_enc}",
        "IEEE Xplore": f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={q_enc}",
        "Google Patents": f"https://patents.google.com/?q={q_enc}",
        "Lens.org": f"https://www.lens.org/lens/search/scholar/list?q={q_enc}"
    }


def interroger_arxiv(query, max_results=10):
    """Effectue une requête Pull ciblée sur l'API arXiv avec tri par date de soumission."""
    q_enc = urllib.parse.quote(query, safe="():+=&")
    url = f"https://export.arxiv.org/api/query?search_query={q_enc}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (veille-active-ifri)"})
    try:
        xml_bytes = urllib.request.urlopen(req, timeout=30).read()
        return collecte.lire_flux(xml_bytes, SOURCE_ACTIVE_CRAAP)
    except Exception as e:
        print(f"Erreur d'interrogation arXiv : {e}")
        return []


def executer_veille_active(theme=None, requete_libre=None, max_articles=8):
    print("=" * 65)
    print("[*] SESSION DE VEILLE ACTIVE (METHODE PULL)")
    print("=" * 65)

    if theme and theme in THEMES_ACTIFS:
        info_theme = THEMES_ACTIFS[theme]
        print(f"Theme selectionne : {info_theme['nom']}")
        query_arxiv = info_theme["query_arxiv"]
        terme_global = info_theme["scholar_query"]
    elif requete_libre:
        print(f"Requete personnalisee : {requete_libre}")
        query_arxiv = f'all:"{requete_libre}" AND (cat:cs.AI OR cat:cs.CV OR cat:cs.RO OR cat:cs.LG)'
        terme_global = requete_libre
    else:
        info_theme = THEMES_ACTIFS["conception"]
        query_arxiv = info_theme["query_arxiv"]
        terme_global = info_theme["scholar_query"]

    # Affichage des requêtes externes complémentaires (Bases académiques & Brevets)
    liens = generer_liens_recherche_externe(terme_global)
    print("\n[Equations pour approfondissement multi-sources]")
    for moteur, url in liens.items():
        print(f"  * {moteur:<16} : {url}")

    print(f"\n[Interrogation directe arXiv API] (max {max_articles} articles)...")
    articles = interroger_arxiv(query_arxiv, max_results=max_articles)
    print(f"  -> {len(articles)} publications scientifiques recuperees.")

    # Filtrage par mots-clés du domaine
    pertinents = [a for a in articles if filtre.pertinent(a)]
    print(f"  -> {len(pertinents)} articles valides par le filtre IA/BTP.")

    # Dédoublonnage vectoriel
    base = Base("data/vecteurs.json")
    liens_connus = sortie.lire_liens("data/liens_vus.txt")
    gardes, ecartes = doublons.retirer_doublons(pertinents, base, liens_connus)
    print(f"  -> {len(gardes)} nouvelles publications inedites (ecartees : {len(ecartes)}).")

    # Analyse LLM & Scoring
    maintenant = datetime.now(timezone.utc)
    lignes = []
    for a in gardes:
        print(f"  Analyse LLM de : {a['titre'][:60]}...")
        analyse = llm.analyser(a)
        if not analyse["pertinent"]:
            ecartes.append((a, "Hors sujet selon LLM : " + analyse["raison"]))
            continue
        score, fraicheur = scoring.note_finale(a, analyse)
        lignes.append({
            "date_collecte": f"{maintenant:%Y-%m-%d}",
            "date_pub": f"{a['date']:%Y-%m-%d}" if a["date"] else "",
            "source": f"{a['source']} (Active Pull)",
            "titre": a["titre"],
            "lien": a["lien"],
            "phase": analyse["phase"],
            "trl": analyse["trl"],
            "impact": analyse["impact"],
            "pertinence": analyse["pertinence"],
            "fiabilite": a["fiabilite"],
            "fraicheur": fraicheur,
            "score": score,
            "methode": analyse["methode"],
            "resume_fr": analyse["resume_fr"]
        })

    if lignes:
        lignes.sort(key=lambda l: -l["score"])
        sortie.ecrire_csv("data/veille.csv", lignes)
        base.sauver()
        sortie.sauver_liens("data/liens_vus.txt", liens_connus)
        # Mise à jour immédiate du dashboard
        toutes_lignes = sortie.lire_csv("data/veille.csv")
        tous_rejets = [({"source": r.get("source", ""), "titre": r.get("titre", ""), "lien": r.get("lien", "")}, r.get("motif_rejet", ""))
                       for r in sortie.lire_rejets("data/rejets.csv")]
        dashboard.ecrire("docs/index.html", toutes_lignes[-200:], 7.0, tous_rejets)

        print(f"\n[+] {len(lignes)} fiches ajoutees avec succes a la base de veille (data/veille.csv).")
        for l in lignes:
            print(f"  [{l['phase']}] {l['score']}/10 - {l['titre']}")
            print(f"    Synthese : {l['resume_fr'][:120]}...\n")
    else:
        print("\nAucun nouvel article n'a ete insere (deja presents dans la base ou hors-sujet).")

    return {
        "succes": True,
        "nouvelles": len(lignes),
        "recuperees": len(articles),
        "pertinents": len(pertinents),
        "ecartees": len(ecartes)
    }




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Veille Active (Pull) - Requêtes ciblées")
    parser.add_argument("--theme", choices=["conception", "chantier", "exploitation", "afrique"],
                        help="Thème prédéfini avec chaînes de recherche optimisées")
    parser.add_argument("--query", type=str, help="Requête booléenne libre")
    parser.add_argument("--max", type=int, default=8, help="Nombre max d'articles à rapatrier")
    args = parser.parse_args()

    executer_veille_active(theme=args.theme, requete_libre=args.query, max_articles=args.max)
