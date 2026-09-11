from PIL import Image

im_atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
im_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png").convert("RGBA")
claws = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png").convert("RGBA")

print("atk size:", im_atk.size)
print("idle size:", im_idle.size)
print("claws bbox:", claws.getbbox())

# Let us check how attack.png looks like around the hands.
# Where are the hands in attack.png?
# In macaque attack.png:
# Let's find pixels where hands / fist are.
