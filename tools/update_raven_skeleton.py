#!/usr/bin/env python3
"""為第四十一族星儀渡鴉 (The Armillary Raven, raven) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/ARMILLARY_RAVEN_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 raven 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_raven_obsidian_brass_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_raven_obsidian_brass_default",
            "name": "星儀渡鴉黑曜白鐵防鏽馬口鐵素體",
            "race": "raven",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_raven_astronomer_hood_beak" for v in head_variants):
        head_variants.append({
            "id": "head_raven_astronomer_hood_beak",
            "name": "天文占星金屬風帽與黃銅機械喙",
            "race": "raven",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_raven_armillary_sphere_brass" for v in key_variants):
        key_variants.append({
            "id": "key_raven_armillary_sphere_brass",
            "name": "渾天雙環天球儀黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_raven_horologist_scholar_robe" for v in costume_variants):
        costume_variants.append({
            "id": "costume_raven_horologist_scholar_robe",
            "name": "鐘錶學者齒輪短披肩與星圖筒",
            "race": "raven",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_raven_astrolabe_monocle_lens" for v in face_variants):
        face_variants.append({
            "id": "face_raven_astrolabe_monocle_lens",
            "name": "單片多重游標石英目鏡與天藍星核",
            "race": "raven",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_raven_armillary_wand" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_raven_armillary_wand",
            "name": "渾天星儀發條短杖",
            "weapon_type": "magic",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_raven_articulated_steampunk_wings" for v in curio_variants):
        curio_variants.append({
            "id": "curio_raven_articulated_steampunk_wings",
            "name": "多節沖壓冷軋鎢鋼聯動機械羽翼",
            "race": "raven",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 41

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "raven" for r in races_list):
        races_list.append({
            "race_id": "raven",
            "aliases": [
                "armillary_raven",
                "astronomer_raven",
                "horologist_raven",
                "celestial_raven"
            ],
            "name_zh": "星儀渡鴉",
            "name_en": "The Armillary Raven",
            "class_archetype": "法師 (Mage)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "摩天齒輪工坊群、天文大鐘、高架重軌引橋·巨輪城站、晨曦天軌 4 號工業月台、自律工廠與天街吊橋、中央巨輪動力廣場、老鐘錶匠·星擺與總工技師·銅齒",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (俐落天頂觀測鳥偶、三同心天球儀與多節鎢鋼折扇羽翼剪影)",
                "posture": "身軀呈微偏頭輕微前傾之觀測立姿，金屬三趾雙爪穩健抓地，右手單持渾天星儀發條短杖斜立於側，左翼金屬羽爪微張護身導引氣流，背後渾天雙環發條鑰匙勻速自轉，右眼單片多重目鏡專注調焦",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "水滴流線形黑曜冷鋼金屬風帽緊湊包覆頭部，帽簷帶有游標測角刻度；前方銜接精密切削的雙瓣高碳黃銅機械喙，內置微型拉簧；頭頂立起一根纖細黃銅指向天線",
                "ears": "右眼古典黃銅支架多重放大觀測目鏡，三層石英鏡圈可獨立微調焦距；左眼澄澈天藍高透石英球目鏡，目光專注深邃",
                "torso_and_limbs": "通體覆蓋冷軋沖壓鍍黑曜冷鋼與陽光奶油米白雙色馬口鐵板件，胸前裝配弧形護心板與拋光黃銅壓條；雙足為三趾黃銅抓握爪，內置微型球窩關節與防滑減震矽膠墊",
                "tail": "多節沖壓冷軋鎢鋼聯動機械羽翼，由每翼7片重疊弧形鎢鋼片與微型四連桿機構鉸接而成，翼根帶彈簧阻尼筒，施法時如精密折扇流暢展開",
                "weapon_system": "右手單持專屬「渾天星儀發條短杖（Armillary Clockwork Wand）」，長度約45cm拋光黃銅桿身帶刻度，頂端三同心環旋轉天球儀懸浮天藍石英靈核，完全符合 0-MKT7 與 mage/magic 體系，底層掛載 equipment.json 既有 star_rod (tier 1) 與 void_quill (tier 5)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (陽光奶油米白烤漆馬口鐵，胸腹板件與內襯)",
                "secondary": "#FFA010 (多巴胺暖橘，加厚防油帆布學者短斗篷)",
                "brass_gear": "#FFD028 (拋光金黃黃銅，渾天雙環天球儀發條鑰匙、短杖刻度桿、六角齒輪領針)",
                "mint_green": "#4ED86A (清新薄荷綠，學者斗篷防磨滾邊、測繪筒刻度標線)",
                "core_cyan": "#38A0FF (澄澈天藍，高透石英目鏡球、短杖天球核心靈核)",
                "blush_coral": "#FF5E8A (珊瑚粉，微型關節減震阻尼膠墊、警示指示標記)",
                "tungsten_gray": "#3A3644 (冷鋼鍍黑曜鎢鋼深灰，聯動機械羽翼、金屬風帽、素體主外裝板件)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_raven.png (品牌形象立牌)",
                        "web/media/hero/char_raven.png (官網英雄展示立繪)",
                        "docs/art/armillary_raven_concept.png (概念立繪)",
                        "game/assets/sprites/player/raven_idle.png (64x64 待機)",
                        "game/assets/sprites/player/raven_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/raven_idle.png (隊伍待機)",
                        "web/media/hero/raven_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/raven_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/raven_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/raven_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/raven_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/raven_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/raven_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/raven/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/raven.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/raven_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/armillary_raven.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/raven/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_raven.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/armillary_raven_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_raven.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/raven_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/raven_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/raven_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/raven_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/raven_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/raven_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/raven_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/raven/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/raven.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/armillary_raven.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/raven/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 41 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "四十一重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    raven_dir = "game/assets/sprites/player/paperdoll/raven/"
    if raven_dir not in races_dirs:
        races_dirs.append(raven_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/raven")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/raven")
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
