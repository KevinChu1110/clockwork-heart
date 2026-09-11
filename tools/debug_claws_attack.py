from PIL import Image

claws = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png").convert("RGBA")
print("claws size:", claws.size)
print("claws bbox:", claws.getbbox())
opaque_pixels = sum(1 for px in claws.getdata() if px[3] > 8)
print("opaque pixels (a > 8):", opaque_pixels)

atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
print("atk size:", atk.size)
print("atk bbox:", atk.getbbox())

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png").convert("RGBA")
print("idle size:", idle.size)
print("idle bbox:", idle.getbbox())
