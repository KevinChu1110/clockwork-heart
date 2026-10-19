#!/usr/bin/env python3
from PIL import Image

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")
# 放大 2 倍看 (200..300, 140..240) 的臉部和胸口
crop = im.crop((180, 140, 320, 260))
crop.save("/tmp/godot_face_zoom.png")
print("Saved /tmp/godot_face_zoom.png")
