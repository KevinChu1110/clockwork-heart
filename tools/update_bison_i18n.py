#!/usr/bin/env python3
"""為第四十四族撼地野牛 (The Groundshaker Bison, bison) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/GROUNDSHAKER_BISON_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
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
        "舊庫拆解工兵重胸甲": "폐품고 해체 공병 중흉갑",
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
