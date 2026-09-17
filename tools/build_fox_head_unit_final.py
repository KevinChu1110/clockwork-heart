import numpy as np
from PIL import Image

ch_path = "game/assets/sprites/player/paperdoll/fox/chassis/paint_fox_orange_512.png"
ch = Image.open(ch_path).convert("RGBA")
ch_arr = np.array(ch)

W, H = 512, 512

# Step 1: Base head_unit is extracted strictly from the chassis head (y in [40, 252])
# Exclude winding key on the right (x >= 392 when y >= 210)
head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ch_alpha = ch_arr[:, :, 3]

for y in range(40, 253):
    for x in range(W):
        if y >= 210 and x >= 392:
            continue
        if ch_alpha[y, x] > 20:
            head.putpixel((x, y), tuple(ch_arr[y, x]))

# Step 2: Hollow out eye sockets cleanly (Alpha = 0)
# Dark eye regions:
# Left eye center: (216, 192), radius rx=25.5, ry=24.5
# Right eye center: (313, 192), radius rx=25.5, ry=24.5
for y in range(155, 218):
    for x in range(180, 350):
        is_left_eye = ((x - 216)**2) / (25.5**2) + ((y - 192)**2) / (24.5**2) <= 1.0
        is_right_eye = ((x - 313)**2) / (25.5**2) + ((y - 192)**2) / (24.5**2) <= 1.0
        if is_left_eye or is_right_eye:
            head.putpixel((x, y), (0, 0, 0, 0))

# NO artificial outline circles around eyes! Keep pure natural original hand-drawn borders!

# Save 512 head_unit
out_hd_512 = "game/assets/sprites/player/paperdoll/fox/head_unit/ear_fox_radar_512.png"
head.save(out_hd_512)
print(f"Saved {out_hd_512}")

# Also generate 128 version via LANCZOS downsampling
out_hd_128 = "game/assets/sprites/player/paperdoll/fox/head_unit/ear_fox_radar.png"
head_128 = head.resize((128, 128), Image.Resampling.LANCZOS)
head_128.save(out_hd_128)
print(f"Saved {out_hd_128}")

# Composite with chassis for verification:
comp = Image.alpha_composite(ch, head)
out_comp = "proofs/head_unit_analysis/final_fox_composite_512.png"
comp.save(out_comp)
print(f"Saved {out_comp}")

crop = comp.crop((110, 10, 415, 290))
out_crop = "proofs/head_unit_analysis/final_fox_composite_crop.png"
crop.save(out_crop)
print(f"Saved {out_crop}")
