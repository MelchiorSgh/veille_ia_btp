"""MODULE 5 - Base vectorielle : garde les vecteurs des articles déjà vus (dans un fichier JSON)."""
import json, os
from embeddings import similarite


class Base:
    def __init__(self, chemin):
        self.chemin = chemin
        if os.path.exists(chemin):
            with open(chemin, "r", encoding="utf-8") as f:
                self.vecteurs = json.load(f)
        else:
            self.vecteurs = {}  # {lien: vecteur}

    def ajouter(self, lien, vecteur):
        self.vecteurs[lien] = vecteur

    def meilleure_similarite(self, vecteur):
        """Proximité avec l'article le plus ressemblant déjà en mémoire."""
        return max((similarite(vecteur, v) for v in self.vecteurs.values()), default=0)

    def sauver(self):
        derniers = dict(list(self.vecteurs.items())[-500:])   # on ne garde que les 500 derniers
        with open(self.chemin, "w", encoding="utf-8") as f:
            json.dump({lien: [round(x, 4) for x in v] for lien, v in derniers.items()}, f)

