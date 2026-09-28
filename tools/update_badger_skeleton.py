#!/usr/bin/env python3
"""為第四十六族破星蜜獾 (The Starbreaker Honey Badger, badger) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/STARBREAKER_BADGER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 badger 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_badger_polymer_space_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_badger_polymer_space_default",
            "name": "高密度聚合物平頭抗衝擊素體",
            "race": "badger",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_badger_flathead_ballistic_visor" for v in head_variants):
        head_variants.append({
            "id": "head_badger_flathead_ballistic_visor",
            "name": "平頭防暴沖壓護額",
            "race": "badger",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_badger_four_vane_antenna_gold" for v in key_variants):
        key_variants.append({
            "id": "key_badger_four_vane_antenna_gold",
            "name": "四葉天線金黃發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_badger_eva_heavy_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_badger_eva_heavy_harness",
            "name": "軌道高抗衝擊防護工裝",
            "race": "badger",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_badger_amber_led_matrix_visor" for v in face_variants):
        face_variants.append({
            "id": "face_badger_amber_led_matrix_visor",
            "name": "琥珀點陣 LED 護目面罩",
            "race": "badger",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_badger_starbreaker_ripper_claw" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_badger_starbreaker_ripper_claw",
            "name": "逐星裂空機關爪",
            "weapon_type": "claw",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_badger_dual_coldgas_reaction_thruster" for v in curio_variants):
        curio_variants.append({
            "id": "curio_badger_dual_coldgas_reaction_thruster",
            "name": "雙聯冷氣反推推進背包",
            "race": "badger",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_list = races_spec["races"]

    if not any(r.get("race_id") == "badger" for r in races_list):
        races_list.append({
            "race_id": "badger",
            "aliases": [
                "starbreaker_badger",
                "astral_badger",
                "clockwork_badger",
                "space_badger"
            ],
            "name_zh": "破星蜜獾",
            "name_en": "The Starbreaker Honey Badger",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
            "lore_anchor": "巡弋於星穹軌道·外星基地「聚合物太空艙模組」與「高光懸空螢光軌道」，巡防「太陽能帆板與微型排氣天線」、「太空拼裝維修船塢」、「高壓地熱升空彈射井·軌道受壓對接艙」、「垂直磁浮天軌·星穹軌道月台」、「軌道廢棄排障滑道」與「失重慣性磁力捕捉網」，並駐守「高真空抗靜電除塵室」，配合宇航機器人隊長·螺栓隊長、太空發條小狗·萊卡波波與軌道站資深工程師·光纖婆婆；通體覆蓋高密度消光白工程塑料板件（ABS/POM）、平頭防暴沖壓護額、四葉天線金黃發條鑰匙、軌道高抗衝擊防護工裝、琥珀點陣 LED 護目面罩、雙聯冷氣反推推進背包，右手單持專屬逐星裂空機關爪，以失重微浮力冷氣反推向量衝鋒、正面撕裂防線硬核攻堅見長的星穹無畏破陣武術家",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (古典發條鐵皮平頭動作機械獾、平頂防暴護額與雙聯冷氣推進背包剪影)",
                "posture": "側身 45 度穩固低重心站姿，四肢微屈，雙爪自然下沉，右手逐星裂空機關爪橫護於胸前斜下方，左爪微張維持失重平衡，背後四葉發條天線鑰匙勻速自轉，琥珀點陣 LED 目鏡專注警戒",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "一體沖壓平頂防暴金屬護簷與象牙白聚合物抗震板，兩側裝配小型圓形黃銅散熱孔與通訊小耳罩，臉頰兩側帶有珊瑚粉微型排氣孔",
                "ears": "護額兩側微型圓形散熱孔與通訊小耳罩，兼具真空短波通訊天線功能",
                "torso_and_limbs": "高抗衝擊工程聚合物塑料模組（ABS/POM）覆深空消光曜黑塗層（#1F1A3A），背部嵌裝象牙白消光隆脊板件（#FFFDF8），關節為球形金屬卡扣；四肢粗壯沉穩",
                "tail": "圓錐形黃銅冷氣排氣尾錐，內部裝載微型發條減壓排氣閥，輔助失重姿態平衡",
                "weapon_system": "右手單持專屬「逐星裂空機關爪（Star-Breaker Vacuum Ripper Claw）」，三聯切削高碳鋼合金彎爪鍍氮化鈦金光澤，爪背內嵌冷氣反推噴嘴與螢光天藍磁吸線圈，完全符合 0-MKT7 與 monk/claw 體系，底層掛載 equipment.json 既有 hunt_claw (tier 3)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (基底象牙奶油白，背部隆脊裝甲板與太空頭盔邊框底色)",
                "secondary": "#1F1A3A (主色深空消光曜黑，四肢底盤、腹部耐磨護板與胸甲襯底)",
                "brass_gear": "#FFD028 (裝飾多巴胺金黃，四葉發條天線鑰匙外柄、琥珀 LED 目鏡與合金爪刃鍍層)",
                "amber_led": "#FFD028 (琥珀點陣 LED 護目面罩發光色)",
                "core_cyan": "#38A0FF (功能天藍，冷氣反推噴嘴排氣光暈、軌道磁吸指示燈與能量管線)",
                "blush_coral": "#FF5E8A (腮紅珊瑚粉，面罩臉頰兩側微型散熱排氣小圓孔)",
                "accent_gold": "#FFA010 (裝飾暖橘，胸甲卡扣、噴嘴散熱喉管與肩關節護圈)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_badger.png (品牌形象立牌)",
                        "web/media/hero/char_badger.png (官網英雄展示立繪)",
                        "docs/art/starbreaker_badger_concept.png (概念立繪)",
                        "game/assets/sprites/player/badger_idle.png (64x64 待機)",
                        "game/assets/sprites/player/badger_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/badger_idle.png (隊伍待機)",
                        "web/media/hero/badger_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/badger_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/badger_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/badger_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/badger_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/badger_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/badger_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/badger/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/badger.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/badger_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/starbreaker_badger.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/badger/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_badger.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/starbreaker_badger_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_badger.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/badger_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/badger_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/badger_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/badger_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/badger_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/badger_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/badger_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/badger/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/badger.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/starbreaker_badger.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/badger/{slot_id}/{item_id}.png [待產出]"
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
            base_rule = f"四十六重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲、撼地野牛粗獷寬厚駝峰重甲與舊庫拆解工兵胸甲、巡管守宮靈敏扁平爬壁體態與耐熱暗忍胸甲、破星蜜獾平頂抗衝擊體態與軌道防護工裝) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    badger_dir = "game/assets/sprites/player/paperdoll/badger/"
    if badger_dir not in races_dirs:
        races_dirs.append(badger_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/badger")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/badger")
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
