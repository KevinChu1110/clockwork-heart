from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

# Let's inspect attack without atk_fx
import sys
sys.path.append("tools")
from build_chameleon_combat_poses import generate_poses

poses = generate_poses()
for name in poses:
    arr = np.array(poses[name])
    alpha = arr[:, :, 3]
    filled = binary_fill_holes(alpha > 10)
    holes = filled & (alpha <= 10)
    lbl, num = label(holes)
    max_c = 0
    for i in range(1, num + 1):
        cnt = np.sum(lbl == i)
        if cnt > max_c:
            max_c = cnt
    print(f"{name:10s}: total_holes={np.sum(holes):3d}, max_cluster={max_c:3d}")
