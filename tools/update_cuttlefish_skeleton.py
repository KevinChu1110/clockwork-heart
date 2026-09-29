#!/usr/bin/env python3
import json
import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slots_spec = {
  "chassis": {
    "slot_id": "chassis",
    "name": "素體底盤",
    "item_id": "chassis_cuttlefish_abyssal_cyan_default",
    "display_name": "鍍鈦合金與琉璃海藍搪瓷素體底盤"
  },
  "head_unit": {
    "slot_id": "head_unit",
    "name": "頭部模組",
    "item_id": "head_cuttlefish_diving_cowl_fins",
    "display_name": "深潛圓頂頭盔與氣動平衡側鰭"
  },
  "winding_key": {
    "slot_id": "winding_key",
    "name": "發條鑰匙",
    "item_id": "key_cuttlefish_tri_vane_turbine_brass",
    "display_name": "三葉深海渦輪水流發條鑰匙"
  },
  "costume": {
    "slot_id": "costume",
    "name": "外裝服飾",
    "item_id": "costume_cuttlefish_abyssal_shinobi_cuirass",
    "display_name": "海淵夜行輕量耐壓背心"
  },
  "optic_core": {
    "slot_id": "optic_core",
    "name": "光學目鏡",
    "item_id": "face_cuttlefish_dual_quartz_optic_lens",
    "display_name": "雙聯水下耐壓石英探照目鏡"
  },
  "weapon": {
    "slot_id": "weapon",
    "name": "武器槽位",
    "item_id": "weapon_cuttlefish_abyssal_inksmoke_dagger",
    "display_name": "海淵墨影雙鋒匕"
  },
  "back_curio": {
    "slot_id": "back_curio",
    "name": "背部奇物",
    "item_id": "curio_cuttlefish_pneumatic_ink_siphon",
    "display_name": "氣動高壓發煙雙聯墨囊氣罐"
  }
}

cuttlefish_race_spec = {
    "race_id": "cuttlefish",
    "aliases": ["inksmoke_cuttlefish", "abyssal_cuttlefish", "mimic_cuttlefish", "clockwork_cuttlefish"],
    "name_zh": "墨影烏賊",
    "name_en": "The Inksmoke Cuttlefish",
    "class_archetype": "忍者 (Ninja)",
    "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
    "lore_anchor": "穿行於琉璃汪洋·發條海淵「海淵地表與馬賽克步道」、「發條珊瑚群」與「水下發條宮殿與氧氣泡罩」，巡檢「磷光水母街燈與流體排氣柱」、「水下丁達爾藍晶光柱」與「天頂巨型青銅錨鏈秒針」，駐守「深淵排污豎井管道·耐壓吊籠」、「晨曦天軌 5 號深海浮標月台」與「深海熱液湧泉管道」，配合小黃鴨船長·舵手巴克、海馬信差·碧浪與深海鐘錶貝·珠貝長老；通體覆蓋高抗壓防腐鍍鈦薄板外殼與琉璃海藍搪瓷底盤、深潛圓頂頭盔與氣動平衡側鰭、三葉深海渦輪水流發條鑰匙、海淵夜行輕量耐壓背心、雙聯水下耐壓石英探照目鏡、氣動高壓發煙雙聯墨囊氣罐，右手反握專屬海淵墨影雙鋒匕，以2.2頭身流線型體態、四對分節軟鋼機械觸肢滾足、流體阻尼水下煙幕遁術、弱點死角連刺見長的深海暗影匿蹤忍者",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末古典鐵皮發條潛水烏賊玩具與鐘錶水下氣動發煙機關偶)",
        "posture": "2.2 頭身矮萌身軀微伏，四對短小金屬觸肢抓地平穩，右手反握主鋒匕橫於胸前，左手短匕斜指向下，三葉渦輪發條鑰匙隨海淵秒針律動沉穩旋轉",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "一體沖壓成型鐘形鍍鈦深潛頭盔（#38A0FF），頂部裝配黃銅洩壓閥門（#FFD028），兩側對稱鉸接一對薄沖壓黃銅波浪平衡側鰭，眼窩處精準中空供 optic_core 穿透",
        "ears": "頭部兩側對稱鉸接薄沖壓黃銅波浪平衡側鰭（#FFD028），隨水流與走時律動微動，無生物耳廓",
        "torso_and_limbs": "高抗壓防腐沖壓鍍鈦薄板外殼（#38A0FF）嵌合象牙白防滑陶瓷釉襯板（#FFFDF8），下身配置四對分節軟鋼機械觸肢滾足與耐磨橡膠吸盤",
        "tail": "背部上側裝載雙聯垂直排列沖壓鍍鈦氣動高壓發煙墨囊氣罐（#38A0FF），頂部配備微型氣壓表與虹吸發煙噴嘴，底部連接柔性黃銅編織輸氣軟管",
        "weapon_system": "右手單手反握主短匕於身前、左爪持副匕微屈護胸專屬「海淵墨影雙鋒匕（Abyssal Inksmoke Twin Daggers）」，雙持鍍鈦弧刃短匕帶深藍流體導槽，底層掛載 equipment.json 既有 star_fang (tier 2) 與 nebula_needle (tier 3)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光鋁鎳金屬，面甲眼周高光、腹部內層襯板與關節活動襯墊)",
        "primary": "#38A0FF (主色多巴胺海天藍，沖壓鍍鈦圓頂頭盔外殼、側鰭主體、雙鋒短匕護手與背部氣罐塗裝)",
        "secondary": "#4ED86A (次色薄荷冷翡翠，石英目鏡內部刻度發光圈、側鰭邊緣防撞膠條與短匕刃面高光)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，發條鑰匙中心轉軸鉚釘、氣罐壓力警戒指針與頭頂洩壓氣閥按鈕)",
        "metal": "#FFD028 (金屬天元黃銅金與海軍深藍防鏽漆板 #1A3558，深海發條鐘錶玩具精緻感)",
        "outline": "#1F1A3A (深藍紫/深暖褐手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_cuttlefish.png (品牌形象立牌)",
                "web/media/hero/char_cuttlefish.png (官網英雄展示立繪)",
                "docs/art/inksmoke_cuttlefish_concept.png (概念立繪)",
                "game/assets/sprites/player/cuttlefish_idle.png (64x64 待機)",
                "game/assets/sprites/player/cuttlefish_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/cuttlefish_idle.png (隊伍待機)",
                "web/media/hero/cuttlefish_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/cuttlefish_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/cuttlefish_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/cuttlefish_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/cuttlefish_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/cuttlefish_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/cuttlefish_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/cuttlefish/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/cuttlefish.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/cuttlefish_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/inksmoke_cuttlefish.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/cuttlefish/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_cuttlefish.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/inksmoke_cuttlefish_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_cuttlefish.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/cuttlefish_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/cuttlefish_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/cuttlefish_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/cuttlefish_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/cuttlefish_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/cuttlefish_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/cuttlefish_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/cuttlefish/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/cuttlefish.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/inksmoke_cuttlefish.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/cuttlefish/{slot_id}/{item_id}.png [待產出]"
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
                    "tier": "common"
                }
                if sid == "weapon":
                    new_var["weapon_type"] = "dagger"
                elif sid != "winding_key":
                    new_var["race"] = "cuttlefish"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    if not any(r.get("race_id") == "cuttlefish" for r in races_list):
        races_list.append(cuttlefish_race_spec)

    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("五十重大種族", "五十一重大種族")
            if "墨影烏賊" not in rule_str:
                rule_str = rule_str.replace("蔓谷深林工兵板甲)", "蔓谷深林工兵板甲、墨影烏賊流線型體態與海淵夜行輕量耐壓背心)")
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    cuttlefish_dir = "game/assets/sprites/player/paperdoll/cuttlefish/"
    if cuttlefish_dir not in races_dirs:
        races_dirs.append(cuttlefish_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/cuttlefish")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/cuttlefish")
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
