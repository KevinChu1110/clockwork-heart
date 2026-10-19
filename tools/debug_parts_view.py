#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

# 1. 檢查 key
k = Image.open(f"{PARTS_DIR}/winding_key/key_classic_brass.png").convert("RGBA")
k.save("/tmp/debug_key.png")

# 2. 檢查 harness
h = Image.open(f"{PARTS_DIR}/costume/costume_viking_harness.png").convert("RGBA")
h.save("/tmp/debug_harness.png")

# 3. 檢查 ironclad
i = Image.open(f"{PARTS_DIR}/costume/costume_viking_ironclad.png").convert("RGBA")
i.save("/tmp/debug_ironclad.png")

print("Saved debug_key.png, debug_harness.png, debug_ironclad.png to /tmp")
