#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

for paint in ["paint_brass_gold", "paint_ivory_stock", "paint_molten_crimson"]:
    p = f"{BOAR_DIR}/chassis/{paint}_512.png"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    # 檢查 (199..261, 275..337) 區域
    sub = arr[275:338, 199:262]
    # 檢查是否有 cyan (R<100, G>150, B>150)
    cyan_cnt = np.sum((sub[:, :, 0] < 100) & (sub[:, :, 1] > 150) & (sub[:, :, 2] > 150) & (sub[:, :, 3] > 50))
    print(f"{paint}: bbox={im.getbbox()}, cyan core px in (199..261, 275..337): {cyan_cnt}")
