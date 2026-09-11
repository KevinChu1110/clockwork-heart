#!/usr/bin/env python3
from PIL import Image, ImageChops

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

print("idle_x3 bbox:", idle_x3.getbbox())
print("comp bbox:   ", comp.getbbox())
print("ivory bbox:  ", ivory.getbbox())

diff = ImageChops.difference(idle_x3, comp)
bbox_diff = diff.getbbox()
print("Diff between idle_x3 and composite:", bbox_diff)
