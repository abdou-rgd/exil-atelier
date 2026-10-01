"""Prépare le jeu d'entraînement du LoRA « exilstyle » (format kohya sd-scripts).

Chaque sprite de 60 px de haut est agrandi par un facteur entier (sans lissage)
et posé sur un fond gris uni, avec une légende .txt à côté.
Usage : python preparer-donnees.py <dossier_sortie> sprite.png=classe ...
Le dossier créé s'appelle <sortie>/10_exilstyle (10 répétitions par époque).
"""
import sys
from pathlib import Path

from PIL import Image

DESCRIPTIONS = {
    "mare-luna": "young woman in a mist-blue hooded cloak",
    "calidus": "young smith with a leather apron and bare forearms",
    "vectis": "young woman with a long wooden pole, wool beanie and green scarf",
    "inertia": "broad-shouldered young man in a heavy dark cloak",
    "tenax": "young woman with a coiled rope across her chest",
    "specula": "young woman with a wide-brimmed purple hat and a long coat",
}
FOND = (143, 138, 134, 255)
TOILE = (640, 1024)


def main(sortie, *paires):
    dossier = Path(sortie) / "10_exilstyle"
    dossier.mkdir(parents=True, exist_ok=True)
    for i, paire in enumerate(paires):
        chemin, classe = paire.split("=")
        px = Image.open(chemin).convert("RGBA")
        z = min(TOILE[0] // px.width, TOILE[1] // px.height)
        grand = px.resize((px.width * z, px.height * z), Image.Resampling.NEAREST)
        toile = Image.new("RGBA", TOILE, FOND)
        toile.alpha_composite(grand, ((TOILE[0] - grand.width) // 2, (TOILE[1] - grand.height) // 2))
        nom = f"{i:02d}-{classe}"
        toile.convert("RGB").save(dossier / f"{nom}.png")
        (dossier / f"{nom}.txt").write_text(
            f"exilstyle, pixel art, full body game sprite, {DESCRIPTIONS[classe]}, plain grey background",
            encoding="utf-8")
    print(len(paires), "images dans", dossier)


if __name__ == "__main__":
    main(*sys.argv[1:])
