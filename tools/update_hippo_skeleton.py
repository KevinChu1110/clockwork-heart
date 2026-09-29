#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slots_spec = {
    "chassis": {
        "slot_id": "chassis",
        "name": "素體底盤",
        "item_id": "chassis_hippo_thick_cast_brass_default",
        "display_name": "沖壓厚鑄黃銅鎢鋼矮萌底盤",
    },
    "head_unit": {
        "slot_id": "head_unit",
        "name": "頭部模組",
        "item_id": "head_hippo_ballast_safety_valve_cowl",
        "display_name": "沖壓金屬面甲活動大頜兜帽",
    },
    "winding_key": {
        "slot_id": "winding_key",
        "name": "發條鑰匙",
        "item_id": "key_hippo_dual_valve_handwheel_brass",
        "display_name": "雙聯閥門輪轂黃銅發條鑰匙",
    },
    "costume": {
        "slot_id": "costume",
        "name": "外裝服飾",
        "item_id": "costume_hippo_greatcog_high_pressure_cuirass",
        "display_name": "巨輪城重裝抗震高壓鉚釘胸甲",
    },
    "optic_core": {
        "slot_id": "optic_core",
        "name": "光學目鏡",
        "item_id": "face_hippo_dual_pressure_gauge_quartz_lens",
        "display_name": "雙聯同軸高壓石英壓力表目鏡",
    },
    "weapon": {
        "slot_id": "weapon",
        "name": "武器槽位",
        "item_id": "weapon_hippo_steamvalve_piston_heavy_lance",
        "display_name": "重閥活塞衝刺長槍",
        "weapon_type": "spear",
    },
    "back_curio": {
        "slot_id": "back_curio",
        "name": "背部奇物",
        "item_id": "curio_hippo_dual_steam_exhaust_ballast_tail",
        "display_name": "雙聯蒸氣排氣壓載水箱短尾",
    },
}

hippo_race_spec = {
    "race_id": "hippo",
    "aliases": [
        "steamvalve_hippo",
        "ballast_hippo",
        "pressure_hippo",
        "greatcog_hippo",
        "clockwork_hippo"
    ],
    "name_zh": "重閥河馬",
    "name_en": "The Steamvalve Hippo",
    "class_archetype": "騎士 (Knight)",
    "origin_realm": "R04 黃銅都市·巨輪城 / Brass Metropolis: The Great Cog City",
    "lore_anchor": "穿行於黃銅都市·巨輪城「摩天齒輪工坊群」、「高壓蒸氣管道網」與「高架重軌引橋·巨輪城站」，巡檢「自律工廠與天街吊橋」與「中央蒸氣沐浴池」，駐守防護「磁吸緩衝防墜鋼網」，配合總工技師·銅齒、管道巡檢員·小鎢與老鐘錶匠·星擺；通體覆蓋沖壓厚鑄黃銅板件與冷軋鎢鋼骨架、雙聯旋轉式微型氣壓安全洩壓閥門耳、雙聯同軸高壓石英壓力表目鏡、巨輪城重裝抗震高壓鉚釘胸甲、雙聯蒸氣排氣壓載水箱、雙聯閥門輪轂黃銅發條鑰匙，雙手持握專屬重閥活塞衝刺長槍，以2.2頭身矮萌微胖體態、四足活塞減震金屬蹄、蒸氣超壓衝程、沉穩低重心防禦反震見長的巨輪城防衛者與鋼鐵壁壘騎士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1930s-1950s 古典鐵皮發條河馬自動機與維多利亞蒸氣管道洩壓自動檢測偶)",
        "posture": "2.2 頭身矮萌身軀沉穩屹立，四足活塞蹄扎實抓地，右手單手持長槍斜指前方，雙耳微型洩壓閥門伴隨秒針每1.5秒跳動一格規律旋轉排氣，雙聯閥門手輪發條鑰匙隨走時均勻自轉",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "沖壓厚鑄黃銅面甲（#FFFDF8 / #FFA010）配可活動式金屬大頜，內置黃銅冷卻進氣散熱隔柵，眼窩處精準沖孔供 optic_core 穿透",
        "ears": "頭部頂端雙聯旋轉式微型黃銅安全洩壓閥（#FFD028），外圈帶有珊瑚粉超壓警示環，隨走時排氣自轉，無生物耳廓",
        "torso_and_limbs": "沖壓厚鑄耐壓黃銅板件（#FFA010）包覆冷軋鎢鋼框架，下身配置四足圓柱形活塞避震腿與加厚黃銅防滑蹄蓋",
        "tail": "圓柱形微型黃銅壓載水箱與錐形排水閥短尾（#FFA010 / #FFD028），以固定重量提供低重心衝鋒配重平衡",
        "weapon_system": "單手挽持專屬「重閥活塞衝刺長槍（Steamvalve Piston Heavy Lance）」，槍身內置雙腔往復活塞，突刺時釋放高壓蒸氣二次加速，底層掛載 equipment.json 既有 knight_pike (tier 1) 與 ash_spear (tier 2/3)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光馬口鐵，面部前頜高光、腹部抗震襯板與活動襯墊)",
        "primary": "#FFA010 (主色多巴胺巨輪暖橘，厚鑄黃銅外殼、胸甲塗裝與長槍配重段)",
        "secondary": "#4ED86A (次色薄荷冷翡翠，眼部壓力表盤背光、長槍導壓液發光線與瞄準刻度)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，洩壓閥安全指示環、胸甲應急拉閥與排風標籤)",
        "metal": "#FFD028 (金屬天元黃銅金，長槍主槍管、發條閥門手輪鑰匙、四足活塞管與面頰齒輪)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_hippo.png (品牌形象立牌)",
                "web/media/hero/char_hippo.png (官網英雄展示立繪)",
                "docs/art/steamvalve_hippo_concept.png (概念立繪)",
                "game/assets/sprites/player/hippo_idle.png (64x64 待機)",
                "game/assets/sprites/player/hippo_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/hippo_idle.png (隊伍待機)",
                "web/media/hero/hippo_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/hippo_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/hippo_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/hippo_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/hippo_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/hippo_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/hippo_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/hippo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/hippo.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/hippo_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/steamvalve_hippo.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/hippo/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_hippo.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/steamvalve_hippo_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_hippo.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/hippo_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/hippo_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/hippo_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/hippo_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/hippo_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/hippo_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/hippo_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/hippo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/hippo.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/steamvalve_hippo.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/hippo/{slot_id}/{item_id}.png [待產出]"
    }
}

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slots = data["slots_architecture"]["slots"]

    for slot_obj in slots:
        sid = slot_obj["slot_id"]
        if sid in slots_spec:
            item_info = slots_spec[sid]
            var_id = item_info["item_id"]
            if not any(v.get("id") == var_id for v in slot_obj["sample_variants"]):
                new_var = {
                    "id": var_id,
                    "name": item_info["display_name"],
                    "tier": "common",
                }
                if sid == "weapon":
                    new_var["weapon_type"] = item_info.get("weapon_type", "spear")
                elif sid != "winding_key":
                    new_var["race"] = "hippo"
                slot_obj["sample_variants"].append(new_var)

    races_list = [r for r in data["races_specification"]["races"] if r.get("race_id") != "mole"]
    found = False
    for i, r in enumerate(races_list):
        if r.get("race_id") == "hippo":
            found = True
            races_list[i] = hippo_race_spec
            break
    if not found:
        races_list.append(hippo_race_spec)

    data["races_specification"]["races"] = races_list
    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("五十四重大種族", "五十五重大種族")
            rule_str = rule_str.replace("五十三重大種族", "五十五重大種族")
            rule_str = rule_str.replace("五十二重大種族", "五十五重大種族")
            if "重閥河馬" not in rule_str:
                rule_str = rule_str.replace(
                    "鐘塔長頸鹿三節黃銅伸縮頸管矮萌體態與晨曦禮賓防風呢絨斗篷披肩)",
                    "鐘塔長頸鹿三節黃銅伸縮頸管矮萌體態與晨曦禮賓防風呢絨斗篷披肩、重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲)"
                )
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    hippo_dir = "game/assets/sprites/player/paperdoll/hippo/"
    if hippo_dir not in races_dirs:
        races_dirs.append(hippo_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/hippo")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/hippo")
    os.makedirs(poses_dir, exist_ok=True)
    poses_keep = os.path.join(poses_dir, ".gitkeep")
    if not os.path.exists(poses_keep):
        with open(poses_keep, "w") as f:
            pass
        print(f"建立 {poses_keep}")

if __name__ == "__main__":
    create_gitkeeps(repo_root)
    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        update_paperdoll_slots(os.path.join(repo_root, p))
