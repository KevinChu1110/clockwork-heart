#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slots_spec = {
    "chassis": {
        "slot_id": "chassis",
        "name": "素體底盤",
        "item_id": "chassis_giraffe_sanded_tinplate_default",
        "display_name": "沖壓馬口鐵胡桃拼花矮萌底盤",
    },
    "head_unit": {
        "slot_id": "head_unit",
        "name": "頭部模組",
        "item_id": "head_giraffe_telescoping_periscope_cowl",
        "display_name": "三節黃銅伸縮潛望觀測兜帽",
    },
    "winding_key": {
        "slot_id": "winding_key",
        "name": "發條鑰匙",
        "item_id": "key_giraffe_three_ring_carillon_brass",
        "display_name": "三環鏤空八音音筒發條鑰匙",
    },
    "costume": {
        "slot_id": "costume",
        "name": "外裝服飾",
        "item_id": "costume_giraffe_dawn_herald_woolen_cape",
        "display_name": "晨曦禮賓防風呢絨斗篷披肩",
    },
    "optic_core": {
        "slot_id": "optic_core",
        "name": "光學目鏡",
        "item_id": "face_giraffe_dual_periscope_quartz_lens",
        "display_name": "雙聯潛望測距石英凸透鏡",
    },
    "weapon": {
        "slot_id": "weapon",
        "name": "武器槽位",
        "item_id": "weapon_giraffe_belfry_celestial_bow",
        "display_name": "鐘樓天弦複合機關弓",
        "weapon_type": "bow",
    },
    "back_curio": {
        "slot_id": "back_curio",
        "name": "背部奇物",
        "item_id": "curio_giraffe_pendulum_bob_link_tail",
        "display_name": "微型黃銅鐘擺重錘連桿短尾",
    },
}

giraffe_race_spec = {
    "race_id": "giraffe",
    "aliases": [
        "belfry_giraffe",
        "clocktower_giraffe",
        "periscope_giraffe",
        "dawngaze_giraffe",
        "clockwork_giraffe",
    ],
    "name_zh": "鐘塔長頸鹿",
    "name_en": "The Belfry Giraffe",
    "class_archetype": "遊俠 (Ranger)",
    "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
    "lore_anchor": "穿行於晨曦小鎮·木偶集市「懸吊齒輪鐘樓」、「晨曦天軌 2 號月台」與「齒輪吊索大橋·小鎮站」，巡檢「精紡線莊」、「中央油坊」與「蔓谷天梯引道」，駐守「邊界安全防護彈簧網」，配合提線商會會長·巴納姆、彩釉玩偶夫人·瑪德琳與摺紙工匠·小鶴；通體覆蓋沖壓薄馬口鐵板與打磨胡桃木拼花、三節同軸黃銅伸縮潛望頸管、雙聯黃銅測距雷達角與高折射石英稜鏡、晨曦禮賓防風呢絨披肩、雙聯潛望測距石英凸透鏡、三環鏤空八音音筒發條鑰匙，雙手持握專屬鐘樓天弦複合機關弓，以2.2頭身矮萌微胖體態、多層階梯式黃銅步進蹄、高塔潛望測距看破、八音琴弦諧振連發見長的小鎮天軌守望者與制空遊俠",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末至 20 世紀中葉古典鐵皮發條高塔長頸鹿玩具與維多利亞鐘樓觀測自動偶)",
        "posture": "2.2 頭身矮萌身軀微屈蓄勢，四蹄抓地扎實，右手單手持弓斜指地面，三節黃銅頸管伴隨鐘樓每2秒跳動一格的秒針平穩起伏，三環八音發條鑰匙隨走時均勻旋轉",
        "standee_height_px": 840,
        "standee_width_px": 420,
    },
    "mechanical_features": {
        "head_and_neck": "沖壓薄馬口鐵面甲（#FFFDF8）配三節同軸沖壓黃銅伸縮套管（#FFD028），外露直列減速齒條與導向槽，眼窩處精準中空供 optic_core 穿透",
        "ears": "頭部頂端雙聯沖壓黃銅球形測距儀（#FFD028），末端鑲嵌高折射琥珀石英微型稜鏡（#4ED86A），隨步態微幅自轉，無生物耳廓",
        "torso_and_limbs": "沖壓薄馬口鐵板件（#FFFDF8）嵌合打磨胡桃木拼花（#FFA010），下身配置粗短圓柱形步進腿與多層階梯式黃銅防滑蹄",
        "tail": "細直黃銅擺桿連桿短尾（#FFD028），末端懸掛微型扁圓鐘擺重錘，以固定頻率左右擺動平衡射擊後坐力",
        "weapon_system": "單手挽持專屬「鐘樓天弦複合機關弓（Belfry Celestial-String Composite Bow）」，雙階滑輪傳動，高張力精紡鋼絲金弦，底層掛載 equipment.json 既有 reed_bow (tier 1) 與 hawk_longbow (tier 3)",
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光馬口鐵，面甲眼周高光、腹部內層襯板與關節活動襯墊)",
        "primary": "#FFA010 (主色多巴胺晨曦暖橘，胡桃木拼花裝飾板、披肩主體與弓身幾何彩漆)",
        "secondary": "#4ED86A (次色薄荷冷翡翠，頭頂石英稜鏡、胸口石英透鏡發光刻度與瞄準光斑)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心轉軸螺栓、披肩紐扣與耳廓警示印標)",
        "metal": "#FFD028 (金屬天元黃銅金，三節伸縮頸管、頭頂雷達角、三環發條鑰匙與機械步進蹄)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)",
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_giraffe.png (品牌形象立牌)",
                "web/media/hero/char_giraffe.png (官網英雄展示立繪)",
                "docs/art/belfry_giraffe_concept.png (概念立繪)",
                "game/assets/sprites/player/giraffe_idle.png (64x64 待機)",
                "game/assets/sprites/player/giraffe_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/giraffe_idle.png (隊伍待機)",
                "web/media/hero/giraffe_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/giraffe_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/giraffe_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/giraffe_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/giraffe_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/giraffe_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/giraffe_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/giraffe/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/giraffe.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/giraffe_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/belfry_giraffe.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/giraffe/{slot_id}/{item_id}.png (紙娃娃切片圖層)",
            ],
        },
        "branding_standee": "branding/char_giraffe.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/belfry_giraffe_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_giraffe.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/giraffe_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/giraffe_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/giraffe_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/giraffe_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/giraffe_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/giraffe_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/giraffe_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/giraffe/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/giraffe.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/belfry_giraffe.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/giraffe/{slot_id}/{item_id}.png [待產出]",
    },
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
                    new_var["weapon_type"] = "bow"
                elif sid != "winding_key":
                    new_var["race"] = "giraffe"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    found = False
    for r in races_list:
        if r.get("race_id") == "giraffe":
            found = True
            break
    if not found:
        races_list.append(giraffe_race_spec)

    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("五十三重大種族", "五十四重大種族")
            rule_str = rule_str.replace("五十二重大種族", "五十四重大種族")
            if "鐘塔長頸鹿" not in rule_str:
                rule_str = rule_str.replace(
                    "日晷駱駝雙峰矮萌體態與廢土觀星學者帆布補丁長袍)",
                    "日晷駱駝雙峰矮萌體態與廢土觀星學者帆布補丁長袍、鐘塔長頸鹿三節黃銅伸縮頸管矮萌體態與晨曦禮賓防風呢絨斗篷披肩)",
                )
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    giraffe_dir = "game/assets/sprites/player/paperdoll/giraffe/"
    if giraffe_dir not in races_dirs:
        races_dirs.append(giraffe_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/giraffe")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/giraffe")
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
