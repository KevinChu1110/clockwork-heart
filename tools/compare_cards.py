from PIL import Image
import numpy as np

for name in ['proof_card_10_tortoise.png', 'proof_card_11_elephant.png', 'proof_card_12_frog.png', 'proof_card_13_panda.png']:
    im = Image.open(f'/opt/side/bravesoul-game/proofs/web_thirteen_races/{name}')
    arr = np.array(im)
    top_half = arr[:300, :, :]
    print(f"{name}: size={im.size}, top_half mean={top_half.mean():.1f}, min={top_half.min()}, max={top_half.max()}")
