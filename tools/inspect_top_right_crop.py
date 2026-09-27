from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/proofs/combat_poses_512/proof_combat_owl_idle_crop.png").convert("RGBA")
arr = np.array(im)
sub = arr[10:90, 130:190]
for y in range(0, 80, 5):
    row_colors = [f"({sub[y, x, 0]},{sub[y, x, 1]},{sub[y, x, 2]})" for x in range(0, 60, 10)]
    print(f"y={y+10:2d}:", " ".join(row_colors))
