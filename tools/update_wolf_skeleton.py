#!/usr/bin/env python3
"""為第二十二族荒原鋼狼 (wolf) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/SCRAP_WOLF_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 wolf 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_wolf_warm_orange_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_wolf_warm_orange_default",
            "name": "廢土多巴胺暖橘防鏽烤漆鋼板",
            "race": "wolf",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_wolf_gear_mane_cowl" for v in head_variants):
        head_variants.append({
            "id": "head_wolf_gear_mane_cowl",
            "name": "五層同心消光鎢鋼齒輪咬合護頸護甲",
            "race": "wolf",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_wolf_heavy_pojun_cross" for v in key_variants):
        key_variants.append({
            "id": "key_wolf_heavy_pojun_cross",
            "name": "高扭力破軍重工十字發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_wolf_scavenger_scrap_plate_armor" for v in costume_variants):
        costume_variants.append({
            "id": "costume_wolf_scavenger_scrap_plate_armor",
            "name": "廢土拾荒者拼裝板甲",
            "race": "wolf",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_wolf_twin_blue_optic_lens" for v in face_variants):
        face_variants.append({
            "id": "face_wolf_twin_blue_optic_lens",
            "name": "星輝天藍雙聯光學晶核目鏡",
            "race": "wolf",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_wolf_scrap_sawblade_greatsword" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_wolf_scrap_sawblade_greatsword",
            "name": "廢土鋸齒重鋼劍",
            "weapon_type": "sword",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_wolf_segmented_spring_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_wolf_segmented_spring_tail",
            "name": "高扭力螺旋發條多節重鋼平衡尾",
            "race": "wolf",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 22

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "wolf" for r in races_list):
        races_list.append({
            "race_id": "wolf",
            "aliases": [
                "scrap_wolf",
                "dune_wolf",
                "rust_wolf",
                "wasteland_wolf"
            ],
            "name_zh": "荒原鋼狼",
            "name_en": "The Scrap Wolf",
            "class_archetype": "騎士 (Knight)",
            "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
            "lore_anchor": "遊蕩於荒漠舊庫「巨型零件殘骸沙丘」與「拾荒拼裝聚落·齒輪營地」之間的發條流浪騎士，守護著「大齒輪懸索天梯·舊庫總站」與「舊庫重型吊裝龍門架」的零件走廊，通體由廢土多巴胺暖橘防鏽鋼板、象牙米白琺瑯面頰板、五層齒輪咬合護頸護甲、星輝天藍雙聯晶核目鏡、高扭力破軍重工十字發條鑰匙與黑色矽膠行軍靴組裝而成，以右手單持廢土鋸齒重鋼劍、散熱窗口破甲重斬與破軍狂風裂地見長的忠誠騎士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (沉穩剛勁騎士機械體態)",
                "posture": "流浪騎士沉著步態，右手單持廢土鋸齒重鋼劍斜指斜下方，左手自然微曲收於腰側作格擋防守，頸部齒輪護圈緊湊咬合，背部重工十字發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "圓潤剛勁金屬頭殼，配有象牙米白琺瑯面頰板與鍍鉻螺紋調節鈕吻部，雙眼為星輝天藍雙聯光學晶核目鏡，內含同心圓測距刻度標尺，頸部環繞五層同心消光鎢鋼齒輪咬合護頸護甲",
                "ears": "一對折疊沖壓黃銅導風耳，內置微型音頻共鳴簧片，隨風沙機械聲微幅轉向",
                "torso_and_limbs": "背部與側腰覆蓋厚度2.0mm多巴胺暖橘防鏽烤漆鋼板，前胸覆蓋象牙米白琺瑯減震胸甲，四肢末端裝配厚底耐磨防滑黑色工業矽膠行軍靴與厚鎢鋼防撞踢板",
                "tail": "由七節沖壓鎢鋼外殼串聯螺旋發條而成的多節平衡鋼尾，行動時自然擺動保持重心",
                "weapon_system": "右手單持專利「廢土鋸齒重鋼劍 / 破軍殘刃」，加厚鎢鋼鋸齒長劍內置外齒輪配重環，左手空手自然握拳迎擊，完全符合 0-MKT7 與 knight/sword 體系，底層掛載 equipment.json 既有 rusty_blade 與 knight_saber"
            },
            "color_palette": {
                "primary": "#FFA010 (廢土暖橘防鏽烤漆鋼板)",
                "secondary": "#FFFDF8 (象牙米白琺瑯面頰與前胸)",
                "accent": "#FFD028 (金黃多巴胺重工發條鑰匙與齒輪組)",
                "detail": "#38A0FF (星輝天藍雙聯光學晶核目鏡)",
                "warm_highlight": "#FF5E8A (珊瑚粉減震密封矽膠圈與油路端子)",
                "scrap_steel": "#5A5666 (消光沖壓鎢鋼鋸齒刃部)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_wolf.png (品牌形象立牌)",
                        "web/media/hero/char_wolf.png (官網英雄展示立繪)",
                        "docs/art/scrap_wolf_concept.png (概念立繪)",
                        "game/assets/sprites/player/wolf_idle.png (64x64 待機)",
                        "game/assets/sprites/player/wolf_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/wolf_idle.png (隊伍待機)",
                        "game/assets/sprites/player/wolf_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/wolf_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/wolf_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/wolf/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/wolf.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/scrap_wolf.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/wolf/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_wolf.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/scrap_wolf_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_wolf.png (400x840) [待產出]",
                "web_preview": "web/media/hero/wolf_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/wolf_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/wolf_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/wolf_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/wolf_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/wolf_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/wolf_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/wolf/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/wolf.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/scrap_wolf.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/wolf/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 22 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十二大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    wolf_dir = "game/assets/sprites/player/paperdoll/wolf/"
    if wolf_dir not in races_dirs:
        races_dirs.append(wolf_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/wolf")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/wolf")
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
