from PIL import Image
import numpy as np

for r in ['beaver', 'viper', 'courser', 'chameleon']:
    path = f'game/assets/sprites/player/poses/{r}/idle.png'
    try:
        im = Image.open(path)
        arr = np.array(im)
        counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
        print(f'{r:10s} idle bbox: {im.getbbox()} shadow counts: {counts}')
    except Exception as e:
        print(f'{r:10s} error: {e}')
