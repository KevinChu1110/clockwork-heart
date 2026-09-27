#!/usr/bin/env python3
"""為第十九族浪花海獺 (otter) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/TIDAL_OTTER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 otter 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_otter_abyssal_cyan_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_otter_abyssal_cyan_default",
            "name": "深海天藍耐壓電鍍合金板件",
            "race": "otter",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_otter_diver_bell_visor" for v in head_variants):
        head_variants.append({
            "id": "head_otter_diver_bell_visor",
            "name": "古典潛水鐘頭盔護架",
            "race": "otter",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_otter_nautical_rudder_helm" for v in key_variants):
        key_variants.append({
            "id": "key_otter_nautical_rudder_helm",
            "name": "雙舵輪金黃航海發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_otter_deepsea_salvage_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_otter_deepsea_salvage_harness",
            "name": "海淵打撈工匠耐壓雙肩吊帶工裝",
            "race": "otter",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_otter_phosphor_green_gauges" for v in face_variants):
        face_variants.append({
            "id": "face_otter_phosphor_green_gauges",
            "name": "雙聯薄荷螢綠石英泡罩目鏡",
            "race": "otter",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_otter_abyssal_anchor_cleaver" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_otter_abyssal_anchor_cleaver",
            "name": "海錨防禦重斧",
            "weapon_type": "axe",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_otter_articulated_rudder_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_otter_articulated_rudder_tail",
            "name": "五節鉸鏈龍骨轉向舵尾",
            "race": "otter",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 19

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "otter" for r in races_list):
        races_list.append({
            "race_id": "otter",
            "aliases": [
                "tidal_otter",
                "abyssal_otter",
                "clockwork_otter",
                "diver_otter"
            ],
            "name_zh": "浪花海獺",
            "name_en": "The Tidal Otter",
            "class_archetype": "戰士 (Viking)",
            "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
            "lore_anchor": "穿梭於琉璃汪洋「水下發條宮殿」與「藍晶石海淵平原」的發條海獺，漫步於「海淵地表與馬賽克步道」的「發條珊瑚群」之間，通體由深海耐壓天藍鍍鈦板件、象牙米白琺瑯面腹甲、青銅防水透氣拾音耳、吸震黑色矽膠潛水靴與五節龍骨舵尾組裝而成，以右手單持海錨防禦重斧、踏浪浮力下墜破勢與巨斧旋渦重劈見長的海淵開拓戰士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (圓滾滾敦實流線型耐壓體態)",
                "posture": "踏浪伏波沉錨架式，右手單提青銅海錨重斧橫架身前，左手平伸化掌導流，身後五節龍骨舵尾自然翹起，背部雙舵輪發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "圓潤球形耐壓金屬頭部，配有象牙米白琺瑯面頰板與前額水壓平衡閥，雙眼為直徑24px薄荷螢綠石英泡罩光學目鏡，內含同心圓水壓測距儀刻度圈與左右六根鍍銀流速探針鬍鬚",
                "ears": "一對微型青銅防水透氣拾音耳閥，內嵌防砂隔水濾膜，外緣帶有黃銅緊固圓環",
                "torso_and_limbs": "背部與側身覆蓋厚度1.5mm多巴胺天藍耐壓電鍍合金板件，前胸覆蓋圓弧象牙米白減壓琺瑯護板，四肢末端裝配吸震防滑厚底黑色工程矽膠潛水靴與金屬防衝撞踏板",
                "tail": "由五節沖壓鍍鈦金屬龍骨鉸接而成的扁平槳舵尾，尾端中央整合反向旋轉微型黃銅雙螺旋槳推進器",
                "weapon_system": "右手單持專利「海錨防禦重斧 / 琉璃破障重斧」，重型青銅海錨月牙破障厚刃配合耐壓鋼索與高壓氣閥，左手空手導向平衡，完全符合 0-MKT7 與 viking/axe 體系，底層掛載 equipment.json 既有 split_greataxe"
            },
            "color_palette": {
                "primary": "#38A0FF (多巴胺天藍耐壓電鍍合金板件)",
                "secondary": "#FFFDF8 (象牙米白琺瑯面頰與前胸減壓腹板)",
                "accent": "#FFD028 (多巴胺金黃黃銅航海舵輪發條鑰匙與耳廓銅圈)",
                "detail": "#4ED86A (薄荷螢綠深海磷光儀表晶核目鏡透鏡光圈)",
                "warm_highlight": "#FF5E8A (珊瑚粉耐壓密封矽膠圈與洩氣安全閥)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_otter.png (品牌形象立牌)",
                        "web/media/hero/char_otter.png (官網英雄展示立繪)",
                        "docs/art/tidal_otter_concept.png (概念立繪)",
                        "game/assets/sprites/player/otter_idle.png (64x64 待機)",
                        "game/assets/sprites/player/otter_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/otter_idle.png (隊伍待機)",
                        "game/assets/sprites/player/otter_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/otter_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/otter_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/otter/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/otter.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/tidal_otter.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/otter/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_otter.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/tidal_otter_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_otter.png (400x840) [待產出]",
                "web_preview": "web/media/hero/otter_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/otter_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/otter_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/otter_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/otter_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/otter_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/otter_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/otter/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/otter.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/tidal_otter.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/otter/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 19 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十九大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    otter_dir = "game/assets/sprites/player/paperdoll/otter/"
    if otter_dir not in races_dirs:
        races_dirs.append(otter_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/otter")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/otter")
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
