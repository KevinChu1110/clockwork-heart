#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slots_spec = {
    "chassis": {
        "slot_id": "chassis",
        "name": "素體底盤",
        "item_id": "chassis_mole_milky_polymer_default",
        "display_name": "乳白工程塑料合金採礦爪矮萌底盤",
    },
    "head_unit": {
        "slot_id": "head_unit",
        "name": "頭部模組",
        "item_id": "head_mole_orbital_mining_visor_cowl",
        "display_name": "防爆聚碳酸酯採礦護目兜帽",
    },
    "winding_key": {
        "slot_id": "winding_key",
        "name": "發條鑰匙",
        "item_id": "key_mole_four_vane_antenna_brass",
        "display_name": "四葉微型發條天線鑰匙",
    },
    "costume": {
        "slot_id": "costume",
        "name": "外裝服飾",
        "item_id": "costume_mole_orbital_sapper_dungarees",
        "display_name": "軌道高抗衝擊防護工裝背帶褲",
    },
    "optic_core": {
        "slot_id": "optic_core",
        "name": "光學目鏡",
        "item_id": "face_mole_amber_led_mining_visor_lens",
        "display_name": "琥珀點陣LED採礦護目目鏡",
    },
    "weapon": {
        "slot_id": "weapon",
        "name": "武器槽位",
        "item_id": "weapon_mole_orbital_plasma_sledgehammer",
        "display_name": "星穹高頻等離子重鎚",
        "weapon_type": "hammer",
    },
    "back_curio": {
        "slot_id": "back_curio",
        "name": "背部奇物",
        "item_id": "curio_mole_cold_gas_thruster_tail",
        "display_name": "圓筒微型冷氣反推噴嘴短尾",
    },
}

mole_race_spec = {
    "race_id": "mole",
    "aliases": [
        "asteroid_mole",
        "prospector_mole",
        "orbital_mole",
        "space_mole",
        "clockwork_mole"
    ],
    "name_zh": "星岩鼴鼠",
    "name_en": "The Asteroid Mole",
    "class_archetype": "戰士 (Viking)",
    "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
    "lore_anchor": "巡弋於星穹軌道·外星基地「聚合物太空艙模組」與「高光懸空螢光軌道」，巡檢「太陽能帆板與微型排氣天線」與「太空拼裝維修船塢」，守望「高壓地熱升空彈射井·軌道受壓對接艙」與「垂直磁浮天軌·星穹軌道月台」，維護清理「軌道廢棄排障滑道」，依託防護「失重慣性磁力捕捉網」，並在「高真空抗靜電除塵室」保養除塵，配合宇航機器人隊長·螺栓隊長、太空發條小狗·萊卡波波與軌道站資深工程師·光纖婆婆；通體覆蓋高密度乳白工程塑料板件（ABS/POM）與冷軋鎢鋼骨架、防爆聚碳酸酯採礦護目頭盔、雙聯超導微型雷達葉片耳、軌道高抗衝擊防護工裝背帶褲、琥珀點陣LED採礦護目目鏡、圓筒形微型冷氣反推短尾、四葉微型發條天線鑰匙，雙手持握專屬星穹高頻等離子重鎚，以2.2頭身矮萌微胖體態、四足磁吸防滑工程矽膠吸盤滾足、失重磁吸定點霸體、高頻電漿震盪碎岩見長的高軌空間站採礦工程師與鋼鐵重裝戰士",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (1950s-1970s 古典鐵皮發條掘地鼴鼠與太空探索工程自動偶)",
        "posture": "2.2 頭身矮萌身軀沉穩屹立，四足磁吸吸盤牢牢吸附地面，雙爪平穩握持等離子重鎚立於身前偏右，背部冷氣噴管微幅排氣，天線發條鑰匙隨秒針每3.0秒跳拍一格勻速旋轉",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "乳白高密度工程塑料圓形面甲（#FFFDF8 / #38A0FF），前端配備防爆聚碳酸酯採礦護目罩與黃銅微型過濾閥，眼窩處精準中空供 optic_core 穿透",
        "ears": "頭部兩側對稱安裝雙聯超導微型雷達葉片耳（#FFD028 / #4ED86A），超薄黃銅片與薄荷光纖編織，隨走時脈衝微幅自轉，無生物耳廓",
        "torso_and_limbs": "高密度工程塑料板件（#FFFDF8）包覆冷軋鎢鋼框架，雙臂為重型沖壓合金多齒採礦爪，下身配置四足圓柱形腿部與防滑耐磨磁吸矽膠吸盤滾足",
        "tail": "短粗圓筒形高密度塑料冷氣反推排氣噴嘴（#38A0FF / #FF5E8A），末端帶珊瑚粉防撞橡膠環與四孔定向反推微型噴孔",
        "weapon_system": "單手挽持專屬「星穹高頻等離子重鎚（Orbital Plasma Sledgehammer）」，透明聚碳酸酯鎚身內嵌高頻電漿環，下砸釋放引力震盪，底層掛載 equipment.json 既有 anvil_hammer (tier 1)、iron_cudgel (tier 2) 與 bastion_blade (tier 3)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白工程塑料/拋光鋁鎳金屬，面罩基座高光、腹部抗靜電襯板與活動襯墊)",
        "primary": "#38A0FF (主色多巴胺天藍，太空採礦防護外殼、胸甲塗裝與重鎚鎚頭外罩)",
        "secondary": "#4ED86A (次色薄荷冷翡翠，雷達天線導光纖維、等離子重鎚聚能環與面罩刻度光圈)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，冷氣反推噴嘴防撞環、重鎚過載指示燈與發條軸心按鈕)",
        "metal": "#FFD028 (金屬天元黃銅金，四葉發條天線鑰匙、採礦爪同軸齒輪與重鎚金屬握柄)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_mole.png (品牌形象立牌)",
                "web/media/hero/char_mole.png (官網英雄展示立繪)",
                "docs/art/asteroid_mole_concept.png (概念立繪)",
                "game/assets/sprites/player/mole_idle.png (64x64 待機)",
                "game/assets/sprites/player/mole_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/mole_idle.png (隊伍待機)",
                "web/media/hero/mole_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/mole_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/mole_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/mole_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/mole_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/mole_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/mole_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/mole/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/mole.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/mole_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/asteroid_mole.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/mole/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_mole.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/asteroid_mole_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_mole.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/mole_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/mole_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/mole_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/mole_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/mole_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/mole_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/mole_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/mole/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/mole.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/asteroid_mole.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/mole/{slot_id}/{item_id}.png [待產出]"
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
                    new_var["weapon_type"] = item_info.get("weapon_type", "hammer")
                elif sid != "winding_key":
                    new_var["race"] = "mole"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    found = False
    for i, r in enumerate(races_list):
        if r.get("race_id") == "mole":
            found = True
            races_list[i] = mole_race_spec
            break
    if not found:
        races_list.append(mole_race_spec)

    data["races_specification"]["races"] = races_list
    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("五十五重大種族", "五十七重大種族")
            rule_str = rule_str.replace("五十六重大種族", "五十七重大種族")
            rule_str = rule_str.replace("五十四重大種族", "五十七重大種族")
            if "星岩鼴鼠" not in rule_str:
                if "重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲)" in rule_str:
                    rule_str = rule_str.replace(
                        "重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲)",
                        "重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲、星岩鼴鼠乳白工程塑料矮萌體態與軌道高抗衝擊防護工裝背帶褲)"
                    )
                elif "重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲" in rule_str:
                    rule_str = rule_str.replace(
                        "重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲",
                        "重閥河馬沖壓厚鑄耐壓黃銅矮萌體態與巨輪城重裝抗震高壓鉚釘胸甲、星岩鼴鼠乳白工程塑料矮萌體態與軌道高抗衝擊防護工裝背帶褲"
                    )
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    mole_dir = "game/assets/sprites/player/paperdoll/mole/"
    if mole_dir not in races_dirs:
        races_dirs.append(mole_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/mole")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/mole")
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
