#!/usr/bin/env python3
import numpy as np
from PIL import Image

img_c = Image.open("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_creation_hedgehog.png").convert("RGBA")
# Let's crop x: 150..470, y: 340..650
crop_c = img_c.crop((150, 340, 470, 650))
crop_c.save("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_crop_creation_hedgehog.png")
arr_c = np.array(crop_c)
brass_c = (arr_c[:, :, 0] > 140) & (arr_c[:, :, 1] > 90) & (arr_c[:, :, 2] < 90)
print("Creation crop brass pixels:", np.sum(brass_c))

# Wardrobe:
img_w = Image.open("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_wardrobe_hedgehog.png").convert("RGBA")
# Let's see where the character is on the left preview area of wardrobe dialog
# Wardrobe dialog character preview is typically on the left side: x: 100..450, y: 150..620
crop_w = img_w.crop((100, 150, 480, 620))
crop_w.save("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_crop_wardrobe_hedgehog.png")
arr_w = np.array(crop_w)
brass_w = (arr_w[:, :, 0] > 140) & (arr_w[:, :, 1] > 90) & (arr_w[:, :, 2] < 90)
print("Wardrobe crop brass pixels:", np.sum(brass_w))
