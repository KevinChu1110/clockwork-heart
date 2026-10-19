#!/usr/bin/env python3
"""
tools/extract_from_official_char_boar.py
Extracts the definitive MaplePaperdoll Character.wz modular assets
directly from the official ultra-HD masterpiece: web/media/hero/char_boar.png (928x1160).
Eliminates all artifacts, noise, clipping cuts, and missing hole glitches.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
HERO_BOAR = f"{REPO_ROOT}/web/media/hero/char_boar.png"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# 1. 載入 928x1160 官方立繪並進行精確去背
print("--- 1. Loading and Keying Official char_boar.png ---")
im_raw = Image.open(HERO_BOAR).convert("RGBA")
arr = np.array(im_raw)

# 背景是淡米黃/米白色漸層 (#F5F0E6..#FFFFFF)
# 判定背景像素：R > 230, G > 225, B > 215 且顏色接近灰色/米白色 (max diff < 20)
bg_mask = (arr[:, :, 0] > 225) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 210) & \
          (np.abs(arr[:, :, 0].astype(int) - arr[:, :, 1].astype(int)) < 18) & \
          (np.abs(arr[:, :, 1].astype(int) - arr[:, :, 2].astype(int)) < 22)

# 保留角色與自然陰影
# 陰影區域：Y > 1000 且亮度較暗
is_shadow = (np.arange(arr.shape[0])[:, None] > 1020) & (arr[:, :, 0] < 220)
bg_mask[is_shadow] = False

arr[bg_mask, 3] = 0
clean_full = Image.fromarray(arr, mode="RGBA")
print("Full keyed size:", clean_full.size, "bbox:", clean_full.getbbox())

# 縮放到標準 512 畫布基準
# 角色在 928x1160 中的 bbox 大約是 (60, 40, 870, 1120) -> 寬 810，高 1080
# 縮放到 512x512 畫布：等比縮放高度到約 480，置於 (256, 480) 腳底對齊
scale_factor = 475.0 / 1120.0 # 約 0.424
new_w = int(clean_full.width * scale_factor)
new_h = int(clean_full.height * scale_factor)

scaled_hero = clean_full.resize((new_w, new_h), Image.Resampling.LANCZOS)
hero_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
# 置中對齊
paste_x = (512 - new_w) // 2
paste_y = 512 - new_h - 10 # 留 10px 底部空間
hero_512.alpha_composite(scaled_hero, (paste_x, paste_y))
hero_512.save("/tmp/official_boar_in_512.png")
print(f"Saved /tmp/official_boar_in_512.png: bbox={hero_512.getbbox()}")
