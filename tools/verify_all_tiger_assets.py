#!/usr/bin/env python3
import json
import os
import re
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

def verify():
    print("=== VERIFYING ALL EMBER TIGER ASSETS ===")
    
    # 1. Check all required assets exist, correct format, mode and size
    required_assets = [
        # Category 1: 官網英雄圖
        ("branding/char_tiger.png", [(400, 840), (800, 1680), (1344, 1680)], ["RGB", "RGBA"]),
        ("web/media/hero/char_tiger.png", [(400, 840), (1344, 1680)], ["RGB", "RGBA"]),
        ("docs/art/char_tiger_candidate_400x840.png", (400, 840), ["RGB", "RGBA"]),
        ("docs/art/ember_tiger_concept.png", (928, 1152), ["RGB", "RGBA"]),
        
        # Category 2: 戰鬥特寫
        ("game/assets/sprites/player/tiger_battle.png", (128, 128), ["RGBA"]),
        
        # Category 3: 行走動畫
        ("game/assets/sprites/player/tiger_walk_0.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_1.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_2.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_3.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_0_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_1_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_2_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/tiger_walk_3_x3.png", (128, 128), ["RGBA"]),
        
        # Mirror idle assets
        ("game/assets/sprites/player/tiger_idle.png", (64, 64), ["RGBA"]),
        ("game/assets/sprites/player/tiger_idle_x3.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/player/party/tiger_idle.png", (128, 128), ["RGBA"]),
        ("web/media/hero/tiger_idle.png", (128, 128), ["RGBA"]),
        
        # Category 4: HUD 戰鬥頭像 與 對話框半身像
        ("game/assets/sprites/portraits/tiger.png", (128, 128), ["RGBA"]),
        ("game/assets/sprites/portraits/ember_tiger.png", (384, 480), ["RGBA"]),
    ]
    
    for rel_path, expected_size, allowed_modes in required_assets:
        full_path = f"{REPO_ROOT}/{rel_path}"
        assert os.path.exists(full_path), f"MISSING ASSET: {full_path}"
        im = Image.open(full_path)
        valid_sizes = expected_size if isinstance(expected_size, list) else [expected_size]
        assert im.size in valid_sizes, f"WRONG SIZE {im.size} vs {expected_size} for {rel_path}"
        assert im.mode in allowed_modes, f"WRONG MODE {im.mode} vs {allowed_modes} for {rel_path}"
        bbox = im.getbbox()
        assert bbox is not None, f"COMPLETELY EMPTY: {rel_path}"
        print(f"  ✓ {rel_path:52s} size={im.size} mode={im.mode} bbox={bbox}")
        
    # 2. Check paperdoll_slots.json existing list
    with open(f"{REPO_ROOT}/docs/design/paperdoll_slots.json", "r", encoding="utf-8") as f:
        doc_data = json.load(f)
        
    tiger_doc = None
    for r in doc_data["races_specification"]["races"]:
        if r["race_id"] == "tiger":
            tiger_doc = r
            break
    assert tiger_doc is not None
    
    existing_items = tiger_doc["asset_naming_conventions"]["status"]["existing"]
    print(f"\nChecking {len(existing_items)} existing entries for tiger:")
    for item in existing_items:
        clean_item = item.split(" (")[0]
        # expand wildcard if any
        if "{0..3}" in clean_item:
            paths = [clean_item.replace("{0..3}", str(i)) for i in range(4)]
        elif "{slot_id}/{item_id}" in clean_item:
            paths = [
                "game/assets/sprites/player/paperdoll/tiger/chassis/paint_ember_orange.png",
                "game/assets/sprites/player/paperdoll/tiger/head_unit/head_ember_tiger_stock.png",
                "game/assets/sprites/player/paperdoll/tiger/winding_key/key_turbine_flame.png",
                "game/assets/sprites/player/paperdoll/tiger/costume/costume_ember_tunic.png",
                "game/assets/sprites/player/paperdoll/tiger/optic_core/core_molten_amber.png",
                "game/assets/sprites/player/paperdoll/tiger/weapon/wpn_twin_ember_sabers.png",
                "game/assets/sprites/player/paperdoll/tiger/back_curio/curio_exhaust_tiger_tail.png",
            ]
        else:
            paths = [clean_item]
            
        for p in paths:
            fp = f"{REPO_ROOT}/{p}"
            assert os.path.exists(fp), f"Existing entry missing on disk: {fp}"
            print(f"  ✓ Existing on disk: {p}")
            
    print("\n✓ ALL 19 ASSETS EXIST AND VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    verify()
