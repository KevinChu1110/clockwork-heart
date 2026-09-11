import os
from PIL import Image

fox_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
fox_battle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")
staff = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")

print("fox_idle size:", fox_idle.size, "bbox:", fox_idle.getbbox())
print("fox_battle size:", fox_battle.size, "bbox:", fox_battle.getbbox())
print("staff size:", staff.size, "bbox:", staff.getbbox())
