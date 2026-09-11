import os
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
OUTPUT_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")

# Let's inspect the actual saved images in game/assets/sprites/player/poses/fox/
# idle.png, telegraph.png, attack.png, recover.png, skill.png, hit.png
poses = {}
for p in ["idle", "telegraph", "recover", "skill", "hit"]:
    poses[p] = Image.open(os.path.join(OUTPUT_DIR, f"{p}.png")).convert("RGBA")

# Let's load the weapon image
staff_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
# Let's see: how did side analyze the images?
# Could side have extracted staff from each pose, or used the known placed staff?
# Let's check how staff was placed in each pose:
from tools.generate_fox_combat_poses import place_rigid_staff
staff_src = staff_im
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

# Let's check:
placements = {
    "idle": (0, (90, 86)),
    "telegraph": (32, (76, 84)),
    "recover": (18, (88, 86)),
    "skill": (-45, (86, 68)),
    "hit": (-25, (78, 72)),
}

for name, (deg, hand) in placements.items():
    st = place_rigid_staff(clean_staff, deg, hand)
    st_px = st.load()
    pose_px = poses[name].load()
    
    # What if "身體剪影" means:
    # where pose has alpha > 0, excluding the staff?
    # Or what if "身體剪影" is the bounding box or hull or trunk of the body?
    # For example, x between left and right edge of body for each y?
    pass
print("Done check setup")
