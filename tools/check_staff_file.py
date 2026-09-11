import os
from PIL import Image

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png"
im = Image.open(p)
print("wpn_astral_staff bbox:", im.getbbox())
