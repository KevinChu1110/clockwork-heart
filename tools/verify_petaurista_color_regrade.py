#!/usr/bin/env python3
"""
verify_petaurista_color_regrade.py
Quantitative verification script for task t_8d0dcd82:
第五十八族嵐翼鼯鼠(petaurista) 128px 七槽切片色階重繪（0-ART6 上游追修）

Verifies all 6 acceptance criteria:
1. chassis 128 唯一色數 >= 150，七槽每槽 c/100px >= 5
2. alpha 階數 > 2（有抗鋸齒）
3. proof composite 唯一色數 >= 300
4. 內部 flood-fill 破洞 <= 5px，head_unit 對 chassis 同座標同色 < 10%
5. proof composite 對出貨切片重合成 diff bbox = None
6. Godot tests (checked separately or invoked here)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageChops
from scipy.ndimage import binary_fill_holes

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PETAURISTA_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/petaurista"

SLICES = [
    ("winding_key", "key_petaurista_three_leaf_windchime_brass"),
    ("back_curio", "curio_petaurista_bamboo_weave_rudder_tail"),
    ("chassis", "chassis_petaurista_lacquered_bamboo_default"),
    ("head_unit", "head_petaurista_zen_bamboo_ninja_cowl"),
    ("costume", "costume_petaurista_folding_glider_wing_harness"),
    ("optic_core", "face_petaurista_obsidian_goggle_cinnabar_mask"),
    ("weapon", "weapon_petaurista_zen_octagonal_bamboo_dart")
]

def verify():
    print("=== VERIFYING PETAURISTA 128PX COLOR REGRADE (t_8d0dcd82) ===")
    all_ok = True

    # 1 & 2: Slices metrics
    loaded_slices = {}
    print("\n--- 1. 七槽 128px 切片色彩豐富度與抗鋸齒查驗 ---")
    for slot, item_id in SLICES:
        path = f"{PETAURISTA_PD}/{slot}/{item_id}.png"
        im = Image.open(path).convert("RGBA")
        loaded_slices[slot] = im
        arr = np.array(im)
        alpha = arr[:, :, 3]
        op = arr[alpha > 0]
        u = len(np.unique(op[:, :3], axis=0))
        alphas = len(np.unique(alpha))
        c100 = (u / len(op)) * 100.0 if len(op) > 0 else 0

        c100_pass = (c100 >= 5.0)
        alpha_pass = (alphas > 2)
        if slot == "chassis":
            ch_pass = (u >= 150)
            if not ch_pass:
                all_ok = False
            status = f"{'✓ PASS' if (c100_pass and alpha_pass and ch_pass) else '❌ FAIL'}"
        else:
            status = f"{'✓ PASS' if (c100_pass and alpha_pass) else '❌ FAIL'}"

        if not (c100_pass and alpha_pass):
            all_ok = False

        print(f"  [{slot:<12}] px: {len(op):4d}, unique_rgb: {u:3d}, c/100px: {c100:5.2f}% (>=5%), alphas: {alphas:2d} (>2) -> {status}")

    # Check chassis >= 150 specifically
    ch_u = len(np.unique(np.array(loaded_slices["chassis"])[np.array(loaded_slices["chassis"])[:, :, 3] > 0][:, :3], axis=0))
    print(f"\n  Chassis 128 唯一色數: {ch_u} >= 150 -> {'✓ PASS' if ch_u >= 150 else '❌ FAIL'}")

    # 3. Proof composite unique colors >= 300
    comp_path = f"{PETAURISTA_PD}/proof_paperdoll_petaurista_composite.png"
    comp_im = Image.open(comp_path).convert("RGBA")
    comp_arr = np.array(comp_im)
    comp_op = comp_arr[comp_arr[:, :, 3] > 0]
    comp_u = len(np.unique(comp_op[:, :3], axis=0))
    comp_pass = (comp_u >= 300)
    if not comp_pass:
        all_ok = False
    print(f"\n--- 2. Proof Composite 色彩豐富度 (>= 300) ---")
    print(f"  Composite 唯一色數: {comp_u} (>= 300) -> {'✓ PASS' if comp_pass else '❌ FAIL'}")

    # 4. Internal flood-fill holes <= 5px and Head vs Chassis overlap
    print(f"\n--- 3. 內部破洞與圖層獨立性查驗 ---")
    core_mask = comp_arr[35:95, 42:86, 3] > 8
    filled_core = np.asarray(binary_fill_holes(core_mask), dtype=bool)
    num_holes = int(np.sum(filled_core & (~core_mask)))
    hole_pass = (num_holes <= 5)
    if not hole_pass:
        all_ok = False
    print(f"  內部 flood-fill 破洞: {num_holes} px (<= 5px) -> {'✓ PASS' if hole_pass else '❌ FAIL'}")

    head_arr = np.array(loaded_slices["head_unit"])
    ch_arr = np.array(loaded_slices["chassis"])
    overlap_mask = (head_arr[:, :, 3] > 0) & (ch_arr[:, :, 3] > 0)
    overlap_total = int(np.sum(overlap_mask))
    if overlap_total > 0:
        same_color = np.all(head_arr[:, :, :3] == ch_arr[:, :, :3], axis=2) & overlap_mask
        same_count = int(np.sum(same_color))
        same_pct = (same_count / overlap_total) * 100.0
        overlap_pass = (same_pct < 10.0)
        if not overlap_pass:
            all_ok = False
        print(f"  head_unit 對 chassis 同座標同色: {same_count}/{overlap_total} ({same_pct:.2f}% < 10%) -> {'✓ PASS' if overlap_pass else '❌ FAIL'}")
    else:
        print("  head_unit 對 chassis 重疊: 0 px -> ✓ PASS")

    # 5. Proof composite vs Slices recomp diff bbox = None
    print(f"\n--- 4. Proof Composite 對出貨切片重合成查驗 ---")
    recomp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for slot, _ in SLICES:
        recomp.alpha_composite(loaded_slices[slot])

    diff = ImageChops.difference(comp_im, recomp)
    diff_bbox = diff.getbbox()
    diff_pass = (diff_bbox is None)
    if not diff_pass:
        all_ok = False
    print(f"  Composite vs 重合成 diff bbox: {diff_bbox} (None) -> {'✓ PASS' if diff_pass else '❌ FAIL'}")

    print("\n" + ("🎉 ALL 5 IMAGE QUANTITATIVE ACCEPTANCE CRITERIA PASSED!" if all_ok else "❌ SOME CHECKS FAILED!"))
    return all_ok

if __name__ == "__main__":
    ok = verify()
    sys.exit(0 if ok else 1)
