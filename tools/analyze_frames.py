import os
from PIL import Image, ImageChops

proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"

for i in range(1, 21):
    f = os.path.join(proof_dir, f"extracted_frame_{i:02d}.png")
    if os.path.exists(f):
        im = Image.open(f)
        # 裁剪我方角色位置區域 (x: 200~450, y: 220~460)
        p_crop = im.crop((200, 220, 450, 460))
        p_crop.save(os.path.join(proof_dir, f"player_crop_{i:02d}.png"))
        # 裁剪敵方傷害數字跳字區域 (x: 800~1100, y: 150~350)
        e_crop = im.crop((800, 150, 1100, 350))
        e_crop.save(os.path.join(proof_dir, f"enemy_crop_{i:02d}.png"))
print("All crops saved.")
