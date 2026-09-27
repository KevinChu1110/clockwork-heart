#!/usr/bin/env python3
"""為第二十三族琉璃海馬 (seahorse) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 seahorse 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_seahorse_abyssal_cyan_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_seahorse_abyssal_cyan_default",
            "name": "琉璃海馬原廠海藍琺瑯烤漆素體",
            "race": "seahorse",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_seahorse_crown_visor" for v in head_variants):
        head_variants.append({
            "id": "head_seahorse_crown_visor",
            "name": "沖壓高透石英水晶冠冕頂盔",
            "race": "seahorse",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_seahorse_trident_coral_spire" for v in key_variants):
        key_variants.append({
            "id": "key_seahorse_trident_coral_spire",
            "name": "三叉戟珊瑚晶簇黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_seahorse_abyssal_scholar_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_seahorse_abyssal_scholar_harness",
            "name": "海淵天宮星象輕甲工裝",
            "race": "seahorse",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "optic_seahorse_ocean_sapphire" for v in face_variants):
        face_variants.append({
            "id": "optic_seahorse_ocean_sapphire",
            "name": "雙聯深海藍寶石透鏡目鏡",
            "race": "seahorse",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_seahorse_abyssal_prism_astrolabe" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_seahorse_abyssal_prism_astrolabe",
            "name": "深海靈晶浮空星盤",
            "weapon_type": "crystal",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_seahorse_twin_propeller_fins" for v in curio_variants):
        curio_variants.append({
            "id": "curio_seahorse_twin_propeller_fins",
            "name": "雙聯微型發條螺旋推進晶鰭",
            "race": "seahorse",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 23

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "seahorse" for r in races_list):
        races_list.append({
            "race_id": "seahorse",
            "aliases": [
                "crystal_seahorse",
                "abyssal_seahorse",
                "ocean_seahorse",
                "tide_seahorse"
            ],
            "name_zh": "琉璃海馬",
            "name_en": "The Crystal Seahorse",
            "class_archetype": "法師 (Mage)",
            "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
            "lore_anchor": "穿梭於琉璃汪洋「水下發條宮殿」與「藍晶石海淵平原」的發條海馬學者，漫步於「海淵地表與馬賽克步道」的「發條珊瑚群」與「深淵排污豎井管道·耐壓吊籠」之間，通體由多巴胺天藍拋光海藍琺瑯烤漆板件、象牙米白陶瓷面頰板與胸板、三叉齒輪水晶王冠頂盔、雙聯深海藍寶石透鏡目鏡、三叉戟珊瑚晶簇黃銅發條鑰匙與微型三柱液壓接地鰭足組裝而成，以右手單持深海靈晶浮空星盤、洋流阻尼蓄力射擊與潮汐星陣暴發護盾織刃見長的深海學者",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (垂直修長挺拔水生法師體態)",
                "posture": "洋流阻尼優雅懸停架式，右手微曲懸引深海靈晶浮空星盤自轉，左手微曲作引導水流阻尼與晶盾編織起手式，身後雙聯微型螺旋推進晶鰭微幅振顫，背部三叉戟珊瑚晶簇發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓耐壓鍍鈦深海頂盔，額頭裝配三叉王冠狀齒輪晶冠，齒尖為多巴胺金黃，面部為可前後微幅伸縮之套筒式吸水長吻，面頰兩側為象牙米白陶瓷面頰板配外露螺栓，雙眼為雙聯深海藍寶石透鏡目鏡",
                "ears": "頭部兩側微型鍍鈦導流感應鰭閥，隨水流微壓微幅開合調節",
                "torso_and_limbs": "背部與側腰覆蓋多巴胺天藍拋光海藍琺瑯烤漆耐壓裝甲板，前胸覆蓋象牙米白陶瓷減震胸甲並留有直徑14px晶石展示孔，胸口內嵌菱形發條之心天藍晶核，下半身為五節高彈錳鋼螺旋板簧尾，尾端配備三柱微型液壓減震平衡鰭足",
                "tail": "由五節高彈錳鋼螺旋板簧一體成型內卷而成的螺旋減震尾，尾部末端配備三柱微型液壓防滑矽膠接地足",
                "weapon_system": "右手單持專利「深海靈晶浮空星盤 / 琉璃棱鏡核心」，由三層逆向旋轉之鍍鈦經緯金屬刻度環與懸浮八面體深海藍晶石組成，左手空手自然導向平衡，完全符合 0-MKT7 與 mage/crystal 體系，底層掛載 equipment.json 既有 shard_focus 與 prism_scepter"
            },
            "color_palette": {
                "primary": "#38A0FF (琉璃汪洋多巴胺天藍拋光琺瑯烤漆)",
                "secondary": "#FFFDF8 (象牙米白陶瓷面頰板與前胸護板)",
                "accent": "#FFD028 (多巴胺金黃三叉戟珊瑚晶簇發條鑰匙與王冠齒輪尖)",
                "detail": "#1C54B2 (雙眼藍寶石光學透鏡與星盤核心晶石)",
                "warm_highlight": "#FF5E8A (珊瑚粉微型氣壓平衡閥與引力導線端子)",
                "secondary_hull": "#2EC4B6 (薄荷海藍雙聯背鰭與耐壓密封圈)",
                "titanium_frame": "#7A8B99 (消光鍍鈦球窩脊椎關節與長吻套筒)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_seahorse.png (品牌形象立牌)",
                        "web/media/hero/char_seahorse.png (官網英雄展示立繪)",
                        "docs/art/crystal_seahorse_concept.png (概念立繪)",
                        "game/assets/sprites/player/seahorse_idle.png (64x64 待機)",
                        "game/assets/sprites/player/seahorse_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/seahorse_idle.png (隊伍待機)",
                        "game/assets/sprites/player/seahorse_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/seahorse_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/seahorse_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/seahorse/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/seahorse.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/crystal_seahorse.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/seahorse/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_seahorse.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/crystal_seahorse_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_seahorse.png (400x840) [待產出]",
                "web_preview": "web/media/hero/seahorse_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/seahorse_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/seahorse_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/seahorse_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/seahorse_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/seahorse_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/seahorse_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/seahorse/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/seahorse.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/crystal_seahorse.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/seahorse/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 23 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十三大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    seahorse_dir = "game/assets/sprites/player/paperdoll/seahorse/"
    if seahorse_dir not in races_dirs:
        races_dirs.append(seahorse_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/seahorse")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/seahorse")
    os.makedirs(poses_dir, exist_ok=True)
    poses_keep = os.path.join(poses_dir, ".gitkeep")
    if not os.path.exists(poses_keep):
        with open(poses_keep, "w") as f:
            pass
        print(f"建立 {poses_keep}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_gitkeeps(repo_root)
    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        update_paperdoll_slots(os.path.join(repo_root, p))
