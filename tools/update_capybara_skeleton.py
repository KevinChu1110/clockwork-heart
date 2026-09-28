#!/usr/bin/env python3
"""為第四十七族澄心水豚 (The Serene Capybara, capybara) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/SERENE_CAPYBARA_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 capybara 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_capybara_porcelain_timber_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_capybara_porcelain_timber_default",
            "name": "溫潤青瓷椴木禪意底盤",
            "race": "capybara",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_capybara_zen_monk_cowl_hat" for v in head_variants):
        head_variants.append({
            "id": "head_capybara_zen_monk_cowl_hat",
            "name": "天元禪修竹笠斗笠",
            "race": "capybara",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_capybara_bamboo_dual_ring_gold" for v in key_variants):
        key_variants.append({
            "id": "key_capybara_bamboo_dual_ring_gold",
            "name": "三葉竹節雙環金黃發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_capybara_tea_ceremony_wrap" for v in costume_variants):
        costume_variants.append({
            "id": "costume_capybara_tea_ceremony_wrap",
            "name": "道場茶道防塵練功袍",
            "race": "capybara",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_capybara_amber_zen_lens" for v in face_variants):
        face_variants.append({
            "id": "face_capybara_amber_zen_lens",
            "name": "安詳微瞇琥珀石英目鏡",
            "race": "capybara",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_capybara_serene_taiji_crystal" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_capybara_serene_taiji_crystal",
            "name": "澄心太極護體靈晶",
            "weapon_type": "crystal",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_capybara_steaming_tea_kettle_backpack" for v in curio_variants):
        curio_variants.append({
            "id": "curio_capybara_steaming_tea_kettle_backpack",
            "name": "地熱竹香茶爐背包",
            "race": "capybara",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_list = races_spec["races"]

    if not any(r.get("race_id") == "capybara" for r in races_list):
        races_list.append({
            "race_id": "capybara",
            "aliases": [
                "serene_capybara",
                "zen_capybara",
                "clockwork_capybara",
                "crystal_capybara"
            ],
            "name_zh": "澄心水豚",
            "name_en": "The Serene Capybara",
            "class_archetype": "法師 (Mage)",
            "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
            "lore_anchor": "漫步於竹影道場·天元竹林「發條天元竹海」與「青石武鬥古道場·演武坪」，巡防「山門竹煙茶舍」、「飛瀑木簧水碓」、「古老重型零件輸送翻斗軌道·竹林終端站」、「晨曦天軌 9 號演武道場月台」、「凌雲青竹懸索天梯·道場總站」、「天元雲海風帆渡口」與「翠竹彈力阻尼編織網」，並駐守「山門竹煙茶舍」，配合陶瓷熊貓武僧、木雕竹葉青蛇、演武木人童子、煮茶發條偶·阿茶與醉步發條武鬥熊貓·阿波泰坦；通體覆蓋溫潤生漆象牙白青瓷板件與高剛性打磨椴木、天元禪修竹笠斗笠、三葉竹節雙環金黃發條鑰匙、道場茶道防塵練功袍、安詳微瞇琥珀石英目鏡、地熱竹香茶爐背包，右手單持專屬澄心太極護體靈晶，以太極流體阻尼化勁、活得久耗得起、安詳定力織盾成刃見長的天元竹海禪意護盾法師",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (古典東方發條茶道伺服機械偶、浴盆發條水豚動作玩偶與禪意斗笠剪影)",
                "posture": "側身 45 度穩健立正，雙足穩踏地面，身形微微下沉，右手掌心微托懸浮之澄心太極護體靈晶，左掌微屈結定心禪印，神情安詳恬淡，背後茶爐背包裊裊吐出一縷白煙，三葉竹節發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "天然椴木精雕方鈍面罩與雙孔微型黃銅排氣水閥，眼窩精準挖空中空，臉頰兩側帶有珊瑚粉微型散熱孔",
                "ears": "沖壓半圓黃銅回音小耳廓，內置微型音叉片，隨聲波微幅震顫",
                "torso_and_limbs": "象牙米白青瓷板件（#FFFDF8）與打磨椴木複合榫卯結構，腹部嵌裝高透石英視窗可見黃銅平衡陀；四肢短粗沉穩外露純平黃銅螺栓與球窩關節",
                "tail": "扁平圓形黃銅減速陀飛輪洩壓蓋，表面平雕太極游絲紋路，內裝微型平衡陀維持重心，無生物肉質尾",
                "weapon_system": "右手單持專屬「澄心太極護體靈晶（Serene Taiji Shield Crystal）」，八角青玉盤嵌裝雙同軸反向旋轉黃銅太極齒輪環與浮空玉刃，完全符合 0-MKT7 與 mage/crystal 體系，底層掛載 equipment.json 既有 prism_scepter (tier 3) 與 shard_focus (tier 1)"
            },
            "color_palette": {
                "primary": "#FFFDF8 (基底象牙奶油白，青瓷面甲、胸膛主色與道場練功袍裡襯)",
                "secondary": "#4ED86A (主色竹翠綠，澄心太極靈晶本體、青瓷漸層釉色與斗笠邊緣飾線)",
                "brass_gear": "#FFD028 (裝飾多巴胺金黃，三葉竹節發條鑰匙、靈晶黃銅太極外環與目鏡)",
                "accent_gold": "#FFA010 (裝飾暖橘，斗笠頂部發條小金橘配重塊、茶道結飾與茶爐火苗透鏡)",
                "core_cyan": "#38A0FF (提神天藍，靈晶運轉光暈、目鏡施法高光與清泉法陣符文)",
                "blush_coral": "#FF5E8A (腮紅珊瑚粉，鼻吻兩側微型散熱孔與茶道服領口結繩)",
                "outline": "#1F1A3A (深暖褐/深藍紫手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_capybara.png (品牌形象立牌)",
                        "web/media/hero/char_capybara.png (官網英雄展示立繪)",
                        "docs/art/serene_capybara_concept.png (概念立繪)",
                        "game/assets/sprites/player/capybara_idle.png (64x64 待機)",
                        "game/assets/sprites/player/capybara_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/capybara_idle.png (隊伍待機)",
                        "web/media/hero/capybara_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/capybara_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/capybara_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/capybara_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/capybara_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/capybara_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/capybara_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/capybara/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/capybara.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/capybara_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/serene_capybara.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/capybara/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_capybara.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/serene_capybara_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_capybara.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/capybara_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/capybara_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/capybara_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/capybara_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/capybara_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/capybara_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/capybara_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/capybara/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/capybara.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/serene_capybara.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/capybara/{slot_id}/{item_id}.png [待產出]"
            }
        })

    races_spec["total_races"] = len(races_list)

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            base_rule = f"四十七重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲、撼地野牛粗獷寬厚駝峰重甲與舊庫拆解工兵胸甲、巡管守宮靈敏扁平爬壁體態與耐熱暗忍胸甲、破星蜜獾平頂抗衝擊體態與軌道防護工裝、澄心水豚溫潤方鈍體態與道場茶道防塵練功袍) 由渲染器微調縮放適配"
            item["rule"] = base_rule

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    capybara_dir = "game/assets/sprites/player/paperdoll/capybara/"
    if capybara_dir not in races_dirs:
        races_dirs.append(capybara_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/capybara")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/capybara")
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
