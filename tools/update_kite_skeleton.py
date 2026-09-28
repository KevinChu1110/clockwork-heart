#!/usr/bin/env python3
"""為第四十二族熱流赤鳶 (The Thermal Kite, kite) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/THERMAL_KITE_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 kite 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_kite_copper_obsidian_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_kite_copper_obsidian_default",
            "name": "熱流赤鳶赤銅黑曜耐熱馬口鐵素體",
            "race": "kite",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_kite_raptor_cowl_beak" for v in head_variants):
        head_variants.append({
            "id": "head_kite_raptor_cowl_beak",
            "name": "沖壓耐熱赤銅猛禽頭罩與合金剪刀喙",
            "race": "kite",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_kite_turbine_relief_brass" for v in key_variants):
        key_variants.append({
            "id": "key_kite_turbine_relief_brass",
            "name": "四葉渦輪散熱黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_kite_welder_cape_belt" for v in costume_variants):
        costume_variants.append({
            "id": "costume_kite_welder_cape_belt",
            "name": "阻燃帆布焊接短披風與游標腰帶",
            "race": "kite",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_kite_amber_quartz_rangefinder" for v in face_variants):
        face_variants.append({
            "id": "face_kite_amber_quartz_rangefinder",
            "name": "單片橙紅耐火石英測距目鏡",
            "race": "kite",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_kite_crucible_recurve_bow" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_kite_crucible_recurve_bow",
            "name": "熱流淬火複合機關弓",
            "weapon_type": "bow",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_kite_spring_steel_cooling_wings" for v in curio_variants):
        curio_variants.append({
            "id": "curio_kite_spring_steel_cooling_wings",
            "name": "多節沖壓冷軋彈簧鋼同軸散熱羽翼",
            "race": "kite",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 42

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "kite" for r in races_list):
        races_list.append({
            "race_id": "kite",
            "aliases": [
                "thermal_kite",
                "crucible_kite",
                "glider_kite",
                "soaring_kite"
            ],
            "name_zh": "熱流赤鳶",
            "name_en": "The Thermal Kite",
            "class_archetype": "遊俠 (Ranger)",
            "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
            "lore_anchor": "高耐熱粗獷鑄鐵板件、黑曜石淬火耐火磚、金色液態流光鐵水池、重型鍛打氣動連桿、高壓黃銅洩壓儀表塔、金色液態鐵水熔池、黑曜淬火石磚步道、耐火排煙管樹、重型鍛造工坊與衝壓懸橋、晨曦天軌 6 號熔爐重載貨運月台、高壓地熱噴射升空彈射井、火山口中央鍛造神壇、冷卻熔渣重力排料傾卸滑道、磁吸隔熱排渣護欄網、淬火冷卻噴淋池、矮人鐵匠大師·重錘布隆、陶土魔像學徒·黏土泥泥、熔爐溫控長老·坩堝老爹、巡檢工兵蜥蜴小火、高溫上升熱氣流、地熱上升風口、熔爐泰坦·重裝巨型石拳鐵豕",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (俐落猛禽風帽、四葉渦輪鑰匙與多節沖壓同軸散熱羽翼剪影)",
                "posture": "身軀呈微前傾之熱流滑翔巡檢立姿，鎢鋼雙爪微抓地，右手單持熱流淬火複合機關弓斜立於側，左翼同軸彈簧鋼百葉微張導流散熱，背後四葉渦輪黃銅發條鑰匙勻速自轉，右眼單片橙紅石英目鏡十字光標專注瞄準",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓耐熱赤銅猛禽頭罩緊湊包覆頭部，頂部具備兩片向下導流熱浪的散熱背脊鰭片；面部前方銜接鍛造鎢鋼雙刃剪刀喙，雙側帶有外露微型同軸銷釘",
                "ears": "右眼單片橙紅耐火石英測距目鏡，蝕刻十字瞄準線與仰角刻度；左眼澄澈黑色大眼球點陣光核；雙耳位置為黃銅百葉集音窗",
                "torso_and_limbs": "通體覆蓋冷軋沖壓赤銅鍍層馬口鐵板件與黑曜淬火耐火磚護胸板，以四顆黃銅鉚釘固定；四肢為密封式球窩旋轉關節與鎢鋼腳爪",
                "tail": "多節沖壓冷軋彈簧鋼同軸散熱排氣羽翼與雙叉鉸接耐熱方向舵尾羽，五組薄鋼百葉以連桿鉚接，散熱時向上彈開",
                "weapon_system": "右手單持專屬「熱流淬火複合機關弓（Crucible Quenched Recurve Bow）」，弓臂為黑曜淬火雙曲彈簧鋼板鉚接，中央嵌高溫洩壓閥，完全符合 0-MKT7 與 ranger/bow 體系，底層掛載 equipment.json 既有 reed_bow (tier 1) 與 hawk_longbow (tier 3)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (象牙奶油白，胸腹板件內襯與高光區)",
                "secondary": "#FFA010 (暖陽亮橙金，赤銅鍍層素體、風帽外殼與背部渦輪鑰匙)",
                "brass_gear": "#FFD028 (裝飾金黃，黃銅鉚釘、儀表刻度指針與弓臂滑輪樞軸)",
                "mint_green": "#4ED86A (點綴薄荷綠，腰帶游標刻度與護目鏡邊框)",
                "core_cyan": "#38A0FF (功能天藍，雙翼散熱導槽冷卻液光條與箭頭指示燈)",
                "blush_coral": "#FF5E8A (腮紅珊瑚粉，臉頰微型散熱排氣孔微光)",
                "tungsten_gray": "#3A3644 (冷調深灰，黑曜石淬火胸甲、鎢鋼腳爪與弓身握把)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_kite.png (品牌形象立牌)",
                        "web/media/hero/char_kite.png (官網英雄展示立繪)",
                        "docs/art/thermal_kite_concept.png (概念立繪)",
                        "game/assets/sprites/player/kite_idle.png (64x64 待機)",
                        "game/assets/sprites/player/kite_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/kite_idle.png (隊伍待機)",
                        "web/media/hero/kite_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/kite_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/kite_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/kite_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/kite_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/kite_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/kite_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/kite/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/kite.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/kite_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/thermal_kite.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/kite/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_kite.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/thermal_kite_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_kite.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/kite_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/kite_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/kite_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/kite_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/kite_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/kite_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/kite_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/kite/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/kite.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/thermal_kite.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/kite/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 42 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "四十二重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    kite_dir = "game/assets/sprites/player/paperdoll/kite/"
    if kite_dir not in races_dirs:
        races_dirs.append(kite_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/kite")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/kite")
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
