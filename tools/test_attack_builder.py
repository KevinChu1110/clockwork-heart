from PIL import Image, ImageDraw
import numpy as np

# Load base attack
base = Image.open("/tmp/attack_base.png").convert("RGBA")

# Load macaque composite to get canonical ivory chassis and head colors
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")

# Let's inspect ivory chassis in paperdoll:
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
print("ivory size:", ivory.size, "bbox:", ivory.getbbox())

# Let's inspect wpn_spring_claws in paperdoll:
claws = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png").convert("RGBA")
print("claws size:", claws.size, "bbox:", claws.getbbox())
