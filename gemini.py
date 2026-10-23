"""MODULE 3 - Appel à Gemini : une seule fonction, utilisée par les embeddings et par le LLM."""
import os, json, time, urllib.request, urllib.error

MODELE_LLM = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
MODELE_EMB = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
PAUSE = 2  # secondes entre deux appels (le palier gratuit limite le nombre de requêtes par minute)

# Modèles de secours si le modèle demandé n'existe pas (404) ou est surchargé
SECOURS_LLM = ["gemini-flash-lite-latest", "gemini-flash-latest", "gemini-2.5-flash"]
SECOURS_EMB = ["gemini-embedding-001", "gemini-embedding-2"]


def appeler(modele, methode, corps):
    """Envoie une requête à Gemini avec basculement automatique sur modèles valides en cas de 404."""
    global MODELE_LLM, MODELE_EMB
    cle = os.getenv("GEMINI_API_KEY")
    if not cle:
        return None

    # Déterminer la liste ordonnée des modèles à tenter
    candidats = [modele]
    if methode == "generateContent":
        for s in SECOURS_LLM:
            if s not in candidats:
                candidats.append(s)
    elif methode == "batchEmbedContents":
        for s in SECOURS_EMB:
            if s not in candidats:
                candidats.append(s)

    for m in candidats:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:{methode}"
        # Ajuster le nom de modèle dans le corps si batchEmbedContents
        corps_actuel = corps
        if methode == "batchEmbedContents" and "requests" in corps:
            corps_actuel = {
                "requests": [dict(r, model=f"models/{m}") for r in corps["requests"]]
            }

        for essai in range(3):
            try:
                time.sleep(PAUSE)
                requete = urllib.request.Request(
                    url,
                    data=json.dumps(corps_actuel).encode(),
                    headers={"Content-Type": "application/json", "x-goog-api-key": cle}
                )
                reponse = json.loads(urllib.request.urlopen(requete, timeout=35).read())
                # En cas de succès avec un modèle de secours, le mémoriser
                if m != modele:
                    if methode == "generateContent":
                        MODELE_LLM = m
                    else:
                        MODELE_EMB = m
                return reponse
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # Le modèle n'existe pas, on passe au candidat suivant immédiatement
                    break
                if e.code in (429, 500, 503) and essai < 2:  # quota ou serveur occupé : pause
                    time.sleep(6 * (essai + 1))
                    continue
                print(f"  (Gemini HTTP {e.code} avec le modèle {m})")
                break
            except Exception as e:
                if essai < 2:
                    time.sleep(5)
                    continue
                print(f"  (Gemini indisponible avec {m} : {e})")
                break
    return None

