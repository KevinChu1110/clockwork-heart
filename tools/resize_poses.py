from PIL import Image
import numpy as np

# Let's crop the player sprite from f_0078.png
f78 = Image.open("/opt/side/bravesoul-game/proofs/macaque_frames/f_0078.png").convert("RGBA")
# Let's also load the poses and find template match!
poses = ["idle", "attack", "skill", "hit", "telegraph", "recover"]

for p in poses:
    pose_img = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/{p}.png").convert("RGBA")
    # pose_img is 128x128. In battle, PlayerBody custom_minimum_size = (200, 250) or drawn rect.
    # What size is PlayerBody drawn at?
    # In PlayerSlot, custom_minimum_size is (200, 250), stretch_mode = 5 (STRETCH_KEEP_ASPECT_CENTERED).
    # Since 128x128 is 1:1, in (200, 250) it will be 200x200!
    # Let's resize pose_img to 200x200:
    p_resized = pose_img.resize((200, 200), Image.Resampling.LANCZOS)
    p_arr = np.array(p_resized)
    
    # Let's save each resized pose for comparison
    p_resized.save(f"/tmp/pose_200_{p}.png")

print("Saved all 200x200 poses to /tmp")
