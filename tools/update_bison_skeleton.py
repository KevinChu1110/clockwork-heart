#!/usr/bin/env python3
"""為第四十四族撼地野牛 (The Groundshaker Bison, bison) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/GROUNDSHAKER_BISON_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 bison 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_bison_rusted_tinplate_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_bison_rusted_tinplate_default",
            "name": "生鏽耐磨馬口鐵重裝素體",
            "race": "bison",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_bison_riveted_brow_horn_crest" for v in head_variants):
        head_variants.append({
            "id": "head_bison_riveted_brow_horn_crest",
            "name": "鉚接工字鋼曲角重盔",
            "race": "bison",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_bison_heavy_cross_t_bar_cast_iron" for v in key_variants):
        key_variants.append({
            "id": "key_bison_heavy_cross_t_bar_cast_iron",
            "name": "重工十字T柄生鐵發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_bison_junkyard_demolition_cuirass" for v in costume_variants):
        costume_variants.append({
            "id": "costume_bison_junkyard_demolition_cuirass",
            "name": "舊庫拆解工兵重胸甲與防刮裙甲",
            "race": "bison",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_bison_amber_pressure_gauge_eye" for v in face_variants):
        face_variants.append({
            "id": "face_bison_amber_pressure_gauge_eye",
            "name": "琥珀雙針耐震壓力表目鏡",
            "race": "bison",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_bison_wasteland_anvil_crusher_hammer" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_bison_wasteland_anvil_crusher_hammer",
            "name": "廢土重砧碎鐵巨鎚",
            "weapon_type": "hammer",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_bison_twin_vent_exhaust_stack" for v in curio_variants):
        curio_variants.append({
            "id": "curio_bison_twin_vent_exhaust_stack",
            "name": "雙聯排氣散熱煙囪",
            "race": "bison",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 44

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "bison" for r in races_list):
        races_list.append({
            "race_id": "bison",
            "aliases": [
                "groundshaker_bison",
                "clockwork_bison",
                "scrap_bison",
                "iron_bison"
            ],
            "name_zh": "撼地野牛",
            "name_en": "The Groundshaker Bison",
            "class_archetype": "戰士 (Viking)",
            "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
            "lore_anchor": "駐守於底層廢棄深淵界域「R08 荒漠齒輪塚·遺忘舊庫」，巡防「舊庫重型吊裝龍門架」、「零件分揀斜坡裂谷」、「冷卻熔渣重力傾卸滑道·舊庫受料口」、「軌道廢棄排障滑道·舊庫分揀倉」、「大齒輪懸索天梯·舊庫總站」、「古老重型零件輸送翻斗軌道」、「廢料沉降磁吸緩衝沙漏」與「高溫蒸氣除鏽清洗槽」，並守護「拾荒拼裝聚落·齒輪營地」與「破軍星軸（銳齒之魂）」；身軀由高強度沖壓深褐生鏽耐磨馬口鐵板覆亮橘防鏽烤漆鍛造而成，配備鉚接工字鋼曲角重盔、重工十字T柄生鐵發條鑰匙、舊庫拆解工兵重胸甲與防刮裙甲、琥珀雙針耐震壓力表目鏡、雙聯排氣散熱煙囪，右手單持專屬廢土重砧碎鐵巨鎚，以沉穩下砸破障、撼地霸體硬扛見長的荒漠舊庫首席重裝拆解工程戰士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (古典發條鐵皮頂角野牛、工字鋼曲角重盔與駝峰重甲發條主機艙剪影)",
                "posture": "側身 45 度沉穩寬步站姿，生鐵雙瓣蹄踩實地面，右手持廢土重砧碎鐵巨鎚斜倚身側，左手握拳收於胸前護胸板處，背後重工十字T柄發條鑰匙沉穩自轉，雙聯排氣煙囪微噴散熱蒸氣",
                "standee_height_px": 840,
                "standee_width_px": 520
            },
            "mechanical_features": {
                "head_and_neck": "一體成型沖壓厚生鐵球形護盔，前額焊接三重交疊沖壓防沙鋼板護簷，額側延伸出弧形雙工字鋼鍛造機械角，帶有黑黃多巴胺防撞斜紋；鼻吻部帶有珊瑚粉微型散熱孔",
                "ears": "天藍色加厚石英壓力表目鏡，內嵌雙指針游標壓力刻度與薄荷綠安全線；耳側帶有抗震金屬護筒",
                "torso_and_limbs": "通體由高強度深褐生鏽耐磨馬口鐵板覆亮橘防鏽烤漆板件包覆，外露直徑 8mm 冷鉚釘，肩背駝峰內置高扭力發條主機艙；四足為雙瓣鉸接抗震生鐵蹄踏，內嵌壓縮彈簧減震襯墊",
                "tail": "五節粗獷高強度生鐵鏈環串聯多節防塵尾，末端焊接倒圓錐形生鐵配重陀螺，隨重心擺動維持動態平衡",
                "weapon_system": "右手單持專屬「廢土重砧碎鐵巨鎚（Wasteland Anvil Scrap-Crusher Sledgehammer）」，加厚雙鉚接工字鋼梁長柄、四方生鐵砧鎚頭與防打滑蜂窩撞擊面，完全符合 0-MKT7 與 viking/hammer 體系，底層掛載 equipment.json 既有 anvil_hammer (tier 1)、iron_cudgel (tier 2) 與 bastion_blade (tier 3)"
            },
            "color_palette": {
                "base": "#FFFDF8 (基底象牙奶油白，面甲中心與胸前壓力表內底盤)",
                "primary": "#FFA010 (主色廢土多巴胺亮橘，馬口鐵胸背主裝甲與護肩外殼)",
                "secondary": "#E6A15C (副色亮黃銅暖橘，素體金屬倒角與板件磨損飾邊)",
                "accent": "#FFD028 (裝飾多巴胺金黃，工字鋼角飾邊、鎚頭銘文與黃銅大卡扣)",
                "ochre_brown": "#D49B4B (裝飾赭石暖褐，磨砂生鐵骨架、護臂板件與避震護筒)",
                "core_cyan": "#38A0FF (功能天藍，加厚石英壓力表目鏡鏡片與發條能量指示窗)",
                "mint_green": "#4ED86A (點綴薄荷綠，壓力表安全刻度線與關節注油孔標籤)",
                "blush_coral": "#FF5E8A (腮紅珊瑚粉，鼻吻部兩側圓形蒸氣洩壓閥孔)",
                "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_bison.png (品牌形象立牌)",
                        "web/media/hero/char_bison.png (官網英雄展示立繪)",
                        "docs/art/groundshaker_bison_concept.png (概念立繪)",
                        "game/assets/sprites/player/bison_idle.png (64x64 待機)",
                        "game/assets/sprites/player/bison_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/bison_idle.png (隊伍待機)",
                        "web/media/hero/bison_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/bison_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/bison_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/bison_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/bison_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/bison_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/bison_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/bison/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/bison.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/bison_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/groundshaker_bison.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/bison/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_bison.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/groundshaker_bison_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_bison.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/bison_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/bison_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/bison_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/bison_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/bison_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/bison_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/bison_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/bison/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/bison.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/groundshaker_bison.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/bison/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 44 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = "四十四重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲、撼地野牛粗獷寬厚駝峰重甲與舊庫拆解工兵胸甲) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    bison_dir = "game/assets/sprites/player/paperdoll/bison/"
    if bison_dir not in races_dirs:
        races_dirs.append(bison_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/bison")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/bison")
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
