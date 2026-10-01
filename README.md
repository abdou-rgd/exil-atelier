# L'atelier de l'Exil

Les outils qui fabriquent le jeu, à côté du jeu. Le dépôt du jeu (`abdou-rgd/exil`) ne reçoit que les fichiers finis.

Un dossier par outil :

| Dossier | Rôle | État |
|---|---|---|
| `images/` | Sprites, bestiaire, décors et cosmétiques, générés en local sur le PC fixe (ComfyUI, RTX 3060 12 Go) | En cours |

## Règles

- **Rien de lourd dans git** : ni poids de modèles, ni images brutes. Seuls les essais triés sont gardés.
- **Les références tirées d'œuvres existantes restent hors de git** (`images/references/`).
- **Un asset part dans le jeu** quand il est validé par Abdallah, sur une vraie grille de pixels, avec la palette du jeu et un fond transparent. Nom : `categorie-nom-variante.png`.
- Direction artistique : décision 11 de `docs/passation.md` dans le dépôt du jeu (Grimgar pour les décors et la palette, Shadow Slave pour les sujets et la nuit).

## images/

| Fichier | Rôle |
|---|---|
| `generer.py` | Envoie un prompt à ComfyUI et récupère les images brutes |
| `pixeliser.py` | Ramène une image sur une vraie grille de pixels (fond transparent, palette limitée) |
| `retouches/retouches.py` | Pose les détails d'un pixel que le modèle ne sait pas dessiner |
| `prompts/` | Gabarits de prompts : un style commun, un sujet par entrée |
| `workflows/` | Workflows ComfyUI (JSON), pour refaire une image à l'identique |
| `lora/` | Jeu d'entraînement et commande du module de style |
| `references/` | Images de référence, hors de git |
| `essais/` | Essais triés et datés |
| `JOURNAL.md` | Installation du PC fixe, pièges, ce qui a été essayé et ce qu'on en a appris |
