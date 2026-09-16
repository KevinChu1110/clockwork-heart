#!/usr/bin/env python3
import json
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

def verify():
    print("=== VERIFYING ALL CLOUD CRANE & IRON BEAR OFFICIAL ASSETS ===")
    
    races = [
        ("crane", "cloud_crane"),
        ("bear", "iron_bear")
    ]
    
    all_ok = True
    for rid, full_name in races:
        print(f"\n--- Checking race: {rid} ({full_name}) ---")
        required_assets = [
            # Category 1: 官網英雄圖
            (f"branding/char_{rid}.png", [(400, 840), (800, 1680), (1344, 1680)], ["RGB", "RGBA"]),
            (f"web/media/hero/char_{rid}.png", [(400, 840), (1344, 1680)], ["RGB", "RGBA"]),
            (f"docs/art/char_{rid}_candidate_400x840.png", (400, 840), ["RGB", "RGBA"]),
            (f"docs/art/{full_name}_concept.png", None, ["RGB", "RGBA"]),
            
            # Category 2: 戰鬥特寫
            (f"game/assets/sprites/player/{rid}_battle.png", (128, 128), ["RGBA"]),
            
            # Category 3: 行走動畫
            (f"game/assets/sprites/player/{rid}_walk_0.png", (64, 64), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_1.png", (64, 64), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_2.png", (64, 64), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_3.png", (64, 64), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_0_x3.png", (128, 128), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_1_x3.png", (128, 128), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_2_x3.png", (128, 128), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_walk_3_x3.png", (128, 128), ["RGBA"]),
            
            # Mirror idle assets
            (f"game/assets/sprites/player/{rid}_idle.png", (64, 64), ["RGBA"]),
            (f"game/assets/sprites/player/{rid}_idle_x3.png", (128, 128), ["RGBA"]),
            (f"game/assets/sprites/player/party/{rid}_idle.png", (128, 128), ["RGBA"]),
            (f"web/media/hero/{rid}_idle.png", (128, 128), ["RGBA"]),
            
            # Category 4: HUD 戰鬥頭像 與 對話框半身像
            (f"game/assets/sprites/portraits/{rid}.png", (128, 128), ["RGBA"]),
            (f"game/assets/sprites/portraits/{full_name}.png", (384, 480), ["RGBA"]),
        ]
        
        for rel_path, expected_size, allowed_modes in required_assets:
            full_path = f"{REPO_ROOT}/{rel_path}"
            if not os.path.exists(full_path):
                print(f"  ❌ MISSING ASSET: {rel_path}")
                all_ok = False
                continue
            im = Image.open(full_path)
            valid_sizes = expected_size if isinstance(expected_size, list) else [expected_size]
            if expected_size is not None and im.size not in valid_sizes:
                print(f"  ❌ WRONG SIZE {im.size} vs {expected_size} for {rel_path}")
                all_ok = False
                continue
            if im.mode not in allowed_modes:
                print(f"  ❌ WRONG MODE {im.mode} vs {allowed_modes} for {rel_path}")
                all_ok = False
                continue
            bbox = im.getbbox()
            if bbox is None:
                print(f"  ❌ EMPTY ASSET: {rel_path}")
                all_ok = False
                continue
            print(f"  ✓ {rel_path:52s} size={im.size} mode={im.mode} bbox={bbox}")

    if all_ok:
        print("\n✓ ALL CRANE & BEAR ASSETS EXIST AND VERIFIED SUCCESSFULLY!")
    else:
        print("\n❌ SOME ASSETS FAILED VERIFICATION!")
        exit(1)

if __name__ == "__main__":
    verify()
