#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/raw_eye_crop.png")
# Eyeball is centered at (49, 83)
# Crop 40x40 around (49, 83) -> (29, 63, 69, 103)
eye_ball = im.crop((29, 63, 69, 103))
eye_ball.save("/tmp/exact_eyeball.png")
print("Saved /tmp/exact_eyeball.png")
