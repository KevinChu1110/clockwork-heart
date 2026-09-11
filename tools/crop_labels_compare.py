#!/usr/bin/env python3
from PIL import Image

for kind in ["outline", "minicard"]:
    im = Image.open(f"/tmp/test_labels_{kind}.png")
    # Rage area: x: 20~200, y: 80~160
    crop_rage = im.crop((20, 70, 250, 160))
    crop_rage.save(f"/tmp/crop_rage_{kind}.png")
    
    # Enemy tag area: x: 700~1000, y: 140~270
    crop_enemy = im.crop((700, 140, 1000, 270))
    crop_enemy.save(f"/tmp/crop_enemy_{kind}.png")
    
    # Player tag area: x: 250~550, y: 140~270
    crop_player = im.crop((250, 140, 550, 270))
    crop_player.save(f"/tmp/crop_player_{kind}.png")

print("Cropped labels.")
