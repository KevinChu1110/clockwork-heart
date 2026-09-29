#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

weapon_path = "game/assets/sprites/player/paperdoll/kingfisher/weapon/weapon_kingfisher_bamboo_spring_lance.png"
im = Image.open(weapon_path)
arr = np.array(im)
alpha = arr[:, :, 3]
rgb = arr[:, :, :3]
dark = (alpha > 30) & (rgb[:, :, 0] < 12) & (rgb[:, :, 1] < 12) & (rgb[:, :, 2] < 12)
print("Weapon bbox:", im.getbbox())
print("Dark pixels (<12):", np.sum(dark))
white = (alpha > 250) & (np.min(rgb, axis=-1) >= 225)
print("White pixels (>=225):", np.sum(white))
