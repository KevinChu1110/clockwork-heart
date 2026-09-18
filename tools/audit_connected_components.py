#!/usr/bin/env python3
"""
tools/audit_connected_components.py
落實 review.md 0-ART28r：
連通元件檢查：alpha > 40 取連通區塊，
除主體外，列出所有 >= 50px 的獨立區塊 bbox 與面積。
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

def audit_file(filepath: str) -> Dict[str, Any]:
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
    fragments_gte_50 = [c for c in components[1:] if c["count"] >= 50]
    small_fragments = [c for c in components[1:] if c["count"] < 50]
    
    return {
        "path": filepath,
        "total_features": num_features,
        "main_body": main_body,
        "fragments_gte_50": fragments_gte_50,
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
            res = audit_file(full_p)
            results.append(res)
            
            rel_p = os.path.relpath(full_p, BASE_DIR)
            mb = res["main_body"]
            mb_str = "None"
            if mb is not None:
                b = mb["bbox"]
                mb_str = f"cnt={mb['count']} bbox=x{b[0]}-{b[2]}/y{b[1]}-{b[3]}"
            
            fg: List[Dict[str, Any]] = res["fragments_gte_50"]
            status = "PASS" if len(fg) == 0 else "FAIL"
            if len(fg) > 0:
                all_ok = False
            
            print(f"[{status}] {rel_p}")
            print(f"    主體: {mb_str}")
            if fg:
                print(f"    ⚠️ 異常獨立區塊 (>=50px): {len(fg)} 個:")
                for c in fg:
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
