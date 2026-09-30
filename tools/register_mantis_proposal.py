#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

MANTIS_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_mantis_stock",
        "name": "蔓谷沖壓薄銅螳螂底盤",
        "tier": "common",
        "race": "mantis"
    },
    "head_unit": {
        "id": "head_mantis_canopy_cowl",
        "name": "沖壓林冠折角金屬面盔",
        "tier": "common",
        "race": "mantis"
    },
    "winding_key": {
        "id": "key_mantis_vine_brass",
        "name": "蔓谷雙環藤蔓雕花黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_mantis_vine_plate",
        "name": "蔓谷藤蔓鉚接生漆板甲胸甲",
        "tier": "common",
        "race": "mantis"
    },
    "optic_core": {
        "id": "face_mantis_emerald_goggles",
        "name": "雙聯高透翡翠石英琉璃球形目鏡",
        "tier": "common",
        "race": "mantis"
    },
    "weapon": {
        "id": "weapon_mantis_scythe_claw",
        "name": "翠刃連斬機關爪",
        "tier": "common",
        "weapon_type": "claw"
    },
    "back_curio": {
        "id": "curio_mantis_spring_pack",
        "name": "多節同軸彈簧平衡背囊與微型排氣風箱",
        "tier": "common",
        "race": "mantis"
    }
}

MANTIS_RACE_SPEC = {
    "race_id": "mantis",
    "aliases": [
        "jade_mantis",
        "emerald_mantis",
        "clockwork_mantis",
        "tinplate_mantis",
        "scythe_mantis",
        "canopy_mantis"
    ],
    "name_zh": "翠刃螳螂",
    "name_en": "The Jade Mantis",
    "class_archetype": "武術家 (Monk)",
    "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
    "starter_weapon": "hunt_claw",
    "weapon_class": "claw",
    "lore_anchor": "穿梭於翡翠深林·發條蔓谷「機械巨木」、「發條藤蔓」與「樹脂發光菌菇」，巡邏於「加厚短絨氈毛地毯」下方黃銅防滑薄板，守護「樹屋聚落」、「蔓谷天梯引道·深林站」、「晨曦天軌 3 號月台」與「高架重軌引橋·巨輪城站」，巡視「赤焰索道懸橋」並引導迷途玩具重返「防護金屬藤蔓彈力網」，在「丁達爾發條晨曦光斑」下維護金屬防鏽齒輪樹汁導流泵，結伴守林哨兵·風耳、靈尾工藝師·小鈴與老鹿木匠·角木，護衛守林發條小鹿、發條松鼠信差與林木守護木偶；通體覆蓋蔓谷沖壓薄銅螳螂底盤、沖壓林冠折角金屬面盔、雙聯高透翡翠石英琉璃球形目鏡、蔓谷藤蔓鉚接生漆板甲胸甲、多節同軸彈簧平衡背囊與微型排氣風箱、蔓谷雙環藤蔓雕花黃銅發條鑰匙，手持翠刃連斬機關爪，以2.2頭身矮萌靈動身軀、停拍看破連切、撕裂防線與爪痕破勢見長的林冠穿林連切破勢大師武術家",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 歐美與日本野村發條鐵皮行走螳螂自動偶)",
        "posture": "2.2 頭身矮萌身軀呈靈動挺立站位，右手單手將翠刃連斬機關爪橫於胸前，左前肢鐮爪微屈呈現防禦守勢，頭頂雙天線隨風輕擺，背後雙環發條鑰匙隨深林秒針每3~4秒跳動勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 480
    },
    "mechanical_features": {
        "ears_cowl": "沖壓林冠折角金屬面盔，倒三角流線導流斜角設計，內置雙聯黃銅百葉散熱格柵與兩根螺旋黃銅避震天線，隨風靈敏微顫",
        "eyes": "雙聯大尺寸高透翡翠石英琉璃球形目鏡，深藍紫金屬防眩光密封眼圈，浮現天藍同心瞄準分劃線與暖金指針",
        "scythe_claws": "前肢雙聯沖壓薄銅折疊鐮爪，內置微型偏心凸輪軸承與鈍化防磨棘齒，外側塗裝薄荷綠與金黃生漆，展開迅捷清脆",
        "back_pack": "三節鉸接沖壓薄銅同軸彈簧平衡背囊，內置發條減震扭簧與手風琴式排氣微囊，出爪時微量排氣平衡動能",
        "torso_and_limbs": "薄荷綠沖壓薄銅板件，黃銅球形關節，六足底端覆蓋耐磨防滑黑色橡膠吸附墊",
        "key": "蔓谷雙環藤蔓雕花黃銅發條鑰匙，輪緣呈古典藤蔓交錯纏繞雕花造型，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#4ED86A (薄荷綠沖壓面盔與胸腹耐磨生漆板件)",
        "secondary": "#FFD028 (天元金黃雙環發條鑰匙、黃銅關節與機關爪刃部)",
        "accent_blue": "#38A0FF (天藍防眩光琉璃目鏡分劃與林間巡檢防撞標籤)",
        "accent_orange": "#FFA010 (落日暖橘關節防震膠圈與散熱百葉窗襯條)",
        "accent_white": "#FFFDF8 (奶油米白胸腹裝甲高光嵌片與面盔導流條)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與天線頂珠)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_mantis.png (品牌形象立牌)",
                "web/media/hero/char_mantis.png (官網英雄展示立繪)",
                "docs/art/jade_mantis_concept.png (概念立繪)",
                "game/assets/sprites/player/mantis_idle.png (64x64 待機)",
                "game/assets/sprites/player/mantis_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/mantis_idle.png (隊伍待機)",
                "web/media/hero/mantis_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/mantis_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/mantis_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/mantis_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/mantis_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/mantis_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/mantis_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/mantis/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/mantis.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/mantis_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/jade_mantis.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/mantis/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_mantis.png (480x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/jade_mantis_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_mantis.png (480x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/mantis_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/mantis_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/mantis_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/mantis_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/mantis_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/mantis_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/mantis_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/mantis/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/mantis.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/jade_mantis.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/mantis/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_mantis_stock",
        "head_unit": "head_mantis_canopy_cowl",
        "optic_core": "face_mantis_emerald_goggles",
        "costume": "costume_mantis_vine_plate",
        "back_curio": "curio_mantis_spring_pack",
        "winding_key": "key_mantis_vine_brass",
        "weapon": "weapon_mantis_scythe_claw"
    }
}

for file_path in TARGET_FILES:
    print(f"Processing {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Update default_items in slots_architecture.slots
    slots = data["slots_architecture"]["slots"]
    for s in slots:
        slot_id = s["slot_id"]
        if slot_id in MANTIS_DEFAULT_ITEMS:
            item = MANTIS_DEFAULT_ITEMS[slot_id]
            if "default_items" not in s:
                s["default_items"] = []
            existing_ids = [x["id"] for x in s["default_items"]]
            if item["id"] not in existing_ids:
                s["default_items"].append(item)
                print(f"  Added {item['id']} to slot {slot_id} default_items")

    # 2. Update races_specification
    races_spec = data["races_specification"]
    races = races_spec["races"]
    existing_race_ids = [r["race_id"] for r in races]
    if "mantis" not in existing_race_ids:
        races.append(MANTIS_RACE_SPEC)
        print("  Added mantis to races_specification.races")
    races_spec["total_races"] = len(races)
    print(f"  Updated total_races to {len(races)}")

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    univ = compat.get("universal_slots", [])
    for u in univ:
        if u.get("slot_id") == "winding_key":
            u["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races)} 種動物素體"
    adapted = compat.get("race_adapted_slots", [])
    for a in adapted:
        if a.get("slot_id") == "costume":
            old_rule = a.get("rule", "")
            if "翠刃螳螂" not in old_rule:
                new_rule = old_rule.replace("七十重大種族", "七十一重大種族")
                target_str = "伏影沙蠍荒漠沖壓馬口鐵沙蠍底盤與荒漠拾荒鉚接生漆板甲胸甲)"
                if target_str in new_rule:
                    new_rule = new_rule.replace(
                        target_str,
                        "伏影沙蠍荒漠沖壓馬口鐵沙蠍底盤與荒漠拾荒鉚接生漆板甲胸甲、翠刃螳螂蔓谷沖壓薄銅螳螂底盤與蔓谷藤蔓鉚接生漆板甲胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    mantis_dir = "game/assets/sprites/player/paperdoll/mantis/"
    if mantis_dir not in races_dirs:
        races_dirs.append(mantis_dir)
        print(f"  Added {mantis_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Jade Mantis proposal registered specification complete.")
