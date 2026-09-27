from PIL import Image
import numpy as np

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/cat/idle.png")
hit = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/cat/hit.png")

i_arr = np.array(idle)
h_arr = np.array(hit)

# Top 40 rows are head/ears
i_head = (i_arr[:45, :, 3] > 20)
h_head = (h_arr[:45, :, 3] > 20)

i_ys, i_xs = np.where(i_head)
h_ys, h_xs = np.where(h_head)

print(f"Idle head center: ({i_xs.mean():.1f}, {i_ys.mean():.1f})")
print(f"Hit  head center: ({h_xs.mean():.1f}, {h_ys.mean():.1f})")
print(f"Shift: ({h_xs.mean() - i_xs.mean():.1f}, {h_ys.mean() - i_ys.mean():.1f})")
