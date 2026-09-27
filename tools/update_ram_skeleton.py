#!/usr/bin/env python3
"""為第二十九族星盤靈羊 (ram) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/ASTRAL_RAM_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 ram 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_ram_astral_polymer_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_ram_astral_polymer_default",
            "name": "星穹象牙白聚合物素體",
            "race": "ram",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_ram_spiral_balance_horns" for v in head_variants):
        head_variants.append({
            "id": "head_ram_spiral_balance_horns",
            "name": "雙螺旋發條游絲盤角面甲",
            "race": "ram",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_ram_astrolabe_tri_star" for v in key_variants):
        key_variants.append({
            "id": "key_ram_astrolabe_tri_star",
            "name": "星盤三叉星芒發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_ram_gravity_starlight_robe" for v in costume_variants):
        costume_variants.append({
            "id": "costume_ram_gravity_starlight_robe",
            "name": "星軌漫步者引力法袍",
            "race": "ram",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_ram_starlight_amber_optic" for v in face_variants):
        face_variants.append({
            "id": "face_ram_starlight_amber_optic",
            "name": "星光琥珀金色點陣LED目鏡",
            "race": "ram",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_ram_astral_spiral_staff" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_ram_astral_spiral_staff",
            "name": "星軌游絲共鳴杖",
            "weapon_type": "magic",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_ram_gravity_orbit_rings" for v in curio_variants):
        curio_variants.append({
            "id": "curio_ram_gravity_orbit_rings",
            "name": "懸浮反重力星環儀",
            "race": "ram",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 29

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "ram" for r in races_list):
        races_list.append({
            "race_id": "ram",
            "aliases": [
                "astral_ram",
                "celestial_ram",
                "spiral_ram",
                "gravity_ram"
            ],
            "name_zh": "星盤靈羊",
            "name_en": "The Astral Ram",
            "class_archetype": "法師 (Mage)",
            "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
            "lore_anchor": "高軌星穹空間站中掌管星盤觀測與游絲磁通調諧的星階巡禮法師偶，通體由高光象牙白工程聚合物塑料板件、弧面沖壓琺瑯雲紋疊片、雙螺旋超導磷青銅精密發條游絲盤角、星光琥珀金色點陣LED目鏡、星盤三叉星芒發條鑰匙與懸浮反重力星環儀組裝而成，右手單持星軌游絲共鳴杖，以失重微漂引力轟擊與天體軌道脈衝見長",
            "proportions": {
                "head_to_body_ratio": "2.2 ~ 2.8 頭身 (靈巧Q版天體奧術偶、反差萌圓潤剪影)",
                "posture": "身軀以失重微浮力踏地，背部星盤鑰匙與身後反重力星環勻速自轉，雙角游絲柔和微光，右手單持星軌共鳴杖微傾指向星軌",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "高光象牙白聚合物靈羊頭殼，兩側展開雙螺旋超導磷青銅精密發條游絲盤角（#C88A4A），面部嵌有星光琥珀金色點陣LED晶片目鏡（#FFD028），頭戴圓潤聚合物羊耳防撞耳罩",
                "ears": "圓潤聚合物羊耳防撞耳罩，耳軸為鍍金黃銅球窩關節，可靈活調節傾角感知微真空氣流擾動",
                "torso_and_limbs": "主軀幹為高光象牙白工程聚合物外殼（#FFFDF8），頸部與胸前覆蓋弧面沖壓高光琺瑯雲紋疊片，球窩關節為鍍金黃銅，四蹄為鍍金拋光金屬蹄鐵與防滑矽膠底",
                "tail": "超微型工程塑料圓球尾椎與減震橡膠緩衝墊，保持可愛微小剪影不干擾反重力星環運轉",
                "weapon_system": "右手單持專屬「星軌游絲共鳴杖（Astral Spiral Resonance Staff）」，杖身為工程聚合物與鈦鋼連桿，杖頂懸浮微型發條游絲天球儀與光學反重力水晶，完全符合 0-MKT7 與 mage/magic 體系，底層掛載 equipment.json 既有 star_rod"
            },
            "color_palette": {
                "primary": "#FFFDF8 (高光象牙白主軀幹塑料外殼與面部板件)",
                "secondary": "#38A0FF (星穹天藍星軌引力法袍主色與螢光軌道飾條)",
                "costume_coral": "#FF5E8A (珊瑚粉紅法袍內襯滾邊與反重力星環節點)",
                "accent": "#FFD028 (琥珀星光點陣LED目鏡與游絲天球儀核心)",
                "balance_spring": "#C88A4A (超導磷青銅雙螺旋游絲盤角與黃銅齒圈)",
                "frame": "#4A5568 (鈦鋼金屬傳動軸承與四肢骨架連桿)",
                "nebula_glow": "#4ED86A (薄荷星雲施法微光粒子與反重力水晶光芒)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_ram.png (品牌形象立牌)",
                        "web/media/hero/char_ram.png (官網英雄展示立繪)",
                        "docs/art/astral_ram_concept.png (概念立繪)",
                        "game/assets/sprites/player/ram_idle.png (64x64 待機)",
                        "game/assets/sprites/player/ram_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/ram_idle.png (隊伍待機)",
                        "game/assets/sprites/player/ram_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/ram_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/ram_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/ram/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/ram.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/astral_ram.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/ram/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_ram.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/astral_ram_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_ram.png (400x840) [待產出]",
                "web_preview": "web/media/hero/ram_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/ram_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/ram_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/ram_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/ram_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/ram_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/ram_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/ram/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/ram.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/astral_ram.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/ram/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 29 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十九大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    ram_dir = "game/assets/sprites/player/paperdoll/ram/"
    if ram_dir not in races_dirs:
        races_dirs.append(ram_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/ram")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/ram")
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
