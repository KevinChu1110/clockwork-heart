import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
from tools.build_owl_combat_poses import place_scepter, scepter_raw

for deg in [10, 15, 20, 24]:
    for tx in [28, 30, 32, 34]:
        for ty in [65, 68, 70, 72]:
            sc = place_scepter(scepter_raw, deg=deg, target_center=(tx, ty), scale=1.0)
            bb = sc.getbbox()
            if bb and bb[0] >= 6 and bb[2] <= 122 and bb[1] >= 6 and bb[3] <= 122:
                print(f"OK: deg={deg}, tx={tx}, ty={ty} -> bbox={bb}")
