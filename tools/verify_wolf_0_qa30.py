#!/usr/bin/env python3
import json

path = "game/data/tables/paperdoll_slots.json"
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)

wolf_table = None
for r in d["races_specification"]["races"]:
    if r.get("race_id") == "wolf":
        wolf_table = r
        break

print("=== 0-QA30 逐項比對驗證 (wolf) ===")
print("1. 正表 (game/data/tables/paperdoll_slots.json):")
assert wolf_table is not None, "未找到 wolf 定義"
print(f"   race_id: {wolf_table['race_id']}")
print(f"   aliases: {wolf_table['aliases']}")

gd_path = "game/scripts/art/paperdoll_renderer.gd"
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

fallback_line = ""
for line in gd_content.splitlines():
    if '"race_id": "wolf"' in line:
        fallback_line = line.strip()
        break

print("2. 程式 fallback 表 (game/scripts/art/paperdoll_renderer.gd _get_fallback_spec):")
print(f"   fallback 宣告行: {fallback_line}")

expected_aliases = ["scrap_wolf", "dune_wolf", "rust_wolf", "wasteland_wolf"]
assert wolf_table["aliases"] == expected_aliases, f"正表 aliases 不相符！{wolf_table['aliases']} vs {expected_aliases}"
for a in expected_aliases:
    assert f'"{a}"' in fallback_line, f"fallback 表缺少 alias: {a}"

print("3. 比對結果:")
print(f"   正表 aliases:     {wolf_table['aliases']}")
print(f"   預期 aliases:     {expected_aliases}")
print("   ✓ 0-QA30 逐行比對 100% 一致，零分歧！")
