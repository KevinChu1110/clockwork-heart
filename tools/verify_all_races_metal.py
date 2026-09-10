#!/usr/bin/env python3
import os
from PIL import Image

def measure_metal(proof_dir="/opt/side/bravesoul-game/proofs/combat_feel"):
    repo = "/opt/side/bravesoul-game"
    scale = 200.0 / 128.0
    ox = 224.0
    oy = 248.0 # 223.0 + (250.0 - 200.0) / 2.0

    races = {
        "rabbit": {
            "name": "兔族 晨曦長劍 (刃身)",
            "idle": f"{repo}/game/assets/sprites/player/poses/idle.png",
            "screen": f"{proof_dir}/rabbit_battle_idle.png",
            "box": (60, 70, 80, 96),
        },
        "lion": {
            "name": "獅族 騎士長槍 (槍杆)",
            "idle": f"{repo}/game/assets/sprites/player/poses/lion/idle.png",
            "screen": f"{proof_dir}/lion_battle_idle.png",
            "box": (38, 85, 55, 116),
        },
        "fox": {
            "name": "狐族 星芒法杖 (杖身)",
            "idle": f"{repo}/game/assets/sprites/player/poses/fox/idle.png",
            "screen": f"{proof_dir}/fox_battle_idle.png",
            "box": (35, 58, 48, 72),
        },
        "boar": {
            "name": "野豬族 鐵砧巨鎚 (鎚頭)",
            "idle": f"{repo}/game/assets/sprites/player/poses/boar/idle.png",
            "screen": f"{proof_dir}/boar_battle_idle.png",
            "box": (38, 75, 55, 105),
        },
    }

    results = {}
    all_pass = True

    for race_key, data in races.items():
        if not os.path.exists(data["idle"]):
            print(f"Missing idle file: {data['idle']}")
            continue
        if not os.path.exists(data["screen"]):
            print(f"Missing screen file: {data['screen']}")
            continue

        im = Image.open(data["idle"]).convert("RGBA")
        sc = Image.open(data["screen"]).convert("RGB")

        bx0, by0, bx1, by1 = data["box"]
        source_pts = []
        for y in range(by0, by1 + 1):
            for x in range(bx0, bx1 + 1):
                r, g, b, a = im.getpixel((x, y))
                if a > 128 and r > 195 and g > 195 and b > 195 and abs(r - b) < 40:
                    source_pts.append((x, y))

        silvers = 0
        browns = 0
        rgbs = []
        for x, y in source_pts:
            sx = int(round(ox + (x + 0.5) * scale))
            sy = int(round(oy + (y + 0.5) * scale))
            sr, sg, sb = sc.getpixel((sx, sy))
            rgbs.append((sr, sg, sb))
            if sr > 185 and sg > 185 and sb > 185 and abs(sr - sb) < 40:
                silvers += 1
            if sr - sb > 50:
                browns += 1

        n = len(source_pts)
        silv_pct = (silvers / n * 100.0) if n > 0 else 0.0
        brn_pct = (browns / n * 100.0) if n > 0 else 0.0
        avg_r = sum(c[0] for c in rgbs) / n if n > 0 else 0.0
        avg_g = sum(c[1] for c in rgbs) / n if n > 0 else 0.0
        avg_b = sum(c[2] for c in rgbs) / n if n > 0 else 0.0

        is_passed = (silv_pct >= 70.0 and brn_pct <= 15.0)
        if not is_passed:
            all_pass = False

        results[race_key] = {
            "name": data["name"],
            "count": n,
            "silvers": silvers,
            "silver_pct": silv_pct,
            "browns": browns,
            "brown_pct": brn_pct,
            "avg_rgb": (avg_r, avg_g, avg_b),
            "pass": is_passed,
        }

        status_str = "PASS" if is_passed else "FAIL"
        print(f"[{race_key.upper()}] {data['name']} ({n} 點):")
        print(f"  Silver (>=70%): {silvers}/{n} ({silv_pct:.1f}%) | Warm/Brown (<=15%): {browns}/{n} ({brn_pct:.1f}%) | Avg RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f}) -> [{status_str}]")

    print(f"\nOVERALL RESULT: {'ALL PASS' if all_pass else 'FAIL'}")
    return results, all_pass

if __name__ == "__main__":
    measure_metal()
