#!/usr/bin/env python3
"""為第三十族幻彩變色龍 (chameleon) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/MIRAGE_CHAMELEON_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 chameleon 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_chameleon_mirage_titanium_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_chameleon_mirage_titanium_default",
            "name": "幻彩鍍鈦變色合金素體",
            "race": "chameleon",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_chameleon_crested_visor_cowl" for v in head_variants):
        head_variants.append({
            "id": "head_chameleon_crested_visor_cowl",
            "name": "高聳頭冠棱鏡風鏡面罩",
            "race": "chameleon",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_chameleon_prismatic_trivane" for v in key_variants):
        key_variants.append({
            "id": "key_chameleon_prismatic_trivane",
            "name": "三稜透鏡發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_chameleon_wasteland_scout_rig" for v in costume_variants):
        costume_variants.append({
            "id": "costume_chameleon_wasteland_scout_rig",
            "name": "荒原斥候防沙迷彩背心裝甲",
            "race": "chameleon",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_chameleon_turret_rangefinder_lens" for v in face_variants):
        face_variants.append({
            "id": "face_chameleon_turret_rangefinder_lens",
            "name": "雙向砲塔測距雙目光學透鏡",
            "race": "chameleon",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_chameleon_mirage_compound_bow" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_chameleon_mirage_compound_bow",
            "name": "幻彩棱鏡複合機關弓",
            "weapon_type": "bow",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_chameleon_spiral_torsion_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_chameleon_spiral_torsion_tail",
            "name": "多節同軸發條扭簧平衡卷尾",
            "race": "chameleon",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 30

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "chameleon" for r in races_list):
        races_list.append({
            "race_id": "chameleon",
            "aliases": [
                "mirage_chameleon",
                "prismatic_chameleon",
                "scout_chameleon",
                "wasteland_chameleon"
            ],
            "name_zh": "幻彩變色龍",
            "name_en": "The Mirage Chameleon",
            "class_archetype": "遊俠 (Ranger)",
            "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
            "lore_anchor": "底層荒漠齒輪塚中傳奇的拾荒哨戒長，常駐於巨型零件殘骸沙丘、拾荒拼裝齒輪營地、舊庫重型吊裝龍門架、零件分揀斜坡裂谷、冷卻熔渣重力傾卸滑道與大齒輪懸索天梯，通體由象牙白多層光學干涉薄膜鍍鈦板件、高聳頭冠棱鏡風鏡面罩、雙向360度獨立自轉砲塔測距石英目鏡、三稜透鏡發條鑰匙與五節同軸發條扭簧平衡卷尾組裝而成，左手單持幻彩棱鏡複合機關弓，以光學迷彩伏擊、弱點立體測距與超視距精準狙擊見長",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版爬蟲哨兵偶、呆萌反差剪影)",
                "posture": "雙足二三對握夾具爪抓地穩健，身軀微前傾，左手持握幻彩棱鏡複合弓垂於身側，身後同軸扭簧卷尾自然蜷曲，雙向砲塔目鏡獨立旋轉警戒四周",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓成型鍍鈦合金頭殼配三角散熱導流冠，表面帶有暖橘與金黃防擦撞條紋，額頭整合耐磨石英風鏡，兩側嵌有黃銅齒圈環繞的雙向360度獨立自轉砲塔測距目鏡（#FFD028 / #FFA010）",
                "ears": "頭冠兩側微型氣動導流腮孔與內部黃銅微型耳軸，感應荒原風沙擾動與秒針跳格震動",
                "torso_and_limbs": "主軀幹覆蓋象牙白抗磨鍍鈦板件（#FFFDF8）與多層光學干涉薄膜板件，四肢關節為金屬球窩鉸鏈配珊瑚粉防塵矽膠圈，手足為二三對握沖壓金屬機械夾具爪附防滑矽膠墊",
                "tail": "由五節沖壓黃銅關節環與同軸高扭力扁鋼發條游絲盤卷而成的平衡卷尾，可靈活擺動或蜷曲，瞄準時下壓地面抵消後座力",
                "weapon_system": "左手單持專屬「幻彩棱鏡複合機關弓（Mirage Prismatic Compound Bow）」，弓身為雙層鍍鈦彈簧鋼片與偏心滑輪，弓身中段嵌有三色折射棱鏡，完全符合 0-MKT7 與 ranger/bow 體系，底層掛載 equipment.json 既有 reed_bow 與 hawk_longbow"
            },
            "color_palette": {
                "primary": "#FFFDF8 (象牙白主軀幹鍍鈦板件與陶瓷護胸)",
                "secondary": "#FFA010 (暖橘警示背心外緣與頭冠導流條紋)",
                "accent": "#FFD028 (琥珀金雙向砲塔石英目鏡與三稜鑰匙主軸)",
                "camo_mint": "#4ED86A (薄荷翡翠光學干涉薄膜基色與背心滾邊)",
                "sky_cyan": "#38A0FF (晴空天藍光學薄膜折射高光與滑輪軸承)",
                "coral_pink": "#FF5E8A (珊瑚粉紅關節防護矽膠墊圈與指示燈)",
                "frame": "#D49B4B (廢土鍍鈦傳動齒輪、機械夾具爪與偏心滑輪)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_chameleon.png (品牌形象立牌)",
                        "web/media/hero/char_chameleon.png (官網英雄展示立繪)",
                        "docs/art/mirage_chameleon_concept.png (概念立繪)",
                        "game/assets/sprites/player/chameleon_idle.png (64x64 待機)",
                        "game/assets/sprites/player/chameleon_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/chameleon_idle.png (隊伍待機)",
                        "game/assets/sprites/player/chameleon_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/chameleon_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/chameleon_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/chameleon/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/chameleon.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/mirage_chameleon.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/chameleon/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_chameleon.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/mirage_chameleon_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_chameleon.png (400x840) [待產出]",
                "web_preview": "web/media/hero/chameleon_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/chameleon_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/chameleon_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/chameleon_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/chameleon_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/chameleon_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/chameleon_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/chameleon/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/chameleon.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/mirage_chameleon.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/chameleon/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 30 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    chameleon_dir = "game/assets/sprites/player/paperdoll/chameleon/"
    if chameleon_dir not in races_dirs:
        races_dirs.append(chameleon_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/chameleon")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/chameleon")
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
