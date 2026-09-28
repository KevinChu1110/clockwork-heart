#!/usr/bin/env python3
"""0-QA30 逐項比對驗證腳本：破星蜜獾 (badger)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. badger 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. badger 7 大部件目錄與 poses/badger 目錄存在且恪守零佔位圖（僅保留 .gitkeep）
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 逐項比對驗證 (badger) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 badger 規格
badger_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "badger":
        badger_table = r

assert badger_table is not None, "正表未找到 badger 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races >= 46, f"total_races 應至少為 46，實際為 {total_races}"
print(f"✓ 2. 正表 badger 規格就緒: {badger_table['name_zh']} ({badger_table['name_en']}), total_races={total_races}")
print(f"   race_id: {badger_table['race_id']}")
print(f"   aliases: {badger_table['aliases']}")

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

assert len(table_races_map) == len(fallback_races_map), f"正表種族數 ({len(table_races_map)}) 與 fallback 表種族數 ({len(fallback_races_map)}) 不一致！"

diffs = []
for rid, t_aliases in table_races_map.items():
    if rid not in fallback_races_map:
        diffs.append(f"fallback 缺少種族: {rid}")
    elif sorted(t_aliases) != sorted(fallback_races_map[rid]):
        diffs.append(f"種族 {rid} aliases 分歧: 正表={t_aliases} vs fallback={fallback_races_map[rid]}")

assert not diffs, "發現正表與 fallback aliases 分歧: " + "; ".join(diffs)
print(f"✓ 3. 全量 {len(table_races_map)} 族 aliases 在正表與 fallback 表 100% 逐行完全對齊！")

# 4. 驗證 7 大槽位切片已就緒，且 poses/badger 保持零佔位圖（僅保留 .gitkeep）
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/badger")
image_exts = (".png", ".webp", ".jpg", ".jpeg")
expected_slices = {
    "back_curio": ["curio_badger_dual_coldgas_reaction_thruster.png", "curio_badger_dual_coldgas_reaction_thruster_512.png"],
    "chassis": ["chassis_badger_polymer_space_default.png", "chassis_badger_polymer_space_default_512.png"],
    "costume": ["costume_badger_eva_heavy_harness.png", "costume_badger_eva_heavy_harness_512.png"],
    "head_unit": ["head_badger_flathead_ballistic_visor.png", "head_badger_flathead_ballistic_visor_512.png"],
    "optic_core": ["face_badger_amber_led_matrix_visor.png", "face_badger_amber_led_matrix_visor_512.png"],
    "weapon": ["weapon_badger_starbreaker_ripper_claw.png", "weapon_badger_starbreaker_ripper_claw_512.png"],
    "winding_key": ["key_badger_four_vane_antenna_gold.png", "key_badger_four_vane_antenna_gold_512.png"]
}

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    for req_f in expected_slices[s]:
        req_p = os.path.join(s_dir, req_f)
        assert os.path.exists(req_p), f"缺少切片圖檔: {req_p}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/badger")
assert os.path.isdir(poses_dir), f"poses/badger 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/badger 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert not poses_images, f"poses/badger 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位切片已全數就緒且 poses/badger 恪守零美術佔位圖（僅保留 .gitkeep）規範")
print("=== 0-QA30 查驗 100% 通過！ ===")
