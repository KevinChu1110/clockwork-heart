#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"

comp = Image.open("/tmp/boar_proof_harness.png").convert("RGBA")
crop = comp.crop((200, 280, 260, 340))
crop.save("/tmp/chest_glitch_zoom.png")
print("Saved /tmp/chest_glitch_zoom.png")

# 分別檢查 body 和 costume 在這個區域的像素
body = Image.open(f"{PARTS_DIR}/body/paint_brass_gold.png").convert("RGBA")
b_crop = body.crop((200, 280, 260, 340))
b_crop.save("/tmp/body_crop_glitch.png")

costume = Image.open(f"{PARTS_DIR}/costume/costume_viking_harness.png").convert("RGBA")
# costume 在 512 的掛載位置：navel=[256, 340], origin=[72, 80] -> pos = (256-72, 340-80) = (184, 260)
# 裁出對應 (200, 280, 260, 340) 的 costume 區域：(200-184, 280-260, 260-184, 340-260) = (16, 20, 76, 80)
c_crop = costume.crop((16, 20, 76, 80))
c_crop.save("/tmp/costume_crop_glitch.png")
