"""Dessine le squelette de pose commun à tous les personnages (format OpenPose).

ControlNet lit ce squelette et place le personnage dessus : même pose, même
taille, même cadrage pour toutes les classes, ce qui rend les calques de
cosmétiques possibles.
Usage : python gabarit.py sortie.png
"""
import sys

from PIL import Image, ImageDraw

TOILE = (832, 1216)
# Ordre OpenPose : nez, cou, épaule D, coude D, poignet D, épaule G, coude G, poignet G,
# hanche D, genou D, cheville D, hanche G, genou G, cheville G, œil D, œil G, oreille D, oreille G.
POINTS = [
    (416, 180), (416, 290), (321, 295), (300, 470), (285, 640), (511, 295), (532, 470), (547, 640),
    (365, 650), (362, 880), (360, 1100), (467, 650), (470, 880), (472, 1100),
    (396, 160), (436, 160), (372, 172), (460, 172),
]
MEMBRES = [(2, 3), (2, 6), (3, 4), (4, 5), (6, 7), (7, 8), (2, 9), (9, 10), (10, 11), (2, 12),
           (12, 13), (13, 14), (2, 1), (1, 15), (15, 17), (1, 16), (16, 18)]
COULEURS = [(255, 0, 0), (255, 85, 0), (255, 170, 0), (255, 255, 0), (170, 255, 0), (85, 255, 0),
            (0, 255, 0), (0, 255, 85), (0, 255, 170), (0, 255, 255), (0, 170, 255), (0, 85, 255),
            (0, 0, 255), (85, 0, 255), (170, 0, 255), (255, 0, 255), (255, 0, 170), (255, 0, 85)]


def dessiner():
    img = Image.new("RGB", TOILE, (0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (a, b) in enumerate(MEMBRES):
        c = tuple(int(v * 0.6) for v in COULEURS[i])
        d.line([POINTS[a - 1], POINTS[b - 1]], fill=c, width=10)
    for i, (x, y) in enumerate(POINTS):
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=COULEURS[i])
    return img


if __name__ == "__main__":
    dessiner().save(sys.argv[1])
