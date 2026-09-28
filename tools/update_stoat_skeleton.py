#!/usr/bin/env python3
"""為第三十九族旋刃伶鼬 (The Whirling Stoat, stoat) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/WHIRLING_STOAT_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 stoat 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_stoat_ivory_tinplate_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_stoat_ivory_tinplate_default",
            "name": "旋刃伶鼬象牙白馬口鐵防砂素體",
            "race": "stoat",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_stoat_aerodynamic_hood_ears" for v in head_variants):
        head_variants.append({
            "id": "head_stoat_aerodynamic_hood_ears",
            "name": "沖壓防沙流線兜帽與雙聯黃銅拾音立耳",
            "race": "stoat",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_stoat_whirlwind_tri_ring_brass" for v in key_variants):
        key_variants.append({
            "id": "key_stoat_whirlwind_tri_ring_brass",
            "name": "三環旋風棘爪黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_stoat_scavenger_wind_cape" for v in costume_variants):
        costume_variants.append({
            "id": "costume_stoat_scavenger_wind_cape",
            "name": "廢土拾荒輕量防風斗篷與工具束帶",
            "race": "stoat",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_stoat_sapphire_crosshair_lens" for v in face_variants):
        face_variants.append({
            "id": "face_stoat_sapphire_crosshair_lens",
            "name": "天青藍高頻動態追蹤目鏡",
            "race": "stoat",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_stoat_crescent_dagger" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_stoat_crescent_dagger",
            "name": "廢土旋刃弧光短匕",
            "weapon_type": "dagger",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_stoat_flexible_segmented_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_stoat_flexible_segmented_tail",
            "name": "多節同軸彈簧平衡鎢鋼黑尖尾",
            "race": "stoat",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 39

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "stoat" for r in races_list):
        races_list.append({
            "race_id": "stoat",
            "aliases": [
                "whirling_stoat",
                "scavenger_stoat",
                "conduit_stoat",
                "sandstorm_stoat"
            ],
            "name_zh": "旋刃伶鼬",
            "name_en": "The Whirling Stoat",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
            "lore_anchor": "零件分揀斜坡裂谷、軌道廢棄排障滑道·舊庫分揀倉、巨型零件殘骸沙丘、舊庫重型吊裝龍門架、拾荒拼裝聚落·齒輪營地、冷卻熔渣重力傾卸滑道·舊庫受料口、大齒輪懸索天梯·舊庫總站與核心工藝師搭檔「拾荒拼裝大師補丁爺爺」並肩作戰；身軀覆蓋象牙白（#FFFDF8）鍍錫馬口鐵防砂烤漆板件與金黃黃銅接縫、沖壓防沙流線金屬兜帽＋半圓黃銅拾音立耳、天青藍高透石英晶核動態追蹤目鏡、廢土拾荒輕量防風斗篷、三環旋風棘爪黃銅發條鑰匙與7節同軸彈簧平衡鎢鋼黑尖尾，右手單持專屬廢土旋刃弧光短匕，以多節彈簧脊椎穿梭狹管、旋風迴旋斬破開死角與極速機動見長的廢土刺客",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版發條伶鼬、修長圓柱流線身姿與同軸平衡黑尖尾剪影)",
                "posture": "身軀呈敏銳前傾低盤拱背姿態，四肢為微型高彈簧球窩外露關節與矽膠防滑金屬爪掌，右手反手單持廢土旋刃弧光短匕護於側身蓄勢，左手自然虛握微張平衡重心，身後多節同軸彈簧尾靈敏晃動微調陀螺重心，背部三環旋風黃銅發條鑰匙高速旋轉，展現極速敏捷的管道穿梭刺客姿態",
                "standee_height_px": 840,
                "standee_width_px": 400
            },
            "mechanical_features": {
                "head_and_neck": "沖壓防沙流線金屬兜帽＋半圓黃銅拾音立耳，帽沿兩側帶有加固微型六角螺帽，雙耳內部嵌有微型螺旋彈簧避震器自適應旋轉角度",
                "ears": "半圓形沖壓薄黃銅拾音膜片，內嵌微型螺旋彈簧避震器，靈敏捕捉齒輪打滑與敵人腳步聲",
                "torso_and_limbs": "通體覆蓋象牙白（#FFFDF8）鍍錫防砂烤漆板件與金黃黃銅接縫，胸腹為一體成型抗壓白鐵皮，四肢為微型高彈簧球窩關節，末端為覆蓋耐磨防滑高彈性工程矽膠軟墊的金屬爪掌",
                "tail": "由 7 節拋光白鐵皮中空圓環套接而成的同軸彈簧平衡尾，末梢配重塊為一枚淬火黑曜鎢鋼實心錐（#3A3644），高速揮斬與滑行時作為動態陀螺儀維持平衡",
                "weapon_system": "右手單持專屬「廢土旋刃弧光短匕（Scrap Whirling Crescent Dagger）」，弧月形高碳發條鋼刃身與鍍黃銅防滑握柄，完全符合 0-MKT7 與 ninja/dagger 體系，底層掛載 equipment.json 既有 nebula_needle (tier 3) 與 star_fang (tier 2)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (象牙白金，陽光童話奶油米白鍍錫馬口鐵防砂身軀板件)",
                "secondary": "#FFA010 (多巴胺暖橘，防風斗篷外層、目鏡金屬框線、安全警示紋)",
                "brass_gear": "#FFD028 (拋光金黃黃銅，三環旋風發條鑰匙、拾音立耳外框、短匕柄飾)",
                "mint_green": "#4ED86A (清新薄荷綠，斗篷工具扣環、機芯潤滑液指示燈、面頰微光片)",
                "sapphire_optic": "#38A0FF (高透天藍石英，動態追蹤目鏡晶核、短匕能量刻線、排氣噴嘴)",
                "coral_pink": "#FF5E8A (珊瑚粉，面部圓形金屬腮紅、關節減震密封矽膠襯墊)",
                "tungsten_gray": "#3A3644 (冷鋼鎢深灰，黑尖尾平衡配重錐、短匕高碳鋒刃、骨架)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_stoat.png (品牌形象立牌)",
                        "web/media/hero/char_stoat.png (官網英雄展示立繪)",
                        "docs/art/whirling_stoat_concept.png (概念立繪)",
                        "game/assets/sprites/player/stoat_idle.png (64x64 待機)",
                        "game/assets/sprites/player/stoat_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/stoat_idle.png (隊伍待機)",
                        "web/media/hero/stoat_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/stoat_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/stoat_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/stoat_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/stoat_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/stoat_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/stoat_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/stoat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/stoat.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/stoat_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/whirling_stoat.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/stoat/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_stoat.png (400x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/whirling_stoat_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_stoat.png (400x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/stoat_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/stoat_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/stoat_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/stoat_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/stoat_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/stoat_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/stoat_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/stoat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/stoat.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/whirling_stoat.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/stoat/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 39 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "三十九大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    stoat_dir = "game/assets/sprites/player/paperdoll/stoat/"
    if stoat_dir not in races_dirs:
        races_dirs.append(stoat_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/stoat")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/stoat")
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
