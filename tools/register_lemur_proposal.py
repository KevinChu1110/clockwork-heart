#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

LEMUR_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_lemur_orbit_polymer_default",
        "name": "星穹輕量聚合物高機動底盤",
        "tier": "common",
        "race": "lemur"
    },
    "head_unit": {
        "id": "head_lemur_orbit_radar_cowl",
        "name": "星軌冷光雷達耳罩面甲",
        "tier": "common",
        "race": "lemur"
    },
    "winding_key": {
        "id": "key_lemur_tri_ring_orbit_brass",
        "name": "三環軌道星環黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_lemur_astro_stealth_harness",
        "name": "宇航匿蹤輕量安全吊帶胸甲",
        "tier": "common",
        "race": "lemur"
    },
    "optic_core": {
        "id": "face_lemur_amber_pulsar_visors",
        "name": "琥珀脈衝星穹雙目鏡",
        "tier": "common",
        "race": "lemur"
    },
    "weapon": {
        "id": "weapon_lemur_orbital_pulse_daggers",
        "name": "星軌脈衝雙鋒短匕",
        "tier": "common",
        "weapon_type": "dagger"
    },
    "back_curio": {
        "id": "curio_lemur_neon_ring_fiber_tail",
        "name": "多節霓光光纖星環天線尾",
        "tier": "common",
        "race": "lemur"
    }
}

LEMUR_RACE_SPEC = {
    "race_id": "lemur",
    "aliases": [
        "star_ring_lemur",
        "orbit_lemur",
        "ringtail_lemur",
        "clockwork_lemur",
        "pulse_lemur"
    ],
    "name_zh": "星環狐猴",
    "name_en": "The Star-Ring Lemur",
    "class_archetype": "忍者 (Ninja)",
    "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
    "lore_anchor": "穿行於星穹軌道·外星基地「高光懸空螢光軌道」、「太陽能帆板與微型排氣天線」與「太空拼裝維修船塢」，巡檢「聚合物太空艙模組」、「失重慣性磁力捕捉網」與「高真空抗靜電除塵室」，駐守「高壓地熱升空彈射井·軌道受壓對接艙」與「垂直磁浮天軌·星穹軌道月台」，在太空船塢更換特種全氟聚醚耐低溫潤滑油，結伴螺栓隊長、萊卡波波與光纖婆婆，庇護組裝式宇航機器人、太空發條小狗與螢光軌道維護偶；通體覆蓋高抗衝擊工程聚合物塑料底盤與象牙白防滑襯板、星軌冷光雷達耳罩面甲、琥珀脈衝星穹雙目鏡、宇航匿蹤輕量安全吊帶胸甲、多節霓光光纖星環天線尾、三環軌道星環黃銅發條鑰匙，雙持專屬星軌脈衝雙鋒短匕，以2.2頭身輕巧機動體態、掌底矽膠吸附踏步、失重微氣反推向量折返與近戰雙刃死角背刺見長的星穹軌道匿蹤忍者",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1960s-1980s 太空時代發條翻滾玩偶與科幻組裝微縮偶)",
        "posture": "2.2 頭身矮萌輕巧身軀微屈膝靈動站姿，雙腳矽膠吸盤穩踏地面，右手反握主鋒匕橫於胸前，左手副匕微屈護胸，身後光纖星環長尾優雅高翹，背後三環發條鑰匙隨星穹秒針每3.0秒鐘鳴一格勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 520
    },
    "mechanical_features": {
        "ears": "半透明高透聚碳酸酯冷光雷達耳罩，邊緣流動薄荷綠光纖微光，耳根嵌黃銅微型轉軸",
        "eyes": "雙聯球形高透聚碳酸酯太空泡罩目鏡，深藍紫金屬眼圈，浮現落日暖橘脈衝雷達刻線",
        "tail": "七節同軸深空消光黑曜與薄荷綠冷光光纖星環天線尾，末端安裝金黃微型全向天線球",
        "torso_and_limbs": "象牙白高強度工程聚合物塑料外殼，關節為自潤滑尼龍球鉸，雙手掌底與足底嵌導電矽膠吸附墊",
        "key": "三環軌道同心嵌套星環黃銅發條鑰匙，中心飾有多巴胺珊瑚粉防塵鉚釘",
        "weapon_system": "雙持專屬「星軌脈衝雙鋒短匕（Orbital Pulse Twin Daggers）」，沖壓半透明聚碳酸酯星環護手銅環，天藍電離導光槽配薄荷綠光學測距鋸齒，底層掛載 equipment.json 既有 star_fang (tier 2 短匕)"
    },
    "color_palette": {
        "primary": "#FFFDF8 (象牙白高抗衝擊聚合物板件)",
        "secondary": "#38A0FF (多巴胺天藍宇航吊帶胸甲與短匕刃身)",
        "accent_mint": "#4ED86A (薄荷綠冷光光纖尾環與雷達飾圈)",
        "accent_gold": "#FFD028 (金黃星環發條鑰匙與天線姿態球)",
        "accent_orange": "#FFA010 (落日暖橘琥珀目鏡與反光警示條)",
        "accent_pink": "#FF5E8A (珊瑚粉防塵鉚釘與減震密封膠圈)",
        "dark_polymer": "#1A243B (深空消光星夜藍黑聚合物尾環)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_lemur.png (品牌形象立牌)",
                "web/media/hero/char_lemur.png (官網英雄展示立繪)",
                "docs/art/star_ring_lemur_concept.png (概念立繪)",
                "game/assets/sprites/player/lemur_idle.png (64x64 待機)",
                "game/assets/sprites/player/lemur_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/lemur_idle.png (隊伍待機)",
                "web/media/hero/lemur_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/lemur_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/lemur_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/lemur_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/lemur_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/lemur_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/lemur_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/lemur/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/lemur.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/lemur_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/star_ring_lemur.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/lemur/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_lemur.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/star_ring_lemur_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_lemur.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/lemur_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/lemur_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/lemur_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/lemur_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/lemur_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/lemur_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/lemur_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/lemur/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/lemur.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/star_ring_lemur.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/lemur/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_lemur_orbit_polymer_default",
        "head_unit": "head_lemur_orbit_radar_cowl",
        "optic_core": "face_lemur_amber_pulsar_visors",
        "costume": "costume_lemur_astro_stealth_harness",
        "back_curio": "curio_lemur_neon_ring_fiber_tail",
        "winding_key": "key_lemur_tri_ring_orbit_brass",
        "weapon": "weapon_lemur_orbital_pulse_daggers"
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
        if slot_id in LEMUR_DEFAULT_ITEMS:
            item = LEMUR_DEFAULT_ITEMS[slot_id]
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
    if "lemur" not in existing_race_ids:
        races.append(LEMUR_RACE_SPEC)
        print("  Added lemur to races_specification.races")
    races_spec["total_races"] = 63

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    univ = compat.get("universal_slots", [])
    for u in univ:
        if u.get("slot_id") == "winding_key":
            u["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 63 種動物素體"
    adapted = compat.get("race_adapted_slots", [])
    for a in adapted:
        if a.get("slot_id") == "costume":
            old_rule = a.get("rule", "")
            if "星環狐猴" not in old_rule:
                new_rule = old_rule.replace("六十三重大種族", "六十四重大種族")
                if "破竹羚牛青古銅鑄鐵重裝底盤與天元拓荒道袍重肩甲" in new_rule:
                    new_rule = new_rule.replace(
                        "破竹羚牛青古銅鑄鐵重裝底盤與天元拓荒道袍重肩甲)",
                        "破竹羚牛青古銅鑄鐵重裝底盤與天元拓荒道袍重肩甲、星環狐猴象牙白高抗衝擊聚合物底盤與宇航匿蹤輕量安全吊帶胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    lemur_dir = "game/assets/sprites/player/paperdoll/lemur/"
    if lemur_dir not in races_dirs:
        races_dirs.append(lemur_dir)
        print(f"  Added {lemur_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Lemur proposal registered specification complete.")
