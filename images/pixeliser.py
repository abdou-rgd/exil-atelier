"""Ramène une image « façon pixel art » sur une vraie grille de pixels.

Étapes : fond uni rendu transparent (remplissage depuis les bords),
recadrage sur le personnage, réduction par moyenne de zone à la hauteur
voulue, palette limitée à N couleurs, puis agrandissement entier sans
lissage pour l'aperçu.

Usage :
  python pixeliser.py entree.png sortie.png --hauteur 40 --couleurs 16 [--zoom 6]
  python pixeliser.py entree.png sortie.png --hauteur 40 --palette palette.txt
  (palette.txt : un hex par ligne, par exemple #2F2A2C)
"""
import argparse
from collections import deque

from PIL import Image


def fond_transparent(img, tolerance=40):
    """Rend transparent le fond uni relié aux bords de l'image."""
    img = img.convert("RGBA")
    l, h = img.size
    px = img.load()
    ref = px[0, 0]

    def proche(c):
        return sum(abs(c[i] - ref[i]) for i in range(3)) <= tolerance

    vus = set()
    file = deque((x, y) for x in range(l) for y in (0, h - 1))
    file.extend((x, y) for y in range(h) for x in (0, l - 1))
    while file:
        x, y = file.popleft()
        if (x, y) in vus or not (0 <= x < l and 0 <= y < h):
            continue
        vus.add((x, y))
        if not proche(px[x, y]):
            continue
        px[x, y] = (0, 0, 0, 0)
        file.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return img


def lire_palette(chemin):
    couleurs = []
    for ligne in open(chemin, encoding="utf-8"):
        ligne = ligne.strip().lstrip("#")
        if len(ligne) == 6:
            couleurs.append(tuple(int(ligne[i:i + 2], 16) for i in (0, 2, 4)))
    return couleurs


def reduire_couleurs(img, n=None, palette=None):
    """Quantifie les pixels opaques ; l'alpha devient tout ou rien."""
    alpha = img.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    rgb = img.convert("RGB")
    if palette:
        pal = Image.new("P", (1, 1))
        plat = [v for c in palette for v in c]
        pal.putpalette(plat + plat[:3] * (256 - len(palette)))
        q = rgb.quantize(palette=pal, dither=Image.Dither.NONE)
    else:
        q = rgb.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out = q.convert("RGBA")
    out.putalpha(alpha)
    return out


def pixeliser(img, hauteur, couleurs=16, palette=None, tolerance=40):
    img = fond_transparent(img, tolerance)
    boite = img.getchannel("A").getbbox()
    if boite:
        img = img.crop(boite)
    largeur = max(1, round(img.width * hauteur / img.height))
    petit = img.resize((largeur, hauteur), Image.Resampling.BOX)
    return reduire_couleurs(petit, couleurs, palette)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("entree")
    p.add_argument("sortie")
    p.add_argument("--hauteur", type=int, default=40)
    p.add_argument("--couleurs", type=int, default=16)
    p.add_argument("--palette")
    p.add_argument("--tolerance", type=int, default=40)
    p.add_argument("--zoom", type=int, default=1, help="agrandissement entier pour l'aperçu")
    a = p.parse_args()
    pal = lire_palette(a.palette) if a.palette else None
    out = pixeliser(Image.open(a.entree), a.hauteur, a.couleurs, pal, a.tolerance)
    if a.zoom > 1:
        out = out.resize((out.width * a.zoom, out.height * a.zoom), Image.Resampling.NEAREST)
    out.save(a.sortie)


if __name__ == "__main__":
    main()
