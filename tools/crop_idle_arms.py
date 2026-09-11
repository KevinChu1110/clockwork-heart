#!/usr/bin/env python3
from PIL import Image

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")
crop_arm_l = idle_x3.crop((25, 45, 45, 95))
crop_arm_l.save("/tmp/idle_x3_arm_l.png")
crop_arm_r = idle_x3.crop((75, 45, 100, 95))
crop_arm_r.save("/tmp/idle_x3_arm_r.png")
print("Saved idle_x3 arm crops")
