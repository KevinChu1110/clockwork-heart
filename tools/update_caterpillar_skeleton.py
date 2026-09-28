import json, os, re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open("docs/world/BELLOWS_CATERPILLAR_DESIGN_PROPOSAL.md", "r", encoding="utf-8") as f:
    proposal_text = f.read()

m = re.findall(r"```json\s*(\{.*?\})\s*```", proposal_text, re.DOTALL)
slots_spec = json.loads(m[0])
race_spec_block = json.loads(m[1])["caterpillar"]

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
                    new_var["weapon_type"] = "hammer"
                elif sid != "winding_key":
                    new_var["race"] = "caterpillar"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    if not any(r.get("race_id") == "caterpillar" for r in races_list):
        new_race = {
            "race_id": "caterpillar",
            "aliases": race_spec_block["aliases"],
            "name_zh": race_spec_block["name"],
            "name_en": race_spec_block["name_en"],
            "class_archetype": "戰士 (Viking)",
            "origin_realm": race_spec_block["origin_realm"],
            "lore_anchor": "穿行於翡翠深林·發條蔓谷「巨木樹屋聚落」、「蔓谷天梯引道·深林站」與「晨曦天軌 3 號月台」，巡檢「高架重軌引橋·巨輪城站」、「防護金屬藤蔓彈力網」與「觀風石碑塔」，駐守「樹汁導流泵」與「發條藤蔓彈射平台」，配合守林哨兵·風耳、靈尾工藝師·小鈴與老鹿木匠·角木；通體覆蓋多節同軸沖壓薄銅環片與墨綠摺疊皮革風箱骨架、雙探針風箱護額頭盔、雙環重裝風箱發條鑰匙、蔓谷深林工兵板甲、雙圓琥珀聚光透鏡、分節軟鋼風箱蓄壓氣包，右手單持專屬蔓谷風箱重壓鎚，以手風琴式多節風箱伸縮、雙排棘輪滾足定點自鎖、停拍看破窗口極限破障、蔓谷風箱蓄壓夯地見長的翡翠深林重裝工兵戰鎚戰士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末古典鐵皮發條蠕行毛蟲自動機與鐘錶風箱氣動機關偶)",
                "posture": "低重心多節貼地匍匐，敦實矮胖體態，右手持蔓谷風箱重壓鎚立於身前偏右，左爪微屈護於胸前，雙環重裝發條鑰匙隨深林律動沉穩旋轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "半球形沖壓黃銅頭盔，前額加裝耐磨防濺護額鋼板，額頂伸出一對微型螺旋軟鋼絲風向探針，兩側點綴多巴胺珊瑚粉通風孔，眼窩處精準中空供 optic_core 穿透",
                "ears": "頭盔兩側圓形微型氣動消音濾網與風向探針根部球鉸，無生物耳廓",
                "torso_and_limbs": "六節同軸沖壓薄銅環片（#FFD028），夾層為耐磨墨綠摺疊皮革風箱（#204028），腹底嵌裝雙排微型防滑棘輪滾足，腹部包覆象牙白陶瓷隔震襯板（#FFFDF8）",
                "tail": "背部尾端裝載三節同軸套疊分節軟鋼風箱蓄壓氣包，外附金屬防護編織網與微型氣壓表，底部連接黃銅排氣軟管",
                "weapon_system": "右手單手平穩握持專屬「蔓谷風箱重壓鎚（Vine Valley Bellows Compression Hammer）」，重裝鍛造鑄鐵重砧鎚頭內嵌氣動壓縮風箱氣筒，底層掛載 equipment.json 既有 anvil_hammer 與 iron_cudgel"
            },
            "color_palette": {
                "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光鋁鎳金屬，腹部隔震襯板與關節受光高光)",
                "primary": "#4ED86A (主色薄荷翡翠綠與天元黃銅金 #FFD028，沖壓銅環外甲、風向探針與發條鑰匙)",
                "secondary": "#FFA010 (次色晨曦多巴胺暖橘，面甲目鏡光芒、風箱氣閥警示標記與戰鎚衝擊面)",
                "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，風箱褶皺摺痕點綴、氣孔開關與發條鑰匙中心鉚釘)",
                "metal": "#204028 (深墨綠耐磨漆板與復古黃銅 #8B6508，翡翠深林工兵玩具溫潤厚重質感)",
                "outline": "#1F1A3A (深藍紫/深暖褐手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_caterpillar.png (品牌形象立牌)",
                        "web/media/hero/char_caterpillar.png (官網英雄展示立繪)",
                        "docs/art/bellows_caterpillar_concept.png (概念立繪)",
                        "game/assets/sprites/player/caterpillar_idle.png (64x64 待機)",
                        "game/assets/sprites/player/caterpillar_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/caterpillar_idle.png (隊伍待機)",
                        "web/media/hero/caterpillar_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/caterpillar_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/caterpillar_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/caterpillar_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/caterpillar_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/caterpillar_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/caterpillar_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/caterpillar/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/caterpillar.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/caterpillar_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/bellows_caterpillar.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/caterpillar/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_caterpillar.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/bellows_caterpillar_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_caterpillar.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/caterpillar_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/caterpillar_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/caterpillar_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/caterpillar_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/caterpillar_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/caterpillar_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/caterpillar_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/caterpillar/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/caterpillar.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/bellows_caterpillar.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/caterpillar/{slot_id}/{item_id}.png [待產出]"
            }
        }
        races_list.append(new_race)

    data["races_specification"]["total_races"] = len(races_list)

    compat = data.get("interchangeability_and_compatibility", {})
    for item in compat.get("universal_slots", []):
        if item.get("slot_id") == "winding_key":
            item["rule"] = f"上背發條插座公規化，所有鑰匙款式適用於 {len(races_list)} 種動物素體"
    for item in compat.get("race_adapted_slots", []):
        if item.get("slot_id") == "costume":
            rule_str = item.get("rule", "")
            rule_str = rule_str.replace("四十九重大種族", "五十重大種族")
            if "風箱毛蟲" not in rule_str:
                rule_str = rule_str.replace("熔爐鐵砧重裝板甲)", "熔爐鐵砧重裝板甲、風箱毛蟲多節風箱體態與蔓谷深林工兵板甲)")
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    caterpillar_dir = "game/assets/sprites/player/paperdoll/caterpillar/"
    if caterpillar_dir not in races_dirs:
        races_dirs.append(caterpillar_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/caterpillar")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/caterpillar")
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
