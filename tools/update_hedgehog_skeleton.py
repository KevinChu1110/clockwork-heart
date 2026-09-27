#!/usr/bin/env python3
"""為第二十一族棘輪刺蝟 (hedgehog) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 hedgehog 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_hedgehog_amber_brass_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_hedgehog_amber_brass_default",
            "name": "溫暖琥珀橙拋光黃銅外殼",
            "race": "hedgehog",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_hedgehog_brass_tuning_fork_ears" for v in head_variants):
        head_variants.append({
            "id": "head_hedgehog_brass_tuning_fork_ears",
            "name": "古典半圓拋光黃銅音叉耳",
            "race": "hedgehog",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_hedgehog_ratchet_and_pawl_cross" for v in key_variants):
        key_variants.append({
            "id": "key_hedgehog_ratchet_and_pawl_cross",
            "name": "單向棘爪棘輪發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_hedgehog_marionette_tailor_vest" for v in costume_variants):
        costume_variants.append({
            "id": "costume_hedgehog_marionette_tailor_vest",
            "name": "晨曦提線裁縫工匠馬甲",
            "race": "hedgehog",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_hedgehog_watchmaker_precision_loupe" for v in face_variants):
        face_variants.append({
            "id": "face_hedgehog_watchmaker_precision_loupe",
            "name": "薄荷螢綠單片鐘錶匠放大目鏡",
            "race": "hedgehog",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_hedgehog_ratchet_needle_dart" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_hedgehog_ratchet_needle_dart",
            "name": "棘輪穿針機關鏢",
            "weapon_type": "dart",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_hedgehog_spring_steel_quill_pack" for v in curio_variants):
        curio_variants.append({
            "id": "curio_hedgehog_spring_steel_quill_pack",
            "name": "三聯放射狀淬火彈簧鋼棘發射槽",
            "race": "hedgehog",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 21

    races_list = races_spec["races"]

    # 先清理可能重複的 raccoon（保留後面有 existing 標記的較完整版本）
    seen_races = set()
    cleaned_races = []
    # 由後往前遍歷以保留最新定義
    for r in reversed(races_list):
        rid = r.get("race_id")
        if rid not in seen_races:
            seen_races.add(rid)
            cleaned_races.append(r)
    cleaned_races.reverse()
    races_list = cleaned_races
    races_spec["races"] = races_list

    if not any(r.get("race_id") == "hedgehog" for r in races_list):
        races_list.append({
            "race_id": "hedgehog",
            "aliases": [
                "ratchet_hedgehog",
                "bazaar_hedgehog",
                "needle_hedgehog",
                "dawn_hedgehog"
            ],
            "name_zh": "棘輪刺蝟",
            "name_en": "The Ratchet Hedgehog",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
            "lore_anchor": "穿梭於晨曦小鎮「懸吊齒輪鐘樓」與「石板街道集市」的發條刺蝟工匠，漫步於「歐風木造街屋」之間，通體由溫暖琥珀橙拋光黃銅板件、象牙米白琺瑯面頰板、淬火彈簧鋼棘發射槽、薄荷螢綠單片鐘錶放大鏡、單向棘爪發條鑰匙與防滑矽膠工匠靴組裝而成，以右手單持棘輪穿針機關鏢、引線多段折返連續穿刺與天機千針暴風見長的鐘樓密探忍者",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (圓滾滾緊湊工匠機械體態)",
                "posture": "工匠戒備步態，右手平端棘輪穿針機關鏢於身側，左手平抬胸前作引線測距，背部淬火鋼棘自然整齊排列，背部單向棘爪發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "圓潤球形黃銅頭殼，配有象牙米白琺瑯面頰板與鍍鉻螺紋調節鈕吻部，右眼為薄荷螢綠單片鐘錶放大鏡，內含同心圓微米測距光圈，左眼為黑曜石寶石眼，兩側帶有一對金黃走時指針鬍鬚",
                "ears": "一對半圓形拋光黃銅音叉耳，內置微型音準共鳴簧片，隨集市鐘聲微幅震顫",
                "torso_and_limbs": "背部覆蓋厚度1.8mm多巴胺琥珀橙拋光黃銅外殼，胸腹覆蓋象牙米白琺瑯減震板，四肢末端裝配防滑耐磨厚底黑色工匠矽膠靴與圓弧黃銅防撞包角",
                "spines": "由三組放射狀沖壓淬火彈簧鋼片組裝而成的微型棘刺發射槽，蓄力時向外整齊彈開30度，受引線牽引可分離發射",
                "weapon_system": "右手單持專利「棘輪穿針機關鏢 / 巡影飛棘」，高精黃銅飛鏢內置發條回卷線軸與棘爪鎖，左手空手引線導向平衡，完全符合 0-MKT7 與 ninja/dart 體系，底層掛載 equipment.json 既有 mist_darts 與 shadow_chakram"
            },
            "color_palette": {
                "primary": "#FF8C42 (溫暖琥珀橙拋光黃銅外殼)",
                "secondary": "#FFFDF8 (象牙米白琺瑯面頰與腹板)",
                "accent": "#FFD028 (金黃單向棘爪發條鑰匙與齒輪組)",
                "detail": "#4ED86A (薄荷螢綠單片放大鏡與光學刻度)",
                "warm_highlight": "#FF5E8A (珊瑚粉減震密封矽膠圈與引線端子)",
                "quill_steel": "#5A5666 (消光淬火彈簧鋼棘針)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_hedgehog.png (品牌形象立牌)",
                        "web/media/hero/char_hedgehog.png (官網英雄展示立繪)",
                        "docs/art/ratchet_hedgehog_concept.png (概念立繪)",
                        "game/assets/sprites/player/hedgehog_idle.png (64x64 待機)",
                        "game/assets/sprites/player/hedgehog_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/hedgehog_idle.png (隊伍待機)",
                        "game/assets/sprites/player/hedgehog_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/hedgehog_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/hedgehog_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/hedgehog/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/hedgehog.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/ratchet_hedgehog.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/hedgehog/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_hedgehog.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/ratchet_hedgehog_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_hedgehog.png (400x840) [待產出]",
                "web_preview": "web/media/hero/hedgehog_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/hedgehog_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/hedgehog_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/hedgehog_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/hedgehog_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/hedgehog_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/hedgehog_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/hedgehog/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/hedgehog.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/ratchet_hedgehog.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/hedgehog/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 21 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十一大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    hedgehog_dir = "game/assets/sprites/player/paperdoll/hedgehog/"
    if hedgehog_dir not in races_dirs:
        races_dirs.append(hedgehog_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/hedgehog")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/hedgehog")
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
