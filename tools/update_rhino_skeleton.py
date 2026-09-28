#!/usr/bin/env python3
"""為第三十二族重角犀牛 (The Heavyhorn Rhino, rhino) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/HEAVYHORN_RHINO_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 rhino 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_rhino_molten_iron_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_rhino_molten_iron_default",
            "name": "重角犀牛熔鑄粗鐵素體",
            "race": "rhino",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_rhino_crucible_battering_crest" for v in head_variants):
        head_variants.append({
            "id": "head_rhino_crucible_battering_crest",
            "name": "鍛爐衝壓雙重撞角頭盔",
            "race": "rhino",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_rhino_crucible_crosshair_key" for v in key_variants):
        key_variants.append({
            "id": "key_rhino_crucible_crosshair_key",
            "name": "熔爐十字洩壓發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_rhino_crucible_smith_plate" for v in costume_variants):
        costume_variants.append({
            "id": "costume_rhino_crucible_smith_plate",
            "name": "熔火鍛造重裝護胸甲",
            "race": "rhino",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_rhino_dual_amber_pyro_optic" for v in face_variants):
        face_variants.append({
            "id": "face_rhino_dual_amber_pyro_optic",
            "name": "雙聯琥珀金石英觀火目鏡",
            "race": "rhino",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_rhino_crucible_breaker_axe" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_rhino_crucible_breaker_axe",
            "name": "熔爐破陣重鋼戰斧",
            "weapon_type": "axe",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_rhino_steam_furnace_exhaust" for v in curio_variants):
        curio_variants.append({
            "id": "curio_rhino_steam_furnace_exhaust",
            "name": "多管連動發條蒸汽排煙爐",
            "race": "rhino",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 32

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "rhino" for r in races_list):
        races_list.append({
            "race_id": "rhino",
            "aliases": [
                "heavyhorn_rhino",
                "crucible_rhino",
                "molten_rhino",
                "battering_rhino"
            ],
            "name_zh": "重角犀牛",
            "name_en": "The Heavyhorn Rhino",
            "class_archetype": "戰士 (Viking)",
            "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
            "lore_anchor": "穿梭於赤焰熔爐「黑曜石淬火神壇」與「重型鍛造工坊與衝壓懸橋」之間，巡守於「金色液態鐵水熔池」、「黑曜淬火石磚步道」、「黃銅洩壓儀表塔」、「晨曦天軌 6 號熔爐重載貨運月台」與「冷卻熔渣重力排料傾卸滑道」，通體由深沉消光粗砂鑄鐵板件、黑曜石淬火耐火鍍層、雙聯衝壓錐形鍛造重角、雙聯琥珀金石英觀火目鏡、多管連動發條蒸汽排煙爐與熔爐十字洩壓發條鑰匙組裝而成，右手單持專屬熔爐破陣重鋼戰斧，以直線衝壓破陣重劈、高溫過熱碎甲與衝撞破障見長的重裝戰士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版重裝戰士偶、四稜錐重角剪影)",
                "posture": "雙足粗短圓柱形金屬短靴與耐火石墨陶瓷墊踏地穩健，身軀微前傾，右手單手持握熔爐破陣重鋼戰斧斜立於身側，左手半握拳置於腰際作重步平衡身姿，身後三聯蒸汽排氣爐規律噴出白色煙圈",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓成型耐熱粗砂鑄鐵頭罩配雙聯衝壓鍛造重角，角尖呈現金黃色退火光澤（#FFD028），側面飾有散熱格柵與圓頭鉚釘，兩側嵌有黃銅齒圈環繞的雙聯琥珀金石英觀火目鏡（#FBBF24 / #FFA010）",
                "ears": "面罩兩側微型鍛造洩壓排氣閥孔與內部耐震動雙軸承，感應熔爐衝壓共振與秒針跳格震動",
                "torso_and_limbs": "主軀幹覆蓋深沉消光粗砂鑄鐵板件（#2B2836）與黑曜石淬火耐火鍍層板（#1F1A3A），胸前鉚接拋光黃銅鐵砧浮雕與暖橘（#FFA010）警示壓條，四肢為粗短結實鑄鐵機械肢配防燙天藍（#38A0FF）耐熱密封圈",
                "tail": "由三節短粗金屬套管鉚接而成的發條配重短尾，行走時如鐘擺般左右擺動維持平衡",
                "weapon_system": "右手單持專屬「熔爐破陣重鋼戰斧（Crucible Breaker Heavy Steel Waraxe）」，柄長約 38px，由加厚月牙單刃黑曜耐熱合金、氣動鍛壓平頭破甲錘與洩壓散熱孔構成，完全符合 0-MKT7 與 viking/axe 體系，底層掛載 equipment.json 既有 split_greataxe 與 notch_axe"
            },
            "color_palette": {
                "primary": "#2B2836 (消光鑄鐵黑主軀幹裝甲、厚重金屬板件與足部護甲)",
                "secondary": "#FFD028 (熔爐暖金十字發條鑰匙、衝壓角尖退火鍍層與戰斧金屬配重環)",
                "accent": "#FFA010 (熔岩暖橘胸甲警示條紋、排煙管飾邊與戰斧散熱閥門)",
                "optic_amber": "#FBBF24 (琥珀明黃雙聯石英觀火目鏡鏡片、溫度指示刻度與高溫警示燈)",
                "coolant_blue": "#38A0FF (防燙天藍冷卻水管線塗裝、安全洩壓閥指針與耐熱密封圈)",
                "indicator_mint": "#4ED86A (薄荷碧綠壓力安全指示刻度與蒸汽洩壓粒子核心光斑)",
                "ceramic_white": "#FFFDF8 (陶瓷米白胸口鐵砧紋章襯板與面頰防燙陶瓷高光)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_rhino.png (品牌形象立牌)",
                        "web/media/hero/char_rhino.png (官網英雄展示立繪)",
                        "docs/art/heavyhorn_rhino_concept.png (概念立繪)",
                        "game/assets/sprites/player/rhino_idle.png (64x64 待機)",
                        "game/assets/sprites/player/rhino_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/rhino_idle.png (隊伍待機)",
                        "game/assets/sprites/player/rhino_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/rhino_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/rhino_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/rhino/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/rhino.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/heavyhorn_rhino.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/rhino/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_rhino.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/heavyhorn_rhino_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_rhino.png (400x840) [待產出]",
                "web_preview": "web/media/hero/rhino_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/rhino_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/rhino_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/rhino_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/rhino_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/rhino_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/rhino_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/rhino/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/rhino.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/heavyhorn_rhino.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/rhino/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 32 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十二大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    rhino_dir = "game/assets/sprites/player/paperdoll/rhino/"
    if rhino_dir not in races_dirs:
        races_dirs.append(rhino_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/rhino")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/rhino")
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
