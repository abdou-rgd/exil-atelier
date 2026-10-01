"""Génère des images avec ComfyUI (SDXL + LoRA pixel art) par son API locale.

À lancer sur le PC fixe, ComfyUI démarré (python main.py, port 8188) :
  python generer.py --nom calidus --graines 1 2 3 4 --prompt "..."
Les images arrivent dans ./brut/<nom>-<graine>.png, prêtes pour pixeliser.py.
"""
import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "http://127.0.0.1:8188"
NEGATIF = ("blurry, soft, gradient, anti-aliasing, 3d render, photo, text, watermark, "
           "signature, multiple characters, cropped, frame, border")


def flux_de_travail(prompt, graine, largeur, hauteur, lora_force, pose=None, pose_force=0.7):
    flux = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "LoraLoader", "inputs": {
            "model": ["1", 0], "clip": ["1", 1], "lora_name": "pixel-art-xl.safetensors",
            "strength_model": lora_force, "strength_clip": lora_force}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": prompt}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": NEGATIF}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": largeur, "height": hauteur, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {
            "model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0], "latent_image": ["5", 0],
            "seed": graine, "steps": 30, "cfg": 6.0, "sampler_name": "dpmpp_2m",
            "scheduler": "karras", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": "exil"}},
    }
    if pose:  # image de squelette déjà déposée dans ComfyUI/input
        flux["10"] = {"class_type": "ControlNetLoader", "inputs": {"control_net_name": "controlnet-union-sdxl-promax.safetensors"}}
        flux["11"] = {"class_type": "SetUnionControlNetType", "inputs": {"control_net": ["10", 0], "type": "openpose"}}
        flux["12"] = {"class_type": "LoadImage", "inputs": {"image": pose}}
        flux["13"] = {"class_type": "ControlNetApplyAdvanced", "inputs": {
            "positive": ["3", 0], "negative": ["4", 0], "control_net": ["11", 0], "image": ["12", 0],
            "strength": pose_force, "start_percent": 0.0, "end_percent": 0.7, "vae": ["1", 2]}}
        flux["6"]["inputs"]["positive"] = ["13", 0]
        flux["6"]["inputs"]["negative"] = ["13", 1]
    return flux


def appel(chemin, donnees=None):
    req = urllib.request.Request(API + chemin, data=json.dumps(donnees).encode() if donnees else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return r.read()


def generer(prompt, graine, largeur, hauteur, lora_force, pose=None, pose_force=0.7):
    flux = flux_de_travail(prompt, graine, largeur, hauteur, lora_force, pose, pose_force)
    id_ = json.loads(appel("/prompt", {"prompt": flux}))["prompt_id"]
    while True:
        hist = json.loads(appel(f"/history/{id_}"))
        if id_ in hist:
            break
        time.sleep(1)
    img = hist[id_]["outputs"]["8"]["images"][0]
    return appel("/view?" + urllib.parse.urlencode(img))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nom", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--graines", type=int, nargs="+", default=[1, 2, 3, 4])
    p.add_argument("--largeur", type=int, default=832)
    p.add_argument("--hauteur", type=int, default=1216)
    p.add_argument("--lora", type=float, default=1.0)
    p.add_argument("--pose", help="nom d'une image de squelette dans ComfyUI/input (voir gabarit.py)")
    p.add_argument("--pose-force", type=float, default=0.7)
    a = p.parse_args()
    Path("brut").mkdir(exist_ok=True)
    for g in a.graines:
        Path(f"brut/{a.nom}-{g}.png").write_bytes(generer(a.prompt, g, a.largeur, a.hauteur, a.lora, a.pose, a.pose_force))
        print(f"brut/{a.nom}-{g}.png")


if __name__ == "__main__":
    main()
