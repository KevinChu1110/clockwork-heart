import os
from PIL import Image

m_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"
claws = Image.open(f"{m_dir}/weapon/wpn_spring_claws.png").convert("RGBA")
ch_ivory = Image.open(f"{m_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
ch_bronze = Image.open(f"{m_dir}/chassis/paint_bamboo_bronze.png").convert("RGBA")

print("Claws bbox:", claws.getbbox())
# What is inside wpn_spring_claws? Does it have hands or only metal claw gauntlets?
# Claws are brass claw gauntlets that attach over the hand/wrist!
