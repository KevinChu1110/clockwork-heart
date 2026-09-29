#!/usr/bin/env python3
"""
update_petaurista_official_assets_metadata.py
Updates docs/design/paperdoll_slots.json and game/data/tables/paperdoll_slots.json
to mark all official assets suite items for The Stormwing Petaurista (petaurista) as existing.
"""

import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def update_file(path):
    print(f"Updating {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    races = data["races_specification"]["races"]
    petaurista = None
    for r in races:
        if r.get("race_id") == "petaurista":
            petaurista = r
            break

    if not petaurista:
        raise ValueError(f"Petaurista race not found in {path}!")

    asset_naming = petaurista.get("asset_naming_conventions", {})
    existing = [
        "game/assets/sprites/player/petaurista_idle.png (64x64 待機)",
        "game/assets/sprites/player/petaurista_idle_x3.png (128x128 待機)",
        "game/assets/sprites/player/party/petaurista_idle.png (隊伍待機)",
        "web/media/hero/petaurista_idle.png (128x128 官網待機)",
        "game/assets/sprites/player/showcase/petaurista_idle_hd.png (800x1200 HD 展示立繪)",
        "branding/char_petaurista.png (品牌形象立牌)",
        "web/media/hero/char_petaurista.png (官網英雄展示立繪)",
        "docs/art/stormwing_petaurista_concept.png (概念立繪)",
        "game/assets/sprites/player/petaurista_battle.png (128x128 戰鬥特寫姿態)",
        "game/assets/sprites/player/petaurista_battle_512.png (512x512 戰鬥特寫姿態)",
        "game/assets/sprites/player/petaurista_walk_{0..3}.png (64x64 行走動畫)",
        "game/assets/sprites/player/petaurista_walk_{0..3}_x3.png (128x128 行走動畫)",
        "game/assets/sprites/player/petaurista_walk_{0..3}_512.png (512x512 行走動畫)",
        "game/assets/sprites/player/poses/petaurista/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
        "game/assets/sprites/portraits/petaurista.png (HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/petaurista_512.png (512x512 HUD 戰鬥頭像)",
        "game/assets/sprites/portraits/stormwing_petaurista.png (對話半身像)",
        "game/assets/sprites/player/paperdoll/petaurista/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
    ]

    asset_naming["status"] = {
        "existing": existing,
        "pending": []
    }
    asset_naming["branding_standee"] = "branding/char_petaurista.png (420x840 -> 1344x1680) [既有]"
    asset_naming["branding_concept_art"] = "docs/art/stormwing_petaurista_concept.png (928x1152) [既有]"
    asset_naming["web_hero"] = "web/media/hero/char_petaurista.png (420x840 -> 1344x1680) [既有]"
    asset_naming["web_preview"] = "web/media/hero/petaurista_idle.png (128x128) [既有]"
    asset_naming["game_sprite_idle_base"] = "game/assets/sprites/player/petaurista_idle.png (64x64) [既有]"
    asset_naming["game_sprite_idle_hi"] = "game/assets/sprites/player/petaurista_idle_x3.png (128x128) [既有]"
    asset_naming["game_sprite_party_idle"] = "game/assets/sprites/player/party/petaurista_idle.png (128x128) [既有]"
    asset_naming["game_sprite_battle"] = "game/assets/sprites/player/petaurista_battle.png (128x128) [既有]"
    asset_naming["game_sprite_walk"] = "game/assets/sprites/player/petaurista_walk_{0..3}.png (64x64) [既有]"
    asset_naming["game_sprite_walk_hi"] = "game/assets/sprites/player/petaurista_walk_{0..3}_x3.png (128x128) [既有]"
    asset_naming["game_action_poses"] = "game/assets/sprites/player/poses/petaurista/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [既有]"
    asset_naming["portrait_hud"] = "game/assets/sprites/portraits/petaurista.png (128x128) [既有]"
    asset_naming["portrait_dialogue"] = "game/assets/sprites/portraits/stormwing_petaurista.png (384x480) [既有]"
    asset_naming["paperdoll_slices_dir"] = "game/assets/sprites/player/paperdoll/petaurista/{slot_id}/{item_id}.png [既有]"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✓ Updated {path}")


def main():
    update_file(f"{REPO_ROOT}/docs/design/paperdoll_slots.json")
    update_file(f"{REPO_ROOT}/game/data/tables/paperdoll_slots.json")


if __name__ == "__main__":
    main()
