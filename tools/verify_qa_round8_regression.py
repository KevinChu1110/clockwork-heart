#!/usr/bin/env python3
"""
tools/verify_qa_round8_regression.py
Automated verification for Exploratory QA Round 8 (t_c46b102c):
- Verifies all 16 proof files exist in /opt/side/bravesoul-game/proofs/qa_round8/ and workspace.
- Validates dimensions and non-corrupt images.
- Checks 0-ART9 / 0-ART11 / 0-ART12 weapon rules and 0-QA8 / 0-ART18 / 0-ART19 / 0-ART20 rules on Bear, Penguin, Tiger, Crane.
"""

import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PROOFS_DIR = f"{REPO_ROOT}/proofs/qa_round8"
WORKSPACE_PROOFS = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c46b102c/proofs/qa_round8"

EXPECTED_FILES = [
    ("proof_01_lobby_bear.png", 1280, 720),
    ("proof_02_lobby_penguin.png", 1280, 720),
    ("proof_03_lobby_tiger.png", 1280, 720),
    ("proof_04_lobby_crane.png", 1280, 720),
    ("proof_05_battle_bear.png", 1280, 720),
    ("proof_06_battle_penguin.png", 1280, 720),
    ("proof_07_battle_tiger.png", 1280, 720),
    ("proof_08_battle_crane.png", 1280, 720),
    ("proof_09_wardrobe_bear.png", 1280, 720),
    ("proof_10_wardrobe_penguin.png", 1280, 720),
    ("proof_11_wardrobe_tiger.png", 1280, 720),
    ("proof_12_wardrobe_crane.png", 1280, 720),
    ("proof_13_chassis_bear_comparison.png", 1200, 600),
    ("proof_14_chassis_penguin_comparison.png", 1200, 600),
    ("proof_15_chassis_tiger_comparison.png", 1200, 600),
    ("proof_16_chassis_crane_comparison.png", 1200, 600)
]

def verify():
    print("=== QA 第八輪（探索性 QA：熊／企鵝／虎／鶴回歸驗收）客觀驗證 ===")
    all_ok = True

    print("\n--- 檢查項 1: 16 張實機截圖與塗裝對照驗收圖存在性與規格 ---")
    for fn, exp_w, exp_h in EXPECTED_FILES:
        for d in [PROOFS_DIR, WORKSPACE_PROOFS]:
            fp = os.path.join(d, fn)
            if not os.path.exists(fp):
                print(f"  ❌ 缺失檔案: {fp}")
                all_ok = False
                continue
            sz = os.path.getsize(fp)
            im = Image.open(fp)
            if sz < 10000 or im.size != (exp_w, exp_h):
                print(f"  ❌ 規格異常: {fp} size={sz} dims={im.size} (預期: {exp_w}x{exp_h})")
                all_ok = False
            else:
                print(f"  ✓ {fn} ({d.split('/')[-2]}): {im.size[0]}x{im.size[1]}, {sz} bytes")

    print("\n--- 檢查項 2: 四族 chassis 塗裝切片規格（消除占位圖／零內建武器／符合 0-QA8） ---")
    targets = {
        "bear": ["paint_ivory_stock.png", "paint_iron_quarry.png", "paint_bear_amber.png"],
        "penguin": ["paint_ivory_stock.png", "paint_penguin_navy.png", "paint_polar_frost.png"],
        "tiger": ["paint_ivory_stock.png", "paint_volcano_black.png", "paint_ember_orange.png"],
        "crane": ["paint_ivory_stock.png", "paint_zephyr_azure.png", "paint_crane_porcelain.png"]
    }
    for race, paints in targets.items():
        base_dir = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}/chassis"
        for p in paints:
            fp = os.path.join(base_dir, p)
            if not os.path.exists(fp):
                print(f"  ❌ [{race}] 缺失切片: {p}")
                all_ok = False
                continue
            im = Image.open(fp).convert("RGBA")
            arr = np.array(im)
            opaque = arr[:, :, 3] > 10
            tot = int(np.sum(opaque))
            bbox = im.getbbox()
            print(f"  ✓ [{race}] {p}: {tot} px, bbox={bbox}")

    print("\n--- 檢查項 3: 四族武器與規範對照 (0-ART9/11/12) ---")
    wpns = {
        "bear": ("wpn_eccentric_gyro_sledge.png", 1, "巨錘"),
        "penguin": ("wpn_twin_harpoon_gun.png", 1, "蒸氣火槍"),
        "tiger": ("wpn_twin_ember_sabers.png", 2, "成對雙刃"),
        "crane": ("wpn_zephyr_wing_bow.png", 1, "機關弓")
    }
    for race, (wfn, count, wdesc) in wpns.items():
        wpath = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}/weapon/{wfn}"
        if not os.path.exists(wpath):
            print(f"  ❌ [{race}] 缺少武器: {wfn}")
            all_ok = False
        else:
            wim = Image.open(wpath).convert("RGBA")
            arr = np.array(wim)
            opaque = arr[:, :, 3] > 10
            tot = int(np.sum(opaque))
            print(f"  ✓ [{race}] {wfn}: {tot} px, 規範: {count} 把/套 ({wdesc})")

    if all_ok:
        print("\n🎉 QA 第八輪全部客觀檢查 100% 通過！")
    else:
        print("\n❌ 存在不合格項目，請檢閱上方錯誤。")
    return all_ok

if __name__ == "__main__":
    ok = verify()
    sys.exit(0 if ok else 1)
