#!/usr/bin/env python3
import json
import sys

TARGET_FILES = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

SCARAB_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_scarab_obsidian_forge_default",
        "name": "黑曜耐火鑄鐵矮萌底盤",
        "tier": "common",
        "race": "scarab"
    },
    "head_unit": {
        "id": "head_scarab_quenched_obsidian_cowl",
        "name": "黑曜淬火雙叉金角面罩",
        "tier": "common",
        "race": "scarab"
    },
    "winding_key": {
        "id": "key_scarab_crucible_cross_fire_brass",
        "name": "四葉鍛造十字火紋黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_scarab_crucible_artisan_apron",
        "name": "赤焰熔爐隔熱工匠護裙",
        "tier": "common",
        "race": "scarab"
    },
    "optic_core": {
        "id": "face_scarab_amber_crystal_visor",
        "name": "熔金琥珀透鏡耐火面甲",
        "tier": "common",
        "race": "scarab"
    },
    "weapon": {
        "id": "weapon_scarab_crucible_obsidian_focus",
        "name": "赤焰黑曜護體靈晶",
        "tier": "common",
        "weapon_type": "crystal"
    },
    "back_curio": {
        "id": "curio_scarab_twin_vent_exhaust_tail",
        "name": "雙聯微型高壓洩壓排煙管短尾",
        "tier": "common",
        "race": "scarab"
    }
}

SCARAB_RACE_SPEC = {
    "race_id": "scarab",
    "aliases": [
        "obsidian_scarab",
        "crucible_scarab",
        "forge_beetle",
        "clockwork_scarab",
        "volcano_scarab"
    ],
    "name_zh": "黑曜金龜",
    "name_en": "The Obsidian Scarab",
    "class_archetype": "法師 (Mage)",
    "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
    "lore_anchor": "駐守於赤焰熔爐·鍛造火山「火山口中央鍛造神壇」與「黑曜石淬火神壇」，穿行於「金色液態鐵水熔池」兩岸的「黑曜淬火石磚步道」與「耐火排煙管樹」，跨越「重型鍛造工坊與衝壓懸橋」，仰望「黃銅洩壓儀表塔」，巡邏「晨曦天軌 6 號熔爐重載貨運月台」、「高壓地熱噴射升空彈射井」與「冷卻熔渣重力排料傾卸滑道」，依託「磁吸隔熱排渣護欄網」與「淬火冷卻噴淋池」，結伴矮人鐵匠大師·布隆、陶土魔像學徒·泥泥與熔爐溫控長老·坩堝老爹；通體覆蓋高溫淬火黑曜岩底盤與象牙白瓷腮板、黑曜淬火雙叉金角面罩、熔金琥珀水晶目鏡、赤焰熔爐隔熱工匠護裙、可開合雙扇黑曜亮面鞘翅、雙聯微型高壓洩壓排煙管短尾、四葉鍛造十字火紋黃銅發條鑰匙，右手單持專屬赤焰黑曜護體靈晶，以2.2頭身矮萌微胖體態、六足精工黃銅球窩鉸鏈、熔爐地熱晶核吸納、多面晶刃反震破勢與織盾成刃見長的高溫火山機關造物法師",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1900s-1930s 歐洲古典發條鐵皮聖甲蟲與維多利亞鐘錶地熱自動偶)",
        "posture": "2.2 頭身矮萌身軀微側30度穩健站姿，六足微屈下沉抓地，右手向前虛托浮空旋轉靈晶，左手收胸結印，背後四葉發條鑰匙隨秒針每1.5秒跳拍一格勻速自轉",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "打磨黑曜岩半球形頭罩（#2B2630），前額挺立雙叉黃銅機械調諧觸角（#FFD028），兩腮鑲嵌溫潤象牙白瓷耐火腮板（#FFFDF8），眼眶處鏤空透光",
        "ears": "無外耳，以額前雙叉黃銅機械調諧觸角（#FFD028）替代，內置微型熱電偶合金絲隨秒針微顫測溫",
        "torso_and_limbs": "高耐熱粗砂鑄鐵模組（#2B2630）沖壓外殼，胸腹鑲嵌白瓷耐火襯板，四肢為精工黃銅球窩轉動鉸鏈與矽膠吸震軟墊",
        "tail": "雙聯微型高壓洩壓排煙管短尾（#FFD028 / #2B2630），兩根仰角黃銅排氣短管，每隔數秒噴出微型白色蒸氣圈",
        "weapon_system": "右手單持專屬「赤焰黑曜護體靈晶（Crucible Obsidian Shield-Focus）」，浮空旋轉多面黑曜晶核配雙黃銅刻度調諧環，底層掛載 equipment.json 既有 shard_focus (tier 1)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白瓷耐火高光，兩腮腮板、胸腹襯板高光)",
        "primary": "#FFA010 (主色多巴胺暖橘，隔熱工匠圍裙、琥珀透鏡、鞘翅彩繪飾條)",
        "secondary": "#4ED86A (次色多巴胺薄荷淺綠，圍裙密封飾條、靈晶能量外圈光暈)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心鉚釘與口袋刺繡印記)",
        "metal": "#FFD028 (金屬赤焰黃銅金，四葉發條鑰匙、雙叉觸角、鉸鏈與靈晶調諧環)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_scarab.png (品牌形象立牌)",
                "web/media/hero/char_scarab.png (官網英雄展示立繪)",
                "docs/art/obsidian_scarab_concept.png (概念立繪)",
                "game/assets/sprites/player/scarab_idle.png (64x64 待機)",
                "game/assets/sprites/player/scarab_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/scarab_idle.png (隊伍待機)",
                "web/media/hero/scarab_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/scarab_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/scarab_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/scarab_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/scarab_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/scarab_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/scarab_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/scarab/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/scarab.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/scarab_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/obsidian_scarab.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/scarab/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_scarab.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/obsidian_scarab_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_scarab.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/scarab_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/scarab_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/scarab_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/scarab_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/scarab_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/scarab_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/scarab_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/scarab/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/scarab.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/obsidian_scarab.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/scarab/{slot_id}/{item_id}.png [待產出]"
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
        if slot_id in SCARAB_DEFAULT_ITEMS:
            item = SCARAB_DEFAULT_ITEMS[slot_id]
            # Ensure "default_items" exists
            if "default_items" not in s:
                s["default_items"] = []
            # Check if item already exists
            existing_ids = [x["id"] for x in s["default_items"]]
            if item["id"] not in existing_ids:
                s["default_items"].append(item)
                print(f"  Added {item['id']} to slot {slot_id} default_items")

    # 2. Update races_specification
    races_spec = data["races_specification"]
    races = races_spec["races"]
    existing_race_ids = [r["race_id"] for r in races]
    if "scarab" not in existing_race_ids:
        races.append(SCARAB_RACE_SPEC)
        print("  Added scarab to races_specification.races")
    races_spec["total_races"] = 59

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    univ = compat.get("universal_slots", [])
    for u in univ:
        if u.get("slot_id") == "winding_key":
            u["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 59 種動物素體"
    adapted = compat.get("race_adapted_slots", [])
    for a in adapted:
        if a.get("slot_id") == "costume":
            old_rule = a.get("rule", "")
            if "黑曜金龜" not in old_rule:
                # Replace "五十九重大種族" with "六十重大種族" and append scarab
                new_rule = old_rule.replace("五十九重大種族", "六十重大種族")
                if "提線猞猁精雕胡桃木與晨曦小鎮提線雜技工裝背心" in new_rule:
                    new_rule = new_rule.replace(
                        "提線猞猁精雕胡桃木與晨曦小鎮提線雜技工裝背心)",
                        "提線猞猁精雕胡桃木與晨曦小鎮提線雜技工裝背心、黑曜金龜高耐熱鑄鐵底盤與赤焰熔爐隔熱工匠護裙)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    scarab_dir = "game/assets/sprites/player/paperdoll/scarab/"
    if scarab_dir not in races_dirs:
        races_dirs.append(scarab_dir)
        print(f"  Added {scarab_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("All paperdoll_slots.json updates completed successfully.")
