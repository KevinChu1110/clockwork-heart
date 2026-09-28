#!/usr/bin/env python3
"""為第三十七族鐵蹄駿駒 (The Ironhoof Courser, courser) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/IRONHOOF_COURSER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 courser 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_courser_cream_gold_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_courser_cream_gold_default",
            "name": "鐵蹄駿駒奶油金黃合金素體",
            "race": "courser",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_courser_brass_chanfron_mane" for v in head_variants):
        head_variants.append({
            "id": "head_courser_brass_chanfron_mane",
            "name": "巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲",
            "race": "courser",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_courser_baroque_trefoil_gold" for v in key_variants):
        key_variants.append({
            "id": "key_courser_baroque_trefoil_gold",
            "name": "巴洛克雙聯三葉草金飾發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_courser_dawn_patrol_cuirass" for v in costume_variants):
        costume_variants.append({
            "id": "costume_courser_dawn_patrol_cuirass",
            "name": "晨曦巡防騎士拋光輕胸甲",
            "race": "courser",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_courser_sapphire_optic_lens" for v in face_variants):
        face_variants.append({
            "id": "face_courser_sapphire_optic_lens",
            "name": "天藍石英同心圓光學目鏡",
            "race": "courser",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_courser_cavalry_saber" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_courser_cavalry_saber",
            "name": "晨曦齒輪騎兵劍",
            "weapon_type": "sword",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_courser_articulated_spring_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_courser_articulated_spring_tail",
            "name": "鉸接多節彈簧金屬流線甩尾",
            "race": "courser",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 37

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "courser" for r in races_list):
        races_list.append({
            "race_id": "courser",
            "aliases": [
                "ironhoof_courser",
                "cavalry_courser",
                "dawn_courser",
                "patrol_courser"
            ],
            "name_zh": "鐵蹄駿駒",
            "name_en": "The Ironhoof Courser",
            "class_archetype": "騎士 (Knight)",
            "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
            "lore_anchor": "駐守於晨曦小鎮「懸吊齒輪鐘樓」與「石板街道集市」，巡防「齒輪吊索大橋·小鎮站」、「晨曦天軌 2 號月台」、「蔓谷天梯引道」、「巨輪城重型空軌貨運棧橋」與「邊界安全防護彈簧網」，身軀覆蓋奶油米白琺瑯板件與金黃黃銅接縫、巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲、天藍石英同心圓光學目鏡、晨曦巡防騎士拋光輕胸甲、鉸接多節彈簧金屬流線甩尾與巴洛克雙聯三葉草金飾發條鑰匙，右手單持專屬晨曦齒輪騎兵劍，以金屬馬蹄踏過石板街面、高機動巡防步法與優雅拔刀斬擊見長的正義騎士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版發條戰馬、圓潤挺拔身姿與波浪鬃甲剪影)",
                "posture": "身軀圓潤挺拔，四肢為大直徑球窩外露關節與鎢鋼耐磨馬蹄鐵，右手單持晨曦齒輪騎兵劍斜向下警戒，左手自然微曲握持鞍轡飾帶把手維持平衡，背部巴洛克三葉草鑰匙隨時軸輕轉，展現優雅沈穩的巡防騎士姿態",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "巴洛克沖壓黃銅護面額甲＋七聯波浪齒輪片鬃甲＋直立金屬菱形立耳，額甲正中鑲嵌微型三葉草浮雕，隨走時節奏產生微幅波浪狀齒輪聯動",
                "ears": "頭頂金屬菱形立耳，內嵌高靈敏度發條拾音振膜，耳尖帶有鍍金防磨倒角",
                "torso_and_limbs": "通體覆蓋拋光奶油米白（#FFFDF8）琺瑯板件與金黃黃銅接縫，四肢為大直徑球窩外露關節，末端為鎢鋼耐磨馬蹄鐵，踏地清脆紮實",
                "tail": "五節沖壓黃銅圓錐套筒與內置不鏽鋼扭簧組裝的金屬流線甩尾，末端掛載鏤空齒輪鈴鐺，待機隨節奏柔性擺動",
                "weapon_system": "右手單持專屬「晨曦齒輪騎兵劍（Dawn Clockwork Cavalry Saber）」，弧形彈簧鋼劍刃，黃銅齒輪護手盤，完全符合 0-MKT7 與 knight/sword 體系，底層掛載 equipment.json 既有 dawn_blade 與 knight_saber"
            },
            "color_palette": {
                "primary": "#FFFDF8 (陽光奶油米白，琺瑯合金主外甲色)",
                "secondary": "#FFA010 (多巴胺暖橘，護甲滾邊與飾帶底色)",
                "brass_gear": "#FFD028 (巴洛克鍍金黃銅，齒輪鬃甲、發條鑰匙與護手盤)",
                "mint_green": "#4ED86A (清新薄荷綠，胸前琺瑯徽章與鞍轡點綴)",
                "sapphire_optic": "#38A0FF (湛藍石英光學鏡片與聚焦光標)",
                "coral_pink": "#FF5E8A (珊瑚粉，軸承減震襯墊與慶典細節)",
                "tungsten_gray": "#3A3644 (鎢鋼深灰，耐磨馬蹄鐵與骨架關節底色)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_courser.png (品牌形象立牌)",
                        "web/media/hero/char_courser.png (官網英雄展示立繪)",
                        "docs/art/ironhoof_courser_concept.png (概念立繪)",
                        "game/assets/sprites/player/courser_idle.png (64x64 待機)",
                        "game/assets/sprites/player/courser_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/courser_idle.png (隊伍待機)",
                        "game/assets/sprites/player/courser_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/courser_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/courser_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/courser/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/courser.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/ironhoof_courser.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/courser/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_courser.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/ironhoof_courser_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_courser.png (400x840) [待產出]",
                "web_preview": "web/media/hero/courser_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/courser_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/courser_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/courser_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/courser_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/courser_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/courser_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/courser/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/courser.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/ironhoof_courser.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/courser/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 37 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "三十七大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    courser_dir = "game/assets/sprites/player/paperdoll/courser/"
    if courser_dir not in races_dirs:
        races_dirs.append(courser_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/courser")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/courser")
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
