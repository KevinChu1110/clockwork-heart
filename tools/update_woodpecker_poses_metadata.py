#!/usr/bin/env python3
"""
update_woodpecker_poses_metadata.py
Update docs/design/paperdoll_slots.json and game/data/tables/paperdoll_slots.json
reflecting that woodpecker action poses are completed.
"""
import json
import os

REPO_ROOT = "/opt/side/bravesoul-game"
TABLE_PATH = os.path.join(REPO_ROOT, "game/data/tables/paperdoll_slots.json")
DOCS_PATH = os.path.join(REPO_ROOT, "docs/design/paperdoll_slots.json")

def update_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    races = data["races_specification"]["races"]
    woodpecker = next((r for r in races if r["race_id"] == "woodpecker"), None)
    if not woodpecker:
        raise ValueError("woodpecker not found in " + path)

    pose_entry = "game/assets/sprites/player/poses/woodpecker/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)"
    existing = woodpecker["asset_naming_conventions"]["status"]["existing"]
    pending = woodpecker["asset_naming_conventions"]["status"]["pending"]

    if pose_entry in pending:
        pending.remove(pose_entry)
    if pose_entry not in existing:
        existing.append(pose_entry)

    woodpecker["asset_naming_conventions"]["game_action_poses"] = "game/assets/sprites/player/poses/woodpecker/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [既有]"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Updated", path)

if __name__ == "__main__":
    update_json(TABLE_PATH)
    update_json(DOCS_PATH)
