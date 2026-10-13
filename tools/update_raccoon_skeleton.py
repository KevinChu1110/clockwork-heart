#!/usr/bin/env python3
"""為第二十族星巡浣熊 (raccoon) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/ORBIT_RACCOON_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 raccoon 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_raccoon_orbit_aqua_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_raccoon_orbit_aqua_default",
            "name": "電光航太青工程聚合物板件",
            "race": "raccoon",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_raccoon_parabolic_radar_dish" for v in head_variants):
        head_variants.append({
            "id": "head_raccoon_parabolic_radar_dish",
            "name": "雙聯碟形定向通訊雷達耳",
            "race": "raccoon",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_raccoon_quad_solar_sail" for v in key_variants):
        key_variants.append({
            "id": "key_raccoon_quad_solar_sail",
            "name": "四葉光子太陽能翼板發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_raccoon_space_explorer_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_raccoon_space_explorer_harness",
            "name": "星穹宇航探險工裝背帶",
            "race": "raccoon",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_raccoon_hud_polarizer_visor" for v in face_variants):
        face_variants.append({
            "id": "face_raccoon_hud_polarizer_visor",
            "name": "深邃偏光瞄準護目鏡罩",
            "race": "raccoon",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_raccoon_anti_gravity_pulse_blaster" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_raccoon_anti_gravity_pulse_blaster",
            "name": "反重力脈衝光銃",
            "weapon_type": "gun",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_raccoon_coaxial_ring_antenna_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_raccoon_coaxial_ring_antenna_tail",
            "name": "五節同軸高壓放電環形天線長尾",
            "race": "raccoon",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 20

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "raccoon" for r in races_list):
        races_list.append({
            "race_id": "raccoon",
            "aliases": [
                "orbit_raccoon",
                "starfall_raccoon",
                "astro_raccoon",
                "space_raccoon"
            ],
            "name_zh": "星巡浣熊",
            "name_en": "The Orbit Raccoon",
            "class_archetype": "遊俠 (Ranger)",
            "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
            "lore_anchor": "穿梭於星穹軌道「聚合物透明太空艙」與「太空拼裝維修船塢」的發條浣熊，漫步於「高光懸空螢光軌道」與「太陽能帆板與微型排氣天線」之間，通體由電光航太青工程聚合物板件、象牙米白工程塑料胸腹板、雙聯微型碟形定向通訊雷達耳、防滑磁吸工程矽膠靴與五節同軸環形天線長尾組裝而成，以右手單持反重力脈衝光銃、失重滑行反衝彈射與超光速過載脈衝掃射見長的星穹神射遊俠",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (圓滾滾靈巧太空聚合物體態)",
                "posture": "失重懸停持銃架式，右手單提反重力脈衝光銃斜向身前，左手平抬胸前作頻率校準，身後五節環形天線長尾自然翹起，背部四葉太陽能翼板發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "圓潤球形聚合物頭盔部，配有象牙米白工程塑料面頰板與微型螺紋套筒吻部，雙眼為深邃偏光瞄準護目鏡罩，內含雙聯直徑22px薄荷螢綠瞄準光圈與左右六根鍍銀高頻信號探針鬍鬚",
                "ears": "一對360度活動微型碟形定向通訊雷達耳閥，外緣帶有黃銅緊固圓環，內置微型拾音濾網",
                "torso_and_limbs": "背部與側身覆蓋厚度1.5mm多巴胺電光航太青工程塑料板件，前胸覆蓋圓弧象牙米白減震工程塑料板，四肢末端裝配吸震防滑厚底黑色磁吸工程矽膠靴與微型導軌吸盤",
                "tail": "由五節沖壓導電金屬環與夜光聚合物絕緣件鉸接而成的同軸高壓放電長尾，蓄能時自根部逐環亮起電光青霓虹光暈",
                "weapon_system": "右手單持專利「反重力脈衝光銃 / 軌道聚焦發條銃」，高精度輕量聚合物線圈槍管配合高壓排氣管，左手空手導向平衡，完全符合 0-MKT7 與 ranger/gun 體系，底層掛載 equipment.json 既有 blackpowder_rifle"
            },
            "color_palette": {
                "primary": "#00C2CB (電光航太青工程聚合物外殼)",
                "secondary": "#FFFDF8 (象牙米白工程塑料面頰與胸腹減震板)",
                "accent": "#FFD028 (金黃光子太陽能翼板發條鑰匙與耳廓銅圈)",
                "detail": "#4ED86A (薄荷螢綠HUD能量游標與瞄準鏡透鏡光圈)",
                "warm_highlight": "#FF5E8A (珊瑚粉耐壓真空密封矽膠圈與冷氣噴嘴)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_raccoon.png (品牌形象立牌)",
                        "web/media/hero/char_raccoon.png (官網英雄展示立繪)",
                        "docs/art/orbit_raccoon_concept.png (概念立繪)",
                        "game/assets/sprites/player/raccoon_idle.png (64x64 待機)",
                        "game/assets/sprites/player/raccoon_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/raccoon_idle.png (隊伍待機)",
                        "game/assets/sprites/player/raccoon_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/raccoon_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/raccoon_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/raccoon/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/raccoon.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/orbit_raccoon.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/raccoon/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_raccoon.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/orbit_raccoon_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_raccoon.png (400x840) [待產出]",
                "web_preview": "web/media/hero/raccoon_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/raccoon_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/raccoon_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/raccoon_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/raccoon_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/raccoon_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/raccoon_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/raccoon/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/raccoon.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/orbit_raccoon.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/raccoon/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 20 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    raccoon_dir = "game/assets/sprites/player/paperdoll/raccoon/"
    if raccoon_dir not in races_dirs:
        races_dirs.append(raccoon_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/raccoon")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/raccoon")
    os.makedirs(poses_dir, exist_ok=True)
    poses_keep = os.path.join(poses_dir, ".gitkeep")
    if not os.path.exists(poses_keep):
        with open(poses_keep, "w") as f:
            pass
        print(f"建立 {poses_keep}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_gitkeeps(repo_root)
    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        update_paperdoll_slots(os.path.join(repo_root, p))
