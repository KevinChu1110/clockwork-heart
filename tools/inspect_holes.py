import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes

comp_im = Image.open("game/assets/sprites/player/paperdoll/squirrel/proof_paperdoll_squirrel_composite.png").convert("RGBA")
comp_arr = np.array(comp_im)
comp_alpha = comp_arr[:, :, 3] > 8

filled_mask = binary_fill_holes(comp_alpha)
holes = filled_mask & (~comp_alpha)

hole_coords = np.argwhere(holes)
print(f"Total hole pixels: {len(hole_coords)}")
print(f"Hole coords Y range: {hole_coords[:, 0].min()}..{hole_coords[:, 0].max()}")
print(f"Hole coords X range: {hole_coords[:, 1].min()}..{hole_coords[:, 1].max()}")

# Save a map of holes
hole_map = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for y, x in hole_coords:
    hole_map.putpixel((x, y), (255, 0, 0, 255))
hole_map.save("proofs/test_holes_map.png")
print("Saved hole map to proofs/test_holes_map.png")
