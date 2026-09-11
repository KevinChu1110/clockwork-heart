#!/usr/bin/env python3
import os
from PIL import Image

src_path = "/opt/side/bravesoul-game/screenshots/proof_battle_hud_hotbar.png"
if not os.path.exists(src_path):
    print("File not found:", src_path)
    exit(1)

im = Image.open(src_path)
w, h = im.size
print(f"Loaded image {src_path}: {w}x{h}")

os.makedirs("/tmp/hud_crops", exist_ok=True)

# 1. PlayerRageLabel area (left top)
# SideBars offset_left=28, offset_top=16. PlayerSide has title, name, hp, hp_bar, rage_label, rage_bar
# Around x: 20~250, y: 10~150
crop_rage = im.crop((20, 10, 320, 150))
crop_rage.save("/tmp/hud_crops/crop_rage.png")

# 2. PlayerTag & EnemyTag (Arena heads)
# Arena is between y: 80 and 510. PlayerSlot is around x: 250~550, EnemySlot around x: 730~1030
# Top of slots has PlayerTag and EnemyTag
crop_playertag = im.crop((280, 80, 560, 200))
crop_playertag.save("/tmp/hud_crops/crop_playertag.png")

crop_enemytag = im.crop((720, 80, 1000, 200))
crop_enemytag.save("/tmp/hud_crops/crop_enemytag.png")

# 3. LogPanel top edge
# LogPanel is at bottom: anchor_top=1.0, offset_top=-188, offset_bottom=-52 -> y: 532 to 668.
# Top edge of LogPanel is around y: 525~580, x: 20~1260
crop_log_top = im.crop((20, 520, 800, 610))
crop_log_top.save("/tmp/hud_crops/crop_log_top.png")

print("Saved crops to /tmp/hud_crops/")
