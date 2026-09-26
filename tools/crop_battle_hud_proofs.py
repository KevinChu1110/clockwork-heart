from PIL import Image
import os

out_dir = "/opt/side/bravesoul-game/.worktrees/t_07c57dfd/proofs/battle_en_hud_overflow"
crops_dir = os.path.join(out_dir, "crops")
os.makedirs(crops_dir, exist_ok=True)

# 1. EN Crop of Top HUD (y=0 to y=180, full width 1280)
im_en = Image.open(os.path.join(out_dir, "proof_02_battle_broken_en.png"))
top_en = im_en.crop((0, 0, 1280, 180))
top_en.save(os.path.join(crops_dir, "crop_top_hud_en.png"))

# 2. zh_TW Crop of Top HUD
im_tw = Image.open(os.path.join(out_dir, "proof_01_battle_broken_zh_TW.png"))
top_tw = im_tw.crop((0, 0, 1280, 180))
top_tw.save(os.path.join(crops_dir, "crop_top_hud_zh_TW.png"))

# 3. es Crop of Top HUD
im_es = Image.open(os.path.join(out_dir, "proof_03_battle_broken_es.png"))
top_es = im_es.crop((0, 0, 1280, 180))
top_es.save(os.path.join(crops_dir, "crop_top_hud_es.png"))

print("Crops generated successfully in", crops_dir)
