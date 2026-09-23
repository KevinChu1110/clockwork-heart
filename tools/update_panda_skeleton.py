#!/usr/bin/env python3
import json
import os
import sys

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Update sample_variants in slots_architecture
    slots = data["slots_architecture"]["slots"]

    # Slot 1: chassis (index 0)
    chassis_variants = slots[0]["sample_variants"]
    if not any(v.get("id") == "paint_panda_porcelain" for v in chassis_variants):
        chassis_variants.extend([
            {
                "id": "paint_panda_porcelain",
                "name": "原廠羊脂白玉冰裂瓷生漆雙色",
                "race": "panda",
                "tier": "common"
            },
            {
                "id": "paint_panda_celadon",
                "name": "天青雨過冰裂青瓷漆面",
                "race": "panda",
                "tier": "rare"
            }
        ])

    # Slot 2: head_unit (index 1)
    head_variants = slots[1]["sample_variants"]
    if not any(v.get("id") == "head_panda_brass_socket_ears" for v in head_variants):
        head_variants.append({
            "id": "head_panda_brass_socket_ears",
            "name": "雙聯青古銅球窩半球耳罩",
            "race": "panda",
            "tier": "common"
        })

    # Slot 3: winding_key (index 2)
    key_variants = slots[2]["sample_variants"]
    if not any(v.get("id") == "key_panda_taiji_ruyi_brass" for v in key_variants):
        key_variants.append({
            "id": "key_panda_taiji_ruyi_brass",
            "name": "青銅太極如意發條鑰匙",
            "tier": "common"
        })

    # Slot 4: costume (index 3)
    costume_variants = slots[3]["sample_variants"]
    if not any(v.get("id") == "costume_panda_zen_apprentice_robe" for v in costume_variants):
        costume_variants.append({
            "id": "costume_panda_zen_apprentice_robe",
            "name": "天元道場生漆沖壓練功甲",
            "race": "panda",
            "tier": "common"
        })

    # Slot 5: optic_core (index 4)
    optic_variants = slots[4]["sample_variants"]
    if not any(v.get("id") == "core_obsidian_amber_quartz" for v in optic_variants):
        optic_variants.append({
            "id": "core_obsidian_amber_quartz",
            "name": "墨玉琥珀金光學核心",
            "race": "panda",
            "tier": "common"
        })

    # Slot 6: weapon (index 5)
    weapon_variants = slots[5]["sample_variants"]
    if not any(v.get("id") == "wpn_panda_taiji_cestus" for v in weapon_variants):
        weapon_variants.append({
            "id": "wpn_panda_taiji_cestus",
            "name": "乾坤太極機關拳套",
            "weapon_type": "fist",
            "tier": "common"
        })

    # Slot 7: back_curio (index 6)
    curio_variants = slots[6]["sample_variants"]
    if not any(v.get("id") == "curio_panda_floating_taiji_box" for v in curio_variants):
        curio_variants.append({
            "id": "curio_panda_floating_taiji_box",
            "name": "微型發條懸浮太極八音盒",
            "race": "panda",
            "tier": "common"
        })

    # 2. Update races_specification
    races_spec = data["races_specification"]
    races_spec["total_races"] = 13

    races_list = races_spec["races"]
    if not any(r.get("race_id") == "panda" for r in races_list):
        races_list.append({
            "race_id": "panda",
            "aliases": [
                "porcelain_panda",
                "zen_panda",
                "clockwork_panda"
            ],
            "name_zh": "瓷韻熊貓",
            "name_en": "The Porcelain Panda",
            "class_archetype": "武術家 (Monk)",
            "origin_realm": "R09 竹影道場·天元竹林 / Bamboo Grove: Zen Puppet Dojo",
            "lore_anchor": "自天元竹林「青石武鬥古道場·演武坪」與「發條天元竹海」旁修身悟道的發條陶瓷熊貓，通體由高溫黑白生漆亮面陶瓷板件、青古銅榫卯鉸鏈與內置太極重力平衡陀組裝而成，以單戴乾坤太極機關拳套、貼身寸勁連打破勢與動靜化勁見長的武道宗師",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (穩健沉著低重心體態)",
                "posture": "太極抱元沉步架式，右手單戴乾坤太極機關拳套置於胸前，左手平伸化勁引掌，底盤扎實，背部青銅太極如意鑰匙悠然自轉",
                "standee_height_px": 840,
                "standee_width_px": 440
            },
            "mechanical_features": {
                "head_and_neck": "圓潤厚實高溫生漆白瓷頭殼，配備雙聯墨玉琉璃同心圓目鏡與黃銅光圈調焦環，下顎設有橫向一字微型金屬散熱網隙",
                "ears": "雙聯青古銅球窩半球耳罩，內置微調音叉片與散熱細孔，外露打磨平整之沉頭緊固螺栓",
                "torso_and_limbs": "胸腹覆蓋厚實羊脂白玉冰裂釉陶瓷板，胸口中央配置圓形太極雙魚重力平衡陀視窗，四肢為深邃玄墨黑生漆陶瓷護甲與青古銅包角",
                "tail": "圓球形青古銅金屬短尾配重塊，整合底盤穩定配重與發條動力接地栓",
                "weapon_system": "右手單戴專利「乾坤太極機關拳套 / 破勢寸勁生漆拳環」，前腕嵌有高壓微型氣缸與精工衝擊活塞，左手自然半握化勁，完全符合 0-MKT7 與 monk/fist 體系"
            },
            "color_palette": {
                "primary": "#FFFDF8 (羊脂白玉冰裂瓷板)",
                "secondary": "#1F1A3A (玄墨深藍黑生漆板件)",
                "accent": "#FFD028 (天元金黃 / 琥珀金晶石)",
                "detail": "#4ED86A (薄荷竹翠綠太極徽紋)",
                "warm_highlight": "#FFA010 (暖橘發條黃銅鑰匙與銷釘)",
                "outline": "#1F1A3A (深藍紫厚描邊)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "docs/art/porcelain_panda_concept.png (928x1152 概念立繪)",
                        "branding/char_panda.png (400x840 品牌立牌)",
                        "web/media/hero/char_panda.png (400x840 官網英雄圖)",
                        "web/media/hero/panda_idle.png (128x128 官網預覽圖)",
                        "game/assets/sprites/player/panda_idle.png (64x64 基礎待機)",
                        "game/assets/sprites/player/panda_idle_x3.png (128x128 高畫質待機)",
                        "game/assets/sprites/player/party/panda_idle.png (128x128 隊伍展示幀)",
                        "game/assets/sprites/player/panda_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/panda_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/panda_walk_{0..3}_x3.png (128x128 高畫質行走動畫)",
                        "game/assets/sprites/player/poses/panda/ (戰鬥6大動作姿態目錄)",
                        "game/assets/sprites/portraits/panda.png (128x128 HUD戰鬥頭像)",
                        "game/assets/sprites/portraits/porcelain_panda.png (384x480 對話框半身像)",
                        "game/assets/sprites/player/paperdoll/panda/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_panda.png (400x840) [待產出]",
                "branding_concept_art": "docs/art/porcelain_panda_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_panda.png (400x840) [待產出]",
                "web_preview": "web/media/hero/panda_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/panda_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/panda_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/panda_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/panda_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/panda_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/panda_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/panda/{attack,hit,idle,recover,skill,telegraph}.png (128x128) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/panda.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/porcelain_panda.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/panda/{slot_id}/{item_id}.png [待產出]"
            }
        })

    # 3. Update interchangeability_and_compatibility
    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 13 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            item["rule"] = "十三大種族軀幹均維持 2.0~2.5 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分寬肩 (如獅/豬/熊/象) 由渲染器微調縮放 1.05x"

    # 4. Update directory_structure_blueprint
    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    panda_dir = "game/assets/sprites/player/paperdoll/panda/"
    if panda_dir not in races_dirs:
        races_dirs.append(panda_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Successfully updated {path}")

def create_gitkeeps():
    base_dir = "game/assets/sprites/player/paperdoll/panda"
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"Created {keep}")

    poses_dir = "game/assets/sprites/player/poses/panda"
    os.makedirs(poses_dir, exist_ok=True)
    poses_keep = os.path.join(poses_dir, ".gitkeep")
    if not os.path.exists(poses_keep):
        with open(poses_keep, "w") as f:
            pass
        print(f"Created {poses_keep}")

if __name__ == "__main__":
    create_gitkeeps()
    for p in sys.argv[1:]:
        update_file(p)
