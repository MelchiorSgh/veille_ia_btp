"""SERVEUR WEB LOCAL INTERACTIF - OBSERVATOIRE & PILOTAGE DE VEILLE
Centralise tout le contrôle de la veille directement depuis le navigateur :
- Lancement de la Veille Passive quotidienne (Push)
- Lancement de la Veille Active ciblée (Pull)
- Repêchage d'articles rejetés en 1 clic
- Consultation et téléchargement des fichiers (veille.csv, rejets.csv, rapport.md)
- Réinitialisation et test du mode démo

Usage :
    python serveur.py          (mode production)
    python serveur.py --demo   (mode démo)
"""
import sys, os, json, http.server, socketserver, webbrowser, urllib.parse
from pathlib import Path
import main, valider_rejet, sortie

PORT = 8000
DEMO = "--demo" in sys.argv


class GestionnaireVeille(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def repondre_json(self, donnees, code=200):
        reponse = json.dumps(donnees, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(reponse)))
        self.end_headers()
        self.wfile.write(reponse)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        chemin = url_parsed.path

        if chemin in ("/", "/index.html"):
            fichier = "docs/demo_index.html" if DEMO else "docs/index.html"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            with open(fichier, "rb") as f:
                self.wfile.write(f.read())
            return

        elif chemin == "/demo":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            with open("docs/demo_index.html", "rb") as f:
                self.wfile.write(f.read())
            return

        elif chemin == "/api/fichier":
            query = urllib.parse.parse_qs(url_parsed.query)
            nom = query.get("nom", [""])[0]
            est_demo = query.get("demo", ["0"])[0] == "1" or DEMO
            p_prefix = "demo_" if est_demo else ""

            chemins_autorises = {
                "veille.xlsx": f"data/{p_prefix}veille.xlsx",
                "rejets.xlsx": f"data/{p_prefix}rejets.xlsx",
                "veille.csv": f"data/{p_prefix}veille.csv",
                "rejets.csv": f"data/{p_prefix}rejets.csv",
                "rapport.md": f"data/{p_prefix}rapport.md",
                "sources.json": "sources.json"
            }

            if nom in chemins_autorises and os.path.exists(chemins_autorises[nom]):
                cible = chemins_autorises[nom]
                if nom.endswith(".xlsx"):
                    type_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif nom.endswith(".csv"):
                    type_mime = "text/csv; charset=utf-8"
                elif nom.endswith(".json"):
                    type_mime = "application/json; charset=utf-8"
                else:
                    type_mime = "text/markdown; charset=utf-8"
                self.send_response(200)
                self.send_header("Content-Type", type_mime)
                if query.get("telecharger", ["0"])[0] == "1":
                    self.send_header("Content-Disposition", f"attachment; filename={p_prefix}{nom}")
                self.end_headers()
                with open(cible, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.repondre_json({"succes": False, "erreur": "Fichier introuvable"}, 404)
                return

        super().do_GET()

    def do_POST(self):
        url_parsed = urllib.parse.urlparse(self.path)
        chemin = url_parsed.path
        taille = int(self.headers.get("Content-Length", 0))
        corps = json.loads(self.rfile.read(taille).decode("utf-8")) if taille > 0 else {}

        # 1. Lancer la Veille Automatisée (main.py)
        if chemin == "/api/lancer_veille":
            est_demo = bool(corps.get("demo", DEMO))
            try:
                stats = main.executer_veille(demo=est_demo)
                self.repondre_json({"succes": True, "stats": stats})
            except Exception as e:
                self.repondre_json({"succes": False, "erreur": str(e)}, 500)
            return

        # 2. Repêcher un article écarté
        elif chemin == "/api/repecher":
            index = int(corps.get("index", 0))
            est_demo = bool(corps.get("demo", DEMO))
            rejets_csv = "data/demo_rejets.csv" if est_demo else "data/rejets.csv"
            veille_csv = "data/demo_veille.csv" if est_demo else "data/veille.csv"
            try:
                nouvel_article = valider_rejet.valider_article(
                    index, chemin_rejets=rejets_csv, chemin_veille=veille_csv
                )
                if nouvel_article:
                    self.repondre_json({"succes": True, "article": nouvel_article})
                    return
            except Exception as e:
                self.repondre_json({"succes": False, "erreur": str(e)}, 500)
                return
            self.repondre_json({"succes": False, "erreur": "Échec repêchage"}, 400)
            return

        # 4. Réinitialiser la démo
        elif chemin == "/api/reset_demo":
            for f in Path("data").glob("demo_*"):
                try:
                    f.unlink()
                except Exception:
                    pass
            try:
                stats = main.executer_veille(demo=True)
                self.repondre_json({"succes": True, "stats": stats})
            except Exception as e:
                self.repondre_json({"succes": False, "erreur": str(e)}, 500)
            return

        super().do_POST()


def lancer():
    adresse = f"http://localhost:{PORT}"
    print("=" * 70)
    print(f"[*] OBSERVATOIRE TECHNOLOGIQUE ACTIF SUR {adresse}")
    print(f"[*] Mode : {'DÉMONSTRATION (docs/demo_index.html)' if DEMO else 'PRODUCTION (docs/index.html)'}")
    print("    -> Centre de pilotage centralisé ouvert dans votre navigateur.")
    print("    -> Lancez la veille, repêchez en 1 clic et téléchargez les CSV sans terminal.")
    print("    -> Appuyez sur Ctrl+C pour arrêter le serveur.")
    print("=" * 70)

    try:
        webbrowser.open(adresse)
    except Exception:
        pass

    with socketserver.TCPServer(("", PORT), GestionnaireVeille) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur.")
            httpd.server_close()


if __name__ == "__main__":
    lancer()
