from PIL import Image
import numpy as np

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png")
chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png")

arr_i = np.array(idle)
arr_c = np.array(chassis)

# In the upper body / head region y: 10..65:
# What does idle have that chassis doesn't, and what does chassis have?
# Notice: In idle, the head is (x: 25..95, y: 12..65).
# Does idle have the winding key? Yes, the winding key is around x: 70..100, y: 20..50.
# In chassis, the winding key is stripped out.
# But what about the HEAD and FACE?
# In chassis, the head and face is at x: 25..85, y: 12..65.
# Let's inspect where chassis differs from idle in x: 25..85, y: 12..65:
diff = np.any(arr_i != arr_c, axis=-1)
ys, xs = np.where(diff & (np.arange(128)[:, None] < 65) & (np.arange(128)[None, :] < 85) & (np.arange(128)[None, :] > 25))
print(f"Diff in head: y from {ys.min()} to {ys.max()}, x from {xs.min()} to {xs.max()}, total diff pixels: {len(ys)}")

# Where are the winding key pixels in idle?
# winding key in idle is to the right / back: x > 75
# The face and helmet front in idle is x: 25..75, y: 15..62!
# Let's check what chassis has in x: 25..75, y: 15..62:
