from PIL import Image

m_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"
claws = Image.open(f"{m_dir}/weapon/wpn_spring_claws.png").convert("RGBA")
chassis = Image.open(f"{m_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png").convert("RGBA")

print("claws bbox:", claws.getbbox())
# Let's see where claws are in idle
# claws bbox: (23, 70, 78, 91)
# That is x=23..78, y=70..91.
# In idle, macaque has left hand around (25, 75) and right hand around (75, 75).
print("idle bbox:", idle.getbbox())
