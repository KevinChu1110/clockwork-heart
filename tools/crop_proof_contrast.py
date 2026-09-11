#!/usr/bin/env python3
import os
from PIL import Image

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shot_dir = os.path.join(root, "screenshots")
proof_dir = os.path.join(root, "proofs", "battle_hud_contrast")
os.makedirs(proof_dir, exist_ok=True)

src_path = os.path.join(shot_dir, "proof_battle_hud_hotbar.png")
im = Image.open(src_path)
w, h = im.size
print(f"Loaded {src_path}: {w}x{h}")

# 1. Left top PlayerRageLabel ("怒氣"):
# Around x: 25~160, y: 80~140
crop_rage = im.crop((25, 75, 200, 145))
crop_rage.save(os.path.join(shot_dir, "proof_battle_crop_rage.png"))
crop_rage.save(os.path.join(proof_dir, "proof_battle_crop_rage.png"))

# 2. Enemy head tag ("敵方"):
# Around x: 740~980, y: 150~270
crop_enemytag = im.crop((730, 145, 990, 270))
crop_enemytag.save(os.path.join(shot_dir, "proof_battle_crop_enemytag.png"))
crop_enemytag.save(os.path.join(proof_dir, "proof_battle_crop_enemytag.png"))

# Also Player tag ("我方"):
crop_playertag = im.crop((270, 145, 530, 270))
crop_playertag.save(os.path.join(shot_dir, "proof_battle_crop_playertag.png"))
crop_playertag.save(os.path.join(proof_dir, "proof_battle_crop_playertag.png"))

# 3. LogPanel top edge:
# LogPanel is at y: 532~668. Top edge with text lines is y: 525~615, x: 25~800
crop_log_top = im.crop((25, 525, 800, 615))
crop_log_top.save(os.path.join(shot_dir, "proof_battle_crop_log_top.png"))
crop_log_top.save(os.path.join(proof_dir, "proof_battle_crop_log_top.png"))

# 4. Full LogPanel:
crop_log_full = im.crop((25, 525, 800, 675))
crop_log_full.save(os.path.join(shot_dir, "proof_battle_crop_log_full.png"))
crop_log_full.save(os.path.join(proof_dir, "proof_battle_crop_log_full.png"))

print("Successfully cropped all proof images.")
