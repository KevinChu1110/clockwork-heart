from PIL import Image
import numpy as np
im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/armor/gi.png")
arr = np.array(im)
nz = arr[arr[:,:,3] > 0]
print("gi.png avg rgb:", nz.mean(axis=0))
print("gi.png min rgb:", nz.min(axis=0))
print("gi.png max rgb:", nz.max(axis=0))
