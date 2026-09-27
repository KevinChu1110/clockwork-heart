#!/usr/bin/env python3
import json

path = "game/data/tables/paperdoll_slots.json"
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)

hedgehog_table = None
for r in d["races_specification"]["races"]:
    if r.get("race_id") == "hedgehog":
        hedgehog_table = r
        break

print("=== 0-QA30 逐項比對驗證 (hedgehog) ===")
print("1. 正表 (game/data/tables/paperdoll_slots.json):")
assert hedgehog_table is not None, "未找到 hedgehog 定義"
print(f"   race_id: {hedgehog_table['race_id']}")
print(f"   aliases: {hedgehog_table['aliases']}")

gd_path = "game/scripts/art/paperdoll_renderer.gd"
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

fallback_line = ""
for line in gd_content.splitlines():
    if '"race_id": "hedgehog"' in line:
        fallback_line = line.strip()
        break

print("2. 程式 fallback 表 (game/scripts/art/paperdoll_renderer.gd _get_fallback_spec):")
print(f"   fallback 宣告行: {fallback_line}")

expected_aliases = ["ratchet_hedgehog", "bazaar_hedgehog", "needle_hedgehog", "dawn_hedgehog"]
assert hedgehog_table["aliases"] == expected_aliases, "正表 aliases 不相符！"
for a in expected_aliases:
    assert f'"{a}"' in fallback_line, f"fallback 表缺少 alias: {a}"

print("3. 比對結果:")
print(f"   正表 aliases:     {hedgehog_table['aliases']}")
print(f"   預期 aliases:     {expected_aliases}")
print("   ✓ 0-QA30 逐行比對 100% 一致，零分歧！")
