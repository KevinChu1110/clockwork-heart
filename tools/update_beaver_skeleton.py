#!/usr/bin/env python3
"""為第三十八族劈木河狸 (The Woodchopper Beaver, beaver) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/WOODCHOPPER_BEAVER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 beaver 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_beaver_brass_timber_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_beaver_brass_timber_default",
            "name": "劈木河狸墨綠耐磨漆與黃銅沖壓合金素體",
            "race": "beaver",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_beaver_chisel_teeth_lumber_cap" for v in head_variants):
        head_variants.append({
            "id": "head_beaver_chisel_teeth_lumber_cap",
            "name": "沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽",
            "race": "beaver",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_beaver_sawtooth_cog_brass" for v in key_variants):
        key_variants.append({
            "id": "key_beaver_sawtooth_cog_brass",
            "name": "鋸齒環輪雙孔黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_beaver_deepwood_sapper_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_beaver_deepwood_sapper_harness",
            "name": "深林開拓工兵抗磨胸甲與工具背帶",
            "race": "beaver",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_beaver_amber_surveyor_lens" for v in face_variants):
        face_variants.append({
            "id": "face_beaver_amber_surveyor_lens",
            "name": "琥珀金同心圓測量目鏡",
            "race": "beaver",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_beaver_log_greataxe" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_beaver_log_greataxe",
            "name": "深林拓荒劈木巨斧",
            "weapon_type": "axe",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_beaver_perforated_paddle_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_beaver_perforated_paddle_tail",
            "name": "沖壓穿孔重型黃銅壓板扁尾",
            "race": "beaver",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 38

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "beaver" for r in races_list):
        races_list.append({
            "race_id": "beaver",
            "aliases": [
                "woodchopper_beaver",
                "sapper_beaver",
                "timber_beaver",
                "lumber_beaver"
            ],
            "name_zh": "劈木河狸",
            "name_en": "The Woodchopper Beaver",
            "class_archetype": "戰士 (Viking)",
            "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
            "lore_anchor": "駐守於翡翠深林「巨木樹屋聚落」與「樹汁導流泵」，巡防「機械巨木」、「觀風石碑塔」、「蔓谷天梯引道」、「高架重軌引橋」與「發條藤蔓彈射平台」，並與核心工藝師搭檔「老鹿木匠角木」並肩作戰；身軀覆蓋深森墨綠耐磨漆沖壓板件與金黃黃銅接縫、沖壓雙聯黃銅鑿齒護下頜、拓荒伐木工硬帽、琥珀金同心圓測量目鏡、深林開拓工兵抗磨胸甲、鋸齒環輪雙孔黃銅發條鑰匙與沖壓穿孔重型黃銅壓板扁尾，右手單持專屬深林拓荒劈木巨斧，以重尾拍地三腳架定點、停拍窗口開山裂木與勢大力沉破障見長的重裝拓荒戰士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版發條河狸、圓滾水桶腰敦實身姿與寬扁尾剪影)",
                "posture": "身軀圓潤敦實低盤蹲伏，四肢為大直徑球窩外露關節與耐磨防滑平整腳掌，右手單持深林拓荒劈木巨斧斜向後側蓄勢，左手自然微曲護於胸前平衡重心，身後沖壓穿孔黃銅扁尾斜貼地面形成穩定三點支撐，背部鋸齒環輪發條鑰匙隨時軸平穩旋轉，展現沉穩厚重的工兵戰士姿態",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓雙聯黃銅鑿齒護下頜＋墨綠琺瑯圓頂伐木工硬帽＋圓角短金屬耳，帽沿兩側帶有加固固定鉚釘，雙鑿齒表面帶有 45 度排屑刃口與微幅上下咬合聯動",
                "ears": "頭頂圓角金屬短耳，內嵌高靈敏度金屬拾音振膜與鍍金防磨倒角",
                "torso_and_limbs": "通體覆蓋深森墨綠（#4A7C59）冷軋耐磨漆板件與金黃黃銅接縫，四肢為大直徑球窩外露關節，末端為覆蓋耐磨波紋橡膠墊的平整金屬腳掌，抓地力極限穩固",
                "tail": "厚度 2.5mm 沖壓黃銅壓板與 18 處微型六角蜂巢減重孔組裝而成的重型扁尾，根部雙扭簧阻尼鉸鏈與尾椎相連，底部鑲嵌防滑橡膠墊，拍地定點提供三點支撐",
                "weapon_system": "右手單持專屬「深林拓荒劈木巨斧（Deepwood Log-Splitting Greataxe）」，加厚雙面月牙弧形刃與黃銅配重背槌，完全符合 0-MKT7 與 viking/axe 體系，底層掛載 equipment.json 既有 split_greataxe (tier 3) 與 notch_axe (tier 1)"
            },
            "color_palette": {
                "primary": "#4A7C59 (深森墨綠，耐磨冷軋板件主外甲色)",
                "secondary": "#FFA010 (多巴胺暖橘，防護腰帶與背帶滾邊底色)",
                "brass_gear": "#FFD028 (拋光金黃黃銅，雙聯鑿齒、鋸齒發條鑰匙、穿孔扁尾外框與斧刃)",
                "mint_green": "#4ED86A (清新薄荷綠，樹脂指示燈與胸前工具扣環)",
                "sapphire_optic": "#38A0FF (湛藍石英光學鏡片與斧脊冷卻管線)",
                "coral_pink": "#FF5E8A (珊瑚粉，面部圓形腮紅片與關節減震套)",
                "tungsten_gray": "#3A3644 (冷鋼鎢深灰，斧刃開鋒面、尾板鉸鏈與球窩關節底色)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_beaver.png (品牌形象立牌)",
                        "web/media/hero/char_beaver.png (官網英雄展示立繪)",
                        "docs/art/woodchopper_beaver_concept.png (概念立繪)",
                        "game/assets/sprites/player/beaver_idle.png (64x64 待機)",
                        "game/assets/sprites/player/beaver_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/beaver_idle.png (隊伍待機)",
                        "game/assets/sprites/player/beaver_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/beaver_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/beaver_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/beaver/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/beaver.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/woodchopper_beaver.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/beaver/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_beaver.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/woodchopper_beaver_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_beaver.png (400x840) [待產出]",
                "web_preview": "web/media/hero/beaver_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/beaver_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/beaver_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/beaver_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/beaver_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/beaver_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/beaver_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/beaver/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/beaver.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/woodchopper_beaver.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/beaver/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 38 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "三十八大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    beaver_dir = "game/assets/sprites/player/paperdoll/beaver/"
    if beaver_dir not in races_dirs:
        races_dirs.append(beaver_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/beaver")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/beaver")
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
