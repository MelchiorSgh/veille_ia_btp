"""MODULE VÉRIFICATION HUMAINE & GESTION DES REJETS (Human-in-the-Loop)
Conforme au cours IFRI (Slide 22 et 32 : Le tri assisté par IA doit TOUJOURS
pouvoir être soumis à vérification et validation humaine).

Ce script permet au veilleur humain de :
1. Consulter les articles écartés par l'algorithme (filtre lexical, doublons, refus LLM).
2. Valider manuellement un article injustement rejeté (faux négatif) et l'intégrer
   directement dans la base de veille (data/veille.csv) et le tableau de bord.

Usage :
    python valider_rejet.py --lister
    python valider_rejet.py --valider 1
"""
import sys, os, csv, argparse
from datetime import datetime, timezone
import llm, scoring, sortie, dashboard
from base_vectorielle import Base

CSV_VEILLE = "data/veille.csv"
CSV_REJETS = "data/rejets.csv"
PAGE_DASHBOARD = "docs/index.html"
SEUIL_DEFAUT = 7.0


def lister_rejets(chemin_rejets=CSV_REJETS):
    """Affiche la liste numérotée des articles actuellement en quarantaine."""
    rejets = sortie.lire_rejets(chemin_rejets)
    if not rejets:
        print(f"Aucun article rejeté trouvé dans {chemin_rejets}.")
        return []

    print("=" * 75)
    print(f"[*] ARTICLES EN QUARANTAINE / SOUMIS A VERIFICATION HUMAINE ({len(rejets)})")
    print("=" * 75)

    for idx, r in enumerate(rejets, 1):
        decision = r.get("decision_humaine", "En attente")
        print(f"[{idx}] {r.get('source')} | Statut : {decision}")
        print(f"    Titre  : {r.get('titre')}")
        print(f"    Motif  : {r.get('motif_rejet')}")
        print(f"    Lien   : {r.get('lien')}\n")
    return rejets


def valider_article(index_article, chemin_rejets=CSV_REJETS, chemin_veille=CSV_VEILLE):
    """Permet au veilleur humain de forcer l'admission d'un article rejeté."""
    rejets = sortie.lire_rejets(chemin_rejets)
    if not rejets or index_article < 1 or index_article > len(rejets):
        print(f"Index invalide. Choisissez un nombre entre 1 et {len(rejets)}.")
        return

    cible = rejets[index_article - 1]
    print(f"Validation humaine de l'article : {cible.get('titre')}...")

    # Reconstruction de l'objet article pour l'analyse
    article_dict = {
        "titre": cible.get("titre", ""),
        "lien": cible.get("lien", ""),
        "resume": cible.get("titre", ""),
        "source": cible.get("source", "Validation Humaine"),
        "type": "rss",
        "fiabilite": 8.0,
        "date": datetime.now(timezone.utc)
    }

    # Analyse LLM ou fallback mots-clés
    analyse = llm.analyser(article_dict)
    score, fraicheur = scoring.note_finale(article_dict, analyse)

    nouvelle_ligne = {
        "date_collecte": f"{datetime.now():%Y-%m-%d}",
        "date_pub": f"{datetime.now():%Y-%m-%d}",
        "source": f"{cible.get('source')} (Validé Humain)",
        "titre": cible.get("titre"),
        "lien": cible.get("lien"),
        "phase": analyse["phase"],
        "trl": analyse["trl"],
        "impact": analyse["impact"],
        "pertinence": analyse["pertinence"],
        "fiabilite": article_dict["fiabilite"],
        "fraicheur": fraicheur,
        "score": score,
        "methode": "Validation Humaine + " + analyse["methode"],
        "resume_fr": analyse["resume_fr"]
    }

    # Ajout dans la base officielle CSV
    sortie.ecrire_csv(chemin_veille, [nouvelle_ligne])

    # Mise à jour du statut dans rejets.csv
    rejets[index_article - 1]["decision_humaine"] = f"Validé par le veilleur ({datetime.now():%Y-%m-%d})"
    with open(chemin_rejets, "w", newline="", encoding="utf-8-sig") as f:
        ecrivain = csv.DictWriter(f, fieldnames=sortie.CHAMPS_REJETS)
        ecrivain.writeheader()
        ecrivain.writerows(rejets)

    # Mise à jour du dashboard
    lignes = sortie.lire_csv(chemin_veille)
    page_file = "docs/demo_index.html" if "demo" in chemin_veille else PAGE_DASHBOARD
    dashboard.ecrire(page_file, lignes[-200:], SEUIL_DEFAUT, rejets)


    print(f"\n[+] Article validé avec succès !")
    print(f"    Phase : {nouvelle_ligne['phase']} | Score : {nouvelle_ligne['score']}/10")
    print(f"    L'article a été intégré dans {chemin_veille} et le tableau de bord.")
    return nouvelle_ligne



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vérification humaine des articles rejetés")
    parser.add_argument("--lister", action="store_true", help="Lister tous les articles en quarantaine")
    parser.add_argument("--valider", type=int, help="Numéro de l'article rejeté à valider manuellement")
    parser.add_argument("--demo", action="store_true", help="Travailler sur les fichiers de démonstration")
    args = parser.parse_args()

    rejets_file = "data/demo_rejets.csv" if args.demo else CSV_REJETS
    veille_file = "data/demo_veille.csv" if args.demo else CSV_VEILLE

    if args.valider:
        valider_article(args.valider, chemin_rejets=rejets_file, chemin_veille=veille_file)
    else:
        lister_rejets(chemin_rejets=rejets_file)
