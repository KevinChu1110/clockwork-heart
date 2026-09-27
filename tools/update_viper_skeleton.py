#!/usr/bin/env python3
"""為第二十七族竹影青蛇 (viper) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/BAMBOO_VIPER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 viper 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_viper_bamboo_lacquer_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_viper_bamboo_lacquer_default",
            "name": "竹影青蛇原廠翠綠生漆鉸接木雕素體",
            "race": "viper",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_viper_carved_bamboo_crest_hood" for v in head_variants):
        head_variants.append({
            "id": "head_viper_carved_bamboo_crest_hood",
            "name": "多節竹雕蛇冠斗笠",
            "race": "viper",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_viper_bamboo_leaf_fan" for v in key_variants):
        key_variants.append({
            "id": "key_viper_bamboo_leaf_fan",
            "name": "三葉竹葉發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_viper_zen_dojo_shinobi_wrap" for v in costume_variants):
        costume_variants.append({
            "id": "costume_viper_zen_dojo_shinobi_wrap",
            "name": "道場竹影夜行忍裝",
            "race": "viper",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_viper_emerald_glass_optic" for v in face_variants):
        face_variants.append({
            "id": "face_viper_emerald_glass_optic",
            "name": "溫潤翠綠琉璃珠目鏡",
            "race": "viper",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_viper_gale_bamboo_dagger" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_viper_gale_bamboo_dagger",
            "name": "疾風竹影短匕",
            "weapon_type": "dagger",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_viper_articulated_bamboo_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_viper_articulated_bamboo_tail",
            "name": "七節同軸鉸接木簧蛇尾",
            "race": "viper",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 27

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "viper" for r in races_list):
        races_list.append({
            "race_id": "viper",
            "aliases": [
                "bamboo_viper",
                "shadow_viper",
                "zen_viper",
                "shinobi_viper"
            ],
            "name_zh": "竹影青蛇",
            "name_en": "The Bamboo Viper",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
            "lore_anchor": "常駐於竹影道場「發條天元竹海」、「青石武鬥古道場·演武坪」、「山門竹煙茶舍」、「飛瀑木簧水碓」與「翠竹彈力阻尼編織網」的原住機關青蛇偶，通體由高剛性天然竹木纖維多層生漆拋光板件、溫潤奶油米白琺瑯面罩、多節竹雕蛇冠斗笠、溫潤翠綠琉璃珠目鏡、三葉竹葉發條鑰匙與七節同軸鉸接木簧蛇尾組裝而成，以右手單持疾風竹影短匕、波浪遊動身法與竹簧彈跳連刺見長的隱世敏捷忍者",
            "proportions": {
                "head_to_body_ratio": "2.2 ~ 2.8 頭身 (靈巧多節蛇偶、竹梢穿梭身法)",
                "posture": "身軀微側，七節蛇尾於地面呈 S 型優雅盤臥蓄簧，右手單持疾風竹影短匕橫於胸前，左手微展平衡，蛇冠斗笠與琉璃目鏡專注鎖定破綻",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "高剛性天然竹木纖維熱壓成型頭殼（#4ED86A），面頰兩側覆蓋溫潤奶油米白琺瑯面罩（#FFFDF8），微型黃銅平頭鉚釘固定，雙眼為圓形溫潤翠綠琉璃珠光學目鏡（#34D399）內刻同心太極齒輪刻度與瞄準光環",
                "ears": "頭頂多節流線型竹雕蛇影面甲與微型竹笠兜帽，兩側黃銅微型耳軸感應林間氣流",
                "torso_and_limbs": "主軀幹覆蓋翠綠生漆拋光竹木片配水墨青石骨架連桿（#3A4454），四肢關節為打磨椴木連桿與黃銅外露球窩關節，三指多關節精工木雕手握持短匕靈活穩健",
                "tail": "由七節漸細精雕翠竹管節與精密微型黃銅球窩銷釘鉸接串聯的木簧蛇尾，內部裝載高彈性竹篾扭簧與平衡陀，地面滑行提供優雅三點支撐與竹梢彈跳跳板",
                "weapon_system": "右手單持專屬「疾風竹影短匕（Gale Bamboo Shadow Dagger）」，刀身為熱壓碳化青竹板件鑲嵌黃銅穿刺齒紋與綠琉璃血槽，完全符合 0-MKT7 與 ninja/dagger 體系，底層掛載 equipment.json 既有 star_fang 與 nebula_needle"
            },
            "color_palette": {
                "primary": "#4ED86A (竹翠綠高剛性生漆拋光竹木板件)",
                "secondary": "#2E8B57 (溫潤青竹脊骨加固壓條與短匕刀脊)",
                "faceplate": "#FFFDF8 (溫潤奶油米白琺瑯面罩與胸前太極護心盤)",
                "accent": "#FFD028 (天元金黃三葉竹葉發條鑰匙與腰帶繩結)",
                "detail": "#34D399 (溫潤翠綠琉璃珠光學目鏡與短匕能量刃尖)",
                "frame": "#3A4454 (水墨青石內置木簧連桿與球窩關節)",
                "costume_coral": "#FF5E8A (珊瑚粉紅忍裝金屬搭扣與飾結)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_viper.png (品牌形象立牌)",
                        "web/media/hero/char_viper.png (官網英雄展示立繪)",
                        "docs/art/bamboo_viper_concept.png (概念立繪)",
                        "game/assets/sprites/player/viper_idle.png (64x64 待機)",
                        "game/assets/sprites/player/viper_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/viper_idle.png (隊伍待機)",
                        "game/assets/sprites/player/viper_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/viper_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/viper_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/viper/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/viper.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/bamboo_viper.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/viper/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_viper.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/bamboo_viper_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_viper.png (400x840) [待產出]",
                "web_preview": "web/media/hero/viper_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/viper_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/viper_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/viper_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/viper_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/viper_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/viper_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/viper/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/viper.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/bamboo_viper.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/viper/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 27 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十七大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    viper_dir = "game/assets/sprites/player/paperdoll/viper/"
    if viper_dir not in races_dirs:
        races_dirs.append(viper_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/viper")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/viper")
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
