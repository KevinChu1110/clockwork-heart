#!/usr/bin/env python3
from PIL import Image

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")

bg = Image.new("RGBA", (512, 512), (32, 34, 42, 255))
bg.alpha_composite(im)
bg.save("/tmp/boar_healed_dark.png")
print("Saved /tmp/boar_healed_dark.png")
