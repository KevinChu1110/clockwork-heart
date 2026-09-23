#!/usr/bin/env python3
"""
generate_elephant_wardrobe_crops.py
Crops the stage preview character from the wardrobe screenshots for visual inspection.
"""

from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PROOFS_DIR = f"{REPO_ROOT}/proofs/wardrobe_elephant"

def crop_stage(in_fn: str, out_fn: str):
    p = f"{PROOFS_DIR}/{in_fn}"
    im = Image.open(p)
    # The character preview is located in the left area of the wardrobe dialog
    # Screen size is 1280x720. Dialog center is at (640, 360).
    # Character stage is roughly x: 260..580, y: 180..580
    crop = im.crop((270, 180, 570, 580))
    out_p = f"{PROOFS_DIR}/{out_fn}"
    crop.save(out_p)
    print(f"Saved crop: {out_p} ({crop.size})")

if __name__ == "__main__":
    crop_stage("proof_wardrobe_elephant_bastion.png", "proof_crop_wardrobe_elephant_bastion.png")
    crop_stage("proof_wardrobe_elephant_overalls.png", "proof_crop_wardrobe_elephant_overalls.png")
