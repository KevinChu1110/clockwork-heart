from PIL import Image
import numpy as np

f67 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0067.png").convert("RGBA")
f68 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0068.png").convert("RGBA")
f78 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0078.png").convert("RGBA")

# Let's find where steel pixels are in f67 vs f68 vs f78 across the ENTIRE image
for name, im in [("f67", f67), ("f68", f68), ("f78", f78)]:
    arr = np.array(im)
    r = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    b = arr[:, :, 2].astype(int)
    steel = (r > 185) & (g > 185) & (b > 185) & (np.abs(r - b) < 40)
    ys, xs = np.where(steel)
    print(f"=== {name} ===")
    print(f"Total steel pixels in whole screen: {len(xs)}")
    # player side (x < 650)
    p_mask = xs < 650
    px = xs[p_mask]
    py = ys[p_mask]
    print(f"Player side steel pixels: {len(px)}")
    if len(px) > 0:
        print(f"Player steel X: [{px.min()}..{px.max()}], Y: [{py.min()}..{py.max()}]")
