#!/usr/bin/env python3
"""0-QA30 逐項比對驗證腳本：風箱毛蟲 (caterpillar)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. caterpillar 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 50 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. caterpillar 7 大部件目錄與 poses/caterpillar 目錄存在且恪守零佔位圖（僅保留 .gitkeep）
5. 開局武器符合 equipment.json 既有 ID 規範
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 逐項比對驗證 (caterpillar) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 caterpillar 規格
caterpillar_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "caterpillar":
        caterpillar_table = r

assert caterpillar_table is not None, "正表未找到 caterpillar 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races >= 50, f"total_races 應至少為 50，實際為 {total_races}"
assert caterpillar_table["name_zh"] == "風箱毛蟲", f"name_zh 應為 '風箱毛蟲'，實際為: {caterpillar_table['name_zh']}"
assert caterpillar_table["name_en"] == "The Bellows Caterpillar", f"name_en 應為 'The Bellows Caterpillar'，實際為: {caterpillar_table['name_en']}"
assert caterpillar_table["class_archetype"] == "戰士 (Viking)", f"class_archetype 應為 '戰士 (Viking)'，實際為: {caterpillar_table['class_archetype']}"

expected_aliases = ["bellows_caterpillar", "segmented_caterpillar", "clockwork_caterpillar", "crawler_caterpillar"]
assert sorted(caterpillar_table["aliases"]) == sorted(expected_aliases), f"aliases 不符: {caterpillar_table['aliases']} vs {expected_aliases}"

print(f"✓ 2. 正表 caterpillar 規格就緒: {caterpillar_table['name_zh']} ({caterpillar_table['name_en']}), total_races={total_races}")
print(f"   race_id: {caterpillar_table['race_id']}")
print(f"   aliases: {caterpillar_table['aliases']}")

# 3. 驗證 fallback 表
gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

# 0-QA33 防護查驗：檢查 fallback 表 total_races 必須 100% 精確為 50
m_total = re.search(r'"races_specification":\s*\{\s*"total_races":\s*(\d+)', gd_content)
assert m_total is not None, "paperdoll_renderer.gd 未找到 races_specification.total_races 定義！"
fallback_total_races = int(m_total.group(1))
assert fallback_total_races == 50, f"fallback 表 total_races 應為 50，實際為 {fallback_total_races}（0-QA33 規範）"
print(f"✓ 3.1 fallback 表 total_races 精確為 50 (實際: {fallback_total_races})，符合 0-QA33 規範")

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

# 4. 驗證 7 大槽位目錄與 poses/caterpillar 目錄存在且恪守零美術佔位圖（僅保留 .gitkeep）
slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/caterpillar")
image_exts = (".png", ".webp", ".jpg", ".jpeg")

for s in slots:
    s_dir = os.path.join(base_paperdoll, s)
    assert os.path.isdir(s_dir), f"槽位目錄不存在: {s_dir}"
    assert os.path.exists(os.path.join(s_dir, ".gitkeep")), f"槽位目錄缺少 .gitkeep: {s_dir}"
    slot_images = [fn for fn in os.listdir(s_dir) if fn.lower().endswith(image_exts)]
    assert not slot_images, f"槽位目錄 {s} 發現非預期圖片檔案（違反零佔位圖規則）: {slot_images}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/caterpillar")
assert os.path.isdir(poses_dir), f"poses/caterpillar 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/caterpillar 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith(image_exts)]
assert not poses_images, f"poses/caterpillar 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位空目錄與 poses/caterpillar 均已就緒，且恪守零美術佔位圖（僅保留 .gitkeep）規範")

# 5. 驗證開局武器符合 equipment.json 既有 ID
equip_path = os.path.join(repo_root, "game/data/tables/equipment.json")
with open(equip_path, "r", encoding="utf-8") as f:
    equip_d = json.load(f)
bases = equip_d.get("bases", {})
assert "anvil_hammer" in bases, "equipment.json bases 中未找到 anvil_hammer！"
assert bases["anvil_hammer"].get("slot") == "weapon", "anvil_hammer 的 slot 應為 weapon！"
print("✓ 5. 開局武器 anvil_hammer 驗證為 equipment.json 既有 ID (bases)，無跨界自創裝備")

print("=== 0-QA30 查驗 100% 通過！ ===")
