import sys
REPO_ROOT = "/opt/side/bravesoul-game"
sys.path.insert(0, REPO_ROOT)
from tools.generate_fox_combat_poses import place_rigid_staff
from PIL import Image
staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

for hx in [76, 80, 82, 84, 86]:
    for hy in [55, 60, 65, 70]:
        for deg in [-60, -65, -70]:
            st = place_rigid_staff(clean_staff, deg, (hx, hy))
            bbox = st.getbbox()
            if bbox and bbox[2] < 127 and bbox[0] > 0 and bbox[1] > 0 and bbox[3] < 127:
                print(f"SAFE: deg={deg}, hand=({hx}, {hy}), bbox={bbox}")
