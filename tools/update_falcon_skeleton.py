#!/usr/bin/env python3
"""為第二十八族疾影神隼 (falcon) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/SWIFT_FALCON_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 falcon 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_falcon_aero_brass_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_falcon_aero_brass_default",
            "name": "疾影神隼原廠曜金冷軋合金素體",
            "race": "falcon",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_falcon_streamlined_beak_visor" for v in head_variants):
        head_variants.append({
            "id": "head_falcon_streamlined_beak_visor",
            "name": "流線鷹喙沖壓金屬面罩",
            "race": "falcon",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_falcon_aero_twin_quill" for v in key_variants):
        key_variants.append({
            "id": "key_falcon_aero_twin_quill",
            "name": "雙羽旋風發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_falcon_skyline_warden_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_falcon_skyline_warden_harness",
            "name": "空境巡守輕裝風行胸背甲",
            "race": "falcon",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_falcon_amber_quartz_optic" for v in face_variants):
        face_variants.append({
            "id": "face_falcon_amber_quartz_optic",
            "name": "琥珀石英雙聯鷹眼目鏡",
            "race": "falcon",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_falcon_shadow_talon_claw" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_falcon_shadow_talon_claw",
            "name": "疾影穿雲機關爪",
            "weapon_type": "claw",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_falcon_aerodynamic_rudder_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_falcon_aerodynamic_rudder_tail",
            "name": "三聯空氣動力滑翔舵板尾羽",
            "race": "falcon",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 28

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "falcon" for r in races_list):
        races_list.append({
            "race_id": "falcon",
            "aliases": [
                "swift_falcon",
                "shadow_falcon",
                "skyline_falcon",
                "aero_falcon"
            ],
            "name_zh": "疾影神隼",
            "name_en": "The Swift Falcon",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
            "lore_anchor": "世代守護翡翠深林巨木樹屋聚落、觀風石碑塔、樹汁導流泵、神隼翱翔之巢與觀風岩頂的高空巡守發條獵鷹偶，通體由象牙米白琺瑯冷軋薄鋼板件、沖壓高剛性黃銅疊片羽翼、流線鷹喙沖壓金屬面罩、琥珀石英雙聯鷹眼目鏡、雙羽旋風發條鑰匙與三聯空氣動力滑翔舵板尾羽組裝而成，以右手單戴疾影穿雲機關爪、高空俯衝看破與停拍鷹爪突刺見長的空境武術家",
            "proportions": {
                "head_to_body_ratio": "2.2 ~ 2.8 頭身 (靈巧高空猛禽偶、流線俯衝剪影)",
                "posture": "身軀微前傾，金屬雙足抓地穩健，雙翼羽板半收於體側，右手單戴疾影穿雲爪屈橫於胸前，三聯舵板尾羽下壓維持氣流平衡，琥珀目鏡銳利鎖定關節咬合",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "冷軋薄鋼輕量化金屬獵鷹頭盔，面頰為曜石鐵灰沖壓鷹喙護面（#2A2B32），內部為金屬發音齒輪排氣孔，雙眼為圓形琥珀石英雙聯鷹眼目鏡（#FFA010）內刻同心測距環與風向光環",
                "ears": "頭盔頂部飾有一對微型空氣動力導風鰭片與天線耳軸，感應林冠高空氣流擾動",
                "torso_and_limbs": "主軀幹外殼為象牙米白琺瑯冷軋薄鋼板（#FFFDF8）配微型黃銅平頭鉚釘，雙臂為圓柱形外露黃銅球窩關節，雙翼為五層高剛性暖金黃銅薄片（#FFA010）梯級鉸接疊加",
                "tail": "由三片梯級開合的啞光合金金屬舵板構成的三聯空氣動力滑翔舵板尾羽，懸停與滑行時靈活擺動提供氣動配重與姿態制動",
                "weapon_system": "右手單戴專屬「疾影穿雲機關爪（Shadow-Talon Cloud Piercing Claw）」，三指高碳鋼開刃彎爪搭配手腕微型增壓導軌與擒縱棘輪，完全符合 0-MKT7 與 monk/claw 體系，底層掛載 equipment.json 既有 hunt_claw"
            },
            "color_palette": {
                "primary": "#FFA010 (暖金黃銅沖壓雙翼羽板與鷹爪外裝)",
                "secondary": "#FFFDF8 (象牙米白琺瑯輕量化胸腹甲與面頰板件)",
                "faceplate": "#2A2B32 (曜石鐵灰鷹喙面罩與關節基板)",
                "accent": "#FFD028 (天元金黃雙羽鑰匙軸心與目鏡瞄準環)",
                "detail": "#38A0FF (晴空天藍琥珀目鏡反射微光與氣流指示器)",
                "frame": "#5A5666 (暗鎢鋼冷軋骨架與內部連桿)",
                "costume_coral": "#FF5E8A (珊瑚粉紅減震矽膠墊圈與背帶飾繩)",
                "emerald_accent": "#4ED86A (薄荷翡翠巡守風行背甲滾邊飾條)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_falcon.png (品牌形象立牌)",
                        "web/media/hero/char_falcon.png (官網英雄展示立繪)",
                        "docs/art/swift_falcon_concept.png (概念立繪)",
                        "game/assets/sprites/player/falcon_idle.png (64x64 待機)",
                        "game/assets/sprites/player/falcon_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/falcon_idle.png (隊伍待機)",
                        "game/assets/sprites/player/falcon_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/falcon_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/falcon_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/falcon/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/falcon.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/swift_falcon.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/falcon/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_falcon.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/swift_falcon_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_falcon.png (400x840) [待產出]",
                "web_preview": "web/media/hero/falcon_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/falcon_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/falcon_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/falcon_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/falcon_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/falcon_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/falcon_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/falcon/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/falcon.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/swift_falcon.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/falcon/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 28 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十八大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    falcon_dir = "game/assets/sprites/player/paperdoll/falcon/"
    if falcon_dir not in races_dirs:
        races_dirs.append(falcon_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/falcon")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/falcon")
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
