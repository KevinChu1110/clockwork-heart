from PIL import Image
import numpy as np

f78_crop = Image.open("/tmp/player_f_0078.png").convert("RGBA")
arr78 = np.array(f78_crop)

poses = ["idle", "attack", "skill", "hit", "telegraph", "recover"]
for p in poses:
    p_img = Image.open(f"/tmp/pose_200_{p}.png").convert("RGBA")
    arr_p = np.array(p_img)
    mask = arr_p[:, :, 3] > 100
    best_diff = 1e9
    best_pos = None
    H, W = arr78.shape[:2]
    h, w = arr_p.shape[:2]
    for y in range(0, H - h, 5):
        for x in range(0, W - w, 5):
            sub = arr78[y:y+h, x:x+w]
            diff = np.mean(np.abs(sub[mask, :3].astype(int) - arr_p[mask, :3].astype(int)))
            if diff < best_diff:
                best_diff = diff
                best_pos = (x, y)
    print(f"Pose {p:9s}: best_diff={best_diff:.2f} at {best_pos}")
