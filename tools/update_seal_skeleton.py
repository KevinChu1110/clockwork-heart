#!/usr/bin/env python3
"""為第四十族拍浪海豹 (The Clapping Seal, seal) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/CLAPPING_SEAL_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 seal 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_seal_marine_titanium_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_seal_marine_titanium_default",
            "name": "拍浪海豹鍍鈦流線防蝕素體",
            "race": "seal",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_seal_streamline_cowl_sonar" for v in head_variants):
        head_variants.append({
            "id": "head_seal_streamline_cowl_sonar",
            "name": "沖壓流體減阻兜帽與同軸聲納立耳",
            "race": "seal",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_seal_marine_propeller_brass" for v in key_variants):
        key_variants.append({
            "id": "key_seal_marine_propeller_brass",
            "name": "雙葉水力螺旋槳黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_seal_deepsea_diver_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_seal_deepsea_diver_harness",
            "name": "深海武道防壓束帶與珊瑚浮標",
            "race": "seal",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_seal_cyan_quartz_convex_lens" for v in face_variants):
        face_variants.append({
            "id": "face_seal_cyan_quartz_convex_lens",
            "name": "深海琉璃石英凸透目鏡",
            "race": "seal",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_seal_clapper_gauntlets" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_seal_clapper_gauntlets",
            "name": "琉璃氣動拍浪拳套",
            "weapon_type": "fist",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_seal_hydro_ducted_tail_flukes" for v in curio_variants):
        curio_variants.append({
            "id": "curio_seal_hydro_ducted_tail_flukes",
            "name": "氣動導流雙葉金屬尾鰭",
            "race": "seal",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 40

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "seal" for r in races_list):
        races_list.append({
            "race_id": "seal",
            "aliases": [
                "clapping_seal",
                "wave_seal",
                "abyssal_seal",
                "pneumatic_seal"
            ],
            "name_zh": "拍浪海豹",
            "name_en": "The Clapping Seal",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
            "lore_anchor": "水下發條宮殿、藍晶石海淵平原、液態琉璃凝膠海、深淵排污豎井管道·耐壓吊籠、晨曦天軌5號深海浮標月台、海底防鏽超聲油壓艙、深海熱液湧泉管道與核心盟友「小黃鴨船長·舵手巴克」、「海馬信差·碧浪」並肩作戰；身軀覆蓋鍍鈦天藍（#38A0FF）高光防蝕板件與奶白（#FFFDF8）高溫瓷漆腹部、沖壓流體減阻兜帽＋圓形黃銅同軸聲納立耳、澄澈天藍深海防爆石英凸透目鏡、亮橘（#FFA010）深海武道防壓束帶、雙葉水力螺旋槳黃銅發條鑰匙與氣動導流雙葉金屬尾鰭，右手單持專屬琉璃氣動拍浪拳套，以圓潤流線水滴身姿化解洋流阻尼、雙掌高壓活塞衝壓拍浪與剛柔並濟推手破勢見長的深海宗師",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版圓潤海豹、流線水滴身姿與氣動導流雙葉尾鰭剪影)",
                "posture": "身軀呈沉穩流線低盤站姿，雙足鰭板與背後金屬尾鰭形成三點立體支撐，右手配戴琉璃氣動拍浪拳套橫架胸側蓄勢，左手自然虛握成推手守勢，背後雙葉螺旋槳黃銅發條鑰匙勻速旋轉，目鏡柔和律動",
                "standee_height_px": 840,
                "standee_width_px": 400
            },
            "mechanical_features": {
                "head_and_neck": "沖壓流體減阻兜帽緊湊包覆頭部，頂部設有散熱導流鰭片，吻部為沖壓黑金屬鼻頭帶三對固定銅絲鬍鬚",
                "ears": "圓形黃銅聲納立耳，內部嵌有游絲共鳴天線感應水流震盪",
                "torso_and_limbs": "通體覆蓋鍍鈦天藍馬口鐵板件與奶白高溫瓷漆腹部，四肢為高密閉防水球窩關節，末端為流線型金屬鰭板",
                "tail": "氣動導流雙葉金屬尾鰭，由兩片對稱弧形沖壓鎢鋼板件與中心減震筒構成，維持出拳與翻滾之動態平衡",
                "weapon_system": "右手單持專屬「琉璃氣動拍浪拳套（Crystal Pneumatic Clapper Gauntlets）」，20mm高抗衝擊海藍琉璃打擊面與雙活塞氣壓衝壓筒，完全符合 0-MKT7 與 monk/fist 體系，底層掛載 equipment.json 既有 wrap_gloves (tier 1) 與 iron_knuckle (tier 3)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (奶白高溫瓷漆，陽光童話奶油米白胸腹板件)",
                "secondary": "#FFA010 (多巴胺暖橘，深海武道防壓束帶、警示氣球標線)",
                "brass_gear": "#FFD028 (拋光金黃黃銅，雙葉水力螺旋槳發條鑰匙、同軸聲納立耳、海錨扣環)",
                "mint_green": "#4ED86A (清新薄荷綠，減壓氣動閥門指示燈、凝膠循環儀表刻線)",
                "core_cyan": "#38A0FF (澄澈天藍琉璃，深海防爆石英凸透目鏡、拳套打擊面、背脊鍍鈦板件)",
                "coral_pink": "#FF5E8A (珊瑚粉，後腰浮標小球、高彈性關節防水分離襯墊)",
                "tungsten_gray": "#3A3644 (冷鋼鎢深灰，氣動導流雙葉尾鰭、活塞連桿、金屬內部骨架)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_seal.png (品牌形象立牌)",
                        "web/media/hero/char_seal.png (官網英雄展示立繪)",
                        "docs/art/clapping_seal_concept.png (概念立繪)",
                        "game/assets/sprites/player/seal_idle.png (64x64 待機)",
                        "game/assets/sprites/player/seal_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/seal_idle.png (隊伍待機)",
                        "web/media/hero/seal_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/seal_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/seal_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/seal_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/seal_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/seal_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/seal_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/seal/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/seal.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/seal_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/clapping_seal.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/seal/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_seal.png (400x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/clapping_seal_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_seal.png (400x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/seal_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/seal_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/seal_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/seal_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/seal_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/seal_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/seal_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/seal/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/seal.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/clapping_seal.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/seal/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 40 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "四十大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    seal_dir = "game/assets/sprites/player/paperdoll/seal/"
    if seal_dir not in races_dirs:
        races_dirs.append(seal_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/seal")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/seal")
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
