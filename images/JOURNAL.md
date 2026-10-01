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

## 1er octobre, matin : dépôt atelier, direction révisée, pose commune

**Direction (décision 11 révisée, voir la passation du jeu).** Grimgar pour les décors, la lumière et la palette ; Shadow Slave pour les sujets, le bestiaire, les boss et la nuit ; les personnages font le pont. Constat : le pastel de Grimgar vit dans ses décors à l'aquarelle, pas dans ses personnages ; un sprite de 60 px ne peut le porter que par la palette. Les images des deux œuvres peuvent servir de références de travail (hors de git).

**Sur le PC fixe.** Les scripts vivent maintenant dans `C:\Users\abdou\exil-atelier\images` (copie par scp, pas un clone git : le PC fixe n'a pas d'accès au dépôt privé). L'ancien dossier `C:\Users\abdou\exil-essais` contient les lots de la nuit.

**Poids ajoutés** (accord d'Abdallah) dans `ComfyUI\models` :
- `controlnet\controlnet-union-sdxl-promax.safetensors` (xinsir/controlnet-union-sdxl-1.0) ;
- `ipadapter\ip-adapter-plus_sdxl_vit-h.safetensors` et `clip_vision\CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` (h94/IP-Adapter).

**ControlNet : marche, sans rien installer** (nœuds natifs de ComfyUI). `gabarit.py` dessine un squelette de pose au format OpenPose ; `generer.py --pose gabarit-debout.png` y pose le personnage (force 0,7, jusqu'à 70 % des étapes). `lot.py` produit un lot complet et sa planche. Résultat : `essais/2026-10-01-pose/planche.png`, 18 sprites de même posture, même taille, même cadrage. C'est la base des calques de cosmétiques.

**Bloqué par le garde-fou** (code externe, même avec l'accord d'Abdallah ; il doit lancer les commandes lui-même sur le PC fixe ou ajouter une règle de permission) :
1. IP-Adapter : les nœuds `ComfyUI_IPAdapter_plus` (github.com/cubiq/ComfyUI_IPAdapter_plus) à cloner dans `ComfyUI\custom_nodes`. Les poids sont déjà là.
2. LoRA : `kohya-ss/sd-scripts` dans `C:\Users\abdou\sd-scripts` avec son venv (torch cu128, requirements, bitsandbytes). Jeu d'entraînement et commande prêts (`lora/`).
3. Mitsuba (essai borné voulu par Abdallah) : fork `PrismML-Eng/llama.cpp`, branche `prism`, à compiler (cmake, compilateur C++, CUDA) ; fichiers `Mitsuba-ComfyUI-27B-v1.18-PQ2_0.gguf` (7,3 Go) et `mmproj-Q8_0.gguf` sur huggingface.co/isichan-ai/Mitsuba-ComfyUI-27B-GGUF ; `--reasoning off`, température 0,6. Annoncé pour 16 Go : à décharger avant chaque génération sur la 3060.

**Suite prévue, dans l'ordre.**
1. Abdallah dépose ses références dans `references/grimgar` et `references/shadow-slave`.
2. Planche de référence du mélange : un décor de jour, un décor de nuit, un personnage, une créature. À valider avant toute série.
3. IP-Adapter avec ces références, puis comparaison de deux ou trois modèles de base (SDXL de base suit mal les prompts).
4. Essai borné de Mitsuba : la même référence décrite par Mitsuba et par Claude, générations côte à côte.
5. LoRA quand 15 à 20 sprites sont retouchés et validés.
6. Retouches à refaire sur les sprites à pose commune (les coordonnées de `retouches.py` valent pour le lot de la nuit).
