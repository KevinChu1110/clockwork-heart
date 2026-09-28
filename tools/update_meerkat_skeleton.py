#!/usr/bin/env python3
"""為第三十六族沙哨狐獴 (The Sentry Meerkat, meerkat) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/SENTRY_MEERKAT_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 meerkat 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_meerkat_tinplate_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_meerkat_tinplate_default",
            "name": "沙哨狐獴沖壓馬口鐵金屬素體",
            "race": "meerkat",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_meerkat_scavenger_cowl_ears" for v in head_variants):
        head_variants.append({
            "id": "head_meerkat_scavenger_cowl_ears",
            "name": "拾荒風鏡金屬面甲與微型集音漏斗耳",
            "race": "meerkat",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_meerkat_high_torque_scrap_key" for v in key_variants):
        key_variants.append({
            "id": "key_meerkat_high_torque_scrap_key",
            "name": "荒漠生鏽高扭力發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_meerkat_patched_canvas_poncho" for v in costume_variants):
        costume_variants.append({
            "id": "costume_meerkat_patched_canvas_poncho",
            "name": "廢土補丁帆布防沙短斗篷",
            "race": "meerkat",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_meerkat_periscope_rangefinder_lens" for v in face_variants):
        face_variants.append({
            "id": "face_meerkat_periscope_rangefinder_lens",
            "name": "潛望式黃銅測距目鏡",
            "race": "meerkat",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_meerkat_rusted_coil_spring_gun" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_meerkat_rusted_coil_spring_gun",
            "name": "生鏽彈簧刺銃",
            "weapon_type": "gun",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_meerkat_tripod_grounding_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_meerkat_tripod_grounding_tail",
            "name": "鉸接多節生鏽金屬三腳平衡接地擺尾",
            "race": "meerkat",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 36

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "meerkat" for r in races_list):
        races_list.append({
            "race_id": "meerkat",
            "aliases": [
                "sentry_meerkat",
                "desert_meerkat",
                "rust_meerkat",
                "scavenger_meerkat"
            ],
            "name_zh": "沙哨狐獴",
            "name_en": "The Sentry Meerkat",
            "class_archetype": "遊俠 (Ranger)",
            "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
            "lore_anchor": "常年駐守於荒漠齒輪塚「巨型零件殘骸沙丘」與「拾荒拼裝聚落·齒輪營地」，巡弋於「舊庫重型吊裝龍門架」、「零件分揀斜坡裂谷」、「冷卻熔渣重力傾卸滑道·舊庫受料口」、「軌道廢棄排障滑道·舊庫分揀倉」、「大齒輪懸索天梯·舊庫總站」與「廢料沉降磁吸緩衝沙漏」，身軀由沖壓防鏽馬口鐵板件與黃銅鉚釘拼裝、配備拾荒風鏡金屬面甲與微型集音漏斗耳、潛望式黃銅測距目鏡、廢土補丁帆布防沙短斗篷、鉸接多節生鏽金屬三腳平衡接地擺尾與荒漠生鏽高扭力發條鑰匙，右手單持專屬生鏽彈簧刺銃，以高點哨兵狙擊、三腳接地抵消後座與瞬發破甲暴擊見長的廢土遊俠",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版直立哨兵、挺拔身姿與單筒潛望鏡剪影)",
                "posture": "身軀直立挺拔，身後鉸接金屬三腳平衡擺尾接地維持三點重心，左手自然置於腰際微調潛望鏡測距旋鈕，右手單持生鏽彈簧刺銃斜抱身前，頭頂潛望測距鏡隨走時轉動，微型集音耳輕微顫動，展現高度專注的哨兵待命姿態",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "拾荒風鏡金屬面甲與微型集音漏斗耳，右眼延伸出黃銅單筒潛望式測距目鏡（鑲嵌直徑 8px 晶透琥珀金 #FFB703 石英鏡片），左眼為光澤黃銅墊圈眼眸，轉動時發出細碎調焦棘爪齒輪聲",
                "ears": "頭部兩側微型黃銅漏斗薄片集音耳，內部裝有薄膜發條震動傳感片，隨風沙走時節奏同軸微幅自轉",
                "torso_and_limbs": "主軀幹由沖壓耐磨馬口鐵板件與黃銅鉚釘拼裝，面部與腹部覆蓋奶油米白（#FFFDF8）防鏽漆面與亮橘警示斜紋，雙腿為粗壯鐵皮腿柱配外露鉚釘棘輪軸承，腳底鑲嵌防滑深棕聚合物橡膠墊",
                "tail": "鉸接多節生鏽金屬三腳平衡接地擺尾，由5節沖壓金屬骨節組成，尾端配有活動式三腳折疊金屬爪，待機垂地平衡，射擊時爪片展開抓地吸收後座力",
                "weapon_system": "右手單持專屬「生鏽彈簧刺銃（Rusted Coil Spring-Gun）」，雙層高張力發條線圈槍機，前端固定折疊發條刺刀，完全符合 0-MKT7 與 ranger/gun 體系，底層掛載 equipment.json 既有 blackpowder_rifle 與 flint_gun"
            },
            "color_palette": {
                "primary": "#D49B4B (沙丘赭石褐，沖壓馬口鐵主外甲色)",
                "secondary": "#FFA010 (廢土多巴胺亮橘，斗篷拼布與警示斜紋)",
                "brass_gear": "#FFD028 (拋光黃銅鉚釘、發條鑰匙與潛望鏡身)",
                "tinplate_gray": "#514E59 (生鏽馬口鐵青灰，骨架、槍身與齒輪關節底色)",
                "cream_ivory": "#FFFDF8 (陽光奶油米白，面頰板、腹部護板溫暖底色)",
                "amber_optic": "#FFB703 (晶透琥珀金，潛望鏡片與測距光標焦點)",
                "verdigris_teal": "#2A9D8F (氧化銅綠彩，螺絲墊圈與斗篷點綴)",
                "outline": "#2E1F18 (深暖褐手繪外輪廓立體描邊，確保沙盤背景清晰立體)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_meerkat.png (品牌形象立牌)",
                        "web/media/hero/char_meerkat.png (官網英雄展示立繪)",
                        "docs/art/sentry_meerkat_concept.png (概念立繪)",
                        "game/assets/sprites/player/meerkat_idle.png (64x64 待機)",
                        "game/assets/sprites/player/meerkat_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/meerkat_idle.png (隊伍待機)",
                        "game/assets/sprites/player/meerkat_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/meerkat_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/meerkat_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/meerkat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/meerkat.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/sentry_meerkat.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/meerkat/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_meerkat.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/sentry_meerkat_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_meerkat.png (400x840) [待產出]",
                "web_preview": "web/media/hero/meerkat_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/meerkat_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/meerkat_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/meerkat_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/meerkat_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/meerkat_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/meerkat_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/meerkat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/meerkat.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/sentry_meerkat.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/meerkat/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 36 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十六大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    meerkat_dir = "game/assets/sprites/player/paperdoll/meerkat/"
    if meerkat_dir not in races_dirs:
        races_dirs.append(meerkat_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/meerkat")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/meerkat")
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
