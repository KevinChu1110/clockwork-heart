#!/usr/bin/env python3
from PIL import Image

crop = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_macaque_crop_zen_striker.png")
print("crop size:", crop.size)

# Let's check where the character's face is in crop:
# crop is (360, 450)
# Let's crop just the face from this crop:
# In crop, where is the face?
# Let's check x: 80..200, y: 50..180
face_in_crop = crop.crop((80, 50, 220, 180))
face_in_crop.save("/tmp/face_in_crop.png")
print("Saved /tmp/face_in_crop.png")
