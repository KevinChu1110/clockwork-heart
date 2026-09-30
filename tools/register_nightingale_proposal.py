#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

NIGHTINGALE_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_nightingale_stock",
        "name": "晨曦鍍金沖壓黃銅夜鶯底盤",
        "tier": "common",
        "race": "nightingale"
    },
    "head_unit": {
        "id": "head_nightingale_dial_cowl",
        "name": "晨曦鐘面鏤空雕花面盔",
        "tier": "common",
        "race": "nightingale"
    },
    "winding_key": {
        "id": "key_nightingale_clef_brass",
        "name": "晨曦高音譜號雕花黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_nightingale_chime_plate",
        "name": "小鎮禮樂銅板八音胸甲",
        "tier": "common",
        "race": "nightingale"
    },
    "optic_core": {
        "id": "face_nightingale_topaz_goggles",
        "name": "雙聯高透黃玉石英琉璃球形目鏡",
        "tier": "common",
        "race": "nightingale"
    },
    "weapon": {
        "id": "weapon_nightingale_chime_crystal",
        "name": "晨音八音諧振靈晶",
        "tier": "common",
        "weapon_type": "crystal"
    },
    "back_curio": {
        "id": "curio_nightingale_chime_tail",
        "name": "多節沖壓薄銅扇形音律尾翼與微型共鳴風箱",
        "tier": "common",
        "race": "nightingale"
    }
}

NIGHTINGALE_RACE_SPEC = {
    "race_id": "nightingale",
    "aliases": [
        "dawn_nightingale",
        "chime_nightingale",
        "clockwork_nightingale",
        "belfry_nightingale",
        "songbird_nightingale",
        "golden_nightingale"
    ],
    "name_zh": "晨音夜鶯",
    "name_en": "The Dawn Nightingale",
    "class_archetype": "法師 (Mage)",
    "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
    "starter_weapon": "shard_focus",
    "weapon_class": "crystal",
    "lore_anchor": "棲息於晨曦小鎮·木偶集市「懸吊齒輪鐘樓」，穿梭於青銅擒縱輪與金色鐘擺之間，守護鐘面外緣懸掛之「微型發條八音風鈴」，巡邏於「細緻打磨的淺灰硬質磨石灰岩積木」鋪面與金黃銅質防滑飾條街道，穿行於「歐風木造街屋」山形牆商鋪與迷你黃銅發條煙囪之間，守護「齒輪吊索大橋·小鎮站」、「晨曦天軌 2 號月台」、「蔓谷天梯引道」與「巨輪城重型空軌貨運棧橋」，引導迷途玩具重返「邊界安全防護彈簧網」，在「永恆晨曦柔光」下唱響天穹秒針授時之音，結伴提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳與摺紙工匠·小鶴，護衛提線木偶族、彩釉玩偶貴族與摺紙手藝人族；通體覆蓋晨曦鍍金沖壓黃銅夜鶯底盤、晨曦鐘面鏤空雕花面盔、雙聯高透黃玉石英琉璃球形目鏡、小鎮禮樂銅板八音胸甲、多節沖壓薄銅扇形音律尾翼與微型共鳴風箱、晨曦高音譜號雕花黃銅發條鑰匙，引導晨音八音諧振靈晶，以2.2頭身矮萌典雅身軀、八音諧振護體、把護盾織成刃與清脆音刃反震見長的晨曦音律護體靈晶大師法師",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (18-19 世紀瑞士布朗東與羅夏兄弟純金發條八音唱歌鳥自動盒名品)",
        "posture": "2.2 頭身矮萌身軀呈靈動典雅站位，胸前懸浮著晨音八音諧振靈晶緩慢自轉，左前翼自然微收呈現禮儀守勢，頭部輕微左右微側，背後高音譜號發條鑰匙隨小鎮秒針每2秒跳動勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 480
    },
    "mechanical_features": {
        "ears_cowl": "晨曦鐘面鏤空雕花面盔，額前雕刻精細鐘面刻度，兩側設有微型八音孔散熱格柵與一體成型黃銅平扁小喙",
        "eyes": "雙聯大尺寸高透黃玉石英琉璃球形目鏡，深藍紫金屬防眩光密封眼圈，浮現天藍同心音階分劃線與暖金指針",
        "chime_wings": "雙翼三層同軸鉸接冷軋薄鋼沖壓音片小翼，倒角鈍化打磨光滑，隨施法手勢微幅開合發出金屬音律共鳴",
        "back_tail": "五節沖壓薄銅梳齒音片扇形尾翼，內置手風琴式排氣微囊與減震發條扭簧，施法時微量排氣共振平抑震動",
        "torso_and_limbs": "天元金黃沖壓黃銅板件，黃銅球形關節，雙足爪底覆蓋耐磨防滑黑色橡膠吸附墊",
        "key": "晨曦高音譜號雕花黃銅發條鑰匙，輪柄呈古典高音譜號盤旋雕花造型，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#FFD028 (天元金黃沖壓面盔與黃銅夜鶯底盤亮面生漆)",
        "secondary": "#4ED86A (薄荷綠雙翼音片護甲、胸甲滾邊與尾翼底板)",
        "accent_blue": "#38A0FF (天藍防眩光琉璃目鏡分劃與八音靈晶音波光環)",
        "accent_orange": "#FFA010 (落日暖橘關節防震膠圈與禮樂胸甲飾條)",
        "accent_white": "#FFFDF8 (奶油米白胸前裝甲高光嵌片與鐘面刻度環)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與耳羽頂珠)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_nightingale.png (品牌形象立牌)",
                "web/media/hero/char_nightingale.png (官網英雄展示立繪)",
                "docs/art/dawn_nightingale_concept.png (概念立繪)",
                "game/assets/sprites/player/nightingale_idle.png (64x64 待機)",
                "game/assets/sprites/player/nightingale_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/nightingale_idle.png (隊伍待機)",
                "web/media/hero/nightingale_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/nightingale_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/nightingale_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/nightingale_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/nightingale_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/nightingale_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/nightingale_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/nightingale/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/nightingale.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/nightingale_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/dawn_nightingale.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/nightingale/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_nightingale.png (480x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/dawn_nightingale_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_nightingale.png (480x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/nightingale_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/nightingale_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/nightingale_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/nightingale_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/nightingale_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/nightingale_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/nightingale_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/nightingale/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/nightingale.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/dawn_nightingale.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/nightingale/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_nightingale_stock",
        "head_unit": "head_nightingale_dial_cowl",
        "optic_core": "face_nightingale_topaz_goggles",
        "costume": "costume_nightingale_chime_plate",
        "back_curio": "curio_nightingale_chime_tail",
        "winding_key": "key_nightingale_clef_brass",
        "weapon": "weapon_nightingale_chime_crystal"
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
        if slot_id in NIGHTINGALE_DEFAULT_ITEMS:
            item = NIGHTINGALE_DEFAULT_ITEMS[slot_id]
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
    if "nightingale" not in existing_race_ids:
        races.append(NIGHTINGALE_RACE_SPEC)
        print("  Added nightingale to races_specification.races")
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
            if "晨音夜鶯" not in old_rule:
                new_rule = old_rule.replace("七十一重大種族", "七十二重大種族")
                target_str = "翠刃螳螂蔓谷沖壓薄銅螳螂底盤與蔓谷藤蔓鉚接生漆板甲胸甲)"
                if target_str in new_rule:
                    new_rule = new_rule.replace(
                        target_str,
                        "翠刃螳螂蔓谷沖壓薄銅螳螂底盤與蔓谷藤蔓鉚接生漆板甲胸甲、晨音夜鶯晨曦鍍金沖壓黃銅夜鶯底盤與小鎮禮樂銅板八音胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    nightingale_dir = "game/assets/sprites/player/paperdoll/nightingale/"
    if nightingale_dir not in races_dirs:
        races_dirs.append(nightingale_dir)
        print(f"  Added {nightingale_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Dawn Nightingale proposal registered specification complete.")
