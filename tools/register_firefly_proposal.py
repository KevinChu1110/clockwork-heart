#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

FIREFLY_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_firefly_emerald_tinplate_default",
        "name": "深林沖壓薄銅馬口鐵底盤",
        "tier": "common",
        "race": "firefly"
    },
    "head_unit": {
        "id": "head_firefly_brass_antenna_cowl",
        "name": "雙聯微調黃銅觸角調諧冠",
        "tier": "common",
        "race": "firefly"
    },
    "winding_key": {
        "id": "key_firefly_floral_gear_brass",
        "name": "花蕾造型四瓣齒輪黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_firefly_vine_harness_cuirass",
        "name": "藤蔓工裝編織輕量背心胸甲",
        "tier": "common",
        "race": "firefly"
    },
    "optic_core": {
        "id": "face_firefly_dual_lantern_quartz_eyes",
        "name": "雙聯聚碳酸酯夜燈球形目鏡",
        "tier": "common",
        "race": "firefly"
    },
    "weapon": {
        "id": "weapon_firefly_luminescent_vine_staff",
        "name": "深林熒光藤蔓發條長杖",
        "tier": "common",
        "weapon_type": "magic"
    },
    "back_curio": {
        "id": "curio_firefly_luminescent_resin_abdomen",
        "name": "注塑樹脂熒光腹囊與沖壓透光薄翅",
        "tier": "common",
        "race": "firefly"
    }
}

FIREFLY_RACE_SPEC = {
    "race_id": "firefly",
    "aliases": [
        "lantern_firefly",
        "luminescent_firefly",
        "spore_firefly",
        "clockwork_firefly",
        "vine_firefly"
    ],
    "name_zh": "靈燈飛螢",
    "name_en": "The Lantern Firefly",
    "class_archetype": "法師 (Mage)",
    "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
    "lore_anchor": "穿行於翡翠深林·發條蔓谷「巨木樹屋聚落」、「蔓谷天梯引道·深林站」與「觀風石碑塔」，巡檢「機械巨木」、「樹汁導流泵」與「樹脂發光菌菇步道」，駐守「晨曦天軌 3 號月台」與「高架重軌引橋·巨輪城站」，在深林巨木根部塗抹高純度天然發條潤滑樹脂，結伴風耳、小鈴與角木，庇護守林發條小鹿、發條松鼠信差與林木守護木偶；通體覆蓋深林沖壓薄銅馬口鐵底盤與象牙白絕緣底板、雙聯微調黃銅觸角調諧冠、雙聯聚碳酸酯夜燈球形目鏡、藤蔓工裝編織輕量背心胸甲、注塑樹脂熒光腹囊與沖壓透光薄翅、花蕾造型四瓣齒輪黃銅發條鑰匙，手持專屬深林熒光藤蔓發條長杖，以2.2頭身矮萌靈巧身軀、橡膠防滑吸附步法、腹囊微型發電機發光引路與停拍窗口星屑魔法轟擊見長的深林靈光法師",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 昭和發條鐵皮發光螢火蟲玩具與古典鐘錶夜燈自動機)",
        "posture": "2.2 頭身矮萌身軀微屈膝靈動立姿，手握螺旋藤蔓長杖豎立於身側，右手輕護胸前，身後注塑樹脂熒光腹囊隨體內微型齒輪自轉柔和明滅，背後花蕾發條鑰匙隨深林天頂秒針每3~4秒跳動一格勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "antennae": "雙聯精密切削黃銅細彈簧觸角，頂端帶直徑4px游標調諧金球，靈敏感知氣流與秒針停拍震顫",
        "eyes": "雙聯大尺寸高透球形聚碳酸酯夜燈目鏡，深藍紫金屬密封圈，浮現暖金黃同心圓發光鎢絲",
        "abdomen": "半透明注塑光膠發光腹囊，內建微型發條發電機與旋轉齒輪，散發薄荷綠至金黃漸變柔光",
        "wings": "背部一對半透明沖壓薄銅雕花甲翅，帶有葉脈鏤空齒紋，施法時微幅展開",
        "torso_and_limbs": "薄荷綠沖壓薄銅耐磨板件，黃銅球窩關節，足底嵌裝防滑橡膠吸附減震墊",
        "key": "四瓣齒輪花蕾造型加厚黃銅發條鑰匙，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#4ED86A (薄荷綠沖壓薄銅深林耐磨烤漆板件)",
        "secondary": "#FFFDF8 (奶油米白腹部絕緣底板與光罩高光)",
        "accent_gold": "#FFD028 (天元金黃腹囊發電機鎢絲、觸角游標球與發條鑰匙)",
        "accent_orange": "#FFA010 (落日暖橘目鏡刻度與胸甲工裝警示條)",
        "accent_blue": "#38A0FF (多巴胺天藍玻璃管道樹脂光暈與金屬快拆扣)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與防震膠圈)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_firefly.png (品牌形象立牌)",
                "web/media/hero/char_firefly.png (官網英雄展示立繪)",
                "docs/art/lantern_firefly_concept.png (概念立繪)",
                "game/assets/sprites/player/firefly_idle.png (64x64 待機)",
                "game/assets/sprites/player/firefly_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/firefly_idle.png (隊伍待機)",
                "web/media/hero/firefly_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/firefly_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/firefly_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/firefly_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/firefly_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/firefly_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/firefly_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/firefly/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/firefly.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/firefly_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/lantern_firefly.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/firefly/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_firefly.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/lantern_firefly_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_firefly.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/firefly_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/firefly_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/firefly_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/firefly_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/firefly_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/firefly_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/firefly_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/firefly/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/firefly.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/lantern_firefly.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/firefly/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_firefly_emerald_tinplate_default",
        "head_unit": "head_firefly_brass_antenna_cowl",
        "optic_core": "face_firefly_dual_lantern_quartz_eyes",
        "costume": "costume_firefly_vine_harness_cuirass",
        "back_curio": "curio_firefly_luminescent_resin_abdomen",
        "winding_key": "key_firefly_floral_gear_brass",
        "weapon": "weapon_firefly_luminescent_vine_staff"
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
        if slot_id in FIREFLY_DEFAULT_ITEMS:
            item = FIREFLY_DEFAULT_ITEMS[slot_id]
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
    if "firefly" not in existing_race_ids:
        races.append(FIREFLY_RACE_SPEC)
        print("  Added firefly to races_specification.races")
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
            if "靈燈飛螢" not in old_rule:
                new_rule = old_rule.replace("六十五重大種族", "六十六重大種族")
                if "碎石旱獺生鐵青灰耐磨馬口鐵底盤與舊庫拾荒加固帆布工裝胸甲)" in new_rule:
                    new_rule = new_rule.replace(
                        "碎石旱獺生鐵青灰耐磨馬口鐵底盤與舊庫拾荒加固帆布工裝胸甲)",
                        "碎石旱獺生鐵青灰耐磨馬口鐵底盤與舊庫拾荒加固帆布工裝胸甲、靈燈飛螢深林沖壓薄銅馬口鐵底盤與藤蔓工裝編織輕量背心胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    firefly_dir = "game/assets/sprites/player/paperdoll/firefly/"
    if firefly_dir not in races_dirs:
        races_dirs.append(firefly_dir)
        print(f"  Added {firefly_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Lantern Firefly proposal registered specification complete.")
