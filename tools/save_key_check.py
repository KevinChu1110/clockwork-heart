#!/usr/bin/env python3
from PIL import Image

k = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png")
k.save("/tmp/key_check_view.png")
print("Saved /tmp/key_check_view.png, bbox:", k.getbbox())
