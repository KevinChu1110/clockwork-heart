from PIL import Image

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png").convert("RGBA")
claws = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png").convert("RGBA")
atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")

# Let's see: In idle, where are the arms/hands?
# Left hand (screen left): around x=24..36, y=72..88
# Right hand (screen right): around x=64..78, y=72..88
# Hand width: around 12-14px.
# 1.5x hand width: ~18-22px!
# In idle, claws can curve downward/outward from each hand by ~18-24px!
print("idle size:", idle.size)
print("claws current bbox:", claws.getbbox())
print("atk size:", atk.size)
print("atk current bbox:", atk.getbbox())
