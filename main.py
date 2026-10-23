"""MODULE 12 - Chef d'orchestre : appelle tous les modules dans l'ordre.
Usage : python main.py          (vraie collecte)
        python main.py --demo   (faux articles, sans internet)"""
import json, sys, time
from datetime import datetime, timezone, timedelta
import collecte, filtre, doublons, llm, scoring, sortie, dashboard, alertes
from base_vectorielle import Base

DEMO = "--demo" in sys.argv
P = "demo_" if DEMO else ""                      # préfixe pour ne pas mélanger démo et vrais résultats
CSV, RAPPORT, PAGE = f"data/{P}veille.csv", f"data/{P}rapport.md", f"docs/{P}index.html"
REJETS = f"data/{P}rejets.csv"
VECTEURS, LIENS = f"data/{P}vecteurs.json", f"data/{P}liens_vus.txt"



def articles_demo(config):
    """Faux articles du dossier sample_data (pour tester sans internet)."""
    fiabilite = {s["nom"]: round(sum(s["craap"].values()) / len(s["craap"]) * 2, 1) for s in config["sources"]}
    with open("sample_data/sample.json", "r", encoding="utf-8") as f:
        samples = json.load(f)
    return [{"titre": d["titre"], "lien": d["lien"], "resume": d["resume"], "source": d["source"],
             "type": "arxiv" if "arXiv" in d["source"] else "rss", "fiabilite": fiabilite.get(d["source"], 7.0),
             "date": datetime.now(timezone.utc) - timedelta(days=d["jours"])}
            for d in samples]



def executer_veille(demo=False, logger=print):
    config = json.load(open("sources.json", encoding="utf-8"))
    maintenant = datetime.now(timezone.utc)
    p_locale = "demo_" if demo else ""
    csv_path = f"data/{p_locale}veille.csv"
    rapport_path = f"data/{p_locale}rapport.md"
    rejets_path = f"data/{p_locale}rejets.csv"
    page_path = f"docs/{p_locale}index.html"
    vecteurs_path = f"data/{p_locale}vecteurs.json"
    liens_path = f"data/{p_locale}liens_vus.txt"

    # 1. Collecte
    erreurs, articles = [], []
    if demo:
        articles = articles_demo(config)
    else:
        for source in config["sources"]:
            try:
                articles += collecte.collecter(source)
            except Exception as e:
                erreurs.append(f"{source['nom']} : {e}")
            time.sleep(2)
        if not articles:
            return {"succes": False, "erreur": "Aucune source n'a répondu."}

    # 2. Filtre (récents + pertinents)
    recents = [a for a in articles if a["titre"] and a["lien"] and (not a["date"] or (maintenant - a["date"]).days <= config["jours_max"])]
    pertinents = [a for a in recents if filtre.pertinent(a)]
    rejets_filtre = [(a, "Filtre lexical (absence de mots-clés IA ou BTP)") for a in recents if not filtre.pertinent(a)]

    # 3. Doublons
    base = Base(vecteurs_path)
    liens = sortie.lire_liens(liens_path)
    gardes, ecartes = doublons.retirer_doublons(pertinents, base, liens)

    # 4. Analyse + score
    lignes = []
    for a in gardes:
        analyse = llm.analyser(a)
        if not analyse["pertinent"]:                      # 2e filtre : Gemini juge l'article hors sujet
            ecartes.append((a, "jugé hors sujet par le LLM : " + analyse["raison"]))
            continue
        score, fraicheur = scoring.note_finale(a, analyse)
        lignes.append({"date_collecte": f"{maintenant:%Y-%m-%d}", "date_pub": f"{a['date']:%Y-%m-%d}" if a["date"] else "",
                       "source": a["source"], "titre": a["titre"], "lien": a["lien"], "phase": analyse["phase"],
                       "trl": analyse["trl"], "impact": analyse["impact"], "pertinence": analyse["pertinence"],
                       "fiabilite": a["fiabilite"], "fraicheur": fraicheur, "score": score,
                       "methode": analyse["methode"], "resume_fr": analyse["resume_fr"]})
    lignes.sort(key=lambda l: -l["score"])

    # 5. Sorties
    sortie.ecrire_csv(csv_path, lignes)
    liens_valides = {doublons.cle_url(x["lien"]) for x in sortie.lire_csv(csv_path)}
    vrais_rejets = [
        (a, raison) for a, raison in (ecartes + rejets_filtre)
        if doublons.cle_url(a.get("lien", "")) not in liens_valides
    ]
    sortie.ecrire_rejets(rejets_path, vrais_rejets)
    sortie.ecrire_rapport(rapport_path, lignes, vrais_rejets, erreurs, config["seuil_alerte"], {"lus": len(articles), "pertinents": len(pertinents)}, toutes_fiches=sortie.lire_csv(csv_path))
    base.sauver()
    sortie.sauver_liens(liens_path, liens)
    dashboard.ecrire(page_path, sortie.lire_csv(csv_path)[-200:], config["seuil_alerte"], sortie.lire_rejets(rejets_path))
    alertes.discord([l for l in lignes if l["score"] >= config["seuil_alerte"]])

    stats = {
        "succes": True,
        "lus": len(articles),
        "pertinents": len(pertinents),
        "ecartes": len(vrais_rejets),
        "nouvelles": len(lignes),
        "erreurs": erreurs
    }
    logger(f"Lus {len(articles)} | pertinents {len(pertinents)} | écartés {len(vrais_rejets)} | nouvelles fiches {len(lignes)}")
    return stats


def main():
    executer_veille(demo=DEMO)



if __name__ == "__main__":
    main()
