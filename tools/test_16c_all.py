from PIL import Image
import numpy as np

def check_16c(path: str) -> None:
    im = Image.open(path).convert("L")
    arr = np.array(im)
    h, w = arr.shape
    dark_cnt = (arr < 70).sum(axis=1)
    max_band = 0
    bad_rows = []
    for y in range(h):
        frac = y / float(h)
        if 0.35 <= frac <= 0.55:
            max_band = max(max_band, dark_cnt[y])
            if dark_cnt[y] > w * 0.35:
                bad_rows.append(y)
    print(f"[{path}] 16c chest (35%-55%): max dark pixels in row = {max_band}px (threshold > {int(w*0.35)}px), bad rows = {len(bad_rows)}")

for p in [
    "screenshots/proof_battle_full_screen.png",
    "screenshots/proof_battle_attack_full_screen.png",
    "screenshots/proof_battle_equipped_royal_parade.png",
    "screenshots/proof_battle_equipped_steam_artisan.png",
    "screenshots/proof_battle_attack_sword.png"
]:
    check_16c(p)
