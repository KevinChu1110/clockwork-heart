#!/usr/bin/env python3
"""為第四十五族巡管守宮 (The Conduit Gecko, gecko) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/CONDUIT_GECKO_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 gecko 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_gecko_brass_patina_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_gecko_brass_patina_default",
            "name": "冷軋黃銅微弧吸盤素體",
            "race": "gecko",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_gecko_conduit_scout_crest_cowl" for v in head_variants):
        head_variants.append({
            "id": "head_gecko_conduit_scout_crest_cowl",
            "name": "管網巡檢防刮護額",
            "race": "gecko",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_gecko_dual_ring_relief_valve_brass" for v in key_variants):
        key_variants.append({
            "id": "key_gecko_dual_ring_relief_valve_brass",
            "name": "雙環洩壓黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_gecko_highpressure_stealth_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_gecko_highpressure_stealth_harness",
            "name": "耐熱工裝暗忍胸甲與防刮短裙甲",
            "race": "gecko",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_gecko_dual_slit_aperture_quartz_lens" for v in face_variants):
        face_variants.append({
            "id": "face_gecko_dual_slit_aperture_quartz_lens",
            "name": "雙目裂隙光圈石英目鏡",
            "race": "gecko",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_gecko_conduit_ratchet_dart" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_gecko_conduit_ratchet_dart",
            "name": "黃銅棘輪多角機關鏢",
            "weapon_type": "dart",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_gecko_segmented_gear_balance_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_gecko_segmented_gear_balance_tail",
            "name": "微型同軸多節齒輪平衡尾",
            "race": "gecko",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_list = races_spec["races"]

    if not any(r.get("race_id") == "gecko" for r in races_list):
        races_list.append({
            "race_id": "gecko",
            "aliases": [
                "conduit_gecko",
                "clockwork_gecko",
                "brass_gecko",
                "wallrunner_gecko"
            ],
            "name_zh": "巡管守宮",
            "name_en": "The Conduit Gecko",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "穿梭於黃銅都市·巨輪城「摩天齒輪工坊群」與「高壓蒸氣管道網」，巡防「自律工廠與天街吊橋」、「鎢絲防爆街燈」、「高架重軌引橋·巨輪城站」、「晨曦天軌 4 號工業月台」、「深淵排污豎井管道·海淵入口」、「高溫導熱重軌引橋」與「磁吸緩衝防墜鋼網」，並駐守「中央蒸氣沐浴池」，配合鐵皮發條工程師、總工技師·銅齒與管道巡檢員·小鎢；通體覆蓋冷軋高延展性薄黃銅板件與薄荷綠銅抗氧化琺瑯烤漆、管網巡檢防刮護額、雙環洩壓黃銅發條鑰匙、耐熱工裝暗忍胸甲與防刮短裙甲、雙目裂隙光圈石英目鏡、微型同軸多節齒輪平衡尾，右手單持專屬黃銅棘輪多角機關鏢，以微型真空間歇吸盤壁面飛馳、急促超頻高壓洩壓節奏精準折射暗殺見長的高空管道巡檢特工暗忍",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (古典發條鐵皮爬行壁虎、扁平流線護盔與多節同軸齒輪尾剪影)",
                "posture": "身軀呈低重心貼地靈動站姿，四肢微屈，四足吸盤緊抓地面，右手單持黃銅機關鏢橫握於胸前，左手吸盤金屬爪微張維持壁面平衡，背後雙環洩壓鑰匙勻速自轉，大圓雙裂隙石英目鏡專注警戒",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "一體沖壓弧面流線薄黃銅護盔與扁平吻部，前額延伸防刮金屬頂罩與微型導風排氣槽，嘴角帶有珊瑚粉微型洩壓孔",
                "ears": "扁平護盔兩側嵌入微型導風排屑槽，兼具聲波共鳴定位功能",
                "torso_and_limbs": "高延展性冷軋薄黃銅板覆薄荷綠銅抗氧化琺瑯漆（#4ED86A），腹部百葉沖壓散熱槽外露十字螺栓；四肢五指端部配備微型真空間歇吸盤金屬爪",
                "tail": "六節同軸鉸接黃銅空心弧形關節平衡尾，內穿高張力琴鋼絲繩，末端焊接微型磁吸防墜小抓鉤，隨重心波浪律動",
                "weapon_system": "右手單持專屬「黃銅棘輪多角機關鏢（Brass Ratchet Polygon Conduit Shuriken）」，四角冷軋薄鋼迴旋刃嵌裝滾珠軸承黃銅棘輪，完全符合 0-MKT7 與 ninja/dart 體系，底層掛載 equipment.json 既有 mist_darts (tier 1) 與 shadow_chakram (tier 3)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (基底象牙奶油白，腹部散熱百葉槽與面部吻部底色)",
                "secondary": "#4ED86A (主色薄荷綠銅琺瑯，頭盔頂蓋、背部主護甲與齒輪尾外殼)",
                "brass_gear": "#FFA010 (裝飾暖金黃銅，胸甲背帶金屬卡扣、四肢吸盤關節與機關鏢刃高光倒角)",
                "mint_green": "#4ED86A (薄荷綠銅抗氧化琺瑯烤漆)",
                "core_cyan": "#38A0FF (功能天藍，石英目鏡內部游標刻度線與胸口發條壓力表微光)",
                "blush_coral": "#FF5E8A (腮紅珊瑚粉，嘴角兩側微翹處微型洩壓小圓孔)",
                "accent_gold": "#FFD028 (多巴胺金黃，大圓石英目鏡、手腕棘輪飾環與背後發條鑰匙外柄)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_gecko.png (品牌形象立牌)",
                        "web/media/hero/char_gecko.png (官網英雄展示立繪)",
                        "docs/art/conduit_gecko_concept.png (概念立繪)",
                        "game/assets/sprites/player/gecko_idle.png (64x64 待機)",
                        "game/assets/sprites/player/gecko_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/gecko_idle.png (隊伍待機)",
                        "web/media/hero/gecko_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/gecko_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/gecko_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/gecko_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/gecko_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/gecko_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/gecko_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/gecko/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/gecko.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/gecko_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/conduit_gecko.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/gecko/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_gecko.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/conduit_gecko_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_gecko.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/gecko_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/gecko_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/gecko_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/gecko_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/gecko_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/gecko_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/gecko_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/gecko/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/gecko.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/conduit_gecko.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/gecko/{slot_id}/{item_id}.png [待產出]"
            }
        })

    races_spec["total_races"] = len(races_list)

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "四十四重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲、巡管守宮靈敏扁平爬壁體態與耐熱暗忍胸甲) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    gecko_dir = "game/assets/sprites/player/paperdoll/gecko/"
    if gecko_dir not in races_dirs:
        races_dirs.append(gecko_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/gecko")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/gecko")
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
