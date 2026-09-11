from PIL import Image
import numpy as np

for name in [
    "/opt/side/bravesoul-game/proofs/combat_feel/boar_battle_idle.png",
    "/opt/side/bravesoul-game/screenshots/proof_battle_full_screen.png",
    "/opt/side/bravesoul-game/screenshots/proof_battle_equipped_royal_parade.png",
    "/opt/side/bravesoul-game/screenshots/proof_battle_equipped_steam_artisan.png",
    "/opt/side/bravesoul-game/screenshots/proof_battle_attack_sword.png"
]:
    im = Image.open(name)
    arr = np.array(im.convert('L'))
    print(f"File: {name}, Size: {im.size}")
    dark = (arr < 70)
    dark_counts = dark.sum(axis=1)
    bad_rows = []
    for y in range(im.size[1]):
        if dark_counts[y] > im.size[0] * 0.35 and 0.35 <= y / im.size[1] <= 0.55:
            bad_rows.append((y, dark_counts[y]))
    if bad_rows:
        print(f"  FAILED 16c: found {len(bad_rows)} rows in 35%-55% height with > 35% dark pixels! First: {bad_rows[0]}, Last: {bad_rows[-1]}")
    else:
        print("  PASSED 16c: no dark band in 35%-55% height.")
