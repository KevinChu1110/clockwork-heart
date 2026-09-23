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
    if not any(v.get("id") == "paint_frog_emerald" for v in chassis_variants):
        chassis_variants.extend([
            {
                "id": "paint_frog_emerald",
                "name": "原廠薄荷翡翠綠琺瑯烤漆",
                "race": "frog",
                "tier": "common"
            },
            {
                "id": "paint_shadow_obsidian",
                "name": "黑曜暗影漆面",
                "race": "frog",
                "tier": "rare"
            }
        ])

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_spring_frog_stock" for v in head_variants):
        head_variants.append({
            "id": "head_spring_frog_stock",
            "name": "雙聯沖壓黃銅凸透鏡眼罩",
            "race": "frog",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_twin_wing_concentric" for v in key_variants):
        key_variants.append({
            "id": "key_twin_wing_concentric",
            "name": "雙蝶翼同心圓黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_spring_forest_courier" for v in costume_variants):
        costume_variants.append({
            "id": "costume_spring_forest_courier",
            "name": "碧簧巡林客工裝",
            "race": "frog",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    optic_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "core_azure_aperture" for v in optic_variants):
        optic_variants.append({
            "id": "core_azure_aperture",
            "name": "警醒明亮天藍光圈核心",
            "race": "frog",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "wpn_lotus_cog_dart" for v in weapon_variants):
        weapon_variants.append({
            "id": "wpn_lotus_cog_dart",
            "name": "碧葉旋刃機關鏢",
            "weapon_type": "dart",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_lotus_leaf_parasol" for v in curio_variants):
        curio_variants.append({
            "id": "curio_lotus_leaf_parasol",
            "name": "微型發條荷葉浮空傘",
            "race": "frog",
            "tier": "common"
        })

    # 2. Update races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 12

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "frog" for r in races_list):
        races_list.append({
            "race_id": "frog",
            "aliases": [
                "spring_frog",
                "jade_frog",
                "clockwork_frog"
            ],
            "name_zh": "碧簧蛙",
            "name_en": "The Spring-Leg Frog",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
            "lore_anchor": "自翡翠深林「巨木樹屋聚落」與「觀風石碑塔」旁跳躍巡守的發條跳蛙，通體由高光翠綠琺瑯馬口鐵板、雙球透鏡眼與雙層折疊板簧足柱組裝而成，以單持蓮葉旋刃機關鏢、極速看破突襲與多段飛鏢射殺見長的林間斥候",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (靈動半蹲低重心體態)",
                "posture": "半蹲蓄勁，右手單持碧葉旋刃機關鏢橫於胸前，左手平伸平衡，後腿板簧微屈，背部雙蝶翼鑰匙輕快自轉",
                "standee_height_px": 840,
                "standee_width_px": 440
            },
            "mechanical_features": {
                "head_and_neck": "寬扁圓弧沖壓薄鐵皮頭殼，配置雙聯沖壓黃銅圈高透石英凸透鏡眼與機械光圈調節環，下顎設有橫向折疊式吐鏢縫隙與微型散熱口",
                "ears": "無生物外耳，頭部兩側鑲嵌對稱的扁平沉頭黃銅調節旋鈕與微調彈簧螺栓",
                "torso_and_limbs": "胸腹覆蓋沖壓檸檬黃烤漆防撞鋼板，前肢為輕量化空心黃銅管，後肢為高扭力雙層折疊錳鋼板簧與減震阻尼活塞",
                "tail": "無尾部構造，後底盤配置一體成型平整黃銅防撞底托與背部發條插座法蘭盤",
                "weapon_system": "右手單持專利「碧葉旋刃機關鏢 / 破影蓮華連發鏢」，直徑24px，中心咬合黃銅微型滾珠軸承，左手空手平衡，完全符合 0-MKT7 與 ninja/dart 體系"
            },
            "color_palette": {
                "primary": "#4ED86A (薄荷翡翠綠琺瑯烤漆)",
                "secondary": "#FFD028 (檸檬鮮黃沖壓腹板)",
                "accent": "#FFA010 (暖橘發條齒輪箱飾邊與飛鏢銅環)",
                "detail": "#38A0FF (天藍發條之心晶石與石英透鏡雙眼)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "docs/art/spring_frog_concept.png (928x1152 概念立繪)",
                        "branding/char_frog.png (400x840 品牌立牌)",
                        "web/media/hero/char_frog.png (400x840 官網英雄圖)",
                        "web/media/hero/frog_idle.png (128x128 官網預覽圖)",
                        "game/assets/sprites/player/frog_idle.png (64x64 基礎待機)",
                        "game/assets/sprites/player/frog_idle_x3.png (128x128 高畫質待機)",
                        "game/assets/sprites/player/party/frog_idle.png (128x128 隊伍展示幀)",
                        "game/assets/sprites/player/frog_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/frog_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/frog_walk_{0..3}_x3.png (128x128 高畫質行走動畫)",
                        "game/assets/sprites/player/poses/frog/ (戰鬥6大動作姿態目錄)",
                        "game/assets/sprites/portraits/frog.png (128x128 HUD戰鬥頭像)",
                        "game/assets/sprites/portraits/spring_frog.png (384x480 對話框半身像)",
                        "game/assets/sprites/player/paperdoll/frog/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_frog.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/spring_frog_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_frog.png (400x840) [待產出]",
                "web_preview": "web/media/hero/frog_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/frog_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/frog_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/frog_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/frog_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/frog_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/frog_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/frog/{attack,hit,idle,recover,skill,telegraph}.png (128x128) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/frog.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/spring_frog.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/frog/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 12 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十二大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. Update directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    frog_dir = "game/assets/sprites/player/paperdoll/frog/"
    if frog_dir not in races_dirs:
        races_dirs.append(frog_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Successfully updated {path}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        update_file(p)
