#!/usr/bin/env python3
import json
import os
import sys

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILES = [
    os.path.join(repo_root, "docs/design/paperdoll_slots.json"),
    os.path.join(repo_root, "game/data/tables/paperdoll_slots.json")
]

MARMOT_DEFAULT_ITEMS = {
    "chassis": {
        "id": "chassis_marmot_quarry_tinplate_default",
        "name": "碎石耐磨馬口鐵底盤",
        "tier": "common",
        "race": "marmot"
    },
    "head_unit": {
        "id": "head_marmot_alloy_chisel_visor",
        "name": "雙聯合金鑿齒護目面罩",
        "tier": "common",
        "race": "marmot"
    },
    "winding_key": {
        "id": "key_marmot_dual_pawl_brass",
        "name": "雙向棘爪減速黃銅發條鑰匙",
        "tier": "common"
    },
    "costume": {
        "id": "costume_marmot_scavenger_canvas_harness",
        "name": "舊庫拾荒加固帆布工裝胸甲",
        "tier": "common",
        "race": "marmot"
    },
    "optic_core": {
        "id": "face_marmot_amber_dust_goggles",
        "name": "雙聯琥珀防塵石英風鏡",
        "tier": "common",
        "race": "marmot"
    },
    "weapon": {
        "id": "weapon_marmot_eccentric_piston_fists",
        "name": "廢土偏心衝壓機關拳套",
        "tier": "common",
        "weapon_type": "fist"
    },
    "back_curio": {
        "id": "curio_marmot_pneumatic_sand_tail",
        "name": "減震氣動平衡排砂尾",
        "tier": "common",
        "race": "marmot"
    }
}

MARMOT_RACE_SPEC = {
    "race_id": "marmot",
    "aliases": [
        "rockbreaker_marmot",
        "quarry_marmot",
        "piston_marmot",
        "clockwork_marmot",
        "dune_groundhog"
    ],
    "name_zh": "碎石旱獺",
    "name_en": "The Rockbreaker Marmot",
    "class_archetype": "武術家 (Monk)",
    "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
    "lore_anchor": "穿行於荒漠齒輪塚·遺忘舊庫「巨型零件殘骸沙丘」、「零件分揀斜坡裂谷」與「拾荒拼裝聚落·齒輪營地」，巡檢「舊庫重型吊裝龍門架」、「大齒輪懸索天梯·舊庫總站」與「高溫蒸氣除鏽清洗槽」，駐守「冷卻熔渣重力傾卸滑道·舊庫受料口」與「軌道廢棄排障滑道·舊庫分揀倉」，在齒輪營地熬製塗抹高黏度抗氧化除鏽潤滑脂，結伴補丁爺爺、鏽刃阿席與鈴鐺嘟嘟，庇護拾荒拼裝布偶、生鏽發條浪人與發條除鏽工兵偶；通體覆蓋沖壓耐磨馬口鐵底盤與奶油米白隔震襯板、雙聯合金鑿齒護目面罩、雙聯琥珀防塵石英風鏡、舊庫拾荒加固帆布工裝胸甲、減震氣動平衡排砂尾、雙向棘爪減速黃銅發條鑰匙，雙手佩戴專屬廢土偏心衝壓機關拳套，以2.2頭身矮萌扎實身軀、足底黃銅鉚釘扎根步法、偏心連桿高頻活塞衝程與貼身近戰寸勁連打破勢見長的荒原破障武術家",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 昭和發條鐵皮拳擊偶與敲打地鼠自動機)",
        "posture": "2.2 頭身矮萌結實身軀扎馬步抱樁微屈膝，雙足黃銅抓地鉚釘穩踏地面，雙拳佩戴偏心衝壓拳套一前一後微動抱架於胸前，短尾平置地面輔助支撐，背後雙向棘爪發條鑰匙隨舊庫秒針每2.5~3.5秒金屬摩擦聲『喀——嚓！』勻速自轉",
        "standee_height_px": 800,
        "standee_width_px": 540
    },
    "mechanical_features": {
        "ears": "小巧半球形黃銅受音碗耳罩，邊緣飾以微型散熱通風孔，耳根嵌鉚釘固定座",
        "eyes": "雙聯大尺寸琥珀防塵石英風鏡，深藍紫金屬密封圈，浮現落日暖橘同心圓測距刻度與發光指針",
        "teeth": "下顎突出雙聯冷軋沖壓黃銅開山鑿齒，厚度6mm，專門鑿碎卡死齒輪之硬質鏽斑與沉積石塊",
        "tail": "圓柱形短促生鐵馬口鐵排砂尾，內置氣動減震氣缸與旋風排砂濾網，末端飾薄荷綠指示環",
        "torso_and_limbs": "生鐵青灰耐磨馬口鐵沖壓外殼，冷軋鎢鋼自潤滑球鉸關節，雙足底各嵌三枚黃銅圓頭抓地鉚釘",
        "key": "雙向棘爪減速重型黃銅發條鑰匙，外緣帶齒輪棘齒，中心飾有多巴胺珊瑚粉防震鉚釘",
        "weapon_system": "雙手佩戴專屬「廢土偏心衝壓機關拳套（Eccentric Piston Boxing Gauntlets）」，雙聯對稱沖壓護腕，前端雙層鋼砧面配排氣活塞筒，底層掛載 equipment.json 既有 wrap_gloves (tier 1 拳套)"
    },
    "color_palette": {
        "primary": "#5A6E7F (生鐵青灰沖壓耐磨馬口鐵板件)",
        "secondary": "#FFFDF8 (奶油米白腹部抗衝擊隔震襯板與面罩高光)",
        "accent_orange": "#FFA010 (多巴胺落日暖橘衝壓活塞筒身與胸甲警示斜紋)",
        "accent_gold": "#FFD028 (多巴胺天元金黃雙向棘爪發條鑰匙與開山鑿齒)",
        "accent_mint": "#4ED86A (多巴胺薄荷綠氣動壓力表與排砂尾指示環)",
        "accent_blue": "#38A0FF (多巴胺天藍胸甲金屬快拆卡扣與護腕消震墊)",
        "accent_pink": "#FF5E8A (多巴胺珊瑚粉發條鑰匙中心鉚釘與減震膠圈)",
        "canvas_tan": "#D49B4B (舊庫拾荒斑駁耐磨粗帆布工裝胸甲底色)",
        "outline": "#1F1A3A (深藍紫立體手繪描邊)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_marmot.png (品牌形象立牌)",
                "web/media/hero/char_marmot.png (官網英雄展示立繪)",
                "docs/art/rockbreaker_marmot_concept.png (概念立繪)",
                "game/assets/sprites/player/marmot_idle.png (64x64 待機)",
                "game/assets/sprites/player/marmot_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/marmot_idle.png (隊伍待機)",
                "web/media/hero/marmot_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/marmot_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/marmot_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/marmot_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/marmot_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/marmot_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/marmot_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/marmot/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/marmot.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/marmot_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/rockbreaker_marmot.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/marmot/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_marmot.png (520x800 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/rockbreaker_marmot_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_marmot.png (520x800 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/marmot_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/marmot_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/marmot_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/marmot_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/marmot_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/marmot_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/marmot_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/marmot/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/marmot.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/rockbreaker_marmot.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/marmot/{slot_id}/{item_id}.png [待產出]"
    },
    "default_items": {
        "chassis": "chassis_marmot_quarry_tinplate_default",
        "head_unit": "head_marmot_alloy_chisel_visor",
        "optic_core": "face_marmot_amber_dust_goggles",
        "costume": "costume_marmot_scavenger_canvas_harness",
        "back_curio": "curio_marmot_pneumatic_sand_tail",
        "winding_key": "key_marmot_dual_pawl_brass",
        "weapon": "weapon_marmot_eccentric_piston_fists"
    }
}

for file_path in TARGET_FILES:
    print(f"Processing {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Update default_items in slots_architecture.slots
    slots = data["slots_architecture"]["slots"]
    for s in slots:
        slot_id = s["slot_id"]
        if slot_id in MARMOT_DEFAULT_ITEMS:
            item = MARMOT_DEFAULT_ITEMS[slot_id]
            if "default_items" not in s:
                s["default_items"] = []
            existing_ids = [x["id"] for x in s["default_items"]]
            if item["id"] not in existing_ids:
                s["default_items"].append(item)
                print(f"  Added {item['id']} to slot {slot_id} default_items")

    # 2. Update races_specification
    races_spec = data["races_specification"]
    races = races_spec["races"]
    existing_race_ids = [r["race_id"] for r in races]
    if "marmot" not in existing_race_ids:
        races.append(MARMOT_RACE_SPEC)
        print("  Added marmot to races_specification.races")
    races_spec["total_races"] = 64

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    univ = compat.get("universal_slots", [])
    for u in univ:
        if u.get("slot_id") == "winding_key":
            u["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 64 種動物素體"
    adapted = compat.get("race_adapted_slots", [])
    for a in adapted:
        if a.get("slot_id") == "costume":
            old_rule = a.get("rule", "")
            if "碎石旱獺" not in old_rule:
                new_rule = old_rule.replace("六十四重大種族", "六十五重大種族")
                if "星環狐猴象牙白高抗衝擊聚合物底盤與宇航匿蹤輕量安全吊帶胸甲" in new_rule:
                    new_rule = new_rule.replace(
                        "星環狐猴象牙白高抗衝擊聚合物底盤與宇航匿蹤輕量安全吊帶胸甲)",
                        "星環狐猴象牙白高抗衝擊聚合物底盤與宇航匿蹤輕量安全吊帶胸甲、碎石旱獺生鐵青灰耐磨馬口鐵底盤與舊庫拾荒加固帆布工裝胸甲)"
                    )
                a["rule"] = new_rule
                print("  Updated costume rule in race_adapted_slots")

    # 4. Update directory_structure_blueprint
    dir_bp = data.get("directory_structure_blueprint", {}).get("sub_directories", {})
    races_dirs = dir_bp.get("races", [])
    marmot_dir = "game/assets/sprites/player/paperdoll/marmot/"
    if marmot_dir not in races_dirs:
        races_dirs.append(marmot_dir)
        print(f"  Added {marmot_dir} to sub_directories.races")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated {file_path}")

print("Rockbreaker Marmot proposal registered specification complete.")
