#!/usr/bin/env python3
"""
tools/audit_connected_components.py
落實 review.md 0-ART28r：
連通元件檢查：alpha > 40 取連通區塊，
除主體外，列出所有 >= 50px 的獨立區塊 bbox 與面積。
任何 >= 50px 的獨立區塊必須在清單中宣告其解剖結構或用途，未交代者視為破圖殘留。
"""

import os
import sys
from typing import Dict, Any, List, Tuple
from PIL import Image
import numpy as np
import scipy.ndimage

BASE_DIR = "/opt/side/bravesoul-game"
HEAD_UNITS_DIR = os.path.join(BASE_DIR, "game/assets/sprites/player/paperdoll")

RACES = ["lion", "fox", "boar", "macaque", "tiger", "crane"]

# 依 review.md 0-ART28r：除主體外經明確結構交代之 >=50px 獨立構件白名單（非瑕疵碎片）
DECLARED_COMPONENTS = {
    "lion": [
        {"desc": "右側鬃毛下垂金屬尖端", "x_range": (340, 380), "y_range": (220, 280), "cnt_range": (600, 750)},
        {"desc": "左側鬃毛下垂金屬尖端", "x_range": (130, 165), "y_range": (220, 280), "cnt_range": (450, 580)},
    ],
    "macaque": [
        {"desc": "同軸耳齒輪樞軸固定栓", "x_range": (200, 230), "y_range": (185, 210), "cnt_range": (100, 180)},
    ],
    "crane": [
        {"desc": "枕部後頸羽翎鉚釘分件", "x_range": (150, 190), "y_range": (210, 235), "cnt_range": (200, 270)},
    ],
}

def is_declared(race: str, comp: Dict[str, Any]) -> Tuple[bool, str]:
    if race not in DECLARED_COMPONENTS:
        return False, ""
    cnt = comp["count"]
    bbox = comp["bbox"]
    for dec in DECLARED_COMPONENTS[race]:
        if (dec["cnt_range"][0] <= cnt <= dec["cnt_range"][1] and
            dec["x_range"][0] <= bbox[0] and bbox[2] <= dec["x_range"][1] and
            dec["y_range"][0] <= bbox[1] and bbox[3] <= dec["y_range"][1]):
            return True, dec["desc"]
    return False, ""

def audit_file(filepath: str, race: str) -> Dict[str, Any]:
    img = Image.open(filepath)
    arr = np.array(img)
    if arr.ndim != 3 or arr.shape[2] < 4:
        return {"error": "Not RGBA"}
    
    alpha = arr[:, :, 3] > 40
    label_fn: Any = getattr(scipy.ndimage, "label")
    labeled, num_features = label_fn(alpha)
    num_features = int(num_features)
    
    components: List[Dict[str, Any]] = []
    for i in range(1, num_features + 1):
        mask = (labeled == i)
        cnt = int(np.sum(mask))
        ys, xs = np.where(mask)
        bbox: Tuple[int, int, int, int] = (
            int(np.min(xs)),
            int(np.min(ys)),
            int(np.max(xs)),
            int(np.max(ys))
        )
        components.append({"count": cnt, "bbox": bbox, "id": i})
        
    components.sort(key=lambda c: c["count"], reverse=True)
    main_body = components[0] if components else None
    
    declared_fragments = []
    undeclared_fragments = []
    small_fragments = []
    
    for c in components[1:]:
        if c["count"] >= 50:
            decl, desc = is_declared(race, c)
            if decl:
                c["desc"] = desc
                declared_fragments.append(c)
            else:
                undeclared_fragments.append(c)
        else:
            small_fragments.append(c)
    
    return {
        "path": filepath,
        "total_features": num_features,
        "main_body": main_body,
        "declared_fragments": declared_fragments,
        "undeclared_fragments": undeclared_fragments,
        "small_fragments_count": len(small_fragments)
    }

def main() -> int:
    print("=== 0-ART28r 連通元件獨立區塊稽核 (alpha > 40) ===")
    all_ok = True
    results: List[Dict[str, Any]] = []
    
    for race in RACES:
        race_head_dir = os.path.join(HEAD_UNITS_DIR, race, "head_unit")
        if not os.path.isdir(race_head_dir):
            continue
        files = sorted([f for f in os.listdir(race_head_dir) if f.endswith("_512.png")])
        for f in files:
            full_p = os.path.join(race_head_dir, f)
            res = audit_file(full_p, race)
            results.append(res)
            
            rel_p = os.path.relpath(full_p, BASE_DIR)
            mb = res["main_body"]
            mb_str = "None"
            if mb is not None:
                b = mb["bbox"]
                mb_str = f"cnt={mb['count']} bbox=x{b[0]}-{b[2]}/y{b[1]}-{b[3]}"
            
            ud: List[Dict[str, Any]] = res["undeclared_fragments"]
            dec: List[Dict[str, Any]] = res["declared_fragments"]
            status = "PASS" if len(ud) == 0 else "FAIL"
            if len(ud) > 0:
                all_ok = False
            
            print(f"[{status}] {rel_p}")
            print(f"    主體: {mb_str}")
            if dec:
                print(f"    ℹ️ 經宣告獨立結構構件: {len(dec)} 個:")
                for c in dec:
                    cb = c["bbox"]
                    print(f"       - {c['count']}px, bbox=x{cb[0]}-{cb[2]}/y{cb[1]}-{cb[3]}（{c.get('desc')}）")
            if ud:
                print(f"    ⚠️ 未交代異常獨立區塊 (>=50px): {len(ud)} 個:")
                for c in ud:
                    cb = c["bbox"]
                    print(f"       - {c['count']}px, bbox=x{cb[0]}-{cb[2]}/y{cb[1]}-{cb[3]}")
            print()

    if all_ok:
        print("✅ 全量切片 0-ART28r 連通元件稽核 PASS（無 >=50px 未宣告獨立碎片）")
        return 0
    else:
        print("❌ 存在 >=50px 未清除異常獨立區塊")
        return 1

if __name__ == "__main__":
    sys.exit(main())
