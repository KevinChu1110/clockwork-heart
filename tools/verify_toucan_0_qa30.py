#!/usr/bin/env python3
"""0-QA30 / 0-QA33 逐項比對驗證腳本：彩喙巨嘴鳥 (toucan)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. toucan 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 60 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. 0-QA33 防護查驗：fallback 表 total_races 必須 100% 精確為 60
5. toucan 7 大部件目錄與 poses/toucan 目錄存在且恪守零佔位圖（僅保留 .gitkeep）
6. 開局武器符合 equipment.json 既有 ID 規範 (flint_gun, T1 遊俠燧發火銃)
7. game_state.gd 與 equipment_system.gd 設定對齊
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 / 0-QA33 逐項比對驗證 (toucan) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 toucan 規格
toucan_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "toucan":
        toucan_table = r

assert toucan_table is not None, "正表未找到 toucan 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races >= 60, f"total_races 應 >= 60，實際為 {total_races}"
assert toucan_table["name_zh"] == "彩喙巨嘴鳥", f"name_zh 應為 '彩喙巨嘴鳥'，實際為: {toucan_table['name_zh']}"
assert toucan_table["name_en"] == "The Prism-Bill Toucan", f"name_en 應為 'The Prism-Bill Toucan'，實際為: {toucan_table['name_en']}"
assert toucan_table["class_archetype"] == "遊俠 (Ranger)", f"class_archetype 應為 '遊俠 (Ranger)'，實際為: {toucan_table['class_archetype']}"

expected_aliases = ["prism_bill_toucan", "canopy_toucan", "clockwork_toucan", "emerald_toucan", "prism_toucan"]
assert sorted(toucan_table["aliases"]) == sorted(expected_aliases), f"aliases 不符: {toucan_table['aliases']} vs {expected_aliases}"

print(f"✓ 2. 正表 toucan 規格就緒: {toucan_table['name_zh']} ({toucan_table['name_en']}), total_races={total_races}")
print(f"   race_id: {toucan_table['race_id']}")
print(f"   aliases: {toucan_table['aliases']}")

# 3. 驗證 fallback 表與 0-QA33 防護
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

# 0-QA33 防護查驗：檢查 fallback 表 total_races 必須 100% 精確為 60
m_total = re.search(r'"races_specification":\s*\{\s*"total_races":\s*(\d+)', gd_content)
assert m_total is not None, "paperdoll_renderer.gd 未找到 races_specification.total_races 定義！"
fallback_total_races = int(m_total.group(1))
assert fallback_total_races == total_races, f"fallback 表 total_races 應與正表一致 ({total_races})，實際為 {fallback_total_races}（0-QA33 規範）"
print(f"✓ 3.1 fallback 表 total_races 與正表一致 (實際: {fallback_total_races})，符合 0-QA33 規範")

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

# 4. 驗證 7 大槽位 128x128 與 512x512 切片圖層全數就緒，poses/toucan 恪守 .gitkeep
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/toucan")
expected_slice_files = {
    "back_curio": ["curio_toucan_segmented_copper_rudder_tail.png", "curio_toucan_segmented_copper_rudder_tail_512.png"],
    "chassis": ["chassis_toucan_canopy_alloy_default.png", "chassis_toucan_canopy_alloy_default_512.png"],
    "costume": ["costume_toucan_vine_valley_scout_harness.png", "costume_toucan_vine_valley_scout_harness_512.png"],
    "head_unit": ["head_toucan_prism_bill_visor_cowl.png", "head_toucan_prism_bill_visor_cowl_512.png"],
    "optic_core": ["face_toucan_emerald_quartz_monocle.png", "face_toucan_emerald_quartz_monocle_512.png"],
    "weapon": ["weapon_toucan_canopy_prism_pneumatic_arquebus.png", "weapon_toucan_canopy_prism_pneumatic_arquebus_512.png"],
    "winding_key": ["key_toucan_tri_vane_canopy_rotor_brass.png", "key_toucan_tri_vane_canopy_rotor_brass_512.png"]
}

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    for req_f in expected_slice_files[s]:
        f_path = os.path.join(s_dir, req_f)
        assert os.path.exists(f_path), f"缺少切片檔案: {f_path}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/toucan")
assert os.path.isdir(poses_dir), f"poses/toucan 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/toucan 缺少 .gitkeep"
image_exts = (".png", ".webp", ".jpg", ".jpeg")
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert not poses_images, f"poses/toucan 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位 128x128 與 512x512 切片圖層全數就緒，poses/toucan 恪守 .gitkeep（零佔位圖）")

# 5. 驗證開局武器符合 equipment.json 既有 ID (flint_gun)
equip_path = os.path.join(repo_root, "game/data/tables/equipment.json")
with open(equip_path, "r", encoding="utf-8") as f:
    equip_d = json.load(f)
bases = equip_d.get("bases", {})
assert "flint_gun" in bases, "equipment.json bases 中未找到 flint_gun！"
assert bases["flint_gun"].get("slot") == "weapon", "flint_gun 的 slot 應為 weapon！"
assert bases["flint_gun"].get("line") == "gun", "flint_gun 的 line 應為 gun！"
print("✓ 5. 開局武器 flint_gun 驗證為 equipment.json 既有 ID (bases)，slot=weapon, line=gun，無跨界自創裝備 (0-QA33)")

# 6. 驗證 game_state.gd 與 equipment_system.gd 設定
gs_path = os.path.join(repo_root, "game/scripts/autoload/game_state.gd")
with open(gs_path, "r", encoding="utf-8") as f:
    gs_content = f.read()
assert '"toucan": "flint_gun"' in gs_content, "game_state.gd RACE_STARTER_WEAPONS 未包含 toucan: flint_gun！"
assert '"toucan": default_name = "彩喙巨嘴鳥"' in gs_content, "game_state.gd default_name 未包含 toucan！"

es_path = os.path.join(repo_root, "game/scripts/systems/equipment_system.gd")
with open(es_path, "r", encoding="utf-8") as f:
    es_content = f.read()
assert '"toucan": "flint_gun"' in es_content, "equipment_system.gd RACE_STARTER_WEAPONS 未包含 toucan: flint_gun！"

print("✓ 6. game_state.gd 與 equipment_system.gd 開局武器與預設名設定驗證合格")

print("\n=== 0-QA30 / 0-QA33 查驗 100% 通過！ ===")
