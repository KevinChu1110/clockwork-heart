from PIL import Image
import numpy as np

img = Image.open("/opt/side/bravesoul-game/web/media/hero/char_rabbit.png").convert("RGB")
arr = np.array(img)
corners = [arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]]
print("Corners:", corners)
print("Top row unique colors near top-left:", np.unique(arr[0:10, 0:10].reshape(-1, 3), axis=0)[:5])
