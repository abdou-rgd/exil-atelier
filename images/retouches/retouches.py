"""Pose les détails d'un pixel que le modèle ne sait pas dessiner.

Chaque retouche : (x, y, couleur). Couleurs prises dans la palette de
l'emblème (docs/direction-artistique/prompt-claude-design.md).
Usage : python retouches.py dossier_entree dossier_sortie
"""
import sys
from pathlib import Path

from PIL import Image

RETOUCHES = {
    # Deux pixels orange aux mains : la chaleur qu'il donne, prise à son corps.
    "calidus": [(1, 34, "#E8742E"), (16, 34, "#E8742E"), (1, 33, "#D25426"), (16, 33, "#D25426")],
    # La perle pâle au front, sous la capuche.
    "mare-luna": [(8, 5, "#EEF5E6")],
    # Lunettes rondes : un verre sombre, un pixel de reflet.
    "specula": [(7, 7, "#3B3632"), (9, 7, "#F8F7E9")],
}


def hex_rgba(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def main(entree, sortie):
    Path(sortie).mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(entree).glob("sprite-*-essai.png")):
        nom = f.stem.removeprefix("sprite-").removesuffix("-essai")
        im = Image.open(f).convert("RGBA")
        for x, y, c in RETOUCHES.get(nom, []):
            im.putpixel((x, y), hex_rgba(c))
        im.save(Path(sortie) / f"sprite-{nom}.png")
        print(nom, len(RETOUCHES.get(nom, [])), "retouche(s)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
