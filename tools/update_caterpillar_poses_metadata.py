#!/usr/bin/env python3
import json
import os

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
docs_p = f"{REPO_ROOT}/docs/design/paperdoll_slots.json"
table_p = f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json"

with open(docs_p, "r", encoding="utf-8") as f:
    data = json.load(f)

for r in data["races_specification"]["races"]:
    if r.get("race_id") == "caterpillar":
        status = r["asset_naming_conventions"]["status"]
        pose_str = "game/assets/sprites/player/poses/caterpillar/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)"
        if pose_str not in status["existing"]:
            status["existing"].append(pose_str)
        if pose_str in status["pending"]:
            status["pending"].remove(pose_str)
        r["asset_naming_conventions"]["game_action_poses"] = "game/assets/sprites/player/poses/caterpillar/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [既有]"
        print("Updated caterpillar in paperdoll_slots.json")
        break

with open(docs_p, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

with open(table_p, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Successfully synced both docs/design and game/data/tables paperdoll_slots.json")
