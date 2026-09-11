import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
tmp_dir = os.path.join(proof_dir, "tmp_10s")

im1 = Image.open(os.path.join(tmp_dir, "frame_001.png"))
# 找到變化最大的某一幀
max_diff = 0
max_bbox = None
best_frame = 0

for i in range(2, 301):
    cur = Image.open(os.path.join(tmp_dir, f"frame_{i:03d}.png"))
    d = ImageChops.difference(im1, cur)
    b = d.getbbox()
    if b:
        score = sum(list(d.convert("L").getdata()))
        if score > max_diff:
            max_diff = score
            max_bbox = b
            best_frame = i

print(f"Max difference at Frame {best_frame:03d}: bbox={max_bbox}, score={max_diff}")
# 保存最大變化的差分圖與原圖
d_img = ImageChops.difference(im1, Image.open(os.path.join(tmp_dir, f"frame_{best_frame:03d}.png")))
d_img.save(os.path.join(proof_dir, "max_diff_visual.png"))
Image.open(os.path.join(tmp_dir, f"frame_{best_frame:03d}.png")).save(os.path.join(proof_dir, "max_diff_frame.png"))
