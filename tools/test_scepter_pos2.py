import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from PIL import Image
from tools.build_owl_combat_poses import place_scepter, scepter_raw

for deg in range(-35, 36, 5):
    for tx in range(24, 38, 2):
        for ty in range(55, 75, 3):
            sc = place_scepter(scepter_raw, deg=deg, target_center=(tx, ty), scale=0.95)
            bb = sc.getbbox()
            if bb and bb[0] >= 6 and bb[2] <= 122 and bb[1] >= 6 and bb[3] <= 122:
                # check if it's forward leaning
                if deg in [-25, -20, -15, 15, 20]:
                    print(f"deg={deg:+3d}, tx={tx}, ty={ty} -> bbox={bb}")
                    break
