from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/owl/idle.png").convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]
rgb = arr[:, :, :3]

# Check where alpha > 0 and rgb is very dark and if it forms a rectangle
dark_mask = (alpha > 50) & (rgb[:, :, 0] < 45) & (rgb[:, :, 1] < 45) & (rgb[:, :, 2] < 65)
print("Dark mask pixel count:", np.sum(dark_mask))
y_indices, x_indices = np.where(dark_mask)
if len(y_indices) > 0:
    print(f"Dark pixels bounds: x in [{x_indices.min()}, {x_indices.max()}], y in [{y_indices.min()}, {y_indices.max()}]")
    # check outline pixels
    print("Unique dark RGBs:", np.unique(rgb[dark_mask], axis=0))
