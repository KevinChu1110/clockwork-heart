import os
from PIL import Image
import numpy as np

frame_dir = "/opt/side/bravesoul-game/proofs/macaque_frames"
files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])

p_atk = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
p_rec = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/recover.png").convert("RGBA")
p_tel = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/telegraph.png").convert("RGBA")
p_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png").convert("RGBA")

# Let's check which frame in macaque_frames has which pose!
# To do this, let's look at the player area in each frame.
# In PlayerSlot (1280x720): PlayerBody is custom_minimum_size = (200, 250).
# Let's crop PlayerBody area in each frame:
# In idle (f1..f21), PlayerBody is around x: 190..390, y: 220..470
# During lunge, player moves right (towards enemy).
for idx, f in enumerate(files):
    im = Image.open(os.path.join(frame_dir, f)).convert("RGBA")
    # Let's find player body by checking diff against a known background or by checking colors
    # Actually, in Godot, when player_body.texture changes:
    # Does the aspect ratio or bounding box change?
    # attack.png has bbox (19, 12, 123, 108) -> width = 104, max x = 123 (arm lunges right!)
    # recover.png has bbox (36, 50, 89, 112) -> width = 53, crouching low!
    pass

# Let's inspect frames 20 to 35 and frames 70 to 85 specifically!
print("Frames 20 to 35, and 72 to 85:")
for idx in list(range(19, 32)) + list(range(72, 86)):
    f = files[idx]
    im = Image.open(os.path.join(frame_dir, f)).convert("RGB")
    arr = np.array(im)
    # Check player center of mass in x in [100, 600], y in [200, 550]
    sub = arr[200:550, 100:600]
    # Find player pixels: non-background paver color
    # background is around (150..180, 120..150, 90..120)
    # let's find pixels where r,g,b differ from typical paver
    # Or let's measure difference from f_0010 in player area:
    im10 = Image.open(os.path.join(frame_dir, "f_0010.png")).convert("RGB")
    sub10 = np.array(im10)[200:550, 100:600]
    diff = np.max(np.abs(sub.astype(int) - sub10.astype(int)), axis=2)
    diff_cnt = np.count_nonzero(diff > 30)
    
    # Check if this frame has the lunging arm (x > 380 in player area):
    right_diff = np.count_nonzero(diff[:, 280:] > 30)
    print(f"Frame {idx+1:2d} ({f}): diff_from_idle={diff_cnt:5d}, right_diff={right_diff:4d}")
