#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
arr = np.array(im)

# Save an image where RGB is placed on white background
bg_white = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
bg_white.alpha_composite(im)
bg_white.save("/tmp/body_white.png")

# Also check composite on white background
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
comp_white = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
comp_white.alpha_composite(comp)
comp_white.save("/tmp/comp_white.png")

print("Saved /tmp/body_white.png and /tmp/comp_white.png")
