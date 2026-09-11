from PIL import Image
import numpy as np

frame_dir = "/opt/side/bravesoul-game/proofs/macaque_frames"

for fn in ["f_0010.png", "f_0022.png", "f_0023.png", "f_0024.png", "f_0025.png", "f_0028.png", "f_0077.png", "f_0078.png", "f_0079.png", "f_0080.png"]:
    im = Image.open(f"{frame_dir}/{fn}").convert("RGB")
    arr = np.array(im)
    
    # Reviewer's box: y380-500, x150-430
    box = arr[380:501, 150:431]
    r, g, b = box[:, :, 0].astype(int), box[:, :, 1].astype(int), box[:, :, 2].astype(int)
    steel = (r > 185) & (g > 185) & (b > 185) & (np.abs(r - b) < 40)
    cnt = np.count_nonzero(steel)

    # Let's also check where the steel pixels are on the whole player side (x < 650, y in 200..600):
    p_box = arr[200:601, 0:650]
    pr, pg, pb = p_box[:, :, 0].astype(int), p_box[:, :, 1].astype(int), p_box[:, :, 2].astype(int)
    p_steel = (pr > 185) & (pg > 185) & (pb > 185) & (np.abs(pr - pb) < 40)
    p_cnt = np.count_nonzero(p_steel)

    print(f"{fn:12s}: reviewer_box_steel={cnt:4d}, total_player_side_steel={p_cnt:4d}")
