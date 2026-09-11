import os
from PIL import Image
import numpy as np

frame_dir = "/opt/side/bravesoul-game/proofs/macaque_frames"
files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])

# Load macaque attack and idle poses
p_atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
p_rec = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/recover.png").convert("RGBA")
p_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png").convert("RGBA")

print(f"Total extracted frames: {len(files)}")

# Let's check reviewer metric on EVERY frame:
# "手臂區（y380-500, x150-430）鋼色像素"
# r>185, g>185, b>185, abs(r-b)<40
for idx, f in enumerate(files):
    im = Image.open(os.path.join(frame_dir, f)).convert("RGB")
    arr = np.array(im)
    
    # Reviewer's exact arm box:
    arm_crop = arr[380:501, 150:431]
    r = arm_crop[:, :, 0].astype(int)
    g = arm_crop[:, :, 1].astype(int)
    b = arm_crop[:, :, 2].astype(int)
    steel_arm = (r > 185) & (g > 185) & (b > 185) & (np.abs(r - b) < 40)
    cnt_arm = np.count_nonzero(steel_arm)
    
    # Also check break box on Leo side (x>800):
    # Reviewer's check:
    # "量測：f0085 最右 6 px 直條內亮黃像素 207 個，橫跨 y204-557；同位置待機格 f0010 只有 34 個。字確實壓到邊界外。"
    right6 = arr[:, -6:, :]
    r_r = right6[:, :, 0].astype(int)
    g_r = right6[:, :, 1].astype(int)
    b_r = right6[:, :, 2].astype(int)
    yellow_r = (r_r > 200) & (g_r > 160) & (b_r < 100)
    cnt_yellow_r = np.count_nonzero(yellow_r)

    if cnt_arm > 0 or cnt_yellow_r > 50 or idx in [9, 21, 23, 27, 77, 80, 84]:
        print(f"Frame {idx+1:3d} ({f}): arm_steel={cnt_arm:4d}, right6_yellow={cnt_yellow_r:3d}")
