#!/usr/bin/env python3
import json
import os
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

TAKIN_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_takin_bronze_cast_default",
        "name": "青古銅鑄鐵重裝底盤",
        "tier": "common",
        "race": "takin"
    },
    "head_unit": {
        "id": "head_takin_brass_twisted_horn_cowl",
        "name": "黃銅反曲扭角重盔",
        "tier": "common",
        "race": "takin"
    },
    "winding_key": {
        "id": "key_takin_tri_leaf_zen_brass",
        "name": "三葉天元雕花黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_takin_zen_pioneer_heavy_robe",
        "name": "天元拓荒道袍重肩甲",
        "tier": "common",
        "race": "takin"
    },
    "optic_core": {
        "id": "face_takin_emerald_quartz_visors",
        "name": "翡翠石英耐震雙目鏡",
        "tier": "common",
        "race": "takin"
    },
    "weapon": {
        "id": "weapon_takin_zen_bamboo_cleaving_axe",
        "name": "天元破竹開山巨斧",
        "tier": "common",
        "weapon_type": "axe"
    },
    "back_curio": {
        "id": "curio_takin_dual_bamboo_oil_flasks",
        "name": "雙聯竹露油壺減震閥",
        "tier": "common",
        "race": "takin"
    }
}

TAKIN_RACE_SPEC = {
    "race_id": "takin",
    "aliases": [
        "bamboo_cleaving_takin",
        "zen_takin",
        "clockwork_takin",
        "golden_takin",
        "mountain_takin"
    ],
    "name_zh": "破竹羚牛",
    "name_en": "The Bamboo-Cleaving Takin",
    "class_archetype": "戰士 (Viking)",
    "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
    "lore_anchor": "駐守於竹影道場·天元竹林「青石武鬥古道場·演武坪」，穿行於「發條天元竹海」與「飛瀑木簧水碓」之間，仰望「凌雲青竹懸索天梯·道場總站」與「晨曦天軌 9 號演武道場月台」，巡檢「古老重型零件輸送翻斗軌道·竹林終端站」與「翠竹彈力阻尼編織網」，在「山門竹煙茶舍」飲用清香竹露潤滑油保養軸承，結伴圓空師傅、煮茶偶阿茶與木人小師弟木木，庇護陶瓷熊貓武僧、木雕竹葉青蛇與演武木人童子；通體覆蓋沖壓青古銅鑄鐵合金底盤與象牙白瓷護腹板、雙聯鍛造黃銅反曲扭角重盔、翡翠石英耐震雙目鏡、天元拓荒道袍重肩甲、雙聯竹露油壺減震閥、三葉天元雕花黃銅發條鑰匙，右手單持專屬天元破竹開山巨斧，以2.2頭身矮萌厚重體態、扎實青石蹄踏步、霸體蓄力開山重劈見長的天元竹林守護戰士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1920s-1950s 經典古典發條鐵皮重獸偶與東方機巧榫卯自動偶)",
        "posture": "2.2 頭身矮萌重裝身軀微側30度穩重扎馬站姿，雙蹄穩踏地面，右手單持雙刃戰斧斜立於身側，左臂曲於胸前呈厚重防禦架勢，背後三葉發條鑰匙隨竹林秒針每3.0秒鐘鳴一格勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 560
    },
    "mechanical_features": {
        "horns": "雙聯鍛造高光黃銅反曲扭角，角尖微向上翹，刻有同心圓加強肋線，隨步伐微幅震動",
        "face": "沖壓青鋼防塵面甲，雙頰鑲嵌光滑黃銅咬合齒輪，半球形高透耐震翡翠石英雙目鏡",
        "torso_and_limbs": "青古銅鑄鐵合金厚重底盤，胸腹鑲嵌溫潤象牙白生漆陶瓷板，四肢為球形轉向鉸鏈配防滑青石蹄",
        "venting": "背部左右雙聯耐壓玻璃竹露油壺，中央連通微型水碓氣動排氣減震閥門",
        "key": "三葉天元祥雲雕花黃銅發條鑰匙，中心飾有珊瑚粉防震鉚釘",
        "weapon_system": "右手單持專屬「天元破竹開山巨斧（Zen Bamboo-Cleaving Battle Axe）」，青鋼開山重刃配八卦鏤空減震孔，底層掛載 equipment.json 既有 notch_axe (tier 1 戰斧)"
    },
    "color_palette": {
        "primary": "#FFFDF8 (奶油白陶瓷生漆胸腹板與道袍)",
        "secondary": "#4ED86A (多巴胺薄荷綠板件烤漆邊與翡翠石英目鏡)",
        "accent_gold": "#FFD028 (天元金黃雙扭角、發條鑰匙與戰斧雕花)",
        "accent_orange": "#FFA010 (落日暖橘道袍防磨滾邊)",
        "dark_bronze": "#3A4454 (青古銅鑄鐵厚重板件底盤)",
        "accent_pink": "#FF5E8A (珊瑚粉防震鉚釘與油壺浮標)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_takin.png (品牌形象立牌)",
                "web/media/hero/char_takin.png (官網英雄展示立繪)",
                "docs/art/bamboo_cleaving_takin_concept.png (概念立繪)",
                "game/assets/sprites/player/takin_idle.png (64x64 待機)",
                "game/assets/sprites/player/takin_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/takin_idle.png (隊伍待機)",
                "web/media/hero/takin_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/takin_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/takin_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/takin_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/takin_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/takin_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/takin_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/takin/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/takin.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/takin_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/bamboo_cleaving_takin.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/takin/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_takin.png (560x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/bamboo_cleaving_takin_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_takin.png (560x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/takin_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/takin_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/takin_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/takin_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/takin_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/takin_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/takin_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/takin/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/takin.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/bamboo_cleaving_takin.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/takin/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_takin_bronze_cast_default",
        "head_unit": "head_takin_brass_twisted_horn_cowl",
        "optic_core": "face_takin_emerald_quartz_visors",
        "costume": "costume_takin_zen_pioneer_heavy_robe",
        "back_curio": "curio_takin_dual_bamboo_oil_flasks",
        "winding_key": "key_takin_tri_leaf_zen_brass",
        "weapon": "weapon_takin_zen_bamboo_cleaving_axe"
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
        if slot_id in TAKIN_DEFAULT_ITEMS:
            item = TAKIN_DEFAULT_ITEMS[slot_id]
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
    if "takin" not in existing_race_ids:
        races.append(TAKIN_RACE_SPEC)
        print("  Added takin to races_specification.races")
    races_spec["total_races"] = 62

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    univ = compat.get("universal_slots", [])
    for u in univ:
        if u.get("slot_id") == "winding_key":
            u["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 62 種動物素體"
    adapted = compat.get("race_adapted_slots", [])
    for a in adapted:
        if a.get("slot_id") == "costume":
            old_rule = a.get("rule", "")
            if "破竹羚牛" not in old_rule:
                new_rule = old_rule.replace("六十二重大種族", "六十三重大種族")
                if "破冰海象耐壓鍍鈦合金底盤與深淵領航雙排扣水手胸甲" in new_rule:
                    new_rule = new_rule.replace(
                        "破冰海象耐壓鍍鈦合金底盤與深淵領航雙排扣水手胸甲)",
                        "破冰海象耐壓鍍鈦合金底盤與深淵領航雙排扣水手胸甲、破竹羚牛青古銅鑄鐵重裝底盤與天元拓荒道袍重肩甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    takin_dir = "game/assets/sprites/player/paperdoll/takin/"
    if takin_dir not in races_dirs:
        races_dirs.append(takin_dir)
        print(f"  Added {takin_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Takin proposal registered specification complete.")
