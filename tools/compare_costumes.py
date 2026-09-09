from PIL import Image

r_nut = Image.open('game/assets/sprites/player/paperdoll/rabbit/costume/costume_nutcracker_guard.png')
l_nut = Image.open('game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard.png')
r_art = Image.open('game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png')

print("Rabbit nutcracker bbox:", r_nut.getbbox(), "size:", r_nut.size)
print("Lion nutcracker bbox:", l_nut.getbbox(), "size:", l_nut.size)
print("Rabbit steam artisan bbox:", r_art.getbbox(), "size:", r_art.size)
