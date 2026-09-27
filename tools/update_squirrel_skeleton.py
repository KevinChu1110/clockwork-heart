#!/usr/bin/env python3
"""為第二十五族巡林松鼠 (squirrel) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/design/TIMBER_SQUIRREL_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 squirrel 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_squirrel_chestnut_bronze_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_squirrel_chestnut_bronze_default",
            "name": "巡林松鼠原廠栗木暖褐沖壓銅板素體",
            "race": "squirrel",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_squirrel_timber_fencer_beret" for v in head_variants):
        head_variants.append({
            "id": "head_squirrel_timber_fencer_beret",
            "name": "折疊薄銅耳與巡林擊劍貝雷帽",
            "race": "squirrel",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_squirrel_acorn_filigree" for v in key_variants):
        key_variants.append({
            "id": "key_squirrel_acorn_filigree",
            "name": "三環橡果鏤空黃銅發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_squirrel_canopy_courier_harness" for v in costume_variants):
        costume_variants.append({
            "id": "costume_squirrel_canopy_courier_harness",
            "name": "林冠信差遊俠短披風與擊劍皮扣裝甲",
            "race": "squirrel",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_squirrel_mint_crosshair_lens" for v in face_variants):
        face_variants.append({
            "id": "face_squirrel_mint_crosshair_lens",
            "name": "薄荷嫩綠十字準星光學目鏡",
            "race": "squirrel",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_squirrel_emerald_clockwork_foil" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_squirrel_emerald_clockwork_foil",
            "name": "翡翠發條細劍",
            "weapon_type": "sword",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_squirrel_articulated_cog_gyro_tail" for v in curio_variants):
        curio_variants.append({
            "id": "curio_squirrel_articulated_cog_gyro_tail",
            "name": "九節鉸鏈同軸沖壓鏤空黃銅齒輪陀螺大尾巴",
            "race": "squirrel",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 25

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "squirrel" for r in races_list):
        races_list.append({
            "race_id": "squirrel",
            "aliases": [
                "timber_squirrel",
                "canopy_squirrel",
                "emerald_squirrel",
                "courier_squirrel"
            ],
            "name_zh": "巡林松鼠",
            "name_en": "The Timber Squirrel",
            "class_archetype": "騎士 (Knight)",
            "origin_realm": "R03 翡翠深林·發條蔓谷 / Emerald Woods: Vine & Gear Forest",
            "lore_anchor": "常駐於翡翠深林「巨木樹屋聚落」與「觀風石碑塔」的發條巡林信差，穿梭於「蔓谷天梯引道」、「發條藤蔓彈射平台」與「高架重軌引橋」之間，通體由沖壓栗木暖褐薄銅板件、溫潤奶油米白琺瑯面頰、折疊薄銅耳與擊劍貝雷帽、薄荷嫩綠光學水晶目鏡、三環橡果鏤空黃銅發條鑰匙與九節齒輪陀螺大尾巴組裝而成，以右手單持翡翠發條細劍、林間靈巧騰躍與停拍看破突刺見長的林冠擊劍客",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (西洋花劍擊劍架式、靈巧林冠信差身軀)",
                "posture": "靈巧擊劍戒備架式，右手單持翡翠發條細劍斜指斜下方，左手微曲收束於腰間維持平衡，身後九節齒輪蓬鬆大尾巴微幅擺動，背部三環橡果鏤空黃銅鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓栗木暖褐薄銅頭殼，配有溫潤奶油米白琺瑯面頰板與雙顆外露微型沉頭螺釘，頭頂斜戴翡翠墨綠微縮金屬貝雷帽配金色發條飛羽，雙眼為圓形薄荷嫩綠光學水晶目鏡內刻同心圓十字準星",
                "ears": "雙聯折疊式薄銅風向感知耳，耳根由雙軸黃銅萬向節鉸鏈支撐，耳背帶有杏仁金橙色導角漆面與風向刻度槽，隨林間風向靈活微幅偏轉",
                "torso_and_limbs": "背部與軀幹覆蓋沖壓栗木暖褐薄銅板件（#8B5A2B），面頰與胸腹前側為溫潤奶油米白琺瑯板件（#FFFDF8），四肢關節為冷軋鎢鋼球窩鉸鏈（#4A5568），足部為防滑耐磨工程橡膠金屬爪靴配三枚抓地齒",
                "tail": "由九節同軸鉸鏈串接的沖壓鏤空黃銅齒輪蓬鬆大尾巴，中央貫穿彈性軟鋼絲傳動軸與高轉速陀螺平衡儀，待機時豎立微幅擺動，突刺時展開維持動態平衡",
                "weapon_system": "右手單持專利「翡翠發條細劍 / 穿林機關花劍」，金黃鏤空齒輪圓盤護手配鎢鋼刻度細針刃，左手自然微曲收束維持平衡，完全符合 0-MKT7 與 knight/sword 體系，底層掛載 equipment.json 既有 meager_edge 與 knight_saber"
            },
            "color_palette": {
                "primary": "#8B5A2B (沖壓栗木暖褐薄銅板件)",
                "secondary": "#FFFDF8 (溫潤奶油米白琺瑯面頰與前胸護板)",
                "accent": "#FFD028 (多巴胺金黃三環橡果發條鑰匙與齒輪搭扣)",
                "detail": "#4ED86A (薄荷嫩綠光學水晶目鏡與細劍晶核)",
                "warm_highlight": "#D27D2D (杏仁金橙大尾巴外層齒輪片與耳背飾板)",
                "costume_emerald": "#2D8A4E (深林翡翠墨綠短披風與擊劍貝雷帽)",
                "titanium_frame": "#4A5568 (冷軋鎢鋼四肢球窩關節與細針刃劍身)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_squirrel.png (品牌形象立牌)",
                        "web/media/hero/char_squirrel.png (官網英雄展示立繪)",
                        "docs/art/timber_squirrel_concept.png (概念立繪)",
                        "game/assets/sprites/player/squirrel_idle.png (64x64 待機)",
                        "game/assets/sprites/player/squirrel_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/squirrel_idle.png (隊伍待機)",
                        "game/assets/sprites/player/squirrel_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/squirrel_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/squirrel_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/squirrel/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/squirrel.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/timber_squirrel.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/squirrel/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_squirrel.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/timber_squirrel_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_squirrel.png (400x840) [待產出]",
                "web_preview": "web/media/hero/squirrel_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/squirrel_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/squirrel_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/squirrel_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/squirrel_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/squirrel_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/squirrel_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/squirrel/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/squirrel.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/timber_squirrel.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/squirrel/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 25 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "二十五大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    squirrel_dir = "game/assets/sprites/player/paperdoll/squirrel/"
    if squirrel_dir not in races_dirs:
        races_dirs.append(squirrel_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/squirrel")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/squirrel")
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
