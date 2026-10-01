"""Génère un lot : chaque sujet d'un fichier de prompts, plusieurs graines, puis planche.

Usage : python lot.py prompts/classes.json essais/nom-du-lot --graines 1 2 3 [--pose gabarit.png]
Sorties : <dossier>/brut (images du modèle), <dossier>/grille (sprites), <dossier>/planche.png
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from generer import generer
from pixeliser import pixeliser

p = argparse.ArgumentParser()
p.add_argument("prompts")
p.add_argument("dossier")
p.add_argument("--graines", type=int, nargs="+", default=[1, 2, 3, 4])
p.add_argument("--pose")
p.add_argument("--pose-force", type=float, default=0.7)
p.add_argument("--hauteur", type=int, default=60)
p.add_argument("--couleurs", type=int, default=16)
a = p.parse_args()

sujets = json.load(open(a.prompts, encoding="utf-8"))
style = sujets.pop("_style")
base = Path(a.dossier)
(base / "brut").mkdir(parents=True, exist_ok=True)
(base / "grille").mkdir(exist_ok=True)
zoom, cl, lh, m = 4, 200, a.hauteur * 4 + 30, 20
planche = Image.new("RGBA", (m + cl * len(a.graines), m + lh * len(sujets)), (234, 223, 197, 255))
d = ImageDraw.Draw(planche)
for i, (nom, desc) in enumerate(sujets.items()):
    for j, g in enumerate(a.graines):
        brut = base / "brut" / f"{nom}-{g}.png"
        if not brut.exists():
            brut.write_bytes(generer(f"{style}, {desc}", g, 832, 1216, 1.0, a.pose, a.pose_force))
        px = pixeliser(Image.open(brut), a.hauteur, a.couleurs, tolerance=60)
        px.save(base / "grille" / f"{nom}-{g}.png")
        x, y = m + j * cl, m + i * lh
        planche.alpha_composite(px.resize((px.width * zoom, px.height * zoom), Image.Resampling.NEAREST), (x, y + 14))
        d.text((x, y), f"{nom} {g}", fill=(47, 42, 44, 255))
        print(nom, g, flush=True)
planche.save(base / "planche.png")
print("fini")
