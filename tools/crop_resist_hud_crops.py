from PIL import Image
import os

proof_dir = "/opt/side/bravesoul-game/proofs/resist-combat-hud"
crop_dir = os.path.join(proof_dir, "crops")
os.makedirs(crop_dir, exist_ok=True)

# 裁切 PlayerSide (x: 20~280, y: 10~180)
for fname in sorted(os.listdir(proof_dir)):
    if not fname.endswith(".png") or fname.startswith("crop_"):
        continue
    fpath = os.path.join(proof_dir, fname)
    im = Image.open(fpath)
    cropped = im.crop((20, 10, 280, 180))
    crop_name = f"crop_{fname}"
    cropped.save(os.path.join(crop_dir, crop_name))
    print(f"Saved crop: {crop_name}")
