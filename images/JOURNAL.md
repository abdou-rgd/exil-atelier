# IA d'image locale sur le PC fixe

*Mis en place dans la nuit du 30 septembre 2026.*

## Machine

PC fixe `desktop-ka3ttnm`, joignable par Tailscale (`100.102.251.71`) et SSH (clé `~/.ssh/id_ed25519_pcfixe`). RTX 3060 12 Go, 32 Go de mémoire, Python 3.12, Git. Piège : `pip` échoue (WinError 448) à cause d'un dossier du PATH ; lancer les installations avec `set PATH=C:\Windows\System32;C:\Windows;C:\Program Files\Git\cmd`.

## Installé

- ComfyUI dans `C:\Users\abdou\ComfyUI`, environnement `venv` avec PyTorch 2.11 (CUDA 12.8) : la carte est bien vue.
- Pillow dans le même environnement.
- **Manque : les poids du modèle.** Le téléchargement a été bloqué par le garde-fou de sécurité de Claude Code (code externe). À faire par Abdallah ou avec son accord explicite :
  - `models\checkpoints\sd_xl_base_1.0.safetensors` (huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) ;
  - `models\loras\pixel-art-xl.safetensors` (huggingface.co/nerijs/pixel-art-xl).

## Chaîne de travail

1. `generer.py` : envoie un prompt à ComfyUI (SDXL + LoRA pixel art) et récupère les images brutes. **Pas encore testé**, faute de modèle.
2. `pixeliser.py` : fond rendu transparent, recadrage, réduction sur une vraie grille, palette limitée (N couleurs ou palette imposée). **Testé** sur la planche des six classes.
3. Retouche à la main (Aseprite ou LibreSprite) : visages, nettoyage, frames d'animation.
4. Plus tard : entraîner un LoRA sur 15 à 20 sprites validés, pour un style propre à l'Exil.

Essais dans `C:\Users\abdou\exil-essais` sur le PC fixe.

## Premier essai : taille de grille

`essais/comparaison-grilles.png` : les six personnages de la planche d'Abdallah réduits à 20, 40 et 60 pixels de haut.

- **20 de haut** (la grille des anciens sprites, 16 × 20) : illisible par réduction automatique. Cette taille se dessine pixel par pixel, pas depuis une image.
- **40 de haut** : silhouettes et objets lisibles, visages perdus.
- **60 de haut** : personnages reconnaissables, visages à retoucher.

Remarque : la réduction brute garde les mains en feu de Calidus, qu'il faudra retirer (voir plus bas).

## Nuit du 1er octobre : premiers sprites des six classes

Modèle installé (feu vert d'Abdallah), chaîne testée de bout en bout : environ 20 s par image sur la 3060. Prompts dans `prompts/classes.json` ; résultats dans `essais/2026-10-01-classes/` (`selection-classes.png`, un sprite par classe à 60 px de haut, et `toutes-les-variantes.png`).

- **Style Grimgar, tiré de ses illustrations** : proportions réalistes et élancées (pas de chibi), équipement usé et pratique, couleurs désaturées, visages ordinaires et fatigués. Le nom de l'œuvre n'est jamais mis dans les prompts.
- **Ce qui marche** : l'ambiance, les silhouettes, et les objets clés une fois appuyés par une pondération `(objet:1.3)` à `1.5`.
- **Limites** : à `1.5`, la couleur de l'objet déborde sur tout le personnage (Calidus tout rouge) ; les petits détails (barre rougeoyante, perle, cheveux qui flottent, lunettes) ne sortent pas. Le sujet reste souvent de face et trop long pour la grille. Le détourage échoue quand le modèle ajoute un halo clair (Inertia 505).
- **Retouches à faire** : les deux pixels orange aux mains de Calidus, la perle de Mare & Luna, les visages. À faire à la main, ou par un script qui pose des calques sur la grille.
- **Pistes** : un modèle SDXL affiné pour le pixel art, un LoRA entraîné sur nos sprites validés, et une image de référence (IP-Adapter) pour garder le même visage d'une pose à l'autre.

## Calidus, premier prompt (avant les essais)

Sa loi : il déplace sa propre chaleur par contact, il ne crée pas de flamme. Prompt prévu :

> pixel art, full body game sprite of a young smith-wanderer, plain light background, holding a single red-hot iron bar in his bare hand, the only glowing object, pale skin, wool blanket over his shoulders, visible breath mist, small scar on forearm, worn leather apron, muted pastel palette, no fire, no flames

## Module de style (LoRA « exilstyle »)

- Jeu d'entraînement prêt sur le PC fixe : `C:\Users\abdou\exil-lora\donnees\10_exilstyle` (20 sprites : les 6 retouchés et 14 bonnes variantes, légendés avec le mot-clé `exilstyle`). Script : `lora/preparer-donnees.py`.
- Commande d'entraînement prête : `lora/entrainer.bat` (à copier sur le PC fixe), environ 1 h 30 à 2 h.
- **Bloqué** : l'installation de l'outil d'entraînement (github.com/kohya-ss/sd-scripts, avec ses dépendances Python) a été refusée par le garde-fou de sécurité, qui demande un accord explicite pour ce code externe.
- Premier essai à prendre comme tel : les images d'entraînement sont elles-mêmes générées, avec leurs défauts (visages flous). Le vrai module viendra quand 15 à 20 sprites auront été retouchés et validés.
