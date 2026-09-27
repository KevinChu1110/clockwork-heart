#!/usr/bin/env python3
"""為第二十四族鐵拳袋鼠 (kangaroo) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/BOXER_KANGAROO_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 kangaroo 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_kangaroo_caramel_bronze_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_kangaroo_caramel_bronze_default",
            "name": "鐵拳袋鼠原廠焦糖暖褐赤銅素體",
            "race": "kangaroo",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_kangaroo_steampunk_boxer_visor" for v in head_variants):
        head_variants.append({
            "id": "head_kangaroo_steampunk_boxer_visor",
            "name": "蒸氣拳擊長耳護額頭盔",
            "race": "kangaroo",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_kangaroo_champion_double_ring" for v in key_variants):
        key_variants.append({
            "id": "key_kangaroo_champion_double_ring",
            "name": "沖壓黃銅雙環冠軍發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_kangaroo_champion_belt_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_kangaroo_champion_belt_harness",
            "name": "巨輪城工匠拳王加固背帶皮甲",
            "race": "kangaroo",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "optic_kangaroo_amber_dial_core" for v in face_variants):
        face_variants.append({
            "id": "optic_kangaroo_amber_dial_core",
            "name": "雙聯琥珀光學儀表目鏡",
            "race": "kangaroo",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_kangaroo_piston_brass_knuckle" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_kangaroo_piston_brass_knuckle",
            "name": "氣壓活塞衝壓黃銅拳套",
            "weapon_type": "fist",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_kangaroo_steam_exhaust_backpack" for v in curio_variants):
        curio_variants.append({
            "id": "curio_kangaroo_steam_exhaust_backpack",
            "name": "雙聯微型高壓蒸氣散熱背包",
            "race": "kangaroo",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 24

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "kangaroo" for r in races_list):
        races_list.append({
            "race_id": "kangaroo",
            "aliases": [
                "boxer_kangaroo",
                "steam_kangaroo",
                "brass_kangaroo",
                "champion_kangaroo"
            ],
            "name_zh": "鐵拳袋鼠",
            "name_en": "The Boxer Kangaroo",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "常駐於黃銅都市「中央動力廣場」與「摩天齒輪工坊群」的發條拳擊家，穿梭於「高架重軌引橋·巨輪城站」、「深淵排污豎井管道」與「中央蒸氣沐浴池」之間，通體由多巴胺焦糖暖褐赤銅板件、溫潤奶油米白琺瑯面頰與腹袋、蒸氣拳擊長耳護額頭盔、雙聯琥珀光學儀表目鏡、雙環冠軍黃銅發條鑰匙與冷軋鎢鋼雙螺旋減震彈簧後腿組裝而成，以右手單戴氣壓活塞衝壓黃銅拳套、西洋拳擊步法輕快彈跳與過載升龍重拳見長的蒸氣拳擊工匠",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (西洋拳擊起手架式、梨形挺拔彈跳身軀)",
                "posture": "輕快彈跳拳擊起手架式，右手重裝活塞拳套護於胸前作攻擊準備，左拳半握前探護胸蓄勁，身後分節重力平衡長尾微幅點地，背部雙環冠軍黃銅發條鑰匙勻速旋轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓耐磨黃銅拳擊護額頭盔，頭頂配備雙聯沖壓薄銅長耳（耳背設有縱向排氣散熱狹縫），下顎為奶油米白烤漆面頰板配外露螺栓，雙眼為雙聯琥珀光學儀表目鏡",
                "ears": "雙聯沖壓薄銅長耳，耳背設有縱向蒸氣排氣細縫，隨拳擊出拳洩壓微幅前後律動",
                "torso_and_limbs": "背部與側腰覆蓋多巴胺焦糖暖褐赤銅板件，前胸覆蓋奶油米白琺瑯沖壓齒輪置物袋並預留直徑14px晶石孔，胸口內嵌菱形發條之心金黃晶核，下肢為兩組外露冷軋鎢鋼雙螺旋減震彈簧腿",
                "tail": "由四節黃銅套管鉸鏈組裝而成的重力平衡長尾，尾端帶有一枚圓柱形鑄鐵配重塊，確保高速跳躍出拳重心穩固",
                "weapon_system": "右手單戴重裝專利「氣壓活塞衝壓黃銅拳套」，拳面配備雙聯氣動活塞衝頭與黃銅鉚接指節護板，腕部帶有小型黃銅蓄氣筒與洩壓管，左手平曲護胸抱拳蓄勁，完全符合 0-MKT7 與 monk/fist 體系，底層掛載 equipment.json 既有 wrap_gloves 與 iron_knuckle"
            },
            "color_palette": {
                "primary": "#C86D20 (沖壓厚鑄耐磨焦糖暖褐赤銅裝甲板)",
                "secondary": "#FFFDF8 (溫潤奶油米白琺瑯面頰與腹袋置物外殼)",
                "accent": "#FFD028 (多巴胺金黃雙環冠軍發條鑰匙與前袋沖壓齒輪徽飾)",
                "detail": "#FF9F1C (雙眼琥珀真空儀表透鏡與胸口發條之心晶核)",
                "warm_highlight": "#E63946 (多巴胺冠軍胡桃鉗朱紅拳套裝甲與肩甲滾邊)",
                "secondary_hull": "#FFA010 (暖橘蒸氣導熱導管與指針刻度線)",
                "titanium_frame": "#4A5568 (冷軋鎢鋼雙腿減震螺旋彈簧與尾部配重塊)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_kangaroo.png (品牌形象立牌)",
                        "web/media/hero/char_kangaroo.png (官網英雄展示立繪)",
                        "docs/art/boxer_kangaroo_concept.png (概念立繪)",
                        "game/assets/sprites/player/kangaroo_idle.png (64x64 待機)",
                        "game/assets/sprites/player/kangaroo_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/kangaroo_idle.png (隊伍待機)",
                        "game/assets/sprites/player/kangaroo_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/kangaroo_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/kangaroo_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/kangaroo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/kangaroo.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/boxer_kangaroo.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/kangaroo/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_kangaroo.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/boxer_kangaroo_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_kangaroo.png (400x840) [待產出]",
                "web_preview": "web/media/hero/kangaroo_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/kangaroo_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/kangaroo_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/kangaroo_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/kangaroo_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/kangaroo_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/kangaroo_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/kangaroo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/kangaroo.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/boxer_kangaroo.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/kangaroo/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 24 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十四大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    kangaroo_dir = "game/assets/sprites/player/paperdoll/kangaroo/"
    if kangaroo_dir not in races_dirs:
        races_dirs.append(kangaroo_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/kangaroo")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/kangaroo")
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
