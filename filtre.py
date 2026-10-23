"""MODULE 2 - Filtre : garde un article seulement s'il parle d'IA ET d'architecture/BTP."""
import re

MOTS_IA = (r"artificial intelligence|\bai\b|\bia\b|intelligence artificielle|machine learning|deep learning|"
           r"\bgenerative\b|génératif|neural network|\bllms?\b|large language model|computer vision|"
           r"reinforcement learning|digital twin|jumeau num|autonomous (?:robot|excavator|machine)")
MOTS_BTP = (r"\barchitect(?:ure|ural|s)?\b|construction (?:site|industry|project|material|robot)|civil engineering|"
            r"\bbim\b|\bconcrete\b|\bbéton\b|\bbtp\b|chantier|bâtiment|\bbuildings\b|building (?:information|design|energy|industry)|"
            r"fa[cç]ade|structural (?:engineering|design|analysis)|infrastructure|génie civil")


def pertinent(article):
    texte = (article["titre"] + " " + article["resume"]).lower()
    return bool(re.search(MOTS_IA, texte)) and bool(re.search(MOTS_BTP, texte))
