#!/usr/bin/env python3
"""為第十六族靈鐘鴞 (owl) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/CHRONO_OWL_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 owl 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_owl_brass_lamellae_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_owl_brass_lamellae_default",
            "name": "沖壓黃銅疊片羽翼板件",
            "race": "owl",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_owl_brass_plume_antennas" for v in head_variants):
        head_variants.append({
            "id": "head_owl_brass_plume_antennas",
            "name": "半球沖壓黃銅頭蓋骨與翎管天線",
            "race": "owl",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_owl_sun_moon_astrolabe_gold" for v in key_variants):
        key_variants.append({
            "id": "key_owl_sun_moon_astrolabe_gold",
            "name": "三環日月星象黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_owl_dawn_astronomer_robe" for v in costume_variants):
        costume_variants.append({
            "id": "costume_owl_dawn_astronomer_robe",
            "name": "晨曦觀星學者短披肩斗篷",
            "race": "owl",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_owl_clockface_lens_dusk_gold" for v in face_variants):
        face_variants.append({
            "id": "face_owl_clockface_lens_dusk_gold",
            "name": "雙聯同心圓刻度石英鐘面目鏡",
            "race": "owl",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_owl_armillary_escapement_scepter" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_owl_armillary_escapement_scepter",
            "name": "渾天星儀擒縱法杖",
            "weapon_type": "magic",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_owl_floating_micro_orrery" for v in curio_variants):
        curio_variants.append({
            "id": "curio_owl_floating_micro_orrery",
            "name": "懸浮微型太陽系天體儀",
            "race": "owl",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 16

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "owl" for r in races_list):
        races_list.append({
            "race_id": "owl",
            "aliases": [
                "chrono_owl",
                "clockwork_owl",
                "belltower_owl",
                "astral_owl"
            ],
            "name_zh": "靈鐘鴞",
            "name_en": "The Chrono Owl",
            "class_archetype": "法師 (Mage)",
            "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
            "lore_anchor": "自晨曦小鎮「懸吊齒輪鐘樓」之巔守候天文走時的發條鐘鴞，在「石板街道集市」上方展開星儀，通體由沖壓黃銅疊片羽板、雙聯同心圓刻度石英鐘面目鏡、胸前高透石英擒縱陀飛輪透窗與360度棘輪轉向頸環組裝而成，以單持渾天星儀擒縱法杖、延遲天文法陣與大範圍星象爆破見長的時之法師",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (圓滾滾球形天文鐘鳥體態)",
                "posture": "側身星儀守夜巡候架式，右手單持渾天星儀法杖斜立於側，左翼微攏收束，三爪扎地，背部三環日月星象發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 440
            },
            "mechanical_features": {
                "head_and_neck": "圓潤球形沖壓黃銅頭蓋骨，配備360度自鎖棘輪轉向頸環與頭頂青銅翎管微波天線羽，雙眼為直徑28px同心圓刻度石英鐘面目鏡，內含微型發光秒針",
                "ears": "一對沖壓青銅翎管微波天線羽，表面刻有同心星軌刻度，可隨星象磁場輕微偏轉",
                "torso_and_limbs": "軀幹為午夜曜藍烤漆合金外殼搭配象牙米白琺瑯腹板，中央嵌有高透防刮石英觀測透窗，內含雙子擒縱調速輪與星盤齒輪箱；雙足為三爪高剛性鎢鋼機械抓握爪",
                "wings": "由12片沖壓黃銅疊片羽板層疊鉸接而成的折疊機械翼，開合帶有金屬剪切脆響",
                "weapon_system": "右手單持專利「渾天星儀擒縱法杖 / 天文星曆權杖」，杖首三環可差速展開旋轉並聚斂星屑彈道，左翼空手微攏，完全符合 0-MKT7 與 mage/magic 體系"
            },
            "color_palette": {
                "primary": "#FFFDF8 (象牙米白琺瑯烤漆腹板)",
                "secondary": "#38A0FF (星軌晴空天藍羽尖飾邊)",
                "accent": "#FFD028 (日月星象金黃發條鑰匙與鐘面刻度)",
                "detail": "#4ED86A (薄荷螢光星屑晶核與法陣光環)",
                "warm_highlight": "#FFA010 (暖橘金黃指針刻度與關節鉚栓)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_owl.png (品牌形象立牌)",
                        "web/media/hero/char_owl.png (官網英雄展示立繪)",
                        "docs/art/chrono_owl_concept.png (概念立繪)",
                        "game/assets/sprites/player/owl_idle.png (64x64 待機)",
                        "game/assets/sprites/player/owl_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/owl_idle.png (隊伍待機)",
                        "game/assets/sprites/player/owl_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/owl_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/owl_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/owl/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/owl.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/chrono_owl.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/owl/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_owl.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/chrono_owl_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_owl.png (400x840) [待產出]",
                "web_preview": "web/media/hero/owl_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/owl_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/owl_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/owl_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/owl_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/owl_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/owl_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/owl/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/owl.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/chrono_owl.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/owl/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 16 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十六大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    for rdir in ["game/assets/sprites/player/paperdoll/hound/", "game/assets/sprites/player/paperdoll/owl/"]:
        if rdir not in races_dirs:
            races_dirs.append(rdir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/owl")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/owl")
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
