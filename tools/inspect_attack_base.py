from PIL import Image
import numpy as np

base = Image.open("/tmp/attack_base.png").convert("RGBA")
print("base size:", base.size)
print("base bbox:", base.getbbox())

# What colors are in base?
arr = np.array(base)
alpha = arr[:, :, 3]
visible = arr[alpha > 100]
print("visible pixels:", len(visible))
print("mean RGB:", np.mean(visible[:, :3], axis=0))
