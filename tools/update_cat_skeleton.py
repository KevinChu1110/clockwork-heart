#!/usr/bin/env python3
"""為第十七族幽影貓 (cat) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/UMBRAL_CAT_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 cat 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_cat_obsidian_steel_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_cat_obsidian_steel_default",
            "name": "冷軋曜黑碳化鋼板件",
            "race": "cat",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_cat_brass_acoustic_ears" for v in head_variants):
        head_variants.append({
            "id": "head_cat_brass_acoustic_ears",
            "name": "沖壓薄黃銅折角共鳴拾音耳",
            "race": "cat",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_cat_crescent_twin_ring_gold" for v in key_variants):
        key_variants.append({
            "id": "key_cat_crescent_twin_ring_gold",
            "name": "新月夜行雙環黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_cat_skyspire_prowler_vest" for v in costume_variants):
        costume_variants.append({
            "id": "costume_cat_skyspire_prowler_vest",
            "name": "天街巡夜緊身工裝背心",
            "race": "cat",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_cat_slit_optic_emerald" for v in face_variants):
        face_variants.append({
            "id": "face_cat_slit_optic_emerald",
            "name": "雙聯祖母綠石英夜視目鏡",
            "race": "cat",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_cat_shadowspring_stiletto" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_cat_shadowspring_stiletto",
            "name": "暗影發條袖刃",
            "weapon_type": "dagger",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_cat_segmented_gyro_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_cat_segmented_gyro_tail",
            "name": "九節同軸平衡發條鋼索尾",
            "race": "cat",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 17

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "cat" for r in races_list):
        races_list.append({
            "race_id": "cat",
            "aliases": [
                "umbral_cat",
                "shadow_cat",
                "clockwork_cat",
                "nightprowl_cat"
            ],
            "name_zh": "幽影貓",
            "name_en": "The Umbral Cat",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "自巨輪城「摩天齒輪工坊群」高聳屋脊踏著靜音蒸氣穿梭的發條黑貓，在「中央動力廣場」上方的暗夜齒輪死角中游走，通體由冷軋曜黑碳化鋼板件、象牙米白琺瑯面頰板、沖壓薄黃銅折角共鳴拾音耳、吸震黑色矽膠足墊與九節同軸平衡鋼索尾組裝而成，以右手反握暗影發條袖刃、極限靜音步態與弱點死線背刺見長的無聲刺客",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (圓滾滾球形夜行貓體態)",
                "posture": "四足微屈暗夜潛伏巡視架式，右手反握暗影袖刃收於側肋，左爪微張觸地平衡，身後九節平衡鋼索尾優雅微曲，背部新月夜行發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "圓潤球形冷軋曜黑碳化鋼頭蓋骨，配有一體成型象牙米白琺瑯面頰板與六根超細鎢鋼微振彈簧鬚，雙眼為直徑24px雙聯夜視裂隙光學目鏡，內含薄荷綠螢光光圈",
                "ears": "一對沖壓薄黃銅折角共鳴拾音耳，基座配備微型雙軸步進鉸鏈，可隨環境聲波獨立偏轉",
                "torso_and_limbs": "軀幹為曜黑消光烤漆合金裝甲搭配象牙米白胸板，四肢末端裝配吸震耐磨黑色工程矽膠靜音步態足墊，足尖內藏三指高碳鎢鋼精密伸縮爪",
                "tail": "由九節空心沖壓黃銅微型轉子同軸套接於彈簧鋼索組成的陀螺平衡尾，尾尖懸掛黃銅平衡錘",
                "weapon_system": "右手反手單持專利「暗影發條袖刃 / 匿夜弧光短匕」，左爪空手保持平衡，完全符合 0-MKT7 與 ninja/dagger 體系，底層掛載 equipment.json 既有 star_fang / nebula_needle"
            },
            "color_palette": {
                "primary": "#2B2630 (深邃曜黑消光烤漆鋼板)",
                "secondary": "#FFFDF8 (象牙米白琺瑯面頰與前胸護板)",
                "accent": "#FFD028 (多巴胺金黃新月發條鑰匙與眼眶銅圈)",
                "detail": "#4ED86A (薄荷螢光夜視目鏡裂隙光圈)",
                "warm_highlight": "#FFA010 (暖橘金黃關節鉚栓與洩壓飾圈)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_cat.png (品牌形象立牌)",
                        "web/media/hero/char_cat.png (官網英雄展示立繪)",
                        "docs/art/umbral_cat_concept.png (概念立繪)",
                        "game/assets/sprites/player/cat_idle.png (64x64 待機)",
                        "game/assets/sprites/player/cat_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/cat_idle.png (隊伍待機)",
                        "game/assets/sprites/player/cat_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/cat_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/cat_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/cat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/cat.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/umbral_cat.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/cat/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_cat.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/umbral_cat_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_cat.png (400x840) [待產出]",
                "web_preview": "web/media/hero/cat_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/cat_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/cat_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/cat_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/cat_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/cat_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/cat_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/cat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/cat.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/umbral_cat.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/cat/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 17 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十七大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    cat_dir = "game/assets/sprites/player/paperdoll/cat/"
    if cat_dir not in races_dirs:
        races_dirs.append(cat_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/cat")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/cat")
    os.makedirs(poses_dir, exist_ok=True)
    poses_keep = os.path.join(poses_dir, ".gitkeep")
    if not os.path.exists(poses_keep):
        with open(poses_keep, "w") as f:
            pass
        print(f"建立 {poses_keep}")

if __name__ == "__main__":
    repo_root = "/opt/side/bravesoul-game"
    create_gitkeeps(repo_root)
    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        update_paperdoll_slots(os.path.join(repo_root, p))
