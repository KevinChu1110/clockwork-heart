#!/usr/bin/env python3
import subprocess

out = subprocess.check_output(["git", "status", "--porcelain"], text=True)
for line in out.splitlines():
    status = line[:2]
    path = line[3:]
    if status == " M":
        # 如果不是 bison 相關，也不是 paperdoll_slots.json 或 test/unify 腳本，就還原
        if "bison" not in path and path not in [
            "docs/design/paperdoll_slots.json",
            "game/data/tables/paperdoll_slots.json",
            "game/scripts/art/test_race_walk_idle.gd",
            "game/scripts/art/test_nine_races_walk_512.gd",
            "tools/unify_race_cards_4_5.py"
        ]:
            subprocess.run(["git", "checkout", "--", path])
print("✓ Cleaned unrelated modified files")
