#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

MANTA_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_manta_titanium_default",
        "name": "深海沖壓耐蝕鍍鈦金屬底盤",
        "tier": "common",
        "race": "manta"
    },
    "head_unit": {
        "id": "head_manta_hydrofoil_horn_cowl",
        "name": "雙聯微型導流頭角導航冠",
        "tier": "common",
        "race": "manta"
    },
    "winding_key": {
        "id": "key_manta_starfish_gear_brass",
        "name": "海星造型五齒輪黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_manta_diver_harness_cuirass",
        "name": "深海潛水工裝編織輕量胸甲",
        "tier": "common",
        "race": "manta"
    },
    "optic_core": {
        "id": "face_manta_high_pressure_quartz_goggles",
        "name": "雙聯耐高壓深海石英泡罩目鏡",
        "tier": "common",
        "race": "manta"
    },
    "weapon": {
        "id": "weapon_manta_hydro_compound_bow",
        "name": "海淵流體脈衝複合機關弓",
        "tier": "common",
        "weapon_type": "bow"
    },
    "back_curio": {
        "id": "curio_manta_flexible_wings_antenna_tail",
        "name": "柔性鈦合金滑翔翼翅與天線平衡細尾",
        "tier": "common",
        "race": "manta"
    }
}

MANTA_RACE_SPEC = {
    "race_id": "manta",
    "aliases": [
        "tidal_manta",
        "gliding_manta",
        "abyssal_manta",
        "clockwork_manta",
        "ray_manta"
    ],
    "name_zh": "潮汐蝠魟",
    "name_en": "The Tidal Manta",
    "class_archetype": "遊俠 (Ranger)",
    "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
    "lore_anchor": "穿行於琉璃汪洋·發條海淵「液態琉璃凝膠海」、「海淵地表與馬賽克步道」、「水下發條宮殿與氧氣泡罩」與「發條珊瑚群」，巡檢「深淵排污豎井管道·耐壓吊籠」、「晨曦天軌 5 號深海浮標月台」、「深海熱液湧泉管道」與「海底防鏽超聲油壓艙」，在海潮對表儀式中校準水壓刻度，結伴舵手巴克、海馬碧浪與珠貝長老，庇護發條熱帶魚群與橡皮小黃鴨船長；通體覆蓋深海沖壓耐蝕鍍鈦金屬底盤與奶油米白抗壓底板、雙聯微型導流頭角導航冠、雙聯耐高壓深海石英泡罩目鏡、深海潛水工裝編織輕量胸甲、柔性鈦合金滑翔翼翅與天線平衡細尾、海星造型五齒輪黃銅發條鑰匙，手持專屬海淵流體脈衝複合機關弓，以2.2頭身矮萌流線身軀、低重心滑翔步法、超空泡水流脈衝貫穿與弱點精準狙擊見長的深海穿浪遊俠",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 昭和發條鐵皮潛艇滑翔魟魚玩具與古典鐘錶航海六分儀自動機)",
        "posture": "2.2 頭身矮萌身軀微屈膝靈動站立，雙手斜抱流線型複合機關弓立於胸前，背後柔性鍍鈦滑翔雙翼隨呼吸輕柔開合約10度，身後天線細尾優雅微晃，背後海星發條鑰匙隨深海青銅錨鏈秒針每3~4秒划動一格勻速自轉，停拍時精準自鎖",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "antennae": "雙聯沖壓黃銅導流頭角導航冠，外側刻有水壓刻度線，角尖帶直徑3px游標金球，引導凝膠海水減阻分流",
        "eyes": "雙聯大尺寸高透球形深海石英泡罩目鏡，深藍紫金屬密封圈，浮現薄荷綠十字瞄準刻度與暖金水壓指針",
        "wings": "背部一對多節活動鍍鈦滑翔雙翼，透過微型彈簧鉸鏈疊合，展開寬幅約64px，翼緣飾有薄荷綠防撞膠條",
        "tail": "纖細修長的多節同軸鎢鋼天線細尾，尾梢裝配微型發光信標金球，游動時隨波輕擺平衡後座力",
        "torso_and_limbs": "天藍沖壓耐蝕鍍鈦金屬板件，黃銅球窩關節，手足嵌裝防滑減震抗壓橡膠吸附墊",
        "key": "海星造型五齒輪加厚黃銅發條鑰匙，輪緣呈波浪齒槽雕花，中心嵌裝多巴胺珊瑚粉防震橡膠鉚釘"
    },
    "color_palette": {
        "primary": "#38A0FF (天藍沖壓耐蝕鍍鈦金屬深海防鏽烤漆板件與滑翔翼面)",
        "secondary": "#FFFDF8 (奶油米白腹部絕緣底板與光罩高光)",
        "accent_mint": "#4ED86A (多巴胺薄荷綠複合機關弓蓄力弦、目鏡刻度與翼緣防撞膠條)",
        "accent_gold": "#FFD028 (天元金黃海星發條鑰匙、導流頭角游標球與目鏡指針)",
        "accent_orange": "#FFA010 (落日暖橘胸甲工裝安全警示條與快拆卡扣)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與防震膠圈)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_manta.png (品牌形象立牌)",
                "web/media/hero/char_manta.png (官網英雄展示立繪)",
                "docs/art/tidal_manta_concept.png (概念立繪)",
                "game/assets/sprites/player/manta_idle.png (64x64 待機)",
                "game/assets/sprites/player/manta_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/manta_idle.png (隊伍待機)",
                "web/media/hero/manta_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/manta_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/manta_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/manta_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/manta_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/manta_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/manta_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/manta/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/manta.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/manta_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/tidal_manta.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/manta/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_manta.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/tidal_manta_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_manta.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/manta_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/manta_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/manta_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/manta_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/manta_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/manta_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/manta_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/manta/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/manta.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/tidal_manta.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/manta/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_manta_titanium_default",
        "head_unit": "head_manta_hydrofoil_horn_cowl",
        "optic_core": "face_manta_high_pressure_quartz_goggles",
        "costume": "costume_manta_diver_harness_cuirass",
        "back_curio": "curio_manta_flexible_wings_antenna_tail",
        "winding_key": "key_manta_starfish_gear_brass",
        "weapon": "weapon_manta_hydro_compound_bow"
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
        if slot_id in MANTA_DEFAULT_ITEMS:
            item = MANTA_DEFAULT_ITEMS[slot_id]
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
    if "manta" not in existing_race_ids:
        races.append(MANTA_RACE_SPEC)
        print("  Added manta to races_specification.races")
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
            if "潮汐蝠魟" not in old_rule:
                new_rule = old_rule.replace("六十六重大種族", "六十七重大種族")
                if "靈燈飛螢深林沖壓薄銅馬口鐵底盤與藤蔓工裝編織輕量背心胸甲)" in new_rule:
                    new_rule = new_rule.replace(
                        "靈燈飛螢深林沖壓薄銅馬口鐵底盤與藤蔓工裝編織輕量背心胸甲)",
                        "靈燈飛螢深林沖壓薄銅馬口鐵底盤與藤蔓工裝編織輕量背心胸甲、潮汐蝠魟深海沖壓耐蝕鍍鈦金屬底盤與深海潛水工裝編織輕量胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    manta_dir = "game/assets/sprites/player/paperdoll/manta/"
    if manta_dir not in races_dirs:
        races_dirs.append(manta_dir)
        print(f"  Added {manta_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Tidal Manta proposal registered specification complete.")
