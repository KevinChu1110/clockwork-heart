#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_hud_hotbar.png")
# Full LogPanel is at x: 28~1252, y: 532~668.
# LogPanel top edge crop: x: 25~850, y: 520~620
crop_log_top = im.crop((25, 520, 850, 620))
crop_log_top.save("/opt/side/bravesoul-game/screenshots/proof_battle_crop_log_top.png")
crop_log_top.save("/opt/side/bravesoul-game/proofs/battle_hud_contrast/proof_battle_crop_log_top.png")
print("Saved clean crop_log_top.")
