#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

# Let's check the pixels on the face
# What are the coordinates of the face?
# Let's crop (35, 20, 95, 60) and see
crop_face = im.crop((35, 20, 95, 60))
crop_face.save("/tmp/macaque_ivory_face.png")

# Let's crop torso (35, 60, 95, 110)
crop_torso = im.crop((35, 60, 95, 110))
crop_torso.save("/tmp/macaque_ivory_torso.png")

# Also let's inspect paint_bamboo_bronze
im_b = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png").convert("RGBA")
crop_b_face = im_b.crop((35, 20, 95, 60))
crop_b_face.save("/tmp/macaque_bronze_face.png")
crop_b_torso = im_b.crop((35, 60, 95, 110))
crop_b_torso.save("/tmp/macaque_bronze_torso.png")
print("Saved crops to /tmp")
