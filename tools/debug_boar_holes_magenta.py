#!/usr/bin/env python3
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)

# 標記空洞
# 在角色 bounding box 範圍內 (x: 80..440, y: 40..490) 尋找 alpha == 0 的像素
vis = arr.copy()
holes_mask = (vis[40:490, 80:440, 3] == 0)
print("Total internal hole pixels:", np.sum(holes_mask))

# 建立一張在深灰背景 (#202228) 上的合成圖，這樣能清晰看到任何縫隙！
bg = Image.new("RGBA", (512, 512), (32, 34, 42, 255))
bg.alpha_composite(im)
bg.save("/tmp/boar_on_dark_bg.png")
print("Saved /tmp/boar_on_dark_bg.png")
