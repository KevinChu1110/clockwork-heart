#!/usr/bin/env python3
import numpy as np
from PIL import Image

img = Image.open("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_lobby_hedgehog.png").convert("RGBA")
# Let's crop a slightly wider region around the hero avatar in the lobby:
# Center of lobby hero is around x: 500..850, y: 150..600
crop = img.crop((460, 180, 860, 580))
crop.save("/opt/side/bravesoul-game/proofs/exploratory_qa_t_e6bc1e6c/proof_crop_lobby_hedgehog.png")
print("Saved lobby crop (460, 180, 860, 580) -> proof_crop_lobby_hedgehog.png")
