import os
from PIL import Image

races = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin"]
poses = ["attack", "hit", "skill", "telegraph", "recover"]
base = "game/assets/sprites/player/poses"

all_ok = True
total = 0

for r in races:
    for p in poses:
        if r == "rabbit":
            # Test both root and rabbit/
            candidates = [
                os.path.join(base, f"{p}_512.png"),
                os.path.join(base, "rabbit", f"{p}_512.png"),
            ]
        else:
            candidates = [os.path.join(base, r, f"{p}_512.png")]

        for path in candidates:
            total += 1
            if not os.path.exists(path):
                print(f"FAIL: Missing {path}")
                all_ok = False
                continue
            import_path = f"{path}.import"
            if not os.path.exists(import_path):
                print(f"FAIL: Missing import {import_path}")
                all_ok = False
                continue
            with Image.open(path) as im:
                if im.size != (512, 512):
                    print(f"FAIL: {path} size is {im.size}, expected (512, 512)")
                    all_ok = False
                if im.mode != "RGBA":
                    print(f"FAIL: {path} mode is {im.mode}, expected RGBA")
                    all_ok = False

if all_ok:
    print(f"ALL_POSES_512_OK: verified {total} files (512x512, RGBA, .import present).")
else:
    print("POSES_512_FAIL")
