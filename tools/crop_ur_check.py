#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Load composite
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
# Crop around upper right
crop_ur = comp.crop((300, 20, 460, 180))
crop_ur.save("/tmp/crop_ur.png")

# Also crop each layer in this region
layers = [
    ("body", (0, 0), "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png"),
    ("head", (130, 15), "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png"),
    ("key", (342, 60), "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png"),
]

for name, pos, path in layers:
    im = Image.open(path).convert("RGBA")
    full = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    full.paste(im, pos, im)
    cr = full.crop((300, 20, 460, 180))
    cr.save(f"/tmp/crop_ur_{name}.png")

print("Saved crop_ur and each layer crop")
