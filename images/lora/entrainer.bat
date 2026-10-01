@echo off
rem Entraîne le LoRA « exilstyle » sur la RTX 3060 (12 Go), environ 1 h 30 à 2 h.
rem Prérequis : kohya-ss/sd-scripts installé dans C:\Users\abdou\sd-scripts (venv),
rem jeu d'entraînement créé par preparer-donnees.py dans C:\Users\abdou\exil-lora\donnees.
rem Le résultat arrive directement dans les LoRA de ComfyUI.
set PATH=C:\Windows\System32;C:\Windows
cd /d C:\Users\abdou\sd-scripts
venv\Scripts\python sdxl_train_network.py ^
  --pretrained_model_name_or_path C:\Users\abdou\ComfyUI\models\checkpoints\sd_xl_base_1.0.safetensors ^
  --train_data_dir C:\Users\abdou\exil-lora\donnees ^
  --output_dir C:\Users\abdou\ComfyUI\models\loras ^
  --output_name exilstyle-v1 ^
  --caption_extension .txt ^
  --resolution 1024,1024 --enable_bucket --bucket_no_upscale ^
  --network_module networks.lora --network_dim 16 --network_alpha 8 ^
  --network_train_unet_only ^
  --learning_rate 1e-4 --optimizer_type AdamW8bit --lr_scheduler cosine ^
  --train_batch_size 1 --max_train_epochs 10 --save_every_n_epochs 2 ^
  --mixed_precision bf16 --save_precision fp16 ^
  --gradient_checkpointing --cache_latents --cache_text_encoder_outputs ^
  --sdpa --seed 42 ^
  --logging_dir C:\Users\abdou\exil-lora\journaux
