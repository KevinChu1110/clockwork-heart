#!/usr/bin/env python3
"""0-QA30 / 0-QA33 逐項比對驗證腳本：翠刃螳螂 (mantis)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. mantis 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 70 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. 0-QA33 防護查驗：fallback 表 total_races 必須 100% 精確為 70
5. mantis 7 大部件目錄與 poses/mantis、player/mantis 目錄存在且恪守零佔位圖（僅保留 .gitkeep）
6. 開局武器符合 equipment.json 既有 ID 規範 (hunt_claw)
7. game_state.gd 與 equipment_system.gd 設定對齊
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 / 0-QA33 逐項比對驗證 (mantis) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 mantis 規格
mantis_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "mantis":
        mantis_table = r

assert mantis_table is not None, "正表未找到 mantis 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races == 70, f"total_races 應為 70，實際為 {total_races}"
assert mantis_table["name_zh"] == "翠刃螳螂", f"name_zh 應為 '翠刃螳螂'，實際為: {mantis_table['name_zh']}"
assert mantis_table["name_en"] == "The Jade Mantis", f"name_en 應為 'The Jade Mantis'，實際為: {mantis_table['name_en']}"
assert mantis_table["class_archetype"] == "武術家 (Monk)", f"class_archetype 應為 '武術家 (Monk)'，實際為: {mantis_table['class_archetype']}"

expected_aliases = [
    "jade_mantis",
    "emerald_mantis",
    "clockwork_mantis",
    "tinplate_mantis",
    "scythe_mantis",
    "canopy_mantis"
]
assert sorted(mantis_table["aliases"]) == sorted(expected_aliases), f"aliases 不符: {mantis_table['aliases']} vs {expected_aliases}"

print(f"✓ 2. 正表 mantis 規格就緒: {mantis_table['name_zh']} ({mantis_table['name_en']}), total_races={total_races}")
print(f"   race_id: {mantis_table['race_id']}")
print(f"   aliases: {mantis_table['aliases']}")

# 3. 驗證 fallback 表與 0-QA33 防護
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

# 0-QA33 防護查驗：檢查 fallback 表 total_races 必須 100% 精確為 70
m_total = re.search(r'"races_specification":\s*\{\s*"total_races":\s*(\d+)', gd_content)
assert m_total is not None, "paperdoll_renderer.gd 未找到 races_specification.total_races 定義！"
fallback_total_races = int(m_total.group(1))
assert fallback_total_races == 70, f"fallback 表 total_races 應為 70，實際為 {fallback_total_races}（0-QA33 規範）"
print(f"✓ 3.1 fallback 表 total_races 精確為 70 (實際: {fallback_total_races})，符合 0-QA33 規範")

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

# 4. 驗證 7 大槽位切片已全數就緒且 poses/mantis 恪守零美術佔位圖規範
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/mantis")
image_exts = (".png", ".webp", ".jpg", ".jpeg")

expected_slices = {
    "back_curio": ["curio_mantis_spring_pack.png", "curio_mantis_spring_pack_512.png"],
    "chassis": ["chassis_mantis_stock.png", "chassis_mantis_stock_512.png"],
    "costume": ["costume_mantis_vine_plate.png", "costume_mantis_vine_plate_512.png"],
    "head_unit": ["head_mantis_canopy_cowl.png", "head_mantis_canopy_cowl_512.png"],
    "optic_core": ["face_mantis_emerald_goggles.png", "face_mantis_emerald_goggles_512.png"],
    "weapon": ["weapon_mantis_scythe_claw.png", "weapon_mantis_scythe_claw_512.png"],
    "winding_key": ["key_mantis_vine_brass.png", "key_mantis_vine_brass_512.png"]
}

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    for req_f in expected_slices[s]:
        req_p = os.path.join(s_dir, req_f)
        assert os.path.exists(req_p), f"缺少切片圖檔: {req_p}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/mantis")
assert os.path.isdir(poses_dir), f"poses/mantis 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/mantis 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert len(poses_images) == 0, f"poses/mantis 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位切片已全數就緒且 poses/mantis 恪守零美術佔位圖規範")

# 5. 驗證開局武器符合 equipment.json 既有 ID (hunt_claw)
equip_path = os.path.join(repo_root, "game/data/tables/equipment.json")
with open(equip_path, "r", encoding="utf-8") as f:
    equip_d = json.load(f)

bases = equip_d.get("bases", {})
assert "hunt_claw" in bases, "equipment.json bases 中未找到 hunt_claw！"
assert bases["hunt_claw"].get("slot") == "weapon", "hunt_claw 的 slot 應為 weapon！"
assert bases["hunt_claw"].get("line") == "claw", "hunt_claw 的 line 應為 claw！"
print("✓ 5. 開局武器 hunt_claw 驗證為 equipment.json 既有 ID (bases)，slot=weapon, line=claw，無跨界自創裝備 (0-QA33)")

# 6. 驗證 game_state.gd 與 equipment_system.gd 設定
gs_path = os.path.join(repo_root, "game/scripts/autoload/game_state.gd")
with open(gs_path, "r", encoding="utf-8") as f:
    gs_content = f.read()
assert '"mantis": "hunt_claw"' in gs_content, 'game_state.gd RACE_STARTER_WEAPONS 未包含 mantis: hunt_claw！'
assert '"mantis": default_name = "翠刃螳螂"' in gs_content, 'game_state.gd default_name 未包含 mantis！'

es_path = os.path.join(repo_root, "game/scripts/systems/equipment_system.gd")
with open(es_path, "r", encoding="utf-8") as f:
    es_content = f.read()
assert '"mantis": "hunt_claw"' in es_content, 'equipment_system.gd RACE_STARTER_WEAPONS 未包含 mantis: hunt_claw！'

print("✓ 6. game_state.gd 與 equipment_system.gd 開局武器與預設名設定驗證合格")

print("\n=== 0-QA30 / 0-QA33 查驗 100% 通過！ ===")
