#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

SCORPION_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_scorpion_stock",
        "name": "荒漠沖壓馬口鐵沙蠍底盤",
        "tier": "common",
        "race": "scorpion"
    },
    "head_unit": {
        "id": "head_scorpion_dune_visor",
        "name": "沖壓防沙折角金屬面盔",
        "tier": "common",
        "race": "scorpion"
    },
    "winding_key": {
        "id": "key_scorpion_cross_brass",
        "name": "荒漠四角齒輪雕花黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_scorpion_scavenger_plate",
        "name": "荒漠拾荒鉚接生漆板甲胸甲",
        "tier": "common",
        "race": "scorpion"
    },
    "optic_core": {
        "id": "face_scorpion_amber_goggles",
        "name": "雙聯高透琥珀金晶琉璃圓形目鏡",
        "tier": "common",
        "race": "scorpion"
    },
    "weapon": {
        "id": "weapon_scorpion_duneshadow_dart",
        "name": "沙丘穿棘機關鏢",
        "tier": "common",
        "weapon_type": "dart"
    },
    "back_curio": {
        "id": "curio_scorpion_spring_stinger_tail",
        "name": "多節同軸彈簧尾刺導軌與配重重錘",
        "tier": "common",
        "race": "scorpion"
    }
}

SCORPION_RACE_SPEC = {
    "race_id": "scorpion",
    "aliases": [
        "duneshadow_scorpion",
        "sand_scorpion",
        "clockwork_scorpion",
        "tinplate_scorpion",
        "stinger_scorpion",
        "junkyard_scorpion"
    ],
    "name_zh": "伏影沙蠍",
    "name_en": "The Duneshadow Scorpion",
    "class_archetype": "忍者 (Ninja)",
    "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
    "starter_weapon": "mist_darts",
    "weapon_class": "dart",
    "lore_anchor": "穿行於荒漠齒輪塚·遺忘舊庫「巨型零件殘骸沙丘」、「拾荒拼裝聚落·齒輪營地」與「舊庫重型吊裝龍門架」，巡邏於「深褐色斑駁的生鏽粗鑄生鐵壁板與加固黃銅鉚釘角鋼」之沙盤邊界，守護「零件分揀斜坡裂谷」、「冷卻熔渣重力傾卸滑道·舊庫受料口」、「軌道廢棄排障滑道·舊庫分揀倉」與「大齒輪懸索天梯·舊庫總站」，在狂暴沙塵漫反射風鏡界面下引導廢料沉降磁吸緩衝沙漏，結伴補丁爺爺、劍客阿席與小駱駝嘟嘟，護衛拾荒拼裝布偶、生鏽發條浪人與發條除鏽工兵偶；通體覆蓋荒漠沖壓耐磨馬口鐵底盤、沖壓防沙折角金屬面盔、雙聯高透琥珀金晶琉璃圓形目鏡、荒漠拾荒鉚接生漆板甲胸甲、多節同軸彈簧尾刺導軌與配重重錘、荒漠四角齒輪雕花黃銅發條鑰匙，手持沙丘穿棘機關鏢，以2.2頭身矮萌靈動身軀、低重心貼地伏行步法、真假同色的一手與風沙看破穿刺見長的廢土沙丘穿棘潛行特工忍者",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 歐美與日本野村發條鐵皮行走蠍子自動偶)",
        "posture": "2.2 頭身矮萌身軀呈低重心貼地伏行站位，右手單手將沙丘穿棘機關鏢橫於胸前，左前肢黃銅剪鉗微屈呈現防禦守勢，身後五節同軸彈簧黃銅尾如鐘擺般節律輕晃，背後四角發條鑰匙隨舊庫秒針每2.5~3.5秒跳動勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "ears_cowl": "沖壓防沙折角金屬面盔，弧形導流斜角設計，內置雙聯黃銅百葉散熱格柵與微型黃銅避震天線，奔跑跳躍微幅震顫",
        "eyes": "雙聯大尺寸高透琥珀金晶琉璃圓形目鏡，深藍紫金屬防眩光密封眼圈，浮現天藍同心瞄準分劃線與暖橙指針",
        "pincers": "前肢雙聯沖壓黃銅齒輪開合剪鉗，微型鈍化黃銅鋸齒，外側塗裝暖橘與金黃烤漆，開合清脆扎實",
        "tail": "五節鉸接沖壓黃銅同軸彈簧尾，內置銅絲牽引軸芯，尾端裝配圓形黃銅防後座阻尼重錘與機關鏢發射槽",
        "torso_and_limbs": "落日暖橘沖壓耐磨冷軋馬口鐵板件，黃銅球形關節，六足底端覆蓋耐磨防滑黑色橡膠吸附墊",
        "key": "荒漠四角齒輪雕花黃銅發條鑰匙，輪緣呈古典機械齒輪交錯咬合造型，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#FFA010 (落日暖橘沖壓面盔與胸腹耐磨生漆板件)",
        "secondary": "#FFD028 (天元金黃四角發條鑰匙、多節尾刺導軌與黃銅剪鉗齒輪)",
        "accent_blue": "#38A0FF (天藍防眩光琉璃目鏡分劃與拾荒防撞標籤)",
        "accent_mint": "#4ED86A (薄荷綠軸承防震膠圈與機關鏢陀螺軸承襯套)",
        "accent_white": "#FFFDF8 (奶油米白胸腹裝甲高光嵌片與剪鉗護角)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與尾刺頂部減震墊)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_scorpion.png (品牌形象立牌)",
                "web/media/hero/char_scorpion.png (官網英雄展示立繪)",
                "docs/art/duneshadow_scorpion_concept.png (概念立繪)",
                "game/assets/sprites/player/scorpion_idle.png (64x64 待機)",
                "game/assets/sprites/player/scorpion_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/scorpion_idle.png (隊伍待機)",
                "web/media/hero/scorpion_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/scorpion_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/scorpion_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/scorpion_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/scorpion_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/scorpion_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/scorpion_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/scorpion/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/scorpion.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/scorpion_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/duneshadow_scorpion.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/scorpion/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_scorpion.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/duneshadow_scorpion_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_scorpion.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/scorpion_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/scorpion_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/scorpion_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/scorpion_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/scorpion_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/scorpion_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/scorpion_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/scorpion/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/scorpion.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/duneshadow_scorpion.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/scorpion/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_scorpion_stock",
        "head_unit": "head_scorpion_dune_visor",
        "optic_core": "face_scorpion_amber_goggles",
        "costume": "costume_scorpion_scavenger_plate",
        "back_curio": "curio_scorpion_spring_stinger_tail",
        "winding_key": "key_scorpion_cross_brass",
        "weapon": "weapon_scorpion_duneshadow_dart"
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
        if slot_id in SCORPION_DEFAULT_ITEMS:
            item = SCORPION_DEFAULT_ITEMS[slot_id]
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
    if "scorpion" not in existing_race_ids:
        races.append(SCORPION_RACE_SPEC)
        print("  Added scorpion to races_specification.races")
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
            if "伏影沙蠍" not in old_rule:
                new_rule = old_rule.replace("六十九重大種族", "七十重大種族")
                target_str = "闢道頑驢集市工兵沖壓馬口鐵金屬底盤與集市工兵鉚接生漆板甲胸甲)"
                if target_str in new_rule:
                    new_rule = new_rule.replace(
                        target_str,
                        "闢道頑驢集市工兵沖壓馬口鐵金屬底盤與集市工兵鉚接生漆板甲胸甲、伏影沙蠍荒漠沖壓馬口鐵沙蠍底盤與荒漠拾荒鉚接生漆板甲胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    scorpion_dir = "game/assets/sprites/player/paperdoll/scorpion/"
    if scorpion_dir not in races_dirs:
        races_dirs.append(scorpion_dir)
        print(f"  Added {scorpion_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Duneshadow Scorpion proposal registered specification complete.")
