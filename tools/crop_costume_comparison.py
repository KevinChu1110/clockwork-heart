#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

im = Image.open(f"{BOAR_DIR}/proof_boar_costume_comparison.png").convert("RGBA")
# 總寬 472，高 205
# 三個面板：
# 面板 1 (Bare): x: 0..155
# 面板 2 (Harness): x: 155..315
# 面板 3 (Ironclad): x: 315..472

p1 = im.crop((10, 20, 150, 195))
p2 = im.crop((165, 20, 305, 195))
p3 = im.crop((320, 20, 460, 195))

p1.save("/tmp/costume_comp_bare.png")
p2.save("/tmp/costume_comp_harness.png")
p3.save("/tmp/costume_comp_ironclad.png")
print("Saved comparison panels to /tmp/")
