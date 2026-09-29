#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slots_spec = {
  "chassis": {
    "slot_id": "chassis",
    "name": "素體底盤",
    "item_id": "chassis_camel_sanded_tinplate_default",
    "display_name": "磨砂馬口鐵雙峰矮萌素體底盤"
  },
  "head_unit": {
    "slot_id": "head_unit",
    "name": "頭部模組",
    "item_id": "head_camel_sundial_gnomon_cowl",
    "display_name": "日晷晷針折光觀測兜帽"
  },
  "winding_key": {
    "slot_id": "winding_key",
    "name": "發條鑰匙",
    "item_id": "key_camel_armillary_dial_brass",
    "display_name": "黃銅日晷雙環刻度發條鑰匙"
  },
  "costume": {
    "slot_id": "costume",
    "name": "外裝服飾",
    "item_id": "costume_camel_scavenger_astronomer_robe",
    "display_name": "廢土觀星學者帆布補丁長袍"
  },
  "optic_core": {
    "slot_id": "optic_core",
    "name": "光學目鏡",
    "item_id": "face_camel_dual_spectroscope_quartz_lens",
    "display_name": "雙聯光譜分折石英目鏡"
  },
  "weapon": {
    "slot_id": "weapon",
    "name": "武器槽位",
    "item_id": "weapon_camel_sundial_refraction_rod",
    "display_name": "廢土日晷折射短杖",
    "weapon_type": "magic"
  },
  "back_curio": {
    "slot_id": "back_curio",
    "name": "背部奇物",
    "item_id": "curio_camel_twin_condenser_humps",
    "display_name": "雙聯散熱油壺金屬駝峰"
  }
}

camel_race_spec = {
    "race_id": "camel",
    "aliases": ["sundial_camel", "meridian_camel", "caravan_camel", "dune_camel", "clockwork_camel"],
    "name_zh": "日晷駱駝",
    "name_en": "The Sundial Camel",
    "class_archetype": "法師 (Mage)",
    "origin_realm": "R08 荒漠齒輪塚·遺忘舊庫 / Rust Waste: The Forgotten Junkyard",
    "lore_anchor": "穿行於荒漠齒輪塚·遺忘舊庫「巨型零件殘骸沙丘」、「拾荒拼裝聚落·齒輪營地」與「舊庫重型吊裝龍門架」，守望「零件分揀斜坡裂谷」，引導商隊穿梭於「冷卻熔渣重力傾卸滑道·舊庫受料口」、「軌道廢棄排障滑道·舊庫分揀倉」、「大齒輪懸索天梯·舊庫總站」與「古老重型零件輸送翻斗軌道」，避開危險的「廢料沉降磁吸緩衝沙漏」，配合拾荒拼裝大師·補丁爺爺、流浪發條劍客·鏽刃阿席、發條小駱駝·鈴鐺嘟嘟與發條除鏽工兵偶；通體覆蓋沖壓耐磨馬口鐵板件與雙聯金屬潤滑油壺駝峰、黃銅日晷晷針兜帽、黃銅日晷雙環刻度發條鑰匙、廢土觀星學者帆布補丁長袍、雙聯光譜分折石英目鏡、雙聯散熱油壺金屬駝峰，右手持握專屬廢土日晷折射短杖，以2.2頭身矮萌圓潤體態、短粗金屬小蹄步進、捕捉廷得耳金黃光束、日冕折射轟擊見長的荒漠星象法師",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末至 20 世紀中葉古典鐵皮發條沙漠商隊駱駝玩具與鐘錶日晷天文自動偶)",
        "posture": "2.2 頭身矮萌身軀穩立沙地，四隻金屬小蹄均勻分擔體重，右手單持廢土日晷短杖斜立身側，左手平屈微托，雙峰中央日晷發條鑰匙隨走時律動勻速旋轉",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "耐磨砂土棕帆布兜帽（#D49B4B），前額固定沖壓黃銅日晷額冠（#FFD028），中央矗立一枚微型折疊式合金日晷晷針，眼窩處精準中空供 optic_core 探出",
        "ears": "兜帽兩側垂掛防風護耳銅片與微型黃銅小鈴鐺（#FFD028），隨步態與微風輕微擺動，無生物耳廓",
        "torso_and_limbs": "沖壓耐磨馬口鐵板件（#3A322D）邊緣暖金黃銅包邊（#FFD028），下身配置四足模壓深褐硬質防滑橡膠馬蹄（#1F1A3A）與微型螺旋減震彈簧",
        "tail": "背部雙峰中央偏後方咬合黃銅日晷雙環刻度發條鑰匙，雙峰為雙聯微型除鏽潤滑油壺金屬駝峰（#FFD028），排氣閥規律噴出細小白蒸氣圈",
        "weapon_system": "右手單手持握專屬「廢土日晷折射短杖（Wasteland Sundial Refraction Rod）」，頂部日晷圓盤與六角石英晶核折射日光，底層掛載 equipment.json 既有 star_rod (tier 1) 與 void_quill (tier 5)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白陶瓷釉/奶油米白帆布底襯，面部基板與關節襯墊)",
        "primary": "#FFD028 (主色多巴胺天元金黃，黃銅日晷額冠、發條鑰匙與駝峰油罐塗裝)",
        "secondary": "#4ED86A (次色薄荷冷翡翠，石英晶核刻度光柵與目鏡光斑高光)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，軸承密封圈與注油蓋密封墊點綴)",
        "metal": "#FFA010 (金屬日照暖橘與熟褐馬口鐵面 #3A322D，沙漠商隊發條玩具質感)",
        "outline": "#1F1A3A (深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_camel.png (品牌形象立牌)",
                "web/media/hero/char_camel.png (官網英雄展示立繪)",
                "docs/art/sundial_camel_concept.png (概念立繪)",
                "game/assets/sprites/player/camel_idle.png (64x64 待機)",
                "game/assets/sprites/player/camel_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/camel_idle.png (隊伍待機)",
                "web/media/hero/camel_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/camel_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/camel_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/camel_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/camel_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/camel_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/camel_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/camel/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/camel.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/camel_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/sundial_camel.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/camel/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_camel.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/sundial_camel_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_camel.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/camel_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/camel_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/camel_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/camel_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/camel_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/camel_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/camel_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/camel/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/camel.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/sundial_camel.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/camel/{slot_id}/{item_id}.png [待產出]"
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
                    new_var["weapon_type"] = "magic"
                elif sid != "winding_key":
                    new_var["race"] = "camel"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    if not any(r.get("race_id") == "camel" for r in races_list):
        races_list.append(camel_race_spec)

    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("五十二重大種族", "五十三重大種族")
            rule_str = rule_str.replace("五十一重大種族", "五十三重大種族")
            if "日晷駱駝" not in rule_str:
                rule_str = rule_str.replace("熔爐工兵重裝石磚胸甲)", "熔爐工兵重裝石磚胸甲、日晷駱駝雙峰矮萌體態與廢土觀星學者帆布補丁長袍)")
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    camel_dir = "game/assets/sprites/player/paperdoll/camel/"
    if camel_dir not in races_dirs:
        races_dirs.append(camel_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/camel")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/camel")
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
