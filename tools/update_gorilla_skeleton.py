#!/usr/bin/env python3
"""為第三十四族鋼臂巨猩 (The Steelarm Gorilla, gorilla) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/STEELARM_GORILLA_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 gorilla 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_gorilla_brass_heavy_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_gorilla_brass_heavy_default",
            "name": "鋼臂巨猩重型沖壓黃銅素體",
            "race": "gorilla",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_gorilla_riveted_brow_crest" for v in head_variants):
        head_variants.append({
            "id": "head_gorilla_riveted_brow_crest",
            "name": "五聯鉚釘沖壓防撞重額甲",
            "race": "gorilla",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_gorilla_heavy_t_forged_key" for v in key_variants):
        key_variants.append({
            "id": "key_gorilla_heavy_t_forged_key",
            "name": "巨輪鍛工重型T字鍛鐵發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_gorilla_steam_forge_boiler_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_gorilla_steam_forge_boiler_harness",
            "name": "巨輪鍛工高壓鍋爐背帶胸甲",
            "race": "gorilla",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_gorilla_dual_gauge_optic_lens" for v in face_variants):
        face_variants.append({
            "id": "face_gorilla_dual_gauge_optic_lens",
            "name": "雙聯石英蒸氣壓力表目鏡",
            "race": "gorilla",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_gorilla_steam_forging_fist" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_gorilla_steam_forging_fist",
            "name": "高壓蒸氣鍛打拳套",
            "weapon_type": "fist",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_gorilla_twin_turbo_exhaust_chimney" for v in curio_variants):
        curio_variants.append({
            "id": "curio_gorilla_twin_turbo_exhaust_chimney",
            "name": "雙渦輪過熱洩壓排氣煙囪",
            "race": "gorilla",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 34

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "gorilla" for r in races_list):
        races_list.append({
            "race_id": "gorilla",
            "aliases": [
                "steelarm_gorilla",
                "steam_gorilla",
                "forge_gorilla",
                "heavy_gorilla"
            ],
            "name_zh": "鋼臂巨猩",
            "name_en": "The Steelarm Gorilla",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
            "lore_anchor": "穿梭於黃銅都市「摩天齒輪工坊群」與「自律工廠與天街吊橋」之間，巡守於「高壓蒸氣管道網」、「中央動力廣場」、「鎢絲防爆街燈」、「中央蒸氣沐浴池」、「過熱洩壓排氣窗口」與「高架重軌引橋·巨輪城站」，通體由消光鑄鐵黑與沖壓厚鑄黃銅裝甲板件、冷軋鎢鋼外骨架、雙聯石英蒸氣壓力表目鏡、雙渦輪過熱洩壓排氣煙囪、巨輪鍛工高壓鍋爐背帶胸甲與重型T字鍛鐵發條鑰匙組裝而成，右手單持專屬高壓蒸氣鍛打拳套，以沉穩低重心、鐵壁格擋防禦與高壓衝壓直拳破勢見長的重裝武術家",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版重裝發條自動偶、厚重前臂與鍋爐胸甲剪影)",
                "posture": "雙足寬厚金屬防滑掌板踏地極其扎實，身軀微前傾，左手半握拳護於胸前作鐵壁格擋，右手單手持握高壓蒸氣鍛打拳套斜立身側，背部雙排氣煙囪規律吐出白色蒸氣圈，面龐壓力表指針保持在安全綠區",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓高光黃銅防撞重額甲配5顆圓頭冷鉚釘，兩側為圓形黃銅散熱金屬網耳與百葉散熱孔，面部嵌有黃銅齒圈環繞的雙聯石英玻璃蒸氣壓力表目鏡（#FFD028 / #FFA010），內置活動指針與薄荷綠安全刻度（#4ED86A）",
                "ears": "兩側圓形黃銅沖壓散熱網耳，耳後設有微型百葉散熱孔，伴隨呼吸節奏微幅排氣並感應高壓管網氣壓共振",
                "torso_and_limbs": "主軀幹覆蓋消光鑄鐵深暖灰黑板件（#2B2836）與象牙米白琺瑯防護前甲（#FFFDF8），四肢為粗壯冷軋鎢鋼前臂配球窩外露關節，腹部外露兩根水平往復紫銅氣動活塞桿，足底為菱形防滑金屬掌板",
                "tail": "無外露長尾，背部中央動力承座嵌合巨輪鍛工重型T字鍛鐵發條鑰匙，肩胛兩側聳立雙渦輪紫銅高壓蒸氣排氣煙囪",
                "weapon_system": "右手單戴專屬「高壓蒸氣鍛打拳套（High-Pressure Steam Forging Gauntlets）」，多巴胺胡桃鉗朱紅（#E63946）沖壓鋼外罩包裹，拳峰嵌有高壓滑動鎢鋼衝頭，腕部帶有小型耐熱紫銅蓄氣筒與天藍洩壓閥（#38A0FF），完全符合 0-MKT7 與 monk/fist 體系，底層掛載 equipment.json 既有 wrap_gloves 與 iron_knuckle"
            },
            "color_palette": {
                "primary": "#2B2836 (消光鑄鐵深暖灰黑主軀幹裝甲、厚重金屬板件與機械前臂)",
                "secondary": "#FFD028 (金黃高光黃銅防撞額甲、金屬齒輪與指針儀表外框)",
                "accent": "#FFA010 (暖橘壓力指針、過熱警示刻度與排氣閥門飾環)",
                "forge_crimson": "#E63946 (多巴胺胡桃鉗朱紅鍛打拳套外罩與衝壓護手鋼板)",
                "gauge_mint": "#4ED86A (薄荷碧綠壓力安全刻度線與蒸氣核心狀態燈)",
                "coolant_sky": "#38A0FF (高壓冷卻氣動閥門管線與排氣洩壓光斑)",
                "boiler_ivory": "#FFFDF8 (象牙米白琺瑯鍋爐防護胸板與面頰裝甲飾板)",
                "outline": "#2E1F18 (深暖褐手繪厚描邊，確保工業機械輪廓清晰立體)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_gorilla.png (品牌形象立牌)",
                        "web/media/hero/char_gorilla.png (官網英雄展示立繪)",
                        "docs/art/steelarm_gorilla_concept.png (概念立繪)",
                        "game/assets/sprites/player/gorilla_idle.png (64x64 待機)",
                        "game/assets/sprites/player/gorilla_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/gorilla_idle.png (隊伍待機)",
                        "game/assets/sprites/player/gorilla_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/gorilla_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/gorilla_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/gorilla/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/gorilla.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/steelarm_gorilla.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/gorilla/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_gorilla.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/steelarm_gorilla_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_gorilla.png (400x840) [待產出]",
                "web_preview": "web/media/hero/gorilla_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/gorilla_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/gorilla_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/gorilla_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/gorilla_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/gorilla_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/gorilla_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/gorilla/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/gorilla.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/steelarm_gorilla.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/gorilla/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 34 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十四大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    gorilla_dir = "game/assets/sprites/player/paperdoll/gorilla/"
    if gorilla_dir not in races_dirs:
        races_dirs.append(gorilla_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/gorilla")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/gorilla")
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
