#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/web/media/hero/char_boar.png")
# In raw 928x1160, where is the eye?
# Around x: 380..520, y: 320..460
eye_crop = im.crop((380, 320, 520, 460))
eye_crop.save("/tmp/raw_eye_crop.png")
print("Saved /tmp/raw_eye_crop.png")
