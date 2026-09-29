#!/usr/bin/env python3
import json
import os

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
docs_p = f"{REPO_ROOT}/docs/design/paperdoll_slots.json"
table_p = f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json"

with open(docs_p, "r", encoding="utf-8") as f:
    data = json.load(f)

for r in data["races_specification"]["races"]:
    if r.get("race_id") == "firefly":
        status = r["asset_naming_conventions"]["status"]
        pose_str = "game/assets/sprites/player/poses/firefly/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)"
        battle_128 = "game/assets/sprites/player/firefly_battle.png (128x128 戰鬥特寫姿態)"
        battle_512 = "game/assets/sprites/player/firefly_battle_512.png (512x512 戰鬥特寫姿態)"

        for item in [pose_str, battle_128, battle_512]:
            if item not in status["existing"]:
                status["existing"].append(item)
            if item in status["pending"]:
                status["pending"].remove(item)

        r["asset_naming_conventions"]["game_sprite_battle"] = "game/assets/sprites/player/firefly_battle.png (128x128) [既有]"
        r["asset_naming_conventions"]["game_action_poses"] = "game/assets/sprites/player/poses/firefly/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [既有]"
        print("Updated firefly in paperdoll_slots.json")
        break

with open(docs_p, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

with open(table_p, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Successfully synced both docs/design and game/data/tables paperdoll_slots.json")
