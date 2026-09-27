#!/usr/bin/env python3
from PIL import Image, ImageChops

for race in ['fawn', 'pangolin']:
    p_b = f"/opt/side/bravesoul-game/game/assets/sprites/player/{race}_battle.png"
    p_a = f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/{race}/attack.png"
    try:
        im_b = Image.open(p_b)
        im_a = Image.open(p_a)
        diff = ImageChops.difference(im_b, im_a).getbbox()
        print(race, "diff between battle and attack:", diff)
    except Exception as e:
        print(race, e)
