#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slots_spec = {
  "chassis": {
    "slot_id": "chassis",
    "name": "素體底盤",
    "item_id": "chassis_crab_molten_iron_default",
    "display_name": "鑄鐵鍛爐矮萌甲殼素體底盤"
  },
  "head_unit": {
    "slot_id": "head_unit",
    "name": "頭部模組",
    "item_id": "head_crab_periscope_visor_cowl",
    "display_name": "雙向潛望測距護額頭盔"
  },
  "winding_key": {
    "slot_id": "winding_key",
    "name": "發條鑰匙",
    "item_id": "key_crab_quad_flue_crucible_t_bar",
    "display_name": "四葉散熱鍛造發條鑰匙"
  },
  "costume": {
    "slot_id": "costume",
    "name": "外裝服飾",
    "item_id": "costume_crab_furnace_sapper_cuirass",
    "display_name": "熔爐工兵重裝石磚胸甲"
  },
  "optic_core": {
    "slot_id": "optic_core",
    "name": "光學目鏡",
    "item_id": "face_crab_dual_gauge_convex_lens",
    "display_name": "雙聯壓力儀表石英凸透鏡"
  },
  "weapon": {
    "slot_id": "weapon",
    "name": "武器槽位",
    "item_id": "weapon_crab_obsidian_stamping_fist",
    "display_name": "黑曜衝壓熔岩拳套",
    "weapon_type": "fist"
  },
  "back_curio": {
    "slot_id": "back_curio",
    "name": "背部奇物",
    "item_id": "curio_crab_pneumatic_exhaust_chimney",
    "display_name": "雙聯氣動洩壓排煙煙囪"
  }
}

crab_race_spec = {
    "race_id": "crab",
    "aliases": ["anvil_crab", "crucible_crab", "molten_crab", "boxer_crab", "clockwork_crab"],
    "name_zh": "熔砧石蟹",
    "name_en": "The Anvil Crab",
    "class_archetype": "武術家 (Monk)",
    "origin_realm": "R06 赤焰熔爐·鍛造火山 / Molten Foundry: Crucible Volcano",
    "lore_anchor": "穿行於赤焰熔爐·鍛造火山「重型鍛造工坊與衝壓懸橋」、「黑曜淬火石磚步道」與「金色液態鐵水熔池」，巡檢「耐火排煙管樹」、「黃銅洩壓儀表塔」與「晨曦天軌 6 號熔爐重載貨運月台」，駐守「高壓地熱噴射升空彈射井」、「火山口中央鍛造神壇」與「黑曜石淬火神壇」，配合矮人鐵匠大師·重錘布隆、陶土魔像學徒·黏土泥泥與熔爐溫控長老·坩堝老爹；通體覆蓋沖壓粗獷鑄鐵板件與黑曜石淬火耐火磚、雙向潛望測距護額頭盔、四葉散熱鍛造發條鑰匙、熔爐工兵重裝石磚胸甲、雙聯壓力儀表石英凸透鏡、雙聯氣動洩壓排煙煙囪，雙手持握專屬黑曜衝壓熔岩拳套，以2.2頭身矮萌微胖體態、三對同軸黃銅步進滾足、熔爐高頻衝壓拳法、橫行碎步閃避見長的火山重裝近身格鬥武道家",
    "proportions": {
        "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末至 20 世紀中葉古典鐵皮發條橫行拳擊蟹玩具與鐘錶氣動鍛打機關偶)",
        "posture": "2.2 頭身矮萌身軀微蹲扎穩低馬步，六足抓地平穩，右手主拳套橫抬於胸前護面，左手副拳套斜指前下方蓄勢，四葉發條鑰匙隨熔爐每1.5秒急促跳動一格的律動輕快轉動",
        "standee_height_px": 840,
        "standee_width_px": 420
    },
    "mechanical_features": {
        "head_and_neck": "沖壓厚鑄生鐵護額拱蓋（#2A272A），外漆赤焰暖橘高溫防銹漆（#FFA010），頂部伸出一對雙向旋轉黃銅潛望式石英測距筒（#FFD028），眼窩處精準中空供 optic_core 穿透",
        "ears": "頭部頂部雙向旋轉黃銅潛望式石英測距目鏡筒（#FFD028），隨橫行步態與走時律動獨立旋轉，無生物耳廓",
        "torso_and_limbs": "沖壓高耐熱粗獷鑄鐵板件（#2A272A）嵌合象牙白耐火陶瓷釉板（#FFFDF8），下身配置三對同軸黃銅步進滾足與耐磨橡膠防滑爪",
        "tail": "背部兩側裝配一對直立沖壓生鐵小型排煙管（#2A272A），頂部配備活動式薄銅洩壓蓋板（#FFD028），出拳時有節律地噴出微型白色蒸氣環",
        "weapon_system": "右手單手持握主拳套高舉護面、左手副拳套收於腰側專屬「黑曜衝壓熔岩拳套（Obsidian Stamping Magma Gauntlets）」，雙手黑曜石鍛造拳套嵌裝熔岩流光受力板，底層掛載 equipment.json 既有 wrap_gloves (tier 1) 與 iron_knuckle (tier 3)"
    },
    "color_palette": {
        "base": "#FFFDF8 (基底象牙白陶瓷釉/精磨耐熱耐火石磚，腹底襯板與關節活動襯墊)",
        "primary": "#FFA010 (主色多巴胺赤焰暖橘，護額高溫防銹漆面、胸甲防撞條與拳套熔岩流光塗裝)",
        "secondary": "#4ED86A (次色薄荷冷翡翠，石英儀表刻度光柵與微型指針高光)",
        "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，高溫預警鉚釘與關節轉軸密封圈)",
        "metal": "#FFD028 (金屬天元黃銅金與熔岩金黃漆面，鍛造黃銅發條鑰匙與潛望鏡筒)",
        "outline": "#1F1A3A (深藍紫/黑曜石手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
    },
    "asset_naming_conventions": {
        "status": {
            "existing": [],
            "pending": [
                "branding/char_crab.png (品牌形象立牌)",
                "web/media/hero/char_crab.png (官網英雄展示立繪)",
                "docs/art/anvil_crab_concept.png (概念立繪)",
                "game/assets/sprites/player/crab_idle.png (64x64 待機)",
                "game/assets/sprites/player/crab_idle_x3.png (128x128 待機)",
                "game/assets/sprites/player/party/crab_idle.png (隊伍待機)",
                "web/media/hero/crab_idle.png (128x128 官網待機)",
                "game/assets/sprites/player/showcase/crab_idle_hd.png (800x1200 HD 展示立繪)",
                "game/assets/sprites/player/crab_battle.png (128x128 戰鬥特寫姿態)",
                "game/assets/sprites/player/crab_battle_512.png (512x512 戰鬥特寫姿態)",
                "game/assets/sprites/player/crab_walk_{0..3}.png (64x64 行走動畫)",
                "game/assets/sprites/player/crab_walk_{0..3}_x3.png (128x128 行走動畫)",
                "game/assets/sprites/player/crab_walk_{0..3}_512.png (512x512 行走動畫)",
                "game/assets/sprites/player/poses/crab/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                "game/assets/sprites/portraits/crab.png (HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/crab_512.png (512x512 HUD 戰鬥頭像)",
                "game/assets/sprites/portraits/anvil_crab.png (對話半身像)",
                "game/assets/sprites/player/paperdoll/crab/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            ]
        },
        "branding_standee": "branding/char_crab.png (420x840 -> 1344x1680) [待產出]",
        "branding_concept_art": "docs/art/anvil_crab_concept.png (928x1152) [待產出]",
        "web_hero": "web/media/hero/char_crab.png (420x840 -> 1344x1680) [待產出]",
        "web_preview": "web/media/hero/crab_idle.png (128x128) [待產出]",
        "game_sprite_idle_base": "game/assets/sprites/player/crab_idle.png (64x64) [待產出]",
        "game_sprite_idle_hi": "game/assets/sprites/player/crab_idle_x3.png (128x128) [待產出]",
        "game_sprite_party_idle": "game/assets/sprites/player/party/crab_idle.png (128x128) [待產出]",
        "game_sprite_battle": "game/assets/sprites/player/crab_battle.png (128x128) [待產出]",
        "game_sprite_walk": "game/assets/sprites/player/crab_walk_{0..3}.png (64x64) [待產出]",
        "game_sprite_walk_hi": "game/assets/sprites/player/crab_walk_{0..3}_x3.png (128x128) [待產出]",
        "game_action_poses": "game/assets/sprites/player/poses/crab/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
        "portrait_hud": "game/assets/sprites/portraits/crab.png (128x128) [待產出]",
        "portrait_dialogue": "game/assets/sprites/portraits/anvil_crab.png (384x480) [待產出]",
        "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/crab/{slot_id}/{item_id}.png [待產出]"
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
                    new_var["weapon_type"] = "fist"
                elif sid != "winding_key":
                    new_var["race"] = "crab"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    if not any(r.get("race_id") == "crab" for r in races_list):
        races_list.append(crab_race_spec)

    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("五十一重大種族", "五十二重大種族")
            rule_str = rule_str.replace("五十重大種族", "五十二重大種族")
            if "熔砧石蟹" not in rule_str:
                rule_str = rule_str.replace("海淵夜行輕量耐壓背心)", "海淵夜行輕量耐壓背心、熔砧石蟹矮萌微胖體態與熔爐工兵重裝石磚胸甲)")
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    crab_dir = "game/assets/sprites/player/paperdoll/crab/"
    if crab_dir not in races_dirs:
        races_dirs.append(crab_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/crab")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/crab")
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
