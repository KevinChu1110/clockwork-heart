from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_owl_idle_crop.png").convert("RGBA")
print("Crop size:", im.size)
arr = np.array(im)
# Find dark navy pixels (31, 26, 58) in the crop
rgb = arr[:, :, :3]
diff = np.abs(rgb.astype(int) - np.array([31, 26, 58]))
match = np.all(diff <= 5, axis=-1)
print("Matching (31, 26, 58) count:", np.sum(match))
ys, xs = np.where(match)
if len(ys) > 0:
    print(f"Match bounds: x in [{xs.min()}, {xs.max()}], y in [{ys.min()}, {ys.max()}]")
