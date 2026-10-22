#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Let's save an image showing only the cream pixels of head and body
head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png").convert("RGBA")
arr_h = np.array(head)

cream_h = (arr_h[:, :, 0] > 220) & (arr_h[:, :, 1] > 210) & (arr_h[:, :, 2] > 190) & (arr_h[:, :, 3] > 0)
mask_h = Image.fromarray((cream_h * 255).astype(np.uint8))
mask_h.save("/tmp/mask_head_cream.png")

body = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
arr_b = np.array(body)

cream_b = (arr_b[:, :, 0] > 220) & (arr_b[:, :, 1] > 210) & (arr_b[:, :, 2] > 190) & (arr_b[:, :, 3] > 0)
mask_b = Image.fromarray((cream_b * 255).astype(np.uint8))
mask_b.save("/tmp/mask_body_cream.png")

print("Saved masks to /tmp/mask_head_cream.png and /tmp/mask_body_cream.png")
