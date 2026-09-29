#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

KINGFISHER_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_kingfisher_enamel_default",
        "name": "竹影沖壓彩釉琺瑯金屬底盤",
        "tier": "common",
        "race": "kingfisher"
    },
    "head_unit": {
        "id": "head_kingfisher_beak_lance_cowl",
        "name": "雙聯微調黃銅鳥喙長刺面盔",
        "tier": "common",
        "race": "kingfisher"
    },
    "winding_key": {
        "id": "key_kingfisher_zen_taichi_gear_brass",
        "name": "天元太極雙輪黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_kingfisher_dojo_lacquer_cuirass",
        "name": "天元道場生漆編織輕量戰袍胸甲",
        "tier": "common",
        "race": "kingfisher"
    },
    "optic_core": {
        "id": "face_kingfisher_zen_slate_goggles",
        "name": "雙聯高透青石琉璃圓形目鏡",
        "tier": "common",
        "race": "kingfisher"
    },
    "weapon": {
        "id": "weapon_kingfisher_bamboo_spring_lance",
        "name": "青竹旋簧刺槍",
        "tier": "common",
        "weapon_type": "spear"
    },
    "back_curio": {
        "id": "curio_kingfisher_bamboo_wings_spring_tail",
        "name": "剛竹纖維高彈摺疊雙翼與分節避震尾翎",
        "tier": "common",
        "race": "kingfisher"
    }
}

KINGFISHER_RACE_SPEC = {
    "race_id": "kingfisher",
    "aliases": [
        "jade_kingfisher",
        "bamboo_kingfisher",
        "halcyon_kingfisher",
        "clockwork_kingfisher",
        "lance_kingfisher"
    ],
    "name_zh": "穿雲翠鳥",
    "name_en": "The Jade Kingfisher",
    "class_archetype": "騎士 (Knight)",
    "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
    "lore_anchor": "穿行於竹影道場·天元竹林「發條天元竹海」、「青石武鬥古道場·演武坪」、「山門竹煙茶舍」與「飛瀑木簧水碓」，巡檢「古老重型零件輸送翻斗軌道·竹林終端站」、「晨曦天軌 9 號演武道場月台」、「凌雲青竹懸索天梯·道場總站」與「天元雲海風帆渡口」，在晨鐘暮鼓調息走時中校準旋簧張力，結伴阿茶、圓空長老與小師弟木木，庇護演武木人童子與木雕竹葉青蛇；通體覆蓋竹影沖壓彩釉琺瑯金屬底盤與奶油米白生漆陶瓷底板、雙聯微調黃銅鳥喙長刺面盔、雙聯高透青石琉璃圓形目鏡、天元道場生漆編織輕量戰袍胸甲、剛竹纖維高彈摺疊雙翼與分節避震尾翎、天元太極雙輪黃銅發條鑰匙，手持專屬青竹旋簧刺槍，以2.2頭身矮萌靈巧身軀、沉穩中距迎擊步法、高頻螺旋鑽頭穿透與中距防線卡位見長的竹海守護長槍騎士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 昭和發條鐵皮俯衝翠鳥玩具與東方天元測風刺擊自動機)",
        "posture": "2.2 頭身矮萌身軀微屈膝靈動站立，雙手斜握青竹旋簧刺槍斜倚身側，背後剛竹羽翼隨呼吸輕柔開合約8度，身後避震尾翎如鐘擺般節律輕晃，背後太極發條鑰匙隨天元秒針每3.0秒晨鐘叮咚聲勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "beak_cowl": "雙聯微調黃銅鳥喙長刺面盔，沖壓黃銅薄板精密切削，內置導流格柵與氣壓游標刻度，造型如尖銳刺槍",
        "eyes": "雙聯大尺寸高透青石琉璃圓形目鏡，深藍紫金屬密封眼圈，浮現薄荷綠同心瞄準刻度與暖金指針",
        "wings": "背部一對多節活動彩釉金屬摺疊羽翼，透過微型彈簧鉸鏈疊合，展開寬幅約60px，翼梢飾有薄荷綠防撞膠條",
        "tail": "三段式鉸接剛竹纖維避震尾翎，尾端嵌裝微型黃銅平衡配重珠，突刺與受擊時提供極致空氣阻尼平衡",
        "torso_and_limbs": "天藍沖壓耐磨彩釉琺瑯金屬板件，黃銅球形關節，雙爪覆蓋防滑減震抗壓黑色橡膠吸附墊",
        "key": "天元太極雙輪加厚黃銅發條鑰匙，雙環太極嚙合齒輪輪緣呈古典祥雲雕花，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#38A0FF (天藍沖壓耐磨彩釉琺瑯金屬背甲與摺疊羽片)",
        "secondary": "#FFFDF8 (奶油米白胸腹生漆陶瓷絕緣底板與面罩高光)",
        "accent_mint": "#4ED86A (薄荷綠翼梢飾條、長槍槍桿生漆塗裝與目鏡分劃)",
        "accent_gold": "#FFD028 (天元金黃太極發條鑰匙、鳥喙長刺面盔、長槍刺錐鑽頭與護心鏡)",
        "accent_orange": "#FFA010 (落日暖橘戰袍胸甲飾帶與快拆黃銅卡扣)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與關節減震膠圈)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_kingfisher.png (品牌形象立牌)",
                "web/media/hero/char_kingfisher.png (官網英雄展示立繪)",
                "docs/art/jade_kingfisher_concept.png (概念立繪)",
                "game/assets/sprites/player/kingfisher_idle.png (64x64 待機)",
                "game/assets/sprites/player/kingfisher_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/kingfisher_idle.png (隊伍待機)",
                "web/media/hero/kingfisher_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/kingfisher_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/kingfisher_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/kingfisher_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/kingfisher_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/kingfisher_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/kingfisher_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/kingfisher/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/kingfisher.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/kingfisher_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/jade_kingfisher.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/kingfisher/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_kingfisher.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/jade_kingfisher_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_kingfisher.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/kingfisher_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/kingfisher_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/kingfisher_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/kingfisher_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/kingfisher_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/kingfisher_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/kingfisher_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/kingfisher/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/kingfisher.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/jade_kingfisher.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/kingfisher/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_kingfisher_enamel_default",
        "head_unit": "head_kingfisher_beak_lance_cowl",
        "optic_core": "face_kingfisher_zen_slate_goggles",
        "costume": "costume_kingfisher_dojo_lacquer_cuirass",
        "back_curio": "curio_kingfisher_bamboo_wings_spring_tail",
        "winding_key": "key_kingfisher_zen_taichi_gear_brass",
        "weapon": "weapon_kingfisher_bamboo_spring_lance"
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
        if slot_id in KINGFISHER_DEFAULT_ITEMS:
            item = KINGFISHER_DEFAULT_ITEMS[slot_id]
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
    if "kingfisher" not in existing_race_ids:
        races.append(KINGFISHER_RACE_SPEC)
        print("  Added kingfisher to races_specification.races")
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
            if "穿雲翠鳥" not in old_rule:
                new_rule = old_rule.replace("六十七重大種族", "六十八重大種族")
                if "潮汐蝠魟深海沖壓耐蝕鍍鈦金屬底盤與深海潛水工裝編織輕量胸甲)" in new_rule:
                    new_rule = new_rule.replace(
                        "潮汐蝠魟深海沖壓耐蝕鍍鈦金屬底盤與深海潛水工裝編織輕量胸甲)",
                        "潮汐蝠魟深海沖壓耐蝕鍍鈦金屬底盤與深海潛水工裝編織輕量胸甲、穿雲翠鳥竹影沖壓彩釉琺瑯金屬底盤與天元道場生漆編織輕量戰袍胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    kingfisher_dir = "game/assets/sprites/player/paperdoll/kingfisher/"
    if kingfisher_dir not in races_dirs:
        races_dirs.append(kingfisher_dir)
        print(f"  Added {kingfisher_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Jade Kingfisher proposal registered specification complete.")
