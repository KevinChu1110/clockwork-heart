#!/usr/bin/env python3
"""為第三十五族稜鏡孔雀 (The Prism Peacock, peacock) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/PRISM_PEACOCK_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 peacock 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_peacock_glazed_porcelain_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_peacock_glazed_porcelain_default",
            "name": "稜鏡孔雀彩釉琺瑯金屬素體",
            "race": "peacock",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_peacock_baroque_diadem_prism" for v in head_variants):
        head_variants.append({
            "id": "head_peacock_baroque_diadem_prism",
            "name": "巴洛克冠羽稜鏡天線",
            "race": "peacock",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_peacock_filigree_sunburst_key" for v in key_variants):
        key_variants.append({
            "id": "key_peacock_filigree_sunburst_key",
            "name": "晨曦巴洛克日曜鏤空發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_peacock_marionette_court_cuirass" for v in costume_variants):
        costume_variants.append({
            "id": "costume_peacock_marionette_court_cuirass",
            "name": "木偶宮廷巴洛克金線胸甲",
            "race": "peacock",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_peacock_kaleidoscope_gem_lens" for v in face_variants):
        face_variants.append({
            "id": "face_peacock_kaleidoscope_gem_lens",
            "name": "萬花筒雙色寶石折光透鏡",
            "race": "peacock",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_peacock_kaleidoscope_prism_focus" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_peacock_kaleidoscope_prism_focus",
            "name": "萬花筒聚能稜鏡",
            "weapon_type": "crystal",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_peacock_articulated_kaleidoscope_fan" for v in curio_variants):
        curio_variants.append({
            "id": "curio_peacock_articulated_kaleidoscope_fan",
            "name": "鉸接萬花筒機械開屏晶扇",
            "race": "peacock",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 35

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "peacock" for r in races_list):
        races_list.append({
            "race_id": "peacock",
            "aliases": [
                "prism_peacock",
                "kaleidoscope_peacock",
                "baroque_peacock",
                "dawn_peacock"
            ],
            "name_zh": "稜鏡孔雀",
            "name_en": "The Prism Peacock",
            "class_archetype": "法師 (Mage)",
            "origin_realm": "R02 晨曦小鎮·木偶集市 / Dawn Town: Marionette Bazaar",
            "lore_anchor": "穿梭於晨曦小鎮「懸吊齒輪鐘樓」與「石板街道集市」之間，巡守於「齒輪吊索大橋·小鎮站」、「晨曦天軌 2 號月台」、「蔓谷天梯引道」、「邊界安全防護彈簧網」、「精紡線莊」與「中央油坊」，通體由帝國孔雀藍彩釉琺瑯與拋光黃銅板件、巴洛克冠羽稜鏡天線、萬花筒雙色寶石折光透鏡、木偶宮廷巴洛克金線胸甲、鉸接萬花筒機械開屏晶扇與晨曦巴洛克日曜鏤空發條鑰匙組裝而成，右手單持專屬萬花筒聚能稜鏡，以優雅芭蕾身姿、全方位光學護盾與萬花折光織盾成刃見長的光學法師",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版光學自動偶、修長芭蕾站姿與開屏晶扇剪影)",
                "posture": "雙足包覆防滑矽膠軟木墊的小巧芭蕾鞋金屬足板踏地優雅，身軀挺拔，左手輕捏宮廷禮儀指法置於腰際，右手單手托舉萬花筒聚能稜鏡斜立身前，背部鉸接機械開屏晶扇微幅舒張，目鏡寶石隨呼吸泛起柔和晨曦微光",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "三聯拋光黃銅鉸接活動細桿構成的巴洛克皇冠天線，頂端各鑲嵌淚滴形多面石英稜鏡，面部嵌有黃銅齒圈環繞的萬花筒雙色寶石折光透鏡（左眼深邃帝國藍寶石 #1B4965、右眼祖母綠翡翠 #4ED86A），內部帶微型行星齒輪",
                "ears": "頭部兩側微型黃銅齒輪集音耳軸與百葉透氣孔，伴隨呼吸節奏微幅開闔並感應鐘樓走時光學傳感器共振",
                "torso_and_limbs": "主軀幹覆蓋帝國孔雀藍彩釉琺瑯金屬板件（#1B4965）與木偶宮廷巴洛克金線胸甲（#FFF8E7 / #FFD028），腹部帶精密微縮擒縱調速窗，雙腿為修長雙層套筒黃銅機械腿配高精度外露球窩關節，足底為小巧芭蕾鞋金屬掌板",
                "tail": "背部鉸接萬花筒機械開屏晶扇，由9根鍍金黃銅連桿搭載18枚八角石英稜鏡組成，背部中央主齒輪箱核心插裝晨曦巴洛克日曜鏤空發條鑰匙",
                "weapon_system": "右手單持專屬「萬花筒聚能稜鏡（Kaleidoscope Prism Focus）」，八角黃銅懸浮座內漂浮天藍（#38A0FF）與翡翠綠雙色結晶聚能水晶，完全符合 0-MKT7 與 mage/crystal 體系，底層掛載 equipment.json 既有 prism_scepter 與 shard_focus"
            },
            "color_palette": {
                "primary": "#1B4965 (彩釉琺瑯金屬外殼主色，深邃尊貴孔雀藍)",
                "secondary": "#FFD028 (多巴胺金黃拋光黃銅骨架、巴洛克卷草花紋與日曜發條鑰匙)",
                "accent": "#FFF8E7 (晨曦柔光米白陶瓷胸甲面甲底色，溫潤明亮)",
                "kaleido_mint": "#4ED86A (萬花筒翡翠綠右眼鏡片、稜鏡反射折射光澤)",
                "ruby_crimson": "#E63946 (寶石胡桃鉗紅胸前飾扣、肩甲滾邊與開屏連桿軸心點綴)",
                "prism_sky": "#38A0FF (稜鏡天藍水晶聚能核心、光學光幕與護盾射線)",
                "amethyst_purple": "#8338EC (丁香紫晶發條鑰匙軸承寶石、冠羽折射輔助光暈)",
                "outline": "#2E1F18 (深暖褐手繪外輪廓立體描邊，確保歐風石板背景中清晰立體)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_peacock.png (品牌形象立牌)",
                        "web/media/hero/char_peacock.png (官網英雄展示立繪)",
                        "docs/art/prism_peacock_concept.png (概念立繪)",
                        "game/assets/sprites/player/peacock_idle.png (64x64 待機)",
                        "game/assets/sprites/player/peacock_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/peacock_idle.png (隊伍待機)",
                        "game/assets/sprites/player/peacock_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/peacock_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/peacock_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/peacock/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/peacock.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/prism_peacock.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/peacock/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_peacock.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/prism_peacock_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_peacock.png (400x840) [待產出]",
                "web_preview": "web/media/hero/peacock_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/peacock_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/peacock_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/peacock_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/peacock_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/peacock_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/peacock_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/peacock/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/peacock.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/prism_peacock.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/peacock/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 35 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十五大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    peacock_dir = "game/assets/sprites/player/paperdoll/peacock/"
    if peacock_dir not in races_dirs:
        races_dirs.append(peacock_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/peacock")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/peacock")
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
