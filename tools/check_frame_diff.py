import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"
im1 = Image.open(os.path.join(proof_dir, "extracted_frame_02.png"))
# 檢查各幀與 frame 2 的差異
for i in range(3, 21):
    im2 = Image.open(os.path.join(proof_dir, f"extracted_frame_{i:02d}.png"))
    # 比較角色區域
    c1 = im1.crop((200, 220, 450, 460))
    c2 = im2.crop((200, 220, 450, 460))
    diff = ImageChops.difference(c1, c2)
    bbox = diff.getbbox()
    if bbox:
        # 計算非零像素量
        stat = sum(list(diff.convert("L").getdata()))
        print(f"Frame {i:02d} vs Frame 02 player diff: bbox={bbox}, sum={stat}")
