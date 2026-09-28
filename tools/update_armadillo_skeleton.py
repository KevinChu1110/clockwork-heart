import json, os, re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open("docs/world/CRUCIBLE_ARMADILLO_DESIGN_PROPOSAL.md", "r", encoding="utf-8") as f:
    proposal_text = f.read()

m = re.findall(r"```json\s*(\{.*?\})\s*```", proposal_text, re.DOTALL)
slots_spec = json.loads(m[0])
race_spec_block = json.loads(m[1])["armadillo"]

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
                    new_var["weapon_type"] = "sword"
                elif sid != "winding_key":
                    new_var["race"] = "armadillo"
                slot_obj["sample_variants"].append(new_var)

    races_list = data["races_specification"]["races"]
    if not any(r.get("race_id") == "armadillo" for r in races_list):
        new_race = {
            "race_id": "armadillo",
            "aliases": race_spec_block["aliases"],
            "name_zh": race_spec_block["name"],
            "name_en": race_spec_block["name_en"],
            "class_archetype": "騎士 (Knight)",
            "origin_realm": race_spec_block["origin_realm"],
            "lore_anchor": "穿行於赤焰熔爐·鍛造火山「黑曜石淬火神壇」、「金色熔流鐵水池」與「重型鍛造工坊與衝壓懸橋」，巡檢「黃銅洩壓儀表塔」、「黑曜淬火石磚步道」與「晨曦天軌 6 號熔爐重載貨運月台」，駐守「高壓地熱升空彈射井」與「冷卻熔渣重力傾卸滑道」，配合矮人鐵匠大師·重錘布隆、陶土魔像學徒·黏土泥泥與熔爐溫控長老·坩堝老爹；通體覆蓋高耐熱粗獷鑄鐵板件與耐高溫合金彈簧骨架、黑曜淬火面甲頭盔、四葉散熱鍛造發條鑰匙、熔爐鐵砧重裝板甲、琥珀耐熱石英目鏡、多節沖壓鑄鐵散熱背甲，右手單持專屬玄鐵重破大劍，以低重心四點扎地步態、多節沖壓鑄鐵背甲蜷曲反震、霸體蓄能破陣重斬、熔爐鐵砧重裝防禦見長的高溫鍛造火山重裝板甲騎士",
            "proportions": {
                "head_to_body_ratio": "2.0 ~ 2.2 頭身 (19 世紀末古典鐵皮發條犰狳自動機與鐘錶工坊抗震滾珠機關偶)",
                "posture": "側身 45 度穩健扎地，低重心四點立正，身後散熱重尾自然垂地平衡，雙手端持玄鐵重破大劍立於身前，神情沉穩堅毅，四葉散熱發條鑰匙勻速自轉",
                "standee_height_px": 840,
                "standee_width_px": 420
            },
            "mechanical_features": {
                "head_and_neck": "一體鑄造弧形黑曜淬火防濺面甲，前額覆蓋金黃衝壓防濺鋼檐，眼窩處精準中空中空供 optic_core 穿透，下巴雙向收縮金屬護頰，兩側點綴多巴胺珊瑚粉散熱孔",
                "ears": "短粗靈巧的折疊黃銅耳鰭，內嵌高溫抗震彈簧與散熱百葉通風孔，無生物耳廓",
                "torso_and_limbs": "重裝雙層沖壓高耐熱鑄鐵球鉸底盤（#2B2630），腹部包覆耐熱象牙白陶瓷隔熱層（#FFFDF8），四肢為帶矽膠密封圈的黃銅球鉸鏈",
                "tail": "四節同心金屬套筒串聯而成的靈動多節鑄鐵散熱重尾，末端裝配鈍圓形防撞配重塊，戰鬥中自然貼地吸收後坐力",
                "weapon_system": "右手主持大劍劍柄、垂直立於身前專屬「玄鐵重破大劍（Black Iron Heavy Greatsword）」，高溫淬火玄鐵鑄鍛劍刃搭配黃銅加厚十字格擋護手，底層掛載 equipment.json 既有 meager_edge (tier 2) 與 knight_saber (tier 3)"
            },
            "color_palette": {
                "base": "#FFFDF8 (基底象牙白陶瓷釉/拋光耐熱鋁鎳合金，腹部隔熱層與關節受光高光)",
                "primary": "#FFD028 (主色天元黃銅金，甲片外緣包邊、外露鉚釘、發條鑰匙與劍柄護手)",
                "secondary": "#FFA010 (次色晨曦多巴胺暖橘，面甲目鏡光芒、劍刃淬火高溫紋路與背甲縫隙熱浪流光)",
                "accent": "#FF5E8A (點綴色多巴胺珊瑚粉，洩壓警示閥門、發條軸承裝飾點與散熱小標記)",
                "metal": "#2B2630 (深曜石鑄鐵藍黑/消光黑曜石耐火塗料，高階金屬玩具厚重質感)",
                "outline": "#1F1A3A (深藍紫/深暖褐手繪立體外輪廓描邊，確保明亮清爽零泥土髒黑)"
            },
            "asset_naming_conventions": {
                "status": {
                    "existing": [],
                    "pending": [
                        "branding/char_armadillo.png (品牌形象立牌)",
                        "web/media/hero/char_armadillo.png (官網英雄展示立繪)",
                        "docs/art/crucible_armadillo_concept.png (概念立繪)",
                        "game/assets/sprites/player/armadillo_idle.png (64x64 待機)",
                        "game/assets/sprites/player/armadillo_idle_x3.png (128x128 待機)",
                        "game/assets/sprites/player/party/armadillo_idle.png (隊伍待機)",
                        "web/media/hero/armadillo_idle.png (128x128 官網待機)",
                        "game/assets/sprites/player/showcase/armadillo_idle_hd.png (800x1200 HD 展示立繪)",
                        "game/assets/sprites/player/armadillo_battle.png (128x128 戰鬥特寫姿態)",
                        "game/assets/sprites/player/armadillo_battle_512.png (512x512 戰鬥特寫姿態)",
                        "game/assets/sprites/player/armadillo_walk_{0..3}.png (64x64 行走動畫)",
                        "game/assets/sprites/player/armadillo_walk_{0..3}_x3.png (128x128 行走動畫)",
                        "game/assets/sprites/player/armadillo_walk_{0..3}_512.png (512x512 行走動畫)",
                        "game/assets/sprites/player/poses/armadillo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS 六大戰鬥姿態)",
                        "game/assets/sprites/portraits/armadillo.png (HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/armadillo_512.png (512x512 HUD 戰鬥頭像)",
                        "game/assets/sprites/portraits/crucible_armadillo.png (對話半身像)",
                        "game/assets/sprites/player/paperdoll/armadillo/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
                    ]
                },
                "branding_standee": "branding/char_armadillo.png (420x840 -> 1344x1680) [待產出]",
                "branding_concept_art": "docs/art/crucible_armadillo_concept.png (928x1152) [待產出]",
                "web_hero": "web/media/hero/char_armadillo.png (420x840 -> 1344x1680) [待產出]",
                "web_preview": "web/media/hero/armadillo_idle.png (128x128) [待產出]",
                "game_sprite_idle_base": "game/assets/sprites/player/armadillo_idle.png (64x64) [待產出]",
                "game_sprite_idle_hi": "game/assets/sprites/player/armadillo_idle_x3.png (128x128) [待產出]",
                "game_sprite_party_idle": "game/assets/sprites/player/party/armadillo_idle.png (128x128) [待產出]",
                "game_sprite_battle": "game/assets/sprites/player/armadillo_battle.png (128x128) [待產出]",
                "game_sprite_walk": "game/assets/sprites/player/armadillo_walk_{0..3}.png (64x64) [待產出]",
                "game_sprite_walk_hi": "game/assets/sprites/player/armadillo_walk_{0..3}_x3.png (128x128) [待產出]",
                "game_action_poses": "game/assets/sprites/player/poses/armadillo/{attack,hit,idle,recover,skill,telegraph}.png (128x128 & 512x512 LANCZOS) [待產出]",
                "portrait_hud": "game/assets/sprites/portraits/armadillo.png (128x128) [待產出]",
                "portrait_dialogue": "game/assets/sprites/portraits/crucible_armadillo.png (384x480) [待產出]",
                "paperdoll_slices_dir": "game/assets/sprites/player/paperdoll/armadillo/{slot_id}/{item_id}.png [待產出]"
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
            rule_str = rule_str.replace("四十八重大種族", "四十九重大種族")
            if "熔鎧犰狳" not in rule_str:
                rule_str = rule_str.replace("高空巡檢工裝)", "高空巡檢工裝、熔鎧犰狳敦實穩重厚裝體態與熔爐鐵砧重裝板甲)")
            item["rule"] = rule_str

    races_dirs = data.get("directory_structure_blueprint", {}).get("sub_directories", {}).get("races", [])
    armadillo_dir = "game/assets/sprites/player/paperdoll/armadillo/"
    if armadillo_dir not in races_dirs:
        races_dirs.append(armadillo_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"成功更新 {path}")

def create_gitkeeps(root):
    base_dir = os.path.join(root, "game/assets/sprites/player/paperdoll/armadillo")
    slots = ["back_curio", "chassis", "costume", "head_unit", "optic_core", "weapon", "winding_key"]
    for s in slots:
        d = os.path.join(base_dir, s)
        os.makedirs(d, exist_ok=True)
        keep = os.path.join(d, ".gitkeep")
        if not os.path.exists(keep):
            with open(keep, "w") as f:
                pass
            print(f"建立 {keep}")

    poses_dir = os.path.join(root, "game/assets/sprites/player/poses/armadillo")
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

