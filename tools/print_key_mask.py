from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/owl/winding_key/key_owl_sun_moon_astrolabe_gold.png"
im = Image.open(p).convert("RGBA")
arr = np.array(im)
sub = arr[17:52, 70:106]
for y, row in enumerate(sub):
    line = "".join("D" if (row[x, 3] > 50 and row[x, 0] == 31 and row[x, 1] == 26 and row[x, 2] == 58) else ("#" if row[x, 3] > 50 else ".") for x in range(len(row)))
    print(f"{y+17:2d}: {line}")
