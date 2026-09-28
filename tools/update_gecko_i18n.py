#!/usr/bin/env python3
"""為第四十五族巡管守宮 (The Conduit Gecko, gecko) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/CONDUIT_GECKO_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
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

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"檔案不存在: {ui_path}")
        continue
    with open(ui_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, v in entries.items():
        if k not in data:
            data[k] = v
            added += 1
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[{loc}] 更新 {ui_path} (新增 {added} 條)")
