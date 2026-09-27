from PIL import Image
import numpy as np

for name in ['char_tortoise.png', 'char_elephant.png', 'char_frog.png', 'char_panda.png']:
    im = Image.open(f'/opt/side/bravesoul-game/web/media/hero/{name}')
    arr = np.array(im)
    print(f"{name}: mode={im.mode}, size={im.size}, corner pixel={arr[0,0] if arr.ndim==3 else arr[0,0,:]}")
