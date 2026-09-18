#!/usr/bin/env python3
"""
驗證 0-ART28r 連通元件檢查：
alpha > 40 取連通區塊，檢查是否有 >= 50px 的孤立雜物。
"""

import os
import sys
sys.path.append("/opt/side/bravesoul-game/tools")
from audit_connected_components import audit_file

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"
PROOFS_DIR = f"{REPO_ROOT}/proofs/head_sync_proofs"

target_files = [
    # Chassis 128 & 512
    f"{BEAR_DIR}/chassis/paint_bear_amber.png",
    f"{BEAR_DIR}/chassis/paint_bear_amber_512.png",
    f"{BEAR_DIR}/chassis/paint_iron_quarry.png",
    f"{BEAR_DIR}/chassis/paint_iron_quarry_512.png",
    f"{BEAR_DIR}/chassis/paint_ivory_stock.png",
    f"{BEAR_DIR}/chassis/paint_ivory_stock_512.png",
    # Head unit
    f"{BEAR_DIR}/head_unit/head_iron_bear_amber_512.png",
    f"{BEAR_DIR}/head_unit/head_iron_bear_quarry_512.png",
    f"{BEAR_DIR}/head_unit/head_iron_bear_stock_512.png",
    # Weapon 128 & 512
    f"{BEAR_DIR}/weapon/wpn_eccentric_gyro_sledge.png",
    f"{BEAR_DIR}/weapon/wpn_eccentric_gyro_sledge_512.png",
    # Composites
    f"{PROOFS_DIR}/composite_512_bear_amber.png",
    f"{PROOFS_DIR}/composite_512_bear_quarry.png",
]

print("=== 0-ART28r 連通元件檢查執行 ===")
all_pass = True

for path in target_files:
    res = audit_file(path, "bear")
    rel = os.path.relpath(path, REPO_ROOT)
    mb = res["main_body"]
    mb_str = f"cnt={mb['count']}, bbox={mb['bbox']}" if mb else "None"
    fg = res["undeclared_fragments"]
    
    # 注意：合成圖 composite 含有合法的微型發條無人機 (5002px)，其他切片皆應為 0
    is_composite = "composite" in path
    if is_composite:
        unexpected = [c for c in fg if not (c["bbox"][0] > 380 and c["bbox"][1] < 160)]
    else:
        unexpected = fg
        
    status = "PASS" if len(unexpected) == 0 else "FAIL"
    if len(unexpected) > 0:
        all_pass = False
        
    print(f"[{status}] {rel}")
    print(f"    主體: {mb_str}")
    print(f"    未宣告獨立碎片 (>=50px): {len(unexpected)} 個")
    for c in unexpected:
        print(f"       - {c['count']}px, bbox={c['bbox']}")
    print(f"    微小碎片 (<50px): {res['small_fragments_count']} 個")
    print()

if all_pass:
    print("✅ 0-ART28r 連通元件檢查全數通過！無任何 >=50px 未宣告孤立雜物。")
    sys.exit(0)
else:
    print("❌ 存在未預期之孤立雜物！")
    sys.exit(1)
