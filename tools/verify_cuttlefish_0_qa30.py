#!/usr/bin/env python3
"""0-QA30 / 0-QA33 逐項比對驗證腳本：墨影烏賊 (cuttlefish)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. cuttlefish 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 51 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. 0-QA33 防護查驗：fallback 表 total_races 必須 100% 精確為 51
5. cuttlefish 7 大部件雙規格切片圖檔全數到位且 poses/cuttlefish 目錄恪守零佔位圖（僅保留 .gitkeep）
6. 開局武器符合 equipment.json 既有 ID 規範 (star_fang)
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 / 0-QA33 逐項比對驗證 (cuttlefish) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 cuttlefish 規格
cuttlefish_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "cuttlefish":
        cuttlefish_table = r

assert cuttlefish_table is not None, "正表未找到 cuttlefish 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races >= 51, f"total_races 應至少為 51，實際為 {total_races}"
assert cuttlefish_table["name_zh"] == "墨影烏賊", f"name_zh 應為 '墨影烏賊'，實際為: {cuttlefish_table['name_zh']}"
assert cuttlefish_table["name_en"] == "The Inksmoke Cuttlefish", f"name_en 應為 'The Inksmoke Cuttlefish'，實際為: {cuttlefish_table['name_en']}"
assert cuttlefish_table["class_archetype"] == "忍者 (Ninja)", f"class_archetype 應為 '忍者 (Ninja)'，實際為: {cuttlefish_table['class_archetype']}"

expected_aliases = ["inksmoke_cuttlefish", "abyssal_cuttlefish", "mimic_cuttlefish", "clockwork_cuttlefish"]
assert sorted(cuttlefish_table["aliases"]) == sorted(expected_aliases), f"aliases 不符: {cuttlefish_table['aliases']} vs {expected_aliases}"

print(f"✓ 2. 正表 cuttlefish 規格就緒: {cuttlefish_table['name_zh']} ({cuttlefish_table['name_en']}), total_races={total_races}")
print(f"   race_id: {cuttlefish_table['race_id']}")
print(f"   aliases: {cuttlefish_table['aliases']}")

# 3. 驗證 fallback 表與 0-QA33 防護
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

# 0-QA33 防護查驗：檢查 fallback 表 total_races 必須 100% 精確為 51
m_total = re.search(r'"races_specification":\s*\{\s*"total_races":\s*(\d+)', gd_content)
assert m_total is not None, "paperdoll_renderer.gd 未找到 races_specification.total_races 定義！"
fallback_total_races = int(m_total.group(1))
assert fallback_total_races == 51, f"fallback 表 total_races 應為 51，實際為 {fallback_total_races}（0-QA33 規範）"
print(f"✓ 3.1 fallback 表 total_races 精確為 51 (實際: {fallback_total_races})，符合 0-QA33 規範")

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

# 4. 驗證 7 大槽位切片已全數就緒且 poses/cuttlefish 恪守零美術佔位圖（僅保留 .gitkeep）
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/cuttlefish")
image_exts = (".png", ".webp", ".jpg", ".jpeg")
expected_slices = {
    "back_curio": ["curio_cuttlefish_pneumatic_ink_siphon.png", "curio_cuttlefish_pneumatic_ink_siphon_512.png"],
    "chassis": ["chassis_cuttlefish_abyssal_cyan_default.png", "chassis_cuttlefish_abyssal_cyan_default_512.png"],
    "costume": ["costume_cuttlefish_abyssal_shinobi_cuirass.png", "costume_cuttlefish_abyssal_shinobi_cuirass_512.png"],
    "head_unit": ["head_cuttlefish_diving_cowl_fins.png", "head_cuttlefish_diving_cowl_fins_512.png"],
    "optic_core": ["face_cuttlefish_dual_quartz_optic_lens.png", "face_cuttlefish_dual_quartz_optic_lens_512.png"],
    "weapon": ["weapon_cuttlefish_abyssal_inksmoke_dagger.png", "weapon_cuttlefish_abyssal_inksmoke_dagger_512.png"],
    "winding_key": ["key_cuttlefish_tri_vane_turbine_brass.png", "key_cuttlefish_tri_vane_turbine_brass_512.png"]
}

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    for req_f in expected_slices[s]:
        req_p = os.path.join(s_dir, req_f)
        assert os.path.exists(req_p), f"缺少切片圖檔: {req_p}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/cuttlefish")
assert os.path.isdir(poses_dir), f"poses/cuttlefish 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/cuttlefish 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert not poses_images, f"poses/cuttlefish 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位切片已全數就緒且 poses/cuttlefish 恪守零美術佔位圖（僅保留 .gitkeep）規範")

# 5. 驗證開局武器符合 equipment.json 既有 ID (star_fang)
equip_path = os.path.join(repo_root, "game/data/tables/equipment.json")
with open(equip_path, "r", encoding="utf-8") as f:
    equip_d = json.load(f)
bases = equip_d.get("bases", {})
assert "star_fang" in bases, "equipment.json bases 中未找到 star_fang！"
assert bases["star_fang"].get("slot") == "weapon", "star_fang 的 slot 應為 weapon！"
assert bases["star_fang"].get("line") == "dagger", "star_fang 的 line 應為 dagger！"
print("✓ 5. 開局武器 star_fang 驗證為 equipment.json 既有 ID (bases)，slot=weapon, line=dagger，無跨界自創裝備 (0-QA33)")

print("=== 0-QA30 / 0-QA33 查驗 100% 通過！ ===")
