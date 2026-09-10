#!/usr/bin/env python3
import os
from PIL import Image

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
os.makedirs(proof_dir, exist_ok=True)

races = ["rabbit", "lion", "fox", "boar"]
resample = getattr(Image, 'Resampling', Image).NEAREST

crops = {}
for r in races:
    src_path = os.path.join(proof_dir, f"{r}_battle_idle.png")
    if not os.path.exists(src_path):
        print(f"Missing {src_path}")
        continue
    img = Image.open(src_path).convert("RGB")
    # 角色在 1280x720 畫面上約在 x: 210~440, y: 230~460
    # 裁切出角色主體及武器區域
    cropped = img.crop((210, 230, 440, 460))
    # 放大 3 倍，呈現清晰金屬質感細節
    zoomed = cropped.resize((cropped.width * 3, cropped.height * 3), resample)
    out_path = os.path.join(proof_dir, f"{r}_metal_proof_crop.png")
    zoomed.save(out_path)
    crops[r] = out_path
    print(f"[{r}] Saved metal proof crop: {out_path} ({zoomed.size})")

print("All crops generated successfully!")
