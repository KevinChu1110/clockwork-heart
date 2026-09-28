#!/usr/bin/env python3
"""為第三十一族破浪旗魚 (The Hydrofoil Sailfish, sailfish) 建立資料表骨架與 7 大部件槽位空目錄。
依據 docs/world/HYDROFOIL_SAILFISH_DESIGN_PROPOSAL.md 與 paperdoll_slots.json 規範。
"""

import json
import os
import sys

def update_paperdoll_slots(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 7 大槽位加入 sailfish 預設樣品
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "chassis_sailfish_abyssal_titanium_default" for v in chassis_variants):
        chassis_variants.append({
            "id": "chassis_sailfish_abyssal_titanium_default",
            "name": "破浪旗魚深海鍍鈦骨架素體",
            "race": "sailfish",
            "tier": "common"
        })

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_sailfish_hydrofoil_visor_crest" for v in head_variants):
        head_variants.append({
            "id": "head_sailfish_hydrofoil_visor_crest",
            "name": "深潛騎士折疊導流鰭盔",
            "race": "sailfish",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_sailfish_abyssal_helm_trident" for v in key_variants):
        key_variants.append({
            "id": "key_sailfish_abyssal_helm_trident",
            "name": "深海三叉舵輪發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_sailfish_abyssal_knight_cuirass" for v in costume_variants):
        costume_variants.append({
            "id": "costume_sailfish_abyssal_knight_cuirass",
            "name": "海淵深潛騎士重裝護胸甲",
            "race": "sailfish",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    face_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "face_sailfish_dual_abyssal_optic_lens" for v in face_variants):
        face_variants.append({
            "id": "face_sailfish_dual_abyssal_optic_lens",
            "name": "雙聯深海石英同心刻度目鏡",
            "race": "sailfish",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "weapon_sailfish_hydrofoil_lance" for v in weapon_variants):
        weapon_variants.append({
            "id": "weapon_sailfish_hydrofoil_lance",
            "name": "破浪螺旋合金衝刺長槍",
            "weapon_type": "spear",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_sailfish_clockwork_sailfin_mantle" for v in curio_variants):
        curio_variants.append({
            "id": "curio_sailfish_clockwork_sailfin_mantle",
            "name": "多節聯動發條折疊背鰭帆",
            "race": "sailfish",
            "tier": "common"
        })

    # 2. races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 31

    races_list = races_spec["races"]

    if not any(r.get("race_id") == "sailfish" for r in races_list):
        races_list.append({
            "race_id": "sailfish",
            "aliases": [
                "hydrofoil_sailfish",
                "abyssal_sailfish",
                "wave_sailfish",
                "streamline_sailfish"
            ],
            "name_zh": "破浪旗魚",
            "name_en": "The Hydrofoil Sailfish",
            "class_archetype": "騎士 (Knight)",
            "origin_realm": "R05 琉璃汪洋·發條海淵 / Crystal Ocean: The Clockwork Abyss",
            "lore_anchor": "穿梭於琉璃汪洋「水下發條宮殿與氧氣泡罩」與「海淵地表與馬賽克步道」的深淵巡洋長，穿梭於「發條珊瑚群」與「磷光水母街燈與流體排氣柱」之間，巡守於「深淵排污豎井管道·耐壓吊籠」與「晨曦天軌 5 號深海浮標月台」，通體由象牙白陶瓷胸腹護板、深海陽極氧化鈷藍鍍鈦板件、雙聯深海石英同心刻度目鏡、多節聯動發條折疊背鰭帆與深海三叉舵輪發條鑰匙組裝而成，右手單持專屬破浪螺旋合金衝刺長槍，以洋流阻尼破浪突刺、精準迎擊與深海衝鋒見長的深海騎士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (可愛Q版水生騎士偶、流線破浪剪影)",
                "posture": "雙足流線型金屬短靴與防滑橡膠吸盤墊踏地穩健，身軀微前傾，右手持握破浪螺旋合金長槍斜立於身側，左手微曲作流體控場平衡身姿，身後背鰭帆與推進尾翼協同錨定水流",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "沖壓成型耐壓深海鍍鈦頭殼配水滴流線導流鰭冠，表面飾有亮橘與珊瑚金警示條紋，前額整合防爆石英面罩，兩側嵌有黃銅齒圈環繞的雙聯深海石英同心刻度目鏡（#38A0FF / #FFD028），吻端為精緻合金錐台",
                "ears": "頭冠兩側微型流體減阻導流腮孔與內部黃銅微型耳軸，感應深海亂流震動與秒針跳格波紋",
                "torso_and_limbs": "主軀幹覆蓋深海陽極氧化鈷藍鍍鈦板件（#1E3A8A）與象牙白陶瓷胸腹護板（#FFFDF8），四肢關節為鍍鈦球窩鉸鏈配薄荷碧綠防壓密封圈，手足為流線型金屬短靴配防滑高黏度橡膠吸盤墊",
                "tail": "由雙向差速小齒輪驅動的雙葉流體擺動推進尾翼，走動時靈動擺動，保持 2.2 頭身重心平衡",
                "weapon_system": "右手單持專屬「破浪螺旋合金衝刺長槍（Hydrofoil Spiral Piercing Lance）」，槍身長約 40px，由鍍鈦輕量槍桿、微型發條推進閥護手盤與螺旋鎢鋼破浪錐構成，完全符合 0-MKT7 與 knight/spear 體系，底層掛載 equipment.json 既有 knight_pike 與 ash_spear"
            },
            "color_palette": {
                "primary": "#FFFDF8 (象牙白胸腹陶瓷護板、面頰流線底漆與長槍握把)",
                "secondary": "#1E3A8A (深海陽極氧化鈷藍主軀幹鍍鈦外殼、背鰭帆主葉片與頭盔甲板)",
                "accent": "#FFD028 (珊瑚暖金三叉舵輪發條鑰匙、長槍配重環與海錨浮雕)",
                "optic_cyan": "#38A0FF (波光天藍雙聯石英目鏡、水流高光反光層與刻度指示光標)",
                "alert_orange": "#FFA010 (亮橘警示導流鰭冠條紋與水壓洩壓閥)",
                "accent_mint": "#4ED86A (薄荷碧綠磷光水流指示線與關節密封墊圈)",
                "frame_silver": "#E2E8F0 (珠光銀灰傳動鎢鋼齒輪、螺旋破浪長槍刀錐與球窩關節)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_sailfish.png (品牌形象立牌)",
                        "web/media/hero/char_sailfish.png (官網英雄展示立繪)",
                        "docs/art/hydrofoil_sailfish_concept.png (概念立繪)",
                        "game/assets/sprites/player/sailfish_idle.png (64x64 待機)",
                        "game/assets/sprites/player/sailfish_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/sailfish_idle.png (隊伍待機)",
                        "game/assets/sprites/player/sailfish_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/sailfish_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/sailfish_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/poses/sailfish/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/sailfish.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/hydrofoil_sailfish.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/sailfish/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_sailfish.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/hydrofoil_sailfish_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_sailfish.png (400x840) [待產出]",
                "web_preview": "web/media/hero/sailfish_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/sailfish_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/sailfish_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/sailfish_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/sailfish_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/sailfish_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/sailfish_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/sailfish/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/sailfish.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/hydrofoil_sailfish.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/sailfish/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. 更新 interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 31 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "三十一大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸) 由渲染器微調縮放適配"

    # 4. 更新 directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    sailfish_dir = "game/assets/sprites/player/paperdoll/sailfish/"
    if sailfish_dir not in races_dirs:
        races_dirs.append(sailfish_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(repo_root):
    base_dir = os.path.join(repo_root, "game/assets/sprites/player/paperdoll/sailfish")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(repo_root, "game/assets/sprites/player/poses/sailfish")
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
