#!/usr/bin/env python3
"""為第十八族沙鱗穿山甲 (pangolin) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/DUNE_PANGOLIN_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 pangolin 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_pangolin_dune_orange_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_pangolin_dune_orange_default",
            "name": "沖壓耐磨暖橘金屬覆鱗板件",
            "race": "pangolin",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_pangolin_brass_acoustic_ears" for v in head_variants):
        head_variants.append({
            "id": "head_pangolin_brass_acoustic_ears",
            "name": "沖壓薄黃銅扇形防砂拾音耳",
            "race": "pangolin",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_pangolin_coil_scale_spiral_gold" for v in key_variants):
        key_variants.append({
            "id": "key_pangolin_coil_scale_spiral_gold",
            "name": "同心渦卷金鱗發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_pangolin_scavenger_tinker_vest" for v in costume_variants):
        costume_variants.append({
            "id": "costume_pangolin_scavenger_tinker_vest",
            "name": "齒輪營地拾荒工匠工裝背心",
            "race": "pangolin",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_pangolin_sky_blue_optic_domes" for v in face_variants):
        face_variants.append({
            "id": "face_pangolin_sky_blue_optic_domes",
            "name": "雙聯星輝天藍雙聯透鏡光學目鏡",
            "race": "pangolin",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_pangolin_dune_drill_claw" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_pangolin_dune_drill_claw",
            "name": "渦輪掘進破甲機關爪",
            "weapon_type": "claw",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_pangolin_segmented_scale_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_pangolin_segmented_scale_tail",
            "name": "七節沖壓厚鋼金屬覆鱗尾",
            "race": "pangolin",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 18

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "pangolin" for r in races_list):
        races_list.append({
            "race_id": "pangolin",
            "aliases": [
                "dune_pangolin",
                "sand_pangolin",
                "clockwork_pangolin",
                "armored_pangolin"
            ],
            "name_zh": "沙鱗穿山甲",
            "name_en": "The Dune Pangolin",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
            "lore_anchor": "自遺忘舊庫「巨型零件殘骸沙丘」與「拾荒拼裝聚落·齒輪營地」穿梭而出的發條穿山甲，仰望著「舊庫重型吊裝龍門架」與「大齒輪懸索天梯·舊庫總站」，通體由沖壓暖橘金屬覆鱗板件、象牙米白琺瑯面腹甲、沖壓薄黃銅扇形拾音耳、吸震黑色矽膠足墊與七節厚鋼覆鱗尾組裝而成，以右手單戴渦輪掘進破甲機關爪、重裝下潛破勢與縮球剛勁反震見長的荒原開拓拳師",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (圓滾滾敦實球形覆鱗體態)",
                "posture": "四足抓地穩步微屈架式，右手單戴重型機關爪橫架胸前，左手平伸化勁引掌，身後七節厚鋼覆鱗尾自然垂地支撐，背部同心渦卷發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "圓潤球形金屬頭部，配有象牙米白琺瑯面頰板與後頸三排弧形金屬防護鱗板，雙眼為直徑24px星輝天藍雙聯透鏡光學目鏡，內含同心圓刻度測距儀光圈",
                "ears": "一對沖壓薄黃銅扇形防砂拾音耳，內嵌微孔濾網，基座配備單軸步進鉸鏈，可在風沙中向後收攏防塵",
                "torso_and_limbs": "背部與側身覆蓋層疊活動之沖壓耐磨暖橘電鍍金屬覆鱗板件，胸腹覆蓋象牙米白減震琺瑯護板，四肢末端裝配吸震防滑黑色工程矽膠足墊與金屬防磨蹄套",
                "tail": "由七節沖壓厚鋼金屬覆鱗同軸鉸接於彈簧鋼芯組成的重錘平衡尾，尾尖懸掛八角黃銅配重球",
                "weapon_system": "右手單戴專利「渦輪掘進破甲機關爪 / 沙暴開山穿山爪」，三聯沖壓鎢鋼厚刃配合前臂微型液壓氣缸，左手空手化勁平衡，完全符合 0-MKT7 與 monk/claw 體系，底層掛載 equipment.json 既有 hunt_claw"
            },
            "color_palette": {
                "primary": "#FFA010 (多巴胺暖橘電鍍鋼板覆鱗)",
                "secondary": "#FFFDF8 (象牙米白琺瑯面頰與前胸腹板)",
                "accent": "#FFD028 (多巴胺金黃同心渦卷發條鑰匙與耳廓銅圈)",
                "detail": "#38A0FF (星輝天藍光學晶核目鏡透鏡光圈)",
                "warm_highlight": "#FF5E8A (珊瑚粉關節洩壓環與減震襯墊)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_pangolin.png (品牌形象立牌)",
                        "web/media/hero/char_pangolin.png (官網英雄展示立繪)",
                        "docs/art/dune_pangolin_concept.png (概念立繪)",
                        "game/assets/sprites/player/pangolin_idle.png (64x64 待機)",
                        "game/assets/sprites/player/pangolin_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/pangolin_idle.png (隊伍待機)",
                        "game/assets/sprites/player/pangolin_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/pangolin_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/pangolin_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/pangolin/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/pangolin.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/dune_pangolin.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/pangolin/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_pangolin.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/dune_pangolin_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_pangolin.png (400x840) [待產出]",
                "web_preview": "web/media/hero/pangolin_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/pangolin_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/pangolin_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/pangolin_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/pangolin_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/pangolin_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/pangolin_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/pangolin/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/pangolin.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/dune_pangolin.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/pangolin/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 18 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十八大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    pangolin_dir = "game/assets/sprites/player/paperdoll/pangolin/"
    if pangolin_dir not in races_dirs:
        races_dirs.append(pangolin_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/pangolin")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/pangolin")
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
