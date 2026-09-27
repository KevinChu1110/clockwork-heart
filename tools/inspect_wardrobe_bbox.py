#!/usr/bin/env python3
import numpy as np
from PIL import Image

img = Image.open("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_wardrobe_hedgehog.png").convert("RGBA")
arr = np.array(img)

# Wardrobe character is on the left preview area
# Let's find all non-cream-background pixels in x: 50..650, y: 100..650
# Background in wardrobe preview is around cream color (#FFF8E7 or similar)
# Let's find pixels where alpha > 0 and color is not the background panel color
print("Wardrobe image size:", img.size)

# Let's crop x: 80..600, y: 120..640 and inspect
crop = img.crop((80, 120, 600, 640))
crop.save("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_crop_wardrobe_hedgehog.png")
print("Saved wider crop (80, 120, 600, 640) -> proof_crop_wardrobe_hedgehog.png")
