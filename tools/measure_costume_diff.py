from PIL import Image
import numpy as np

im_royal = Image.open("game/assets/sprites/player/paperdoll/rabbit/costume/costume_royal_parade.png").convert("RGBA")
im_steam = Image.open("game/assets/sprites/player/paperdoll/rabbit/costume/costume_steam_artisan.png").convert("RGBA")
print("Costume texture size:", im_royal.size)
arr_r = np.array(im_royal)
arr_s = np.array(im_steam)
diff = np.any(arr_r != arr_s, axis=2)
print("Diff pixels in 128x128:", diff.sum())

print("Estimated diff in 200x200:", int(diff.sum() * (200/128)**2))
print("Estimated diff in 200x250:", int(diff.sum() * (200/128) * (250/128)))
