from PIL import Image

head = Image.open('game/assets/sprites/player/paperdoll/lion/head_unit/ear_lion_gilded_mane.png').convert('RGBA')
core = Image.open('game/assets/sprites/player/paperdoll/lion/optic_core/core_amber_sun.png').convert('RGBA')
wep = Image.open('game/assets/sprites/player/paperdoll/lion/weapon/wpn_knight_lance.png').convert('RGBA')

print("Head unit bbox:", head.getbbox())
print("Optic core bbox:", core.getbbox())
print("Weapon bbox:", wep.getbbox())
