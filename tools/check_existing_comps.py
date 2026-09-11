import os
import sys
from PIL import Image

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.cc_helper import get_connected_components

for p in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/{p}.png")
    comps = get_connected_components(im, alpha_thresh=40, y_max=118)
    print(f"{p:10s}: comps={len(comps)}, sizes={[len(c) for c in comps]}")
