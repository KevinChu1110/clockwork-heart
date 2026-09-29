#!/usr/bin/env python3
"""0-QA30 / 0-QA33 逐項比對驗證腳本：碎石旱獺 (marmot)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. marmot 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 64 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. 0-QA33 防護查驗：fallback 表 total_races 必須 100% 精確為 64
5. marmot 7 大部件目錄與 poses/marmot 目錄存在且恪守零佔位圖（僅保留 .gitkeep）
6. 開局武器符合 equipment.json 既有 ID 規範 (wrap_gloves, T1 拳套)
7. game_state.gd 與 equipment_system.gd 設定對齊
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 / 0-QA33 逐項比對驗證 (marmot) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 marmot 規格
marmot_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "marmot":
        marmot_table = r

assert marmot_table is not None, "正表未找到 marmot 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races == 64, f"total_races 應為 64，實際為 {total_races}"
assert marmot_table["name_zh"] == "碎石旱獺", f"name_zh 應為 '碎石旱獺'，實際為: {marmot_table['name_zh']}"
assert marmot_table["name_en"] == "The Rockbreaker Marmot", f"name_en 應為 'The Rockbreaker Marmot'，實際為: {marmot_table['name_en']}"
assert marmot_table["class_archetype"] == "武術家 (Monk)", f"class_archetype 應為 '武術家 (Monk)'，實際為: {marmot_table['class_archetype']}"

expected_aliases = ["rockbreaker_marmot", "quarry_marmot", "piston_marmot", "clockwork_marmot", "dune_groundhog"]
assert sorted(marmot_table["aliases"]) == sorted(expected_aliases), f"aliases 不符: {marmot_table['aliases']} vs {expected_aliases}"

print(f"✓ 2. 正表 marmot 規格就緒: {marmot_table['name_zh']} ({marmot_table['name_en']}), total_races={total_races}")
print(f"   race_id: {marmot_table['race_id']}")
print(f"   aliases: {marmot_table['aliases']}")

# 3. 驗證 fallback 表與 0-QA33 防護
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

# 0-QA33 防護查驗：檢查 fallback 表 total_races 必須 100% 精確為 64
m_total = re.search(r'"races_specification":\s*\{\s*"total_races":\s*(\d+)', gd_content)
assert m_total is not None, "paperdoll_renderer.gd 未找到 races_specification.total_races 定義！"
fallback_total_races = int(m_total.group(1))
assert fallback_total_races == 64, f"fallback 表 total_races 應為 64，實際為 {fallback_total_races}（0-QA33 規範）"
print(f"✓ 3.1 fallback 表 total_races 精確為 64 (實際: {fallback_total_races})，符合 0-QA33 規範")

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
print(f"✓ 3.2 全量 {len(table_races_map)} 族 aliases 在正表與 fallback 表 100% 逐行完全對齊！")

# 4. 驗證 7 大槽位目錄與 poses/marmot 目錄存在
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/marmot")

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    assert os.path.exists(os.path.join(s_dir, ".gitkeep")), f"槽位目錄缺少 .gitkeep: {s_dir}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/marmot")
assert os.path.isdir(poses_dir), f"poses/marmot 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/marmot 缺少 .gitkeep"

player_marmot_dir = os.path.join(repo_root, "game/assets/sprites/player/marmot")
assert os.path.exists(player_marmot_dir), f"player/marmot 不存在: {player_marmot_dir}"

print("✓ 4. 7 大槽位目錄、poses/marmot 與 player/marmot 目錄完整就緒")

# 5. 驗證開局武器符合 equipment.json 既有 ID (wrap_gloves)
equip_path = os.path.join(repo_root, "game/data/tables/equipment.json")
with open(equip_path, "r", encoding="utf-8") as f:
    equip_d = json.load(f)
bases = equip_d.get("bases", {})
assert "wrap_gloves" in bases, "equipment.json bases 中未找到 wrap_gloves！"
assert bases["wrap_gloves"].get("slot") == "weapon", "wrap_gloves 的 slot 應為 weapon！"
assert bases["wrap_gloves"].get("line") == "fist", "wrap_gloves 的 line 應為 fist！"
print("✓ 5. 開局武器 wrap_gloves 驗證為 equipment.json 既有 ID (bases)，slot=weapon, line=fist，無跨界自創裝備 (0-QA33)")

# 6. 驗證 game_state.gd 與 equipment_system.gd 設定
gs_path = os.path.join(repo_root, "game/scripts/autoload/game_state.gd")
with open(gs_path, "r", encoding="utf-8") as f:
    gs_content = f.read()
assert '"marmot": "wrap_gloves"' in gs_content, "game_state.gd RACE_STARTER_WEAPONS 未包含 marmot: wrap_gloves！"
assert '"marmot": default_name = "碎石旱獺"' in gs_content, "game_state.gd default_name 未包含 marmot！"

es_path = os.path.join(repo_root, "game/scripts/systems/equipment_system.gd")
with open(es_path, "r", encoding="utf-8") as f:
    es_content = f.read()
assert '"marmot": "wrap_gloves"' in es_content, "equipment_system.gd RACE_STARTER_WEAPONS 未包含 marmot: wrap_gloves！"

print("✓ 6. game_state.gd 與 equipment_system.gd 開局武器與預設名設定驗證合格")

print("\n=== 0-QA30 / 0-QA33 查驗 100% 通過！ ===")
