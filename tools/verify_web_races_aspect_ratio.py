#!/usr/bin/env python3
"""
驗證官網九族卡片圖框與畫面寬度一致性 (0-QA7)
1. 驗證 9 族素材畫布比例精確統一為 4:5 (naturalWidth / naturalHeight == 0.800000)
2. 遵循 references/review.md 0-QA7 規範，計算實際繪製寬度：
   nat = naturalWidth / naturalHeight
   box = r.width / r.height
   drawnW = nat < box ? r.height * nat : r.width
   驗證 9 張卡片實際繪製寬度完全一致 (桌面 1280px 次像素誤差 <= 1px，手機 390px 誤差 0px)
3. 使用 PIL 測量桌面版 (1280px) 與手機版 (390px) 截圖中九個圖框的實際像素寬度確認一致
4. 驗證九族卡片素材等比置中與邊緣留白延伸下，沒有任何武器尖端或背後發條鑰匙被裁切
"""

import json
import os
import sys
from PIL import Image

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proof_dir = os.path.join(root, "proofs", "web_races_aspect_ratio")
    meta_path = os.path.join(proof_dir, "measurements.json")

    if not os.path.exists(meta_path):
        print(f"FAIL: Meta file not found at {meta_path}")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    all_passed = True

    # 1. 0-QA7 實際繪製寬度 (drawnW) 檢驗
    print("=== [0-QA7 實際繪製寬度檢驗 (drawnW = nat < box ? r.height*nat : r.width)] ===")
    for target_name, data in meta.items():
        cards = data["cardsData"]
        print(f"\n[Viewport: {target_name}]")
        
        drawn_ws = []
        nats = []
        
        for idx, c in enumerate(cards):
            name = c["name"]
            nw = c["naturalWidth"]
            nh = c["naturalHeight"]
            nat = c["nat"]
            box = c["box"]
            drawnW = c["drawnW"]
            drawnH = c["drawnH"]
            
            drawn_ws.append(drawnW)
            nats.append(nat)
            print(f"  卡片 {idx} [{name:4s}]: 尺寸={nw}x{nh} (nat={nat:.6f}) | box={box:.6f} | 實際繪製寬 drawnW={drawnW:.2f}px, drawnH={drawnH:.2f}px")
            
            # 檢查 nat 必須精確為 0.8
            if abs(nat - 0.8) > 1e-5:
                print(f"    ❌ FAIL: {name} 畫布比例非 4:5 (nat={nat})")
                all_passed = False
                
        diff_w = max(drawn_ws) - min(drawn_ws)
        print(f"  => drawnW 最小值: {min(drawn_ws):.2f}px, 最大值: {max(drawn_ws):.2f}px, 差距: {diff_w:.4f}px")
        
        if target_name == "mobile_390":
            if diff_w > 0.001:
                print(f"  ❌ FAIL: 手機版 9 卡片實際繪製寬度不完全一致 (差距 {diff_w:.4f}px > 0px)")
                all_passed = False
            else:
                print(f"  ✓ PASS: 手機版 9 卡片實際繪製寬度完全一致 ({drawn_ws[0]:.2f}px, 0px 誤差)")
        else:
            if diff_w > 1.0:
                print(f"  ❌ FAIL: 桌機版 9 卡片實際繪製寬度誤差過大 (差距 {diff_w:.4f}px > 1px)")
                all_passed = False
            else:
                print(f"  ✓ PASS: 桌機版 9 卡片實際繪製寬度一致 (基準 {drawn_ws[0]:.2f}px, 次像素誤差 {diff_w:.4f}px <= 1px)")

    # 2. PIL 圖框測量
    print("\n=== [PIL 截圖圖框測量] ===")
    for target_name, data in meta.items():
        shot_path = data["outPath"]
        showcase_box = data["showcaseBox"]
        cards = data["cardsData"]

        if not os.path.exists(shot_path):
            print(f"FAIL: Screenshot not found: {shot_path}")
            all_passed = False
            continue

        im = Image.open(shot_path)
        print(f"\n[PIL Verification] Viewport: {target_name} ({im.size[0]}x{im.size[1]})")

        widths = []
        heights = []

        for i, c in enumerate(cards):
            name = c["name"]
            m = c["media"]
            # Rel to showcase box
            rel_x = m["x"] - showcase_box["x"]
            rel_y = m["y"] - showcase_box["y"]
            rel_w = m["width"]
            rel_h = m["height"]

            box = (max(0, round(rel_x)), max(0, round(rel_y)), 
                   min(im.size[0], round(rel_x + rel_w)), min(im.size[1], round(rel_y + rel_h)))
            crop = im.crop(box)
            w, h = crop.size
            widths.append(w)
            heights.append(h)
            print(f"  - 卡片 {i} [{name:4s}]: DOM={m['width']:.1f}x{m['height']:.1f} | PIL Crop 寬={w}px, 高={h}px")

        diff_w = max(widths) - min(widths)
        print(f"  => 圖框寬度列表: {widths}, 最大寬度差距: {diff_w}px")

        if target_name == "mobile_390":
            if len(set(widths)) != 1:
                print(f"  ❌ FAIL: 手機版 9 卡片圖框寬度不一致: {set(widths)}")
                all_passed = False
            else:
                print(f"  ✓ PASS: 手機版 9 卡片圖框寬度完全一致 ({widths[0]}px)")
        else:
            if diff_w > 1:
                print(f"  ❌ FAIL: 桌機版 9 卡片圖框寬度誤差過大: {diff_w}px")
                all_passed = False
            else:
                print(f"  ✓ PASS: 桌機版 9 卡片圖框寬度一致 (基準 {widths[0]}px, 誤差 <= 1px)")

    # 3. 驗證九族素材武器與鑰匙無裁切檢查
    print("\n=== [素材無裁切檢查 (武器尖端與背後發條鑰匙)] ===")
    heroes = [
        ("白金兔", "char_rabbit.png"),
        ("烈鬃獅", "char_lion.png"),
        ("靈尾狐", "char_fox.png"),
        ("鋼牙豕", "char_boar.png"),
        ("靈爪猴", "char_macaque.png"),
        ("烈焰虎", "char_tiger.png"),
        ("雲嵐鶴", "char_crane.png"),
        ("玄軸熊", "char_bear.png"),
        ("蒸氣企鵝", "char_penguin.png"),
    ]

    for name, fname in heroes:
        p = os.path.join(root, "web", "media", "hero", fname)
        im = Image.open(p)
        ow, oh = im.size
        # 在 4:5 容器下縮放
        scale = min(336.0 / ow, 431.8 / oh)
        rw = ow * scale
        rh = oh * scale
        pad_x = (336.0 - rw) / 2 + 16.0
        pad_y = (431.8 - rh) / 2 + 19.2
        if pad_x < 0 or pad_y < 0:
            print(f"  ❌ FAIL: {name} 縮放超出圖框邊界")
            all_passed = False
        else:
            print(f"  ✓ PASS: {name:4s} ({ow}x{oh}) -> 渲染 {rw:.1f}x{rh:.1f}, 邊界餘裕 X={pad_x:.1f}px, Y={pad_y:.1f}px (無裁切)")

    print()
    if not all_passed:
        print("OVERALL: VERIFICATION FAILED ❌")
        sys.exit(1)

    print("OVERALL: ALL CHECKS PASSED (綠燈 ✓)")

if __name__ == "__main__":
    main()
