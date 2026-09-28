#!/usr/bin/env python3
"""0-QA30 逐項比對驗證腳本：熱流赤鳶 (kite)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. kite 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 42 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. kite 7 大部件目錄與 poses/kite 目錄存在且恪守零佔位圖（僅有 .gitkeep）
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 逐項比對驗證 (kite) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 kite 規格
kite_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "kite":
        kite_table = r

assert kite_table is not None, "正表未找到 kite 定義！"
assert table_d["races_specification"]["total_races"] == 42, f"total_races 應為 42，實際為 {table_d['races_specification']['total_races']}"
print(f"✓ 2. 正表 kite 規格就緒: {kite_table['name_zh']} ({kite_table['name_en']}), total_races=42")
print(f"   race_id: {kite_table['race_id']}")
print(f"   aliases: {kite_table['aliases']}")

# 3. 驗證 fallback 表
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

fallback_races_map = {}
for line in gd_content.splitlines():
    m = re.search(r'\{\s*"race_id":\s*"([^"]+)"', line)
    if m:
        rid = m.group(1)
        m_al = re.search(r'"aliases":\s*(\[[^\]]*\])', line)
        if m_al:
            aliases = json.loads(m_al.group(1))
        else:
            aliases = []
        fallback_races_map[rid] = aliases

assert len(table_races_map) == 42, f"正表種族數應為 42，實際為 {len(table_races_map)}"
assert len(fallback_races_map) == 42, f"fallback 表種族數應為 42，實際為 {len(fallback_races_map)}"

diffs = []
for rid, t_aliases in table_races_map.items():
    if rid not in fallback_races_map:
        diffs.append(f"fallback 缺少種族: {rid}")
    elif sorted(t_aliases) != sorted(fallback_races_map[rid]):
        diffs.append(f"種族 {rid} aliases 分歧: 正表={t_aliases} vs fallback={fallback_races_map[rid]}")

assert not diffs, "發現正表與 fallback aliases 分歧: " + "; ".join(diffs)
print(f"✓ 3. 全量 42 族 aliases 在正表與 fallback 表 100% 逐行完全對齊！")

# 4. 驗證 7 大槽位切片已就緒，且 poses/kite 保持零佔位圖（僅保留 .gitkeep）
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/kite")
image_exts = (".png", ".webp", ".jpg", ".jpeg")
expected_slices = {
    "back_curio": ["curio_kite_spring_steel_cooling_wings.png", "curio_kite_spring_steel_cooling_wings_512.png"],
    "chassis": ["chassis_kite_copper_obsidian_default.png", "chassis_kite_copper_obsidian_default_512.png"],
    "costume": ["costume_kite_welder_cape_belt.png", "costume_kite_welder_cape_belt_512.png"],
    "head_unit": ["head_kite_raptor_cowl_beak.png", "head_kite_raptor_cowl_beak_512.png"],
    "optic_core": ["face_kite_amber_quartz_rangefinder.png", "face_kite_amber_quartz_rangefinder_512.png"],
    "weapon": ["weapon_kite_crucible_recurve_bow.png", "weapon_kite_crucible_recurve_bow_512.png"],
    "winding_key": ["key_kite_turbine_relief_brass.png", "key_kite_turbine_relief_brass_512.png"]
}

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    for req_f in expected_slices[s]:
        req_p = os.path.join(s_dir, req_f)
        assert os.path.exists(req_p), f"缺少切片圖檔: {req_p}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/kite")
assert os.path.isdir(poses_dir), f"poses/kite 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/kite 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert not poses_images, f"poses/kite 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位切片圖檔 100% 就緒，poses/kite 恪守 .gitkeep 規範")
print("=== 0-QA30 查驗 100% 通過！ ===")
