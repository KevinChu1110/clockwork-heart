#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
with open(path, "r", encoding="utf-8") as f:
    d = json.load(f)

ram_table = None
for r in d["races_specification"]["races"]:
    if r.get("race_id") == "ram":
        ram_table = r
        break

print("=== 0-QA30 逐項比對驗證 (ram) ===")
print("1. 正表 (game/data/tables/paperdoll_slots.json):")
assert ram_table is not None, "未找到 ram 定義"
print(f"   race_id: {ram_table['race_id']}")
print(f"   aliases: {ram_table['aliases']}")

docs_path = os.path.join(repo_root, "docs/design/paperdoll_slots.json")
with open(docs_path, "r", encoding="utf-8") as f:
    docs_d = json.load(f)

docs_ram_table = None
for r in docs_d["races_specification"]["races"]:
    if r.get("race_id") == "ram":
        docs_ram_table = r
        break

assert docs_ram_table is not None, "docs/design 未找到 ram 定義"
assert docs_ram_table["aliases"] == ram_table["aliases"], "docs/design 與 game/data/tables aliases 不一致！"

gd_path = os.path.join(repo_root, "game/scripts/art/paperdoll_renderer.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd_content = f.read()

fallback_line = ""
for line in gd_content.splitlines():
    if '"race_id": "ram"' in line:
        fallback_line = line.strip()
        break

print("2. 程式 fallback 表 (game/scripts/art/paperdoll_renderer.gd _get_fallback_spec):")
print(f"   fallback 宣告行: {fallback_line}")

expected_aliases = ["astral_ram", "celestial_ram", "spiral_ram", "gravity_ram"]
assert ram_table["aliases"] == expected_aliases, f"正表 aliases 不相符！{ram_table['aliases']} vs {expected_aliases}"
for a in expected_aliases:
    assert f'"{a}"' in fallback_line, f"fallback 表缺少 alias: {a}"

print("3. 比對結果:")
print(f"   正表 aliases:     {ram_table['aliases']}")
print(f"   預期 aliases:     {expected_aliases}")
print("   ✓ 0-QA30 逐行比對 100% 一致，零分歧！")
