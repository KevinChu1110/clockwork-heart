#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

DONKEY_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_donkey_tinplate_default",
        "name": "集市工兵沖壓馬口鐵金屬底盤",
        "tier": "common",
        "race": "donkey"
    },
    "head_unit": {
        "id": "head_donkey_ratchet_ears_cowl",
        "name": "雙聯棘輪立體折疊長耳面盔",
        "tier": "common",
        "race": "donkey"
    },
    "winding_key": {
        "id": "key_donkey_dawn_clover_brass",
        "name": "晨曦三葉雕花黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_donkey_sapper_harness",
        "name": "集市工兵鉚接生漆板甲胸甲",
        "tier": "common",
        "race": "donkey"
    },
    "optic_core": {
        "id": "face_donkey_slate_goggles",
        "name": "雙聯高透青石琉璃圓形目鏡",
        "tier": "common",
        "race": "donkey"
    },
    "weapon": {
        "id": "weapon_donkey_bazaar_clearing_axe",
        "name": "集市天軌闢道重斧",
        "tier": "common",
        "weapon_type": "axe"
    },
    "back_curio": {
        "id": "curio_donkey_cograil_pack_tail",
        "name": "雙聯天軌木榫馱架與分節配重平衡尾",
        "tier": "common",
        "race": "donkey"
    }
}

DONKEY_RACE_SPEC = {
    "race_id": "donkey",
    "aliases": [
        "sapper_donkey",
        "bazaar_donkey",
        "clockwork_donkey",
        "burro",
        "pack_donkey",
        "iron_donkey"
    ],
    "name_zh": "闢道頑驢",
    "name_en": "The Sapper Donkey",
    "class_archetype": "戰士 (Viking)",
    "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
    "starter_weapon": "notch_axe",
    "weapon_class": "axe",
    "lore_anchor": "穿行於晨曦小鎮·木偶集市「懸吊齒輪鐘樓」、「歐風木造街屋」與「多邊形胡桃木拼花浮空展台底座」，巡邏於「街道鋪面採用細緻打磨的淺灰硬質磨石灰岩積木拼合而成，步道邊緣鑲嵌著細小的金黃銅質防滑飾條」之街道，守護「巨輪城重型空軌貨運棧橋」、「齒輪吊索大橋·小鎮站」、「蔓谷天梯引道」與「晨曦天軌 2 號月台」，在永恆晨曦柔光下引導邊界安全防護彈簧網，結伴巴納姆會長、瑪德琳夫人與工匠小鶴，護衛提線木偶族、彩釉玩偶貴族與摺紙手藝人族；通體覆蓋集市工兵沖壓馬口鐵金屬底盤、雙聯棘輪立體折疊長耳面盔、雙聯高透青石琉璃圓形目鏡、集市工兵鉚接生漆板甲胸甲、雙聯天軌木榫馱架與分節配重平衡尾、晨曦三葉雕花黃銅發條鑰匙，手持集市天軌闢道重斧，以2.2頭身矮萌扎實身軀、沉穩四平破障步法、一擊要有重量的重劈與頑固防線卡位見長的集市重裝開拓鐵衛戰士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1900s-1930s 歐洲萊曼發條鐵皮頑皮驢與巴伐利亞木雕工兵自動偶)",
        "posture": "2.2 頭身矮萌身軀穩健立定於地面，右手單手將集市闢道重斧立於身側地面，左臂曲於胸前呈現沉穩守勢，頭頂雙聯黃銅長耳隨呼吸輕柔後擺約10度，身後分節黃銅尾如鐘擺般節律輕晃，背後三葉發條鑰匙隨小鎮秒針每2~3秒跳動勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "ears_cowl": "雙聯棘輪立體折疊長耳面盔，沖壓黃銅薄板多節鉸接，內置單向棘爪棘輪與散熱格柵，受擊重擊發出清脆嗒嗒聲",
        "eyes": "雙聯大尺寸高透青石琉璃圓形目鏡，深藍紫金屬密封眼圈，浮現天藍同心瞄準刻度與暖金指針",
        "saddle_pack": "後背雙聯天軌木榫馱架，百年胡桃木與黃銅榫卯結構，兩側捆紮微縮鐵道枕木與備用齒輪",
        "tail": "三段式鉸接黃銅平衡尾，尾端嵌有圓形黃銅防後座阻尼重錘，重斧全力下劈時提供極致空氣與接地阻尼平衡",
        "torso_and_limbs": "奶油米白沖壓耐磨冷軋馬口鐵板件，黃銅球形關節，四足覆蓋防滑減震抗壓黑色橡膠蹄墊",
        "key": "晨曦三葉雕花黃銅發條鑰匙，輪緣呈古典巴洛克幸運草雕花鏤空，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#FFFDF8 (奶油米白沖壓胸腹耐磨生漆板件)",
        "secondary": "#FFA010 (明亮暖橘工兵背心飾帶、長耳外罩彩漆與馱架扣帶)",
        "accent_blue": "#38A0FF (天藍防眩光琉璃目鏡分劃與天軌防撞標籤)",
        "accent_mint": "#4ED86A (薄荷綠軸承防震膠圈與重斧握柄生漆防滑刻紋帶)",
        "accent_gold": "#FFD028 (晨曦金黃三葉發條鑰匙、黃銅鉚釘、長耳棘輪齒與斧刃破勢鑲邊)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與耳尖減震軟墊)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_donkey.png (品牌形象立牌)",
                "web/media/hero/char_donkey.png (官網英雄展示立繪)",
                "docs/art/sapper_donkey_concept.png (概念立繪)",
                "game/assets/sprites/player/donkey_idle.png (64x64 待機)",
                "game/assets/sprites/player/donkey_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/donkey_idle.png (隊伍待機)",
                "web/media/hero/donkey_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/donkey_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/donkey_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/donkey_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/donkey_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/donkey_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/donkey_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/donkey/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/donkey.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/donkey_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/sapper_donkey.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/donkey/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_donkey.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/sapper_donkey_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_donkey.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/donkey_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/donkey_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/donkey_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/donkey_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/donkey_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/donkey_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/donkey_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/donkey/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/donkey.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/sapper_donkey.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/donkey/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_donkey_tinplate_default",
        "head_unit": "head_donkey_ratchet_ears_cowl",
        "optic_core": "face_donkey_slate_goggles",
        "costume": "costume_donkey_sapper_harness",
        "back_curio": "curio_donkey_cograil_pack_tail",
        "winding_key": "key_donkey_dawn_clover_brass",
        "weapon": "weapon_donkey_bazaar_clearing_axe"
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
        if slot_id in DONKEY_DEFAULT_ITEMS:
            item = DONKEY_DEFAULT_ITEMS[slot_id]
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
    if "donkey" not in existing_race_ids:
        races.append(DONKEY_RACE_SPEC)
        print("  Added donkey to races_specification.races")
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
            if "闢道頑驢" not in old_rule:
                new_rule = old_rule.replace("六十八重大種族", "六十九重大種族")
                if "穿雲翠鳥竹影沖壓彩釉琺瑯金屬底盤與天元道場生漆編織輕量戰袍胸甲)" in new_rule:
                    new_rule = new_rule.replace(
                        "穿雲翠鳥竹影沖壓彩釉琺瑯金屬底盤與天元道場生漆編織輕量戰袍胸甲)",
                        "穿雲翠鳥竹影沖壓彩釉琺瑯金屬底盤與天元道場生漆編織輕量戰袍胸甲、闢道頑驢集市工兵沖壓馬口鐵金屬底盤與集市工兵鉚接生漆板甲胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    donkey_dir = "game/assets/sprites/player/paperdoll/donkey/"
    if donkey_dir not in races_dirs:
        races_dirs.append(donkey_dir)
        print(f"  Added {donkey_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Sapper Donkey proposal registered specification complete.")
