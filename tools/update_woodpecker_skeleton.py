#!/usr/bin/env python3
"""為第四十八族振律啄木鳥 (The Resonance Woodpecker, woodpecker) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/RESONANCE_WOODPECKER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 woodpecker 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_woodpecker_tinplate_brass_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_woodpecker_tinplate_brass_default",
            "name": "鍍鎳鐵皮黃銅高剛性素體底盤",
            "race": "woodpecker",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_woodpecker_scarlet_crest_cowl" for v in head_variants):
        head_variants.append({
            "id": "head_woodpecker_scarlet_crest_cowl",
            "name": "振律多巴胺亮紅散熱冠羽頭盔",
            "race": "woodpecker",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_woodpecker_high_frequency_percussion_key" for v in key_variants):
        key_variants.append({
            "id": "key_woodpecker_high_frequency_percussion_key",
            "name": "雙葉調速高頻音叉發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_woodpecker_skyspire_inspector_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_woodpecker_skyspire_inspector_harness",
            "name": "摩天工坊高空巡檢鉚接工裝",
            "race": "woodpecker",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_woodpecker_precision_gauge_monocle" for v in face_variants):
        face_variants.append({
            "id": "face_woodpecker_precision_gauge_monocle",
            "name": "同軸同心圓測振壓力目鏡",
            "race": "woodpecker",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_woodpecker_resonance_pneumatic_heavy_gun" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_woodpecker_resonance_pneumatic_heavy_gun",
            "name": "振律重型氣動火銃",
            "weapon_type": "gun",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_woodpecker_riveted_tinplate_prop_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_woodpecker_riveted_tinplate_prop_tail",
            "name": "鋼板沖壓三角抗震支撐尾板",
            "race": "woodpecker",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_list = races_spec["races"]

    if not any(r.get("race_id") == "woodpecker" for r in races_list):
        races_list.append({
            "race_id": "woodpecker",
            "aliases": [
                "resonance_woodpecker",
                "percussion_woodpecker",
                "clockwork_woodpecker",
                "brass_woodpecker"
            ],
            "name_zh": "振律啄木鳥",
            "name_en": "The Resonance Woodpecker",
            "class_archetype": "遊俠 (Ranger)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "穿行於黃銅都市·巨輪城「摩天齒輪工坊群」與「自律工廠與天街吊橋」，巡檢「高壓蒸氣管道網」、「鎢絲防爆街燈」與「高架重軌引橋·巨輪城站」，駐守「中央動力廣場」，配合總工技師·銅齒、管道巡檢員·小鎢與鋼岳巨象、幽影夜貓、鐵拳袋鼠、鋼臂巨猩、星儀渡鴉與巡管守宮；通體覆蓋沖壓薄鋼板鍍鎳防鏽板件與高剛性冷軋鎢鋼骨架、振律多巴胺亮紅散熱冠羽頭盔、雙葉調速高頻音叉發條鑰匙、摩天工坊高空巡檢鉚接工裝、同軸同心圓測振壓力目鏡、鋼板沖壓三角抗震支撐尾板，右手單持專屬振律重型氣動火銃，以X型雙前雙後對趾磁吸機械爪扣合鋼樑、三角尾板接地抗震鎖死、音頻諧振穿甲高頻點射、超遠距致命狙擊見長的巨輪城摩天工坊高空巡檢火槍遊俠",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (古典鐵皮發條啄木鳥敲擊玩具、鐘錶工坊高頻擒縱測振鳥與高空狙擊手剪影)",
                "posture": "側身 45 度穩健立正，X 型對趾雙爪咬合地面，身後三角抗震尾板接地支撐，雙手端持振律重型氣動火銃，神情專注冷靜，頭頂猩紅冠羽隨氣壓微微張合，雙葉音叉發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "八角截面車削冷軋鎢鋼精密長鑿喙，雙頰帶有雙聯微型排氣孔，眼窩處精準鏤空中空供 optic_core 穿透，頭頂裝配三階層疊式磷銅多巴胺猩紅烤漆彈簧散熱羽片與微型音叉",
                "ears": "沖壓圓弧黃銅側向測振受音孔，內置高靈敏微型諧振膜片與減震黃銅外罩，無生物耳廓",
                "torso_and_limbs": "亮面沖壓鍍鎳薄鋼板胸腹外殼（#FFFDF8），腹部嵌圓形高透石英視窗可窺見擒縱調速輪與指針式氣壓表，四肢為高剛性黃銅球鉸鏈",
                "tail": "三層鉚接加固之冷軋鋼板三角抗震支撐尾板，末端包覆耐磨黑色橡膠緩衝墊，開火時重重接地抵消後坐力，無生物肉質尾",
                "weapon_system": "右手主持槍身握把扣引扳機、左手托護木防滑握槽專屬「振律重型氣動火銃（Resonance Pneumatic Heavy Gun）」，冷軋鎢鋼八角槍管搭配高壓儲氣筒與多孔消焰散熱針型槍口，完全符合 0-MKT7 與 ranger/gun 體系，底層掛載 equipment.json 既有 flint_gun (tier 1) 與 blackpowder_rifle (tier 2)"
            },
            "color_palette": {
                "base": "#FFFDF8 (基底鍍鎳冷亮銀/象牙白，胸腹主色與面甲受光面)",
                "primary": "#FFD028 (主色天元黃銅金，雙翼覆羽沖壓銅片、發條鑰匙與機械關節)",
                "secondary": "#FF5E8A (次色多巴胺鮮亮猩紅，頭頂散熱冠羽、工裝警示條與目鏡同心圓游標)",
                "accent": "#FFA010 (點綴晨曦暖橘，工裝防墜反光標識與氣閥調速鈕)",
                "core_cyan": "#38A0FF (提神晴空亮天藍，目鏡光學鍍膜、排氣微光與高頻諧振震波)",
                "outline": "#1F1A3A (深暖褐/深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_woodpecker.png (品牌形象立牌)",
                        "web/media/hero/char_woodpecker.png (官網英雄展示立繪)",
                        "docs/art/resonance_woodpecker_concept.png (概念立繪)",
                        "game/assets/sprites/player/woodpecker_idle.png (64x64 待機)",
                        "game/assets/sprites/player/woodpecker_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/woodpecker_idle.png (隊伍待機)",
                        "web/media/hero/woodpecker_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/woodpecker_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/woodpecker_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/woodpecker_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/woodpecker_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/woodpecker_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/woodpecker_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/woodpecker/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/woodpecker.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/woodpecker_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/resonance_woodpecker.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/woodpecker/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_woodpecker.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/resonance_woodpecker_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_woodpecker.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/woodpecker_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/woodpecker_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/woodpecker_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/woodpecker_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/woodpecker_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/woodpecker_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/woodpecker_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/woodpecker/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/woodpecker.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/resonance_woodpecker.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/woodpecker/{slot_id}/{item_id}.png [待產出]"
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
            base_rule = f"四十八重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲、撼地野牛粗獷寬厚駝峰重甲與舊庫拆解工兵胸甲、巡管守宮靈敏扁平爬壁體態與耐熱暗忍胸甲、破星蜜獾平頂抗衝擊體態與軌道防護工裝、澄心水豚溫潤方鈍體態與道場茶道防塵練功袍、振律啄木鳥挺拔精幹體態與高空巡檢工裝) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    woodpecker_dir = "game/assets/sprites/player/paperdoll/woodpecker/"
    if woodpecker_dir not in races_dirs:
        races_dirs.append(woodpecker_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/woodpecker")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/woodpecker")
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
