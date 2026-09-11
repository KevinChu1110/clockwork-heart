#!/usr/bin/env python3
from PIL import Image

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")
crop = idle_x3.crop((35, 20, 95, 60))
crop.save("/tmp/idle_x3_face.png")
print("Saved /tmp/idle_x3_face.png")
