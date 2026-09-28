#!/usr/bin/env python3
"""為第三十三族星翼蝙蝠 (The Starwing Bat, bat) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/STARWING_BAT_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 bat 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_bat_astral_polymer_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_bat_astral_polymer_default",
            "name": "星翼蝙蝠極光紫黑航太聚合物素體",
            "race": "bat",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_bat_sonar_parabolic_crest" for v in head_variants):
        head_variants.append({
            "id": "head_bat_sonar_parabolic_crest",
            "name": "雙聯拋物面聲納雷達集音耳",
            "race": "bat",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_bat_orbital_pulsar_key" for v in key_variants):
        key_variants.append({
            "id": "key_bat_orbital_pulsar_key",
            "name": "星穹雙環脈衝發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_bat_orbital_stealth_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_bat_orbital_stealth_harness",
            "name": "星穹失重匿蹤飛行胸甲",
            "race": "bat",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_bat_dual_amber_optic_lens" for v in face_variants):
        face_variants.append({
            "id": "face_bat_dual_amber_optic_lens",
            "name": "雙聯琥珀夜視石英目鏡",
            "race": "bat",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_bat_superconducting_pulse_dart" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_bat_superconducting_pulse_dart",
            "name": "超導脈衝星紋鏢",
            "weapon_type": "dart",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_bat_articulated_starwing_mantle" for v in curio_variants):
        curio_variants.append({
            "id": "curio_bat_articulated_starwing_mantle",
            "name": "六聯折疊螢光星翼披風",
            "race": "bat",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 33

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "bat" for r in races_list):
        races_list.append({
            "race_id": "bat",
            "aliases": [
                "starwing_bat",
                "orbital_bat",
                "astral_bat",
                "pulsar_bat"
            ],
            "name_zh": "星翼蝙蝠",
            "name_en": "The Starwing Bat",
            "class_archetype": "忍者 (Ninja)",
            "origin_realm": "R07 星穹軌道·外星基地 / Starfall Orbit: Polymer Space Station",
            "lore_anchor": "高軌星穹沙盤界域 R07 的失重暗影刺客，平時倒懸棲息於「聚合物太空艙模組」網格，穿梭於「高光懸空螢光軌道」、「太陽能帆板與微型排氣天線」、「太空拼裝維修船塢」、「高壓地熱升空彈射井·軌道受壓對接艙」、「垂直磁浮天軌·星穹軌道月台」與「失重慣性磁力捕捉網」，通體由消光深空極光紫黑航太工程塑料板件、透明聚碳酸酯拋物面聲納雷達耳、雙聯琥珀夜視石英目鏡、六聯折疊螢光星翼披風、星穹失重匿蹤飛行胸甲與星穹雙環脈衝發條鑰匙組裝而成，右手單持專屬超導脈衝星紋鏢，以失重懸停、高頻聲納弱點鎖定與電磁脈衝直線破甲見長的暗影刺客",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版失重忍者偶、雙耳蝠翼反差剪影)",
                "posture": "雙足倒懸磁吸矽膠軟墊爪踏地輕盈，身軀微前傾，身後六聯星翼微幅收攏為斗篷，右手單手持握超導脈衝星紋鏢斜立胸前，左手微曲作失重平衡雷達調頻身姿，雙耳雷達靈活旋轉警戒四周",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "射出成型消光極光紫黑航太塑料頭盔配雙聯拋物面聲納雷達耳，耳廓外緣飾有薄荷綠螢光電路（#4ED86A），額頭兩側嵌有黃銅齒圈環繞的雙聯高透琥珀金夜視石英偏光目鏡（#FFD028 / #FFA010）與內置點陣LED瞄準刻度",
                "ears": "頭頂半透明聚碳酸酯雙聯拋物面聲納雷達集音耳，內置黃銅微型集音網與步進馬達，可360度獨立旋轉感應空間站氣壓震動與秒針跳格波紋",
                "torso_and_limbs": "主軀幹覆蓋消光深空極光紫黑工程塑料板件（#1F1A3A）與象牙米白琺瑯防護前甲（#FFFDF8），四肢為曜黑球窩關節（#2B2836）配珊瑚粉防塵矽膠圈（#FF5E8A），足部為四指輕量化合金卡扣配倒懸磁吸矽膠減震墊",
                "tail": "由背部延伸之六聯折疊螢光星翼披風，高韌性POM骨架夾持天藍發光冷凝薄膜（#38A0FF），收攏時如忍者短斗篷，跳躍滑翔時如折扇向兩側張開成蝠翼",
                "weapon_system": "右手單持專屬「超導脈衝星紋鏢（Superconducting Pulse Astral Shuriken）」，直徑約 32px，外環為六瓣高精度超導電磁薄刃，中央嵌有一枚脈衝螢光微型陀螺儀核心，完全符合 0-MKT7 與 ninja/dart 體系，底層掛載 equipment.json 既有 shadow_chakram 與 mist_darts"
            },
            "color_palette": {
                "primary": "#1F1A3A (消光深空極光紫黑航太工程塑料主軀幹裝甲、頭罩與外殼板件)",
                "secondary": "#2B2836 (曜黑關節鉸鏈、手足耐磨件與翼骨框架)",
                "accent": "#FFD028 (太陽琥珀金雙聯石英夜視目鏡、脈衝星紋鏢刃尖端高光)",
                "neon_mint": "#4ED86A (多巴胺螢光薄荷綠耳廓聲納電路、翼膜邊緣飾條與狀態指示燈)",
                "electric_sky": "#38A0FF (航太電光天藍星翼發光冷凝液、胸甲指示燈與等離子尾跡)",
                "coral_pulse": "#FF5E8A (脈衝珊瑚粉矽膠磁吸腳爪減震墊、微型洩壓閥密封圈與能量卡扣)",
                "enamel_ivory": "#FFFDF8 (象牙米白琺瑯胸腹模組化防護板與面頰裝甲陶瓷襯板)",
                "outline": "#2E1F18 (深暖褐手繪厚描邊，確保深邃宇宙背景中輪廓清晰立體)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_bat.png (品牌形象立牌)",
                        "web/media/hero/char_bat.png (官網英雄展示立繪)",
                        "docs/art/starwing_bat_concept.png (概念立繪)",
                        "game/assets/sprites/player/bat_idle.png (64x64 待機)",
                        "game/assets/sprites/player/bat_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/bat_idle.png (隊伍待機)",
                        "game/assets/sprites/player/bat_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/bat_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/bat_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/bat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/bat.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/starwing_bat.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/bat/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_bat.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/starwing_bat_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_bat.png (400x840) [待產出]",
                "web_preview": "web/media/hero/bat_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/bat_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/bat_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/bat_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/bat_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/bat_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/bat_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/bat/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/bat.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/starwing_bat.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/bat/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 33 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十三大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    bat_dir = "game/assets/sprites/player/paperdoll/bat/"
    if bat_dir not in races_dirs:
        races_dirs.append(bat_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/bat")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/bat")
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
