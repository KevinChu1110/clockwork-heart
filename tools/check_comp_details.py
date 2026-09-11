import os
import sys
from PIL import Image

sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.cc_helper import get_connected_components

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox/skill.png")
comps = get_connected_components(im, alpha_thresh=40, y_max=118)
for i, comp in enumerate(comps):
    min_x = min(x for x, y in comp)
    max_x = max(x for x, y in comp)
    min_y = min(y for x, y in comp)
    max_y = max(y for x, y in comp)
    print(f"Comp {i}: size={len(comp)}, bbox=({min_x}, {min_y}, {max_x}, {max_y})")
