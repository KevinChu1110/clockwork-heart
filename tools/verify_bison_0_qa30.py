#!/usr/bin/env python3
"""0-QA30 逐項比對驗證腳本：撼地野牛 (bison)
驗證：
1. game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 100% 一致
2. bison 正表 aliases 與 paperdoll_renderer.gd fallback 表 aliases 100% 對齊一致
3. 全部 44 族 aliases 在正表與 fallback 表 100% 逐族對齊，零分歧
4. bison 7 大部件切片（128px 與 512px LANCZOS）完整齊備，poses/bison 恪守零佔位圖（僅保留 .gitkeep）
"""
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
table_path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")

print("=== 0-QA30 逐項比對驗證 (bison) ===")

# 1. 比對正表與 docs/design 是否一致
with open(table_path, "r", encoding="utf-8") as f:
    table_d = json.load(f)
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

table_str = json.dumps(table_d, sort_keys=True)
docs_str = json.dumps(docs_d, sort_keys=True)
assert table_str == docs_str, "game/data/tables/paperdoll_slots.json 與 docs/design/paperdoll_slots.json 內容不一致！"
print("✓ 1. 正表與 docs/design 兩份 paperdoll_slots.json 100% 一致")

# 2. 驗證 bison 規格
bison_table = None
table_races_map = {}
for r in table_d["races_specification"]["races"]:
    table_races_map[r["race_id"]] = r.get("aliases", [])
    if r.get("race_id") == "bison":
        bison_table = r

assert bison_table is not None, "正表未找到 bison 定義！"
total_races = table_d["races_specification"]["total_races"]
assert total_races >= 44, f"total_races 應至少為 44，實際為 {total_races}"
print(f"✓ 2. 正表 bison 規格就緒: {bison_table['name_zh']} ({bison_table['name_en']}), total_races={total_races}")
print(f"   race_id: {bison_table['race_id']}")
print(f"   aliases: {bison_table['aliases']}")

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
assert len(table_races_map) >= 44, f"正表種族數應至少為 44，實際為 {len(table_races_map)}"

diffs = []
for rid, t_aliases in table_races_map.items():
    if rid not in fallback_races_map:
        diffs.append(f"fallback 缺少種族: {rid}")
    elif sorted(t_aliases) != sorted(fallback_races_map[rid]):
        diffs.append(f"種族 {rid} aliases 分歧: 正表={t_aliases} vs fallback={fallback_races_map[rid]}")

assert not diffs, "發現正表與 fallback aliases 分歧: " + "; ".join(diffs)
print("✓ 3. 全量 44 族 aliases 在正表與 fallback 表 100% 逐行完全對齊！")

# 4. 驗證 7 大槽位切片檔案齊備且非空，poses/bison 保持零佔位圖
slots_items = [
    ("chassis", "chassis_bison_rusted_tinplate_default"),
    ("head_unit", "head_bison_riveted_brow_horn_crest"),
    ("winding_key", "key_bison_heavy_cross_t_bar_cast_iron"),
    ("costume", "costume_bison_junkyard_demolition_cuirass"),
    ("optic_core", "face_bison_amber_pressure_gauge_eye"),
    ("weapon", "weapon_bison_wasteland_anvil_crusher_hammer"),
    ("back_curio", "curio_bison_twin_vent_exhaust_stack")
]
base_paperdoll = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/bison")

for s, item_id in slots_items:
    p128 = os.path.join(base_paperdoll, s, f"{item_id}.png")
    p512 = os.path.join(base_paperdoll, s, f"{item_id}_512.png")
    assert os.path.isfile(p128), f"缺少 128px 切片檔案: {p128}"
    assert os.path.isfile(p512), f"缺少 512px 切片檔案: {p512}"
    assert os.path.getsize(p128) > 0, f"128px 切片檔案為空: {p128}"
    assert os.path.getsize(p512) > 0, f"512px 切片檔案為空: {p512}"

poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/bison")
assert os.path.isdir(poses_dir), f"poses/bison 目錄不存在: {poses_dir}"
assert os.path.exists(os.path.join(poses_dir, ".gitkeep")), "poses/bison 缺少 .gitkeep"
poses_images = [fn for fn in os.listdir(poses_dir) if fn.lower().endswith((".png", ".webp", ".jpg", ".jpeg"))]
assert not poses_images, f"poses/bison 發現非預期圖片檔案（違反零佔位圖規則）: {poses_images}"

print("✓ 4. 7 大槽位切片雙規格齊備，poses/bison 恪守零美術佔位圖規範")
print("=== 0-QA30 查驗 100% 通過！ ===")
