#!/usr/bin/env python3
"""0-QA30 逐項比對驗證腳本：旋音天鵝 (swan)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. swan 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 43 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. swan 7 大部件目錄與 poses/swan 目錄存在且恪守零佔位圖（僅有 .gitkeep）
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 逐項比對驗證 (swan) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 swan 規格
swan_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "swan":
        swan_table = r

assert swan_table is not None, "正表未找到 swan 定義！"
assert table_d["races_specification"]["total_races"] == 43, f"total_races 應為 43，實際為 {table_d['races_specification']['total_races']}"
print(f"✓ 2. 正表 swan 規格就緒: {swan_table['name_zh']} ({swan_table['name_en']}), total_races=43")
print(f"   race_id: {swan_table['race_id']}")
print(f"   aliases: {swan_table['aliases']}")

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

assert len(table_races_map) == 43, f"正表種族數應為 43，實際為 {len(table_races_map)}"
assert len(fallback_races_map) == 43, f"fallback 表種族數應為 43，實際為 {len(fallback_races_map)}"

diffs = []
for rid, t_aliases in table_races_map.items():
    if rid not in fallback_races_map:
        diffs.append(f"fallback 缺少種族: {rid}")
    elif sorted(t_aliases) != sorted(fallback_races_map[rid]):
        diffs.append(f"種族 {rid} aliases 分歧: 正表={t_aliases} vs fallback={fallback_races_map[rid]}")

assert not diffs, "發現正表與 fallback aliases 分歧: " + "; ".join(diffs)
print(f"✓ 3. 全量 43 族 aliases 在正表與 fallback 表 100% 逐行完全對齊！")

# 4. 驗證 7 大槽位切片已就緒，且 poses/swan 保持零佔位圖（僅保留 .gitkeep）
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/swan")
image_exts = (".png", ".webp", ".jpg", ".jpeg")
expected_slices = {
    "back_curio": ["curio_swan_spring_steel_ballet_wings.png", "curio_swan_spring_steel_ballet_wings_512.png"],
    "chassis": ["chassis_swan_silver_enamel_default.png", "chassis_swan_silver_enamel_default_512.png"],
    "costume": ["costume_swan_theatre_herald_cuirass.png", "costume_swan_theatre_herald_cuirass_512.png"],
    "head_unit": ["head_swan_tiara_beak_visor.png", "head_swan_tiara_beak_visor_512.png"],
    "optic_core": ["face_swan_prismatic_crystal_monocle.png", "face_swan_prismatic_crystal_monocle_512.png"],
    "weapon": ["weapon_swan_octave_spiral_lance.png", "weapon_swan_octave_spiral_lance_512.png"],
    "winding_key": ["key_swan_octave_dual_loop_brass.png", "key_swan_octave_dual_loop_brass_512.png"]
}

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    for req_f in expected_slices[s]:
        req_p = os.path.join(s_dir, req_f)
        assert os.path.exists(req_p), f"缺少切片圖檔: {req_p}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/swan")
assert os.path.isdir(poses_dir), f"poses/swan 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/swan 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert not poses_images, f"poses/swan 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位切片已全數就緒且 poses/swan 恪守零美術佔位圖（僅保留 .gitkeep）規範")
print("=== 0-QA30 查驗 100% 通過！ ===")
