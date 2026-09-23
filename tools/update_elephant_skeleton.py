#!/usr/bin/env python3
import json
import sys

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Update sample_variants in slots_architecture
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "paint_elephant_brass" for v in chassis_variants):
        chassis_variants.extend([
            {
                "id": "paint_elephant_brass",
                "name": "原廠巨輪工坊黃銅原金",
                "race": "elephant",
                "tier": "common"
            },
            {
                "id": "paint_tungsten_iron",
                "name": "高爐鎢鋼淬火黑",
                "race": "elephant",
                "tier": "rare"
            }
        ])

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_colossus_elephant_stock" for v in head_variants):
        head_variants.append({
            "id": "head_colossus_elephant_stock",
            "name": "沖壓深金頂盔與六節套筒長鼻",
            "race": "elephant",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_heavy_cross_wheel" for v in key_variants):
        key_variants.append({
            "id": "key_heavy_cross_wheel",
            "name": "重工十字同心輪造型黃銅鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_cog_workshop_overalls" for v in costume_variants):
        costume_variants.append({
            "id": "costume_cog_workshop_overalls",
            "name": "巨輪工坊先鋒吊帶甲",
            "race": "elephant",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    optic_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "core_sky_quartz" for v in optic_variants):
        optic_variants.append({
            "id": "core_sky_quartz",
            "name": "原廠天藍石英透鏡核心",
            "race": "elephant",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "wpn_colossus_cleaver_axe" for v in weapon_variants):
        weapon_variants.append({
            "id": "wpn_colossus_cleaver_axe",
            "name": "巨輪開山重斧",
            "weapon_type": "axe",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_dual_pressure_gauge" for v in curio_variants):
        curio_variants.append({
            "id": "curio_dual_pressure_gauge",
            "name": "雙聯黃銅蒸氣壓力表與減壓排氣閥",
            "race": "elephant",
            "tier": "common"
        })

    # 2. Update races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 11

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "elephant" for r in races_list):
        races_list.append({
            "race_id": "elephant",
            "aliases": [
                "colossus_elephant",
                "iron_elephant"
            ],
            "name_zh": "鋼岳象",
            "name_en": "The Colossus Elephant",
            "class_archetype": "戰士 (Viking)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "自巨輪城「中央動力廣場」巨型摩天齒輪樞紐下甦醒的發條鋼象，通體由厚鑄黃銅板件、六節套筒液壓長鼻與扇形散熱耳板組裝而成，以單持飛輪開山戰斧、極限質量重斬與一擊破陣見長的重工先鋒",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (沉穩巍峨重裝體態)",
                "posture": "扎實立足，右手單持巨輪開山重斧垂直立於身側，左手握拳垂放平衡，長鼻微卷排氣，背部十字同心輪鑰匙強勁自轉",
                "standee_height_px": 840,
                "standee_width_px": 440
            },
            "mechanical_features": {
                "head_and_neck": "半球狀深金厚鋼頭殼，配置六節套筒式拋光黃銅液壓長鼻與雙瓣沖壓排氣噴嘴，面部鑲嵌一對象牙色高光合金防撞鈍角短角與雙聯天藍石英鏡片",
                "ears": "扇形沖壓鉚接雙層散熱金屬耳板，外緣帶有一圈沉頭十字螺栓，內側刻有多道輻射狀散熱鰭片",
                "torso_and_limbs": "胸腹覆蓋圓弧象牙合金純白防撞鋼板，四肢為四柱重裝液壓活塞足柱，足底配置防滑圓柱橡膠襯墊",
                "tail": "三節鉸鏈沖壓黃銅避雷接地短尾舵，平貼於底盤後端維持重心平衡",
                "weapon_system": "右手單持專利「巨輪開山重斧 / 撼地飛輪戰斧」，斧身長48px，中心咬合直徑16px黃銅同心齒輪配重盤，左手空手垂放，完全符合 0-MKT7 與 viking/axe 體系"
            },
            "color_palette": {
                "primary": "#D4A017 (淬火黃銅原金金屬烤漆)",
                "secondary": "#FFFDF8 (象牙合金純白防撞胸甲)",
                "accent": "#FFA010 (高壓蒸氣暖橘排氣閥與耳邊鑲飾)",
                "detail": "#38A0FF (天藍發條之心晶石與石英透鏡雙眼)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "docs/art/colossus_elephant_concept.png (928x1152 概念立繪)",
                        "branding/char_elephant.png (400x840 品牌立牌)",
                        "web/media/hero/char_elephant.png (400x840 官網英雄圖)",
                        "web/media/hero/elephant_idle.png (128x128 官網預覽圖)",
                        "game/assets/sprites/player/elephant_idle.png (64x64 基礎待機)",
                        "game/assets/sprites/player/elephant_idle_x3.png (128x128 高畫質待機)",
                        "game/assets/sprites/player/party/elephant_idle.png (128x128 隊伍展示幀)",
                        "game/assets/sprites/player/elephant_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/elephant_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/elephant_walk_{0..3}_x3.png (128x128 高畫質行走動畫)",
                        "game/assets/sprites/player/poses/elephant/ (戰鬥6大動作姿態目錄)",
                        "game/assets/sprites/portraits/elephant.png (128x128 HUD戰鬥頭像)",
                        "game/assets/sprites/portraits/colossus_elephant.png (384x480 對話框半身像)",
                        "game/assets/sprites/player/paperdoll/elephant/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_elephant.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/colossus_elephant_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_elephant.png (400x840) [待產出]",
                "web_preview": "web/media/hero/elephant_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/elephant_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/elephant_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/elephant_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/elephant_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/elephant_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/elephant_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/elephant/{attack,hit,idle,recover,skill,telegraph}.png (128x128) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/elephant.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/colossus_elephant.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/elephant/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 11 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十一大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. Update directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    elephant_dir = "game/assets/sprites/player/paperdoll/elephant/"
    if elephant_dir not in races_dirs:
        races_dirs.append(elephant_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Successfully updated {path}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        update_file(p)
