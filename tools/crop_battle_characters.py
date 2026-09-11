import os
from PIL import Image

races = ["rabbit", "lion", "fox", "boar"]
proof_dir = "/opt/side/bravesoul-game/proofs/combat_feel"

for r in races:
    img_path = os.path.join(proof_dir, f"{r}_battle_attack_full.png")
    if not os.path.exists(img_path):
        print(f"Missing {img_path}")
        continue
    img = Image.open(img_path)
    # PlayerSlot 在 1280x720 畫面左側約 x: 180~480, y: 160~480
    # 裁切角色軀幹與手部區域
    crop_box = (180, 160, 480, 480)
    cropped = img.crop(crop_box)
    
    # 放大 3 倍便於視覺檢視武器與手部細節
    try:
        resample = Image.Resampling.NEAREST
    except AttributeError:
        resample = Image.NEAREST
    large = cropped.resize((cropped.width * 3, cropped.height * 3), resample)
    out_path = os.path.join(proof_dir, f"{r}_battle_crop_weapon.png")
    large.save(out_path)
    print(f"Saved {out_path}")
