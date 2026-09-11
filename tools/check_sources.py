from PIL import Image

f1 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png")
f2 = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png")
f3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png")

print("party_fox_idle size:", f1.size)
print("char_no_shadow_no_wep size:", f2.size)
print("wpn_astral_staff size:", f3.size)
