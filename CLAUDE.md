# L'atelier de l'Exil : consignes pour Claude

Ce dépôt contient les outils qui fabriquent le jeu L'Exil (dépôt du jeu : `C:\Users\abdou\Lexile`, github.com/abdou-rgd/exil). Lire d'abord, à chaque session :

1. `images/JOURNAL.md` : état de la chaîne d'images, pièges, ce qui a été essayé.
2. Dans le dépôt du jeu, `docs/passation.md` : la décision 11 (direction artistique) et la section « Travailler avec Abdallah ».
3. Dans le dépôt du jeu, `docs/lore/classes-et-bestiaire-propositions.md` : chaque sprite doit obéir à la loi physique de sa classe (Calidus ne crée pas de flamme).

## Travailler avec Abdallah

- En français, tutoiement. Il ne connaît ni JavaScript ni Python : expliquer chaque choix technique en une ou deux phrases simples.
- Une question à la fois, avec des options et une recommandation.
- Les choix de goût (quelle image garder, quelles références) lui reviennent. Montrer des planches, ne pas choisir à sa place.
- Fichiers à supprimer : à la corbeille.
- Sous-agents : `sonnet` ou `opus`, jamais Fable par défaut ; prévenir avant d'en lancer plus de deux.

## Le PC fixe

- `desktop-ka3ttnm`, Tailscale `100.102.251.71`, SSH avec `~/.ssh/id_ed25519_pcfixe` (passer par l'adresse IP). RTX 3060 12 Go.
- ComfyUI : `C:\Users\abdou\ComfyUI` (venv, port 8188). Le démarrer par SSH en arrière-plan, l'arrêter à la fin (`taskkill` sur les deux processus `python main.py`).
- `pip` échoue (WinError 448) sans `set PATH=C:\Windows\System32;C:\Windows;C:\Program Files\Git\cmd`.
- **Le garde-fou de Claude Code refuse d'installer du code externe sur le PC fixe** (git clone, pip install d'un outil), même avec l'accord d'Abdallah dans la conversation. Ne pas le contourner : lui donner les commandes à lancer lui-même, ou lui proposer d'ajouter une règle de permission. Les téléchargements de poids (`.safetensors`) passent avec son accord explicite.
- Abdallah demande parfois d'éteindre les PC en fin de session : le fixe d'abord (`shutdown /s /t 60`), le portable ensuite.

## Règles de l'atelier

- Rien de lourd dans git : ni poids, ni images brutes. Les références tirées de Grimgar et de Shadow Slave restent hors de git (`images/references/`).
- Jamais le nom d'une œuvre dans un prompt. Dans le jeu : ni leurs images, ni leurs personnages reconnaissables, ni leurs noms.
- Les noms latins des classes ne se traduisent jamais dans une image ni dans le jeu.
- Un asset ne part dans le dépôt du jeu qu'une fois validé par Abdallah : vraie grille de pixels, palette du jeu, fond transparent, nom `categorie-nom-variante.png`.
- Tenir `images/JOURNAL.md` à jour à chaque session, et enregistrer tout workflow qui a donné un bon résultat dans `images/workflows/`.
- Commits conventionnels en français (`feat:`, `fix:`, `docs:`, `chore:`).
