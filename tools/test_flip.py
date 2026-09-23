#!/usr/bin/env python3
import numpy as np
from PIL import Image

def test_flipped():
    raw = Image.open("/opt/side/bravesoul-game/docs/art/xuanji_tortoise_concept.png").convert("RGBA")
    # Horizontal flip
    flipped = raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    flipped.save("/tmp/tortoise_concept_flipped.png")
    print("Saved /tmp/tortoise_concept_flipped.png")

if __name__ == "__main__":
    test_flipped()
