#!/usr/bin/env python3
import json
import os
import re

REPO_ROOT = "/opt/side/bravesoul-game"

def resolve_projects_json():
    path = os.path.join(REPO_ROOT, "docs/PROJECTS.json")
    # Reset from HEAD first
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure bison-skeleton is in projects
    bison_proj = {
        "id": "bison-skeleton",
        "cat": "遊戲",
        "title": "第四十四族撼地野牛(bison)資料表骨架與空目錄先行建置",
        "status": "已上線",
        "note": "審核通過合進 main",
        "keys": ["第四十四族撼地野"]
    }
    gecko_prop = {
        "id": "gecko-proposal",
        "cat": "世界觀",
        "title": "第四十五種動物巡管守宮紙娃娃角色設計提案",
        "status": "已上線",
        "note": "完成第四十五種動物巡管守宮世界觀與角色設計提案，審核通過合進 main",
        "keys": ["第四十五種動物巡"]
    }
    gecko_skel = {
        "id": "gecko-skeleton",
        "cat": "遊戲",
        "title": "第四十五族巡管守宮(gecko)資料表骨架與空目錄先行建置",
        "status": "已上線",
        "note": "完成資料表骨架與空目錄先行建置，審核通過合進 main",
        "keys": ["第四十五族巡管守"]
    }
    gecko_slices = {
        "id": "gecko-slices",
        "cat": "遊戲",
        "title": "第四十五族巡管守宮7大部件槽位紙娃娃切片與雙規格資產",
        "status": "已上線",
        "note": "完成切片產出，審核通過合進 main",
        "keys": ["第四十五族巡管守"]
    }

    # Update or append
    projects = data.get("projects", [])
    proj_map = {p["id"]: p for p in projects}

    for p in [bison_proj, gecko_prop, gecko_skel, gecko_slices]:
        if p["id"] in proj_map:
            proj_map[p["id"]].update(p)
        else:
            projects.append(p)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("✓ Resolved docs/PROJECTS.json")

def resolve_ui_json():
    # Both bison and gecko i18n entries need to be present in each locale
    bison_i18n = {
        "zh_TW": {
            "撼地野牛": "撼地野牛",
            "野牛": "野牛",
            "生鏽耐磨馬口鐵重裝素體": "生鏽耐磨馬口鐵重裝素體",
            "鉚接工字鋼曲角重盔": "鉚接工字鋼曲角重盔",
            "重工十字T柄生鐵發條鑰匙": "重工十字T柄生鐵發條鑰匙",
            "舊庫拆解工兵重胸甲與防刮裙甲": "舊庫拆解工兵重胸甲與防刮裙甲",
            "舊庫拆解工兵重胸甲": "舊庫拆解工兵重胸甲",
            "琥珀雙針耐震壓力表目鏡": "琥珀雙針耐震壓力表目鏡",
            "廢土重砧碎鐵巨鎚": "廢土重砧碎鐵巨鎚",
            "雙聯排氣散熱煙囪": "雙聯排氣散熱煙囪",
        },
        "zh_CN": {
            "撼地野牛": "撼地野牛",
            "野牛": "野牛",
            "生鏽耐磨馬口鐵重裝素體": "生锈耐磨马口铁重装素体",
            "鉚接工字鋼曲角重盔": "铆接工字钢曲角重盔",
            "重工十字T柄生鐵發條鑰匙": "重工十字T柄生铁发条钥匙",
            "舊庫拆解工兵重胸甲與防刮裙甲": "旧库拆解工兵重胸甲与防刮裙甲",
            "舊庫拆解工兵重胸甲": "旧库拆解工兵重胸甲",
            "琥珀雙針耐震壓力表目鏡": "琥珀双针耐震压力表目镜",
            "廢土重砧碎鐵巨鎚": "废土重砧碎铁巨锤",
            "雙聯排氣散熱煙囪": "双联排气散热烟囱",
        },
        "en": {
            "撼地野牛": "The Groundshaker Bison",
            "野牛": "Bison",
            "生鏽耐磨馬口鐵重裝素體": "Rusted Tinplate Chassis",
            "鉚接工字鋼曲角重盔": "Riveted I-Beam Brow Horn Crest",
            "重工十字T柄生鐵發條鑰匙": "Heavy Cross T-Bar Cast-Iron Winding Key",
            "舊庫拆解工兵重胸甲與防刮裙甲": "Junkyard Demolition Cuirass & Tassets",
            "舊庫拆解工兵重胸甲": "Junkyard Demolition Cuirass",
            "琥珀雙針耐震壓力表目鏡": "Amber Dual-Needle Pressure Gauge Eye",
            "廢土重砧碎鐵巨鎚": "Wasteland Anvil Scrap-Crusher Sledgehammer",
            "雙聯排氣散熱煙囪": "Twin-Vent Exhaust Heat-Sink Stack",
        },
        "ja": {
            "撼地野牛": "撼地の野牛 (カンチノヤギュウ)",
            "野牛": "野牛",
            "生鏽耐磨馬口鐵重裝素體": "錆びた耐摩耗ブリキ重装素体",
            "鉚接工字鋼曲角重盔": "リベット留めI形鋼曲角重兜",
            "重工十字T柄生鐵發條鑰匙": "重工十字T字ハンドル銑鉄ぜんまい鍵",
            "舊庫拆解工兵重胸甲與防刮裙甲": "旧庫解体工兵重胸甲と耐傷草摺",
            "舊庫拆解工兵重胸甲": "旧庫解体工兵重胸甲",
            "琥珀雙針耐震壓力表目鏡": "琥珀二重針耐震圧力計接眼レンズ",
            "廢土重砧碎鐵巨鎚": "ウェイストランド重金床砕鉄大槌",
            "雙聯排氣散熱煙囪": "二連排気放熱煙突",
        },
        "ko": {
            "撼地野牛": "진지들소",
            "野牛": "들소",
            "生鏽耐磨馬口鐵重裝素體": "녹슨 내마모 양철 중장 소체",
            "鉚接工字鋼曲角重盔": "리벳 접합 I형강 곡각 중투구",
            "重工十字T柄生鐵發條鑰匙": "중공업 십자 T형 주철 태엽 열쇠",
            "舊庫拆解工兵重胸甲與防刮裙甲": "폐품고 해체 공병 중흉갑과 흠집 방지 스커트",
            "舊庫拆解工兵重胸甲": "폐품고 해체 공兵 중흉갑",
            "琥珀雙針耐震壓力表目鏡": "호박색 쌍침 내진 압력계 접안렌즈",
            "廢土重砧碎鐵巨鎚": "황무지 앤빌 쇄철 대형 해머",
            "雙聯排氣散熱煙囪": "2연 배기 방열 굴뚝",
        },
        "es": {
            "撼地野牛": "El Bisonte Tiemblatierra",
            "野牛": "Bisonte",
            "生鏽耐磨馬口鐵重裝素體": "Chasis de Hojalata Oxidada Resistente al Desgaste",
            "鉚接工字鋼曲角重盔": "Yelmo Pesado de Cuernos de Viga I Remachada",
            "重工十字T柄生鐵發條鑰匙": "Llave de Cuerda de Hierro Fundido con Mango en T Cruzado Pesado",
            "舊庫拆解工兵重胸甲與防刮裙甲": "Coraza de Demolición del Depósito y Escarselas Antiarañazos",
            "舊庫拆解工兵重胸甲": "Coraza de Demolición del Depósito",
            "琥珀雙針耐震壓力表目鏡": "Ojo de Manómetro Antivibración de Doble Aguja de Ámbar",
            "廢土重砧碎鐵巨鎚": "Gran Martillo Machacahierro de Yunque del Yermo",
            "雙聯排氣散熱煙囪": "Chimenea de Escape Doble Disipadora de Calor",
        },
    }

    gecko_i18n = {
        "zh_TW": {
            "巡管守宮": "巡管守宮",
            "守宮": "守宮",
            "黃銅棘輪多角機關鏢": "黃銅棘輪多角機關鏢",
            "雙環洩壓黃銅發條鑰匙": "雙環洩壓黃銅發條鑰匙",
            "微型同軸多節齒輪平衡尾": "微型同軸多節齒輪平衡尾",
            "冷軋黃銅微弧吸盤素體": "冷軋黃銅微弧吸盤素體",
            "管網巡檢防刮護額": "管網巡檢防刮護額",
            "耐熱工裝暗忍胸甲與防刮短裙甲": "耐熱工裝暗忍胸甲與防刮短裙甲",
            "雙目裂隙光圈石英目鏡": "雙目裂隙光圈石英目鏡",
            "耐熱工裝暗忍胸甲": "耐熱工裝暗忍胸甲",
        },
        "zh_CN": {
            "巡管守宮": "巡管守宫",
            "守宮": "守宫",
            "黃銅棘輪多角機關鏢": "黄铜棘轮多角机关镖",
            "雙環洩壓黃銅發條鑰匙": "双环泄压黄铜发条钥匙",
            "微型同軸多節齒輪平衡尾": "微型同轴多节齿轮平衡尾",
            "冷軋黃銅微弧吸盤素體": "冷轧黄铜微弧吸盘素体",
            "管網巡檢防刮護額": "管网巡检防刮护额",
            "耐熱工裝暗忍胸甲與防刮短裙甲": "耐热工装暗忍胸甲与防刮短裙甲",
            "雙目裂隙光圈石英目鏡": "双目裂隙光圈石英目镜",
            "耐熱工裝暗忍胸甲": "耐热工装暗忍胸甲",
        },
        "en": {
            "巡管守宮": "The Conduit Gecko",
            "守宮": "Gecko",
            "黃銅棘輪多角機關鏢": "Brass Ratchet Conduit Shuriken",
            "雙環洩壓黃銅發條鑰匙": "Dual-Ring Relief Brass Winding Key",
            "微型同軸多節齒輪平衡尾": "Segmented Gear Balance Tail",
            "冷軋黃銅微弧吸盤素體": "Cold-Rolled Brass Chassis",
            "管網巡檢防刮護額": "Conduit Scout Crest Cowl",
            "耐熱工裝暗忍胸甲與防刮短裙甲": "High-Pressure Stealth Harness & Tassets",
            "雙目裂隙光圈石英目鏡": "Dual-Slit Aperture Quartz Lens",
            "耐熱工裝暗忍胸甲": "High-Pressure Stealth Harness",
        },
        "ja": {
            "巡管守宮": "導管のヤモリ (カンカンノヤモリ)",
            "守宮": "ヤモリ",
            "黃銅棘輪多角機關鏢": "真鍮ラチェット多角機関手裏剣",
            "雙環洩壓黃銅發條鑰匙": "双環調圧真鍮ぜんまい鍵",
            "微型同軸多節齒輪平衡尾": "小型同軸多節歯車バランス尾",
            "冷軋黃銅微弧吸盤素體": "冷間圧延真鍮吸盤素体",
            "管網巡檢防刮護額": "配管巡回耐摩耗額当て",
            "耐熱工裝暗忍胸甲與防刮短裙甲": "耐熱作業暗忍胸甲と防護草摺",
            "雙目裂隙光圈石英目鏡": "双眼スリット絞り石英ゴーグル",
            "耐熱工裝暗忍胸甲": "耐熱作業暗忍胸甲",
        },
        "ko": {
            "巡管守宮": "배관 순찰 도마뱀붙이",
            "守宮": "도마뱀붙이",
            "黃銅棘輪多角機關鏢": "황동 라쳇 다각 기관 표창",
            "雙環洩壓黃銅發條鑰匙": "쌍환 감압 황동 태엽 열쇠",
            "微型同軸多節齒輪平衡尾": "초소형 동축 다절 기어 밸런스 꼬리",
            "冷軋黃銅微弧吸盤素體": "냉간 압연 황동 흡반 소체",
            "管網巡檢防刮護額": "배관망 순찰 긁힘 방지 이마 보호대",
            "耐熱工裝暗忍胸甲與防刮短裙甲": "내열 작업복 암닌 흉갑과 스커트",
            "雙目裂隙光圈石英目鏡": "양안 슬릿 조리개 석영 렌즈",
            "耐熱工裝暗忍胸甲": "내열 작업복 암닌 흉갑",
        },
        "es": {
            "巡管守宮": "El Gecko de los Conductos",
            "守宮": "Gecko",
            "黃銅棘輪多角機關鏢": "Shuriken Mecánico de Trinquete de Latón",
            "雙環洩壓黃銅發條鑰匙": "Llave de Cuerda de Latón con Válvula de Alivio",
            "微型同軸多節齒輪平衡尾": "Cola de Equilibrio de Engranajes Segmentada",
            "冷軋黃銅微弧吸盤素體": "Chasis de Latón Laminado en Frío",
            "管網巡檢防刮護額": "Visera Protectora de Explorador de Conductos",
            "耐熱工裝暗忍胸甲與防刮短裙甲": "Arnés Sigiloso de Alta Presión y Escarselas",
            "雙目裂隙光圈石英目鏡": "Lente de Cuarzo de Apertura con Hendidura Dual",
            "耐熱工裝暗忍胸甲": "Arnés Sigiloso de Alta Presión",
        },
    }

    base_i18n = os.path.join(REPO_ROOT, "game/data/i18n/content")
    for loc in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
        ui_path = os.path.join(base_i18n, loc, "ui.json")
        os.system(f"git -C {REPO_ROOT} checkout HEAD -- {ui_path}")
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in bison_i18n.get(loc, {}).items():
            data[k] = v
        for k, v in gecko_i18n.get(loc, {}).items():
            data[k] = v
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✓ Resolved {ui_path}")

def resolve_paperdoll_slots():
    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        full_p = os.path.join(REPO_ROOT, p)
        os.system(f"git -C {REPO_ROOT} checkout HEAD -- {full_p}")

    import sys
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
    from update_gecko_skeleton import update_paperdoll_slots
    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        full_p = os.path.join(REPO_ROOT, p)
        update_paperdoll_slots(full_p)

    for p in ["docs/design/paperdoll_slots.json", "game/data/tables/paperdoll_slots.json"]:
        full_p = os.path.join(REPO_ROOT, p)
        with open(full_p, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["races_specification"]["total_races"] = 45
        for item in data.get("interchangeability_and_compatibility", {}).get("universal_slots", []):
            if item.get("slot_id") == "winding_key":
                item["rule"] = "上背發條插座公規化，所有鑰匙款式適用於 45 種動物素體"
        for item in data.get("interchangeability_and_compatibility", {}).get("race_adapted_slots", []):
            if item.get("slot_id") == "costume":
                item["rule"] = "四十五重大種族軀幹均維持 2.0~2.8 頭身 Chibi 比例，服飾外裝共用標準胸腰版型，部分特殊體態 (如獅/豬/熊/象/蜥蜴寬肩、青蛇修長靈巧、神隼流線收翼、靈羊微浮披肩、變色龍高聳導流冠、旗魚流體導流護胸、犀牛粗砂鑄鐵重甲護胸、蝙蝠失重匿蹤飛行護胸、巨猩重型鍛工背帶鍋爐胸甲、孔雀修長芭蕾身姿與木偶宮廷胸甲、沙哨狐獴直立哨兵體態與防沙短斗篷、鐵蹄駿駒高雅駿逸挺拔體態與巡防輕胸甲、劈木河狸敦實水桶腰工兵體態與開拓胸甲、旋刃伶鼬流線修長拱背刺客體態與拾荒防風斗篷、拍浪海豹圓潤流線水滴體態與深海武道束帶、星儀渡鴉俐落鳥偶體態與鐘錶學者斗篷、熱流赤鳶俐落猛禽體態與阻燃帆布斗篷、旋音天鵝典雅長頸芭蕾體態與大劇院儀仗胸甲、撼地野牛粗獷寬厚駝峰重甲與舊庫拆解工兵胸甲、巡管守宮靈敏扁平爬壁體態與耐熱暗忍胸甲) 由渲染器微調縮放適配"
        with open(full_p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"✓ Resolved {p} (total_races=45)")

def resolve_gdscript_files():
    # 1. game/scripts/autoload/game_state.gd
    gs_path = os.path.join(REPO_ROOT, "game/scripts/autoload/game_state.gd")
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {gs_path}")
    with open(gs_path, "r", encoding="utf-8") as f:
        gs = f.read()
    # Add gecko after bison in starter_weapon_id
    if '"bison": "anvil_hammer"' in gs and '"gecko": "mist_darts"' not in gs:
        gs = gs.replace('"bison": "anvil_hammer",', '"bison": "anvil_hammer",\n\t"gecko": "mist_darts",')
    # Add gecko after bison in default_name
    if '"bison": default_name = "撼地野牛"' in gs and '"gecko": default_name = "巡管守宮"' not in gs:
        gs = gs.replace('"bison": default_name = "撼地野牛"', '"bison": default_name = "撼地野牛"\n\t\t"gecko": default_name = "巡管守宮"')
    with open(gs_path, "w", encoding="utf-8") as f:
        f.write(gs)
    print("✓ Resolved game_state.gd")

    # 2. game/scripts/systems/equipment_system.gd
    eq_path = os.path.join(REPO_ROOT, "game/scripts/systems/equipment_system.gd")
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {eq_path}")
    with open(eq_path, "r", encoding="utf-8") as f:
        eq = f.read()
    if '"bison": "anvil_hammer"' in eq and '"gecko": "mist_darts"' not in eq:
        eq = eq.replace('"bison": "anvil_hammer",', '"bison": "anvil_hammer",\n\t"gecko": "mist_darts",')
    with open(eq_path, "w", encoding="utf-8") as f:
        f.write(eq)
    print("✓ Resolved equipment_system.gd")

    # 3. game/scripts/art/paperdoll_renderer.gd
    pr_path = os.path.join(REPO_ROOT, "game/scripts/art/paperdoll_renderer.gd")
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {pr_path}")
    with open(pr_path, "r", encoding="utf-8") as f:
        pr = f.read()

    # Update all_races lists to include gecko after bison
    pr = pr.replace(
        '"swan", "bison"]',
        '"swan", "bison", "gecko"]'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "chassis_bison_rusted_tinplate_default"',
        'elif race == "bison":\n\t\t\t\treturn "chassis_bison_rusted_tinplate_default"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "chassis_gecko_brass_patina_default"'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "head_bison_riveted_brow_horn_crest"',
        'elif race == "bison":\n\t\t\t\treturn "head_bison_riveted_brow_horn_crest"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "head_gecko_conduit_scout_crest_cowl"'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "key_bison_heavy_cross_t_bar_cast_iron"',
        'elif race == "bison":\n\t\t\t\treturn "key_bison_heavy_cross_t_bar_cast_iron"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "key_gecko_dual_ring_relief_valve_brass"'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "costume_bison_junkyard_demolition_cuirass"',
        'elif race == "bison":\n\t\t\t\treturn "costume_bison_junkyard_demolition_cuirass"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "costume_gecko_highpressure_stealth_harness"'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "face_bison_amber_pressure_gauge_eye"',
        'elif race == "bison":\n\t\t\t\treturn "face_bison_amber_pressure_gauge_eye"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "face_gecko_dual_slit_aperture_quartz_lens"'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "weapon_bison_wasteland_anvil_crusher_hammer"',
        'elif race == "bison":\n\t\t\t\treturn "weapon_bison_wasteland_anvil_crusher_hammer"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "weapon_gecko_conduit_ratchet_dart"'
    )
    pr = pr.replace(
        'elif race == "bison":\n\t\t\t\treturn "curio_bison_twin_vent_exhaust_stack"',
        'elif race == "bison":\n\t\t\t\treturn "curio_bison_twin_vent_exhaust_stack"\n\t\t\telif race == "gecko":\n\t\t\t\treturn "curio_gecko_segmented_gear_balance_tail"'
    )

    # fallback list in _get_fallback_spec
    bison_entry = '{"race_id": "bison", "aliases": ["groundshaker_bison", "clockwork_bison", "scrap_bison", "iron_bison"], "name_zh": "撼地野牛", "name_en": "The Groundshaker Bison", "class_archetype": "戰士 (Viking)"}'
    gecko_entry = '{"race_id": "gecko", "aliases": ["conduit_gecko", "clockwork_gecko", "brass_gecko", "wallrunner_gecko"], "name_zh": "巡管守宮", "name_en": "The Conduit Gecko", "class_archetype": "忍者 (Ninja)"}'

    if bison_entry in pr and gecko_entry not in pr:
        pr = pr.replace(bison_entry, bison_entry + ',\n\t\t\t\t' + gecko_entry)

    with open(pr_path, "w", encoding="utf-8") as f:
        f.write(pr)
    print("✓ Resolved paperdoll_renderer.gd")

    # 4. game/scripts/ui/paperdoll_select_demo.gd
    sd_path = os.path.join(REPO_ROOT, "game/scripts/ui/paperdoll_select_demo.gd")
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {sd_path}")
    with open(sd_path, "r", encoding="utf-8") as f:
        sd = f.read()

    # Gecko DEMO_PRESET definition
    gecko_preset = '''	},
	"gecko": {
		"id": "gecko",
		"name_zh": "巡管守宮",
		"name_en": "The Conduit Gecko",
		"archetype": "忍者 (Ninja)",
		"thumb": "res://assets/sprites/player/showcase/gecko_idle_hd.png",
		"desc": "黃銅都市巨輪城管網特工暗忍，冷軋黃銅吸盤素體，管網巡檢防刮護額與黃銅棘輪多角機關鏢。",
		"costumes": [
			{"id": "costume_gecko_highpressure_stealth_harness", "name_zh": "耐熱工裝暗忍胸甲", "desc": "雙層沖壓薄黃銅工裝輕胸甲，配備多巴胺暖金卡扣與防刮金屬裙甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現冷軋黃銅微弧吸盤素體與散熱百葉槽"}
		],
		"chassis": [
			{"id": "chassis_gecko_brass_patina_default", "name_zh": "冷軋黃銅微弧吸盤素體", "desc": "冷軋薄黃銅板覆薄荷綠銅抗氧化琺瑯漆，四足微型間歇吸盤金屬爪與齒輪平衡尾"}
		]
	}'''
    # Insert gecko after bison preset
    if '"bison": {' in sd and '"gecko": {' not in sd:
        # Find closing of bison block
        bison_end = sd.find('{"id": "chassis_bison_rusted_tinplate_default", "name_zh": "生鏽耐磨馬口鐵重裝素體", "desc": "沖壓深褐耐磨馬口鐵板覆亮橘防鏽烤漆，高扭力發條駝峰主機艙與密封抗震蹄踏"}\n\t\t]\n\t}')
        if bison_end != -1:
            cut = bison_end + len('{"id": "chassis_bison_rusted_tinplate_default", "name_zh": "生鏽耐磨馬口鐵重裝素體", "desc": "沖壓深褐耐磨馬口鐵板覆亮橘防鏽烤漆，高扭力發條駝峰主機艙與密封抗震蹄踏"}\n\t\t]\n\t}')
            sd = sd[:cut] + gecko_preset + sd[cut:]

    sd = sd.replace('"swan", "bison"]', '"swan", "bison", "gecko"]')
    if '"bison": gs.player_name = "撼地野牛"' in sd and '"gecko": gs.player_name = "巡管守宮"' not in sd:
        sd = sd.replace('"bison": gs.player_name = "撼地野牛"', '"bison": gs.player_name = "撼地野牛"\n\t\t\t\t"gecko": gs.player_name = "巡管守宮"')

    with open(sd_path, "w", encoding="utf-8") as f:
        f.write(sd)
    print("✓ Resolved paperdoll_select_demo.gd")

    # 5. game/scripts/ui/wardrobe_dialog.gd
    wd_path = os.path.join(REPO_ROOT, "game/scripts/ui/wardrobe_dialog.gd")
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {wd_path}")
    with open(wd_path, "r", encoding="utf-8") as f:
        wd = f.read()

    # Add gecko after bison chip
    if '{"id": "bison", "name_zh": "野牛"},' in wd and '{"id": "gecko", "name_zh": "守宮"},' not in wd:
        wd = wd.replace('{"id": "bison", "name_zh": "野牛"},', '{"id": "bison", "name_zh": "野牛"},\n\t{"id": "gecko", "name_zh": "守宮"},')

    # Add gecko in _race_name_zh
    if '"bison": return "野牛"' in wd and '"gecko": return "守宮"' not in wd:
        wd = wd.replace('"bison": return "野牛"', '"bison": return "野牛"\n\t\t"gecko": return "守宮"')

    # Add gecko to all_races
    wd = wd.replace('"swan", "bison"]', '"swan", "bison", "gecko"]')

    with open(wd_path, "w", encoding="utf-8") as f:
        f.write(wd)
    print("✓ Resolved wardrobe_dialog.gd")

    # 6. game/scripts/art/test_paperdoll_race_switch.gd
    rs_path = os.path.join(REPO_ROOT, "game/scripts/art/test_paperdoll_race_switch.gd")
    os.system(f"git -C {REPO_ROOT} checkout HEAD -- {rs_path}")
    with open(rs_path, "r", encoding="utf-8") as f:
        rs = f.read()

    rs = rs.replace('"swan", "bison", "rabbit"]', '"swan", "bison", "gecko", "rabbit"]')
    with open(rs_path, "w", encoding="utf-8") as f:
        f.write(rs)
    print("✓ Resolved test_paperdoll_race_switch.gd")

if __name__ == "__main__":
    resolve_projects_json()
    resolve_ui_json()
    resolve_paperdoll_slots()
    resolve_gdscript_files()
