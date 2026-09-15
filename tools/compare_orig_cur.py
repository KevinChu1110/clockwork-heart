from PIL import Image
import numpy as np

orig = Image.open("/opt/side/bravesoul-game/screenshots/chassis_orig.png")
cur = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")

arr_o = np.array(orig)
arr_c = np.array(cur)

diff = np.any(arr_o != arr_c, axis=-1)
ys, xs = np.where(diff)
print(f"Diff between orig and cur: y from {ys.min()} to {ys.max()}, x from {xs.min()} to {xs.max()}, count={len(ys)}")

# Where are the differences?
# Are there differences in the body or only in the face?
diff_face = diff & (np.arange(128)[:, None] >= 20) & (np.arange(128)[:, None] <= 65)
print(f"Diff in face region: count={np.sum(diff_face)}")

diff_body = diff & ~diff_face
print(f"Diff in body region: count={np.sum(diff_body)}")
