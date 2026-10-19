#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

comp128 = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")
# 裁出胸前區域：在 128 中是 (45, 60, 85, 95)
chest128 = comp128.crop((45, 60, 85, 95))
chest128.resize((160, 140), Image.Resampling.NEAREST).save("/tmp/comp128_chest.png")
print("Saved /tmp/comp128_chest.png")
