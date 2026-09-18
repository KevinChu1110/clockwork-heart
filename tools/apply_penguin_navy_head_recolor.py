#!/usr/bin/env python3
"""
tools/apply_penguin_navy_head_recolor.py
Sculpts and recolors penguin navy head plate following 0-ART28q to achieve L2 distance < 60.0
while preserving outlines, copper beak, brass goggles frame, cyan lens, and high color count.
"""

import numpy as np
from PIL import Image

REPO = "/opt/side/bravesoul-game"
src_p = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock_512.png"
dst_p = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock_512.png"
alias_p = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_navy_512.png"
alias_128_p = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_navy.png"
stock_128_p = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock.png"

im = Image.open(src_p).convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
rgb = arr[:, :, :3].astype(float)

# Protection masks
is_outline = (alpha > 50) & (np.max(rgb, axis=2) <= 50)
is_brass = (alpha > 50) & (rgb[:, :, 0] > 140) & (rgb[:, :, 1] > 80) & (rgb[:, :, 2] < 110)
is_lens = (alpha > 50) & (rgb[:, :, 1] > 120) & (rgb[:, :, 2] > 140) & (rgb[:, :, 0] < 120)
is_strap = (alpha > 50) & (rgb[:, :, 0] > 70) & (rgb[:, :, 0] < 150) & (rgb[:, :, 1] > 40) & (rgb[:, :, 1] < 90) & (rgb[:, :, 2] < 60)

is_plate = (alpha > 200) & (~is_outline) & (~is_brass) & (~is_lens) & (~is_strap)

# Apply harmonic plate tinting matching chassis navy
# Plate gain (30, 35, 55)
new_rgb = rgb.copy()
new_rgb[is_plate, 0] = np.clip(new_rgb[is_plate, 0] + 30.0, 0, 255)
new_rgb[is_plate, 1] = np.clip(new_rgb[is_plate, 1] + 35.0, 0, 255)
new_rgb[is_plate, 2] = np.clip(new_rgb[is_plate, 2] + 55.0, 0, 255)

out_arr = np.dstack([new_rgb.astype(np.uint8), alpha])
out_im = Image.fromarray(out_arr, "RGBA")

out_im.save(dst_p)
out_im.save(alias_p)
print(f"Saved 512: {dst_p}")
print(f"Saved 512 alias: {alias_p}")

out_128 = out_im.resize((128, 128), resample=Image.Resampling.LANCZOS)
out_128.save(alias_128_p)
out_128.save(stock_128_p)
print(f"Saved 128: {stock_128_p}")
print(f"Saved 128 alias: {alias_128_p}")
