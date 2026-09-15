from PIL import Image
import numpy as np

head = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/head_unit/ear_macaque_coaxial.png")
arr = np.array(head)
print("Head shape:", arr.shape)

# Let's find all pixels in head where r > 200, g > 200, b > 200, or where it's near white/translucent
# In the region x: 30..80, y: 25..60
sub = arr[25:60, 30:80]
print("Sub alpha > 0:", np.sum(sub[:,:,3] > 0))
# Unique colors in sub where alpha > 0:
non_trans = sub[sub[:,:,3] > 0]
for c in np.unique(non_trans, axis=0)[:20]:
    print(c)
