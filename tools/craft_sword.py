import os
import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

# Let's inspect current blade and chassis
cur_blade = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
costume = Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA")
head = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")

print("Current blade size:", cur_blade.size)
