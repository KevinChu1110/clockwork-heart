from PIL import Image
import numpy as np

img = Image.open('game/assets/sprites/player/showcase/hedgehog_idle_hd.png')
arr = np.array(img)
alpha = arr[:, :, 3]
non_empty_cols = np.where(alpha.max(axis=0) > 0)[0]
non_empty_rows = np.where(alpha.max(axis=1) > 0)[0]

print(f"Total size: {img.size}")
print(f"X bounds: {non_empty_cols[0]}..{non_empty_cols[-1]} (width {len(non_empty_cols)})")
print(f"Y bounds: {non_empty_rows[0]}..{non_empty_rows[-1]} (height {len(non_empty_rows)})")

# Check right edge
for x in range(780, 800):
    col = alpha[:, x]
    nonzero = int(np.count_nonzero(col))
    max_val = int(col.max())
    y_indices = np.where(col > 0)[0]
    y_range = f"{y_indices[0]}..{y_indices[-1]}" if len(y_indices) > 0 else "none"
    print(f'x={x:3d}: nonzero={nonzero:4d}, max_alpha={max_val:3d}, y_range={y_range}')
