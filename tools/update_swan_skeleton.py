#!/usr/bin/env python3
"""為第四十三族旋音天鵝 (The Melodic Swan, swan) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/MELODIC_SWAN_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 swan 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_swan_silver_enamel_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_swan_silver_enamel_default",
            "name": "銀白琺瑯防鏽馬口鐵素體",
            "race": "swan",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_swan_tiara_beak_visor" for v in head_variants):
        head_variants.append({
            "id": "head_swan_tiara_beak_visor",
            "name": "八音皇冠護額長喙",
            "race": "swan",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_swan_octave_dual_loop_brass" for v in key_variants):
        key_variants.append({
            "id": "key_swan_octave_dual_loop_brass",
            "name": "雙環八音八度黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_swan_theatre_herald_cuirass" for v in costume_variants):
        costume_variants.append({
            "id": "costume_swan_theatre_herald_cuirass",
            "name": "大劇院儀仗近衛胸甲與游標裙甲",
            "race": "swan",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_swan_prismatic_crystal_monocle" for v in face_variants):
        face_variants.append({
            "id": "face_swan_prismatic_crystal_monocle",
            "name": "單片棱鏡聚焦水晶目鏡",
            "race": "swan",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_swan_octave_spiral_lance" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_swan_octave_spiral_lance",
            "name": "八音螺旋穿刺長槍",
            "weapon_type": "spear",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_swan_spring_steel_ballet_wings" for v in curio_variants):
        curio_variants.append({
            "id": "curio_swan_spring_steel_ballet_wings",
            "name": "多節同軸冷軋彈簧鋼滑翔護羽",
            "race": "swan",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 43

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "swan" for r in races_list):
        races_list.append({
            "race_id": "swan",
            "aliases": [
                "melodic_swan",
                "clockwork_swan",
                "silver_swan",
                "opera_swan"
            ],
            "name_zh": "旋音天鵝",
            "name_en": "The Melodic Swan",
            "class_archetype": "騎士 (Knight)",
            "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
            "lore_anchor": "駐守於晨曦小鎮「懸吊齒輪鐘樓」與「石板街道集市」，巡防「齒輪吊索大橋·小鎮站」、「晨曦天軌 2 號月台」、「蔓谷天梯引道」、「巨輪城重型空軌貨運棧橋」與「邊界安全防護彈簧網」，並守護「精紡線莊」與「中央油坊」，配合提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳、摺紙工匠·小鶴與集市守護機關·提線巨偶；身軀覆蓋銀白琺瑯防鏽馬口鐵板件與玫瑰金接縫、八音皇冠護額長喙、雙環八音八度黃銅發條鑰匙、大劇院儀仗近衛胸甲與游標裙甲、單片棱鏡聚焦水晶目鏡、多節同軸冷軋彈簧鋼滑翔護羽，右手單持專屬八音螺旋穿刺長槍，以芭蕾迴旋節奏優雅突刺、八音律動停拍精準迎擊見長的大劇院首席皇家近衛騎士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (古典銀天鵝自動機、八音皇冠長喙與多節同軸彈簧鋼羽翼剪影)",
                "posture": "身軀呈古典芭蕾優雅挺拔立姿，雙腳金屬蹼爪微著地，右手單持八音螺旋穿刺長槍斜立於側，左翼同軸彈簧鋼護羽微張導流平衡，背後雙環八度黃銅發條鑰匙勻速自轉，單片棱鏡聚焦水晶目鏡專注警戒",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "一體沖壓精鋼圓盔與拋光黃銅長平喙，前額鉚接微縮五芒星八音皇冠護額，內嵌四組精密鉸接黃銅球形萬向關節長頸",
                "ears": "單片天藍棱鏡聚焦水晶目鏡，外框包覆極細黃銅齒輪游標金屬箍；面部兩側帶有珊瑚粉微型圓形散熱氣孔",
                "torso_and_limbs": "通體覆蓋冷軋沖壓薄鋼板外覆銀白琺瑯（#E8EFF5）防鏽馬口鐵板件與玫瑰金飾條，胸膛嵌圓形石英音筒視窗；四肢為密封式球窩旋轉關節與金屬蹼爪",
                "tail": "多節沖壓冷軋薄彈簧鋼同軸滑翔護羽與扇形梳齒音律尾翼，三組階梯式同軸鉚接鋼片隨重心開合，中心軸嵌微型扭簧",
                "weapon_system": "右手單持專屬「八音螺旋穿刺長槍（Octave Spiral Piercing Lance）」，冷軋鍍銀精鋼無縫管與黃金螺旋錐刃，內置音筒簧片，完全符合 0-MKT7 與 knight/spear 體系，底層掛載 equipment.json 既有 ash_spear (tier 1) 與 knight_pike (tier 3)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (象牙奶油白，胸腹板件內襯與高光區)",
                "secondary": "#E8EFF5 (古典純銀白，琺瑯防鏽馬口鐵素體、頭盔護額與雙翼主板)",
                "brass_gear": "#FFD028 (裝飾金黃，黃銅長喙、發條鑰匙、皇冠頂珠與槍尖螺旋)",
                "mint_green": "#4ED86A (點綴薄荷綠，腰帶游標刻度與護額微型寶石)",
                "core_cyan": "#38A0FF (功能天藍，單片石英目鏡鏡片與胸前音筒視窗微光)",
                "blush_coral": "#FF5E8A (腮紅珊瑚粉，面部兩側散熱氣孔與裙甲內襯微光)",
                "rose_gold": "#E8A598 (晨曦玫瑰金，胸甲滾邊、裙甲邊框與肩甲飾帶)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_swan.png (品牌形象立牌)",
                        "web/media/hero/char_swan.png (官網英雄展示立繪)",
                        "docs/art/melodic_swan_concept.png (概念立繪)",
                        "game/assets/sprites/player/swan_idle.png (64x64 待機)",
                        "game/assets/sprites/player/swan_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/swan_idle.png (隊伍待機)",
                        "web/media/hero/swan_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/swan_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/swan_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/swan_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/swan_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/swan_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/swan_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/swan/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/swan.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/swan_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/melodic_swan.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/swan/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_swan.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/melodic_swan_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_swan.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/swan_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/swan_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/swan_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/swan_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/swan_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/swan_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/swan_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/swan/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/swan.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/melodic_swan.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/swan/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 43 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "四十三重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    swan_dir = "game/assets/sprites/player/paperdoll/swan/"
    if swan_dir not in races_dirs:
        races_dirs.append(swan_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/swan")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/swan")
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
