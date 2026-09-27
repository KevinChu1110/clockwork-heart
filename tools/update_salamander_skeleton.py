#!/usr/bin/env python3
"""為第二十六族熔火蜥蜴 (salamander) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 salamander 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_salamander_magma_tungsten_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_salamander_magma_tungsten_default",
            "name": "熔火蜥蜴原廠黑曜鎢鋼耐熱金屬素體",
            "race": "salamander",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_salamander_radiator_crest_horns" for v in head_variants):
        head_variants.append({
            "id": "head_salamander_radiator_crest_horns",
            "name": "折疊耐熱散熱鰭角",
            "race": "salamander",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_salamander_four_vane_heatsink" for v in key_variants):
        key_variants.append({
            "id": "key_salamander_four_vane_heatsink",
            "name": "四葉散熱鍛造發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_salamander_foundry_sapper_apron" for v in costume_variants):
        costume_variants.append({
            "id": "costume_salamander_foundry_sapper_apron",
            "name": "地熱工兵耐火鉚接圍裙",
            "race": "salamander",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_salamander_amber_dial_lens" for v in face_variants):
        face_variants.append({
            "id": "face_salamander_amber_dial_lens",
            "name": "琥珀澄光熔壓目鏡",
            "race": "salamander",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_salamander_foundry_stamping_sledgehammer" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_salamander_foundry_stamping_sledgehammer",
            "name": "熔爐衝壓巨錘",
            "weapon_type": "hammer",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_salamander_segmented_damping_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_salamander_segmented_damping_tail",
            "name": "五節重鋼同軸阻尼大尾巴",
            "race": "salamander",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 26

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "salamander" for r in races_list):
        races_list.append({
            "race_id": "salamander",
            "aliases": [
                "magma_salamander",
                "foundry_salamander",
                "crucible_salamander",
                "sapper_salamander"
            ],
            "name_zh": "熔火蜥蜴",
            "name_en": "The Magma Salamander",
            "class_archetype": "戰士 (Viking)",
            "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
            "lore_anchor": "常駐於赤焰熔爐「重型鍛造工坊與衝壓懸橋」、「氣動衝壓懸橋」、「高壓地熱噴射升空彈射井」、「淬火冷卻噴淋池」與「火山口中央核心鍛造神壇」的發條耐火工兵蜥蜴，通體由黑曜鎢鋼冷軋薄板件、溫潤奶油米白琺瑯面罩、雙聯折疊耐熱散熱導流鰭角、琥珀橙光學水晶目鏡、四葉散熱鍛造發條鑰匙與五節重鋼同軸阻尼大尾巴組裝而成，以右手單持熔爐衝壓巨錘、氣動衝壓垂直下砸與剛猛鍛砸見長的重裝鍛火戰士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (低重心重裝架式、流線爬蟲工兵身軀)",
                "posture": "低重心穩健重裝站姿，右手單持熔爐衝壓巨錘斜架於肩頭，左手握拳置於腰側，身後五節重鋼尾巴穩貼地面作為三腳架支撐，散熱鰭角緩緩微張微合",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "黑曜鎢鋼冷軋薄板頭殼（#2A2B32），面頰兩側覆蓋溫潤奶油米白琺瑯面罩（#FFFDF8），四顆沉頭螺栓穩固密封，雙眼為圓形琥珀澄光高溫光學水晶目鏡（#FFA010）內刻同心圓熔壓刻度計與溫度警戒指針",
                "ears": "頭頂兩側雙聯折疊式耐熱薄銅散熱導流鰭角，由細密薄銅散熱葉片層疊而成，在體內過熱時如同百葉窗般展開釋放微型雪白蒸氣",
                "torso_and_limbs": "主軀幹覆蓋黑曜鎢鋼冷軋薄板件配熔岩暖金飾邊（#D47A2A），四肢關節為冷軋鎢鋼耐熱球窩關節（#4A5568），足部為加寬防滑耐磨合金爪靴配三枚平底抓地齒",
                "tail": "由五節同軸鉸鏈串接的沖壓耐熱重鋼大尾巴，內部裝載耐火石墨潤滑阻尼器，在地面滑行提供穩固三點支撐與揮錘反作用力平衡",
                "weapon_system": "右手單持專屬「熔爐衝壓巨錘（Foundry Stamping Sledgehammer）」，長柄為耐熱合金，四方錘頭具備氣動排氣孔與鍛造鐵砧面，揮動時散逸淡金熱浪，完全符合 0-MKT7 與 viking/hammer 體系，底層掛載 equipment.json 既有 anvil_hammer 與 iron_cudgel"
            },
            "color_palette": {
                "primary": "#2A2B32 (黑曜鎢鋼冷軋薄板主軀幹外殼)",
                "secondary": "#D47A2A (熔岩暖金飾邊與鉸鏈環片)",
                "faceplate": "#FFFDF8 (溫潤奶油米白琺瑯面罩與胸板)",
                "accent": "#FFD028 (金黃齒輪散熱窗、發條鑰匙與工具腰帶)",
                "detail": "#FFA010 (琥珀澄光高溫光學水晶目鏡)",
                "frame": "#4A5568 (冷軋鎢鋼四肢球窩關節與合金長柄)",
                "costume_coral": "#FF5E8A (珊瑚粉紅地熱工兵吊帶飾扣)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_salamander.png (品牌形象立牌)",
                        "web/media/hero/char_salamander.png (官網英雄展示立繪)",
                        "docs/art/magma_salamander_concept.png (概念立繪)",
                        "game/assets/sprites/player/salamander_idle.png (64x64 待機)",
                        "game/assets/sprites/player/salamander_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/salamander_idle.png (隊伍待機)",
                        "game/assets/sprites/player/salamander_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/salamander_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/salamander_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/salamander/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/salamander.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/magma_salamander.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/salamander/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_salamander.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/magma_salamander_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_salamander.png (400x840) [待產出]",
                "web_preview": "web/media/hero/salamander_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/salamander_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/salamander_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/salamander_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/salamander_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/salamander_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/salamander_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/salamander/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/salamander.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/magma_salamander.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/salamander/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 26 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十六大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象/蜥蜴) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    salamander_dir = "game/assets/sprites/player/paperdoll/salamander/"
    if salamander_dir not in races_dirs:
        races_dirs.append(salamander_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/salamander")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/salamander")
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
