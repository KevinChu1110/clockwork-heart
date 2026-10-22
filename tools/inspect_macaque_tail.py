#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_tail = Image.open(f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
print("Tail bbox in 128:", im_tail.getbbox())
w = im_tail.getbbox()[2] - im_tail.getbbox()[0]
h = im_tail.getbbox()[3] - im_tail.getbbox()[1]
print(f"Tail content size in 128: ({w}, {h})")

# 裁切緊湊切片
crop_128 = im_tail.crop(im_tail.getbbox())
crop_128.save("/tmp/macaque_test/tail_crop_128.png")
print("Saved /tmp/macaque_test/tail_crop_128.png")
