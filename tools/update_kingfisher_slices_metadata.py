#!/usr/bin/env python3
"""
update_kingfisher_slices_metadata.py
Update docs/design/paperdoll_slots.json and game/data/tables/paperdoll_slots.json
reflecting the existing kingfisher paperdoll slices and idle assets.
"""
import json
import os

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfb84d21"
TABLE_PATH = os.path.join(REPO_ROOT, "game/data/tables/paperdoll_slots.json")
DOCS_PATH = os.path.join(REPO_ROOT, "docs/design/paperdoll_slots.json")

def update_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    races = data["races_specification"]["races"]
    kingfisher = next((r for r in races if r["race_id"] == "kingfisher"), None)
    if not kingfisher:
        raise ValueError("kingfisher not found in " + path)

    kingfisher["asset_naming_conventions"]["status"]["existing"] = [
        "game/assets/sprites/player/kingfisher_idle.png (64x64 待機)",
        "game/assets/sprites/player/kingfisher_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/kingfisher_idle.png (隊伍待機)",
        "web/media/hero/kingfisher_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/kingfisher_idle_hd.png (800x1200 HD 展示立繪)",
        "game/assets/sprites/player/paperdoll/kingfisher/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
    ]

    kingfisher["asset_naming_conventions"]["status"]["pending"] = [
        "branding/char_kingfisher.png (品牌形象立牌)",
        "web/media/hero/char_kingfisher.png (官網英雄展示立繪)",
        "docs/art/jade_kingfisher_concept.png (概念立繪)",
        "game/assets/sprites/player/kingfisher_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/kingfisher_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/kingfisher_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/kingfisher_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/kingfisher_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/kingfisher/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/kingfisher.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/kingfisher_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/jade_kingfisher.png (對話半身像)"
    ]

    kingfisher["asset_naming_conventions"]["web_preview"] = "web/media/hero/kingfisher_idle.png (128x128) [既有]"
    kingfisher["asset_naming_conventions"]["game_sprite_idle_base"] = "game/assets/sprites/player/kingfisher_idle.png (64x64) [既有]"
    kingfisher["asset_naming_conventions"]["game_sprite_idle_hi"] = "game/assets/sprites/player/kingfisher_idle_x3.png (128x128) [既有]"
    kingfisher["asset_naming_conventions"]["game_sprite_party_idle"] = "game/assets/sprites/player/party/kingfisher_idle.png (128x128) [既有]"
    kingfisher["asset_naming_conventions"]["paperdoll_slices_dir"] = "game/assets/sprites/player/paperdoll/kingfisher/{slot_id}/{item_id}.png [既有]"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Updated", path)

if __name__ == "__main__":
    update_json(TABLE_PATH)
    update_json(DOCS_PATH)
