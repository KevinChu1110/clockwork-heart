from PIL import Image
import numpy as np

for name in [
    "screenshots/proof_battle_attack_sword.png",
    "screenshots/proof_battle_equipped_royal_parade.png",
    "screenshots/proof_battle_attack_full_screen.png",
    "screenshots/proof_battle_full_screen.png"
]:
    im = Image.open(name).convert("RGBA")
    crop = im.crop((300, 420, 660, 600))
    crop_path = name.replace(".png", "_feet_crop.png")
    crop.save(crop_path)
    
    # Check dark pixels in crop
    arr = np.array(crop.convert("L"))
    dark_in_crop = (arr < 70).sum()
    print(f"[{name}] feet crop (300,420)-(660,600): dark pixels (<70) = {dark_in_crop}")
