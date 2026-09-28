from PIL import Image
import numpy as np

# Load individual slice layers
base_dir = "game/assets/sprites/player/paperdoll/peacock"
key_src = Image.open(f"{base_dir}/winding_key/key_peacock_filigree_sunburst_key.png").convert("RGBA")
curio_src = Image.open(f"{base_dir}/back_curio/curio_peacock_articulated_kaleidoscope_fan.png").convert("RGBA")
chassis_src = Image.open(f"{base_dir}/chassis/chassis_peacock_glazed_porcelain_default.png").convert("RGBA")
head_src = Image.open(f"{base_dir}/head_unit/head_peacock_baroque_diadem_prism.png").convert("RGBA")
costume_src = Image.open(f"{base_dir}/costume/costume_peacock_marionette_court_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{base_dir}/optic_core/face_peacock_kaleidoscope_gem_lens.png").convert("RGBA")
weapon_src = Image.open(f"{base_dir}/weapon/weapon_peacock_kaleidoscope_prism_focus.png").convert("RGBA")

# Build body_core_raw
body_core_raw = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core_raw.alpha_composite(curio_src)
body_core_raw.alpha_composite(chassis_src)
body_core_raw.alpha_composite(head_src)
body_core_raw.alpha_composite(costume_src)
body_core_raw.alpha_composite(optic_src)

# Smoothly compress y < 45 so y=0 maps to y=4
w, h = body_core_raw.size
src_px = body_core_raw.load()
body_core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dst_px = body_core.load()

for y in range(h):
    if y < 4:
        continue
    elif y < 45:
        src_y = (y - 4) * (45.0 / 41.0)
    else:
        src_y = float(y)
    y0 = int(src_y)
    y1 = min(h - 1, y0 + 1)
    fy = src_y - y0
    for x in range(w):
        p0 = src_px[x, y0]
        p1 = src_px[x, y1]
        rgba = tuple(int(round(p0[c] * (1 - fy) + p1[c] * fy)) for c in range(4))
        dst_px[x, y] = rgba

print("body_core bbox:", body_core.getbbox())

# Let's locate optic centers in body_core
o_arr = np.array(optic_src)
# Left eye (blue), right eye (mint green)
# Left eye x < 64, right eye x > 64
left_eye = np.where((o_arr[:, :64, 3] > 50))
right_eye = np.where((o_arr[:, 64:, 3] > 50))
print("Left eye center in raw optic:", np.mean(left_eye[1]), np.mean(left_eye[0]))
print("Right eye center in raw optic:", 64 + np.mean(right_eye[1]), np.mean(right_eye[0]))

# Check weapon bbox and center
w_bbox = weapon_src.getbbox()
print("weapon raw bbox:", w_bbox)
print("weapon raw center:", (w_bbox[0] + w_bbox[2]) / 2, (w_bbox[1] + w_bbox[3]) / 2)

# Check key bbox and center
k_bbox = key_src.getbbox()
print("key raw bbox:", k_bbox)
print("key raw center:", (k_bbox[0] + k_bbox[2]) / 2, (k_bbox[1] + k_bbox[3]) / 2)
