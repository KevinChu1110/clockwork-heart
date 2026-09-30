#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "伏影沙蠍": "伏影沙蠍",
        "沙蠍": "沙蠍",
        "荒漠沖壓馬口鐵沙蠍底盤": "荒漠沖壓馬口鐵沙蠍底盤",
        "沖壓防沙折角金屬面盔": "沖壓防沙折角金屬面盔",
        "雙聯高透琥珀金晶琉璃圓形目鏡": "雙聯高透琥珀金晶琉璃圓形目鏡",
        "荒漠拾荒鉚接生漆板甲胸甲": "荒漠拾荒鉚接生漆板甲胸甲",
        "多節同軸彈簧尾刺導軌與配重重錘": "多節同軸彈簧尾刺導軌與配重重錘",
        "荒漠四角齒輪雕花黃銅發條鑰匙": "荒漠四角齒輪雕花黃銅發條鑰匙",
        "沙丘穿棘機關鏢": "沙丘穿棘機關鏢",
    },
    "zh_CN": {
        "伏影沙蠍": "伏影沙蝎",
        "沙蠍": "沙蝎",
        "荒漠沖壓馬口鐵沙蠍底盤": "荒漠冲压马口铁沙蝎底盘",
        "沖壓防沙折角金屬面盔": "冲压防沙折角金属面盔",
        "雙聯高透琥珀金晶琉璃圓形目鏡": "双联高透琥珀金晶琉璃圆形目镜",
        "荒漠拾荒鉚接生漆板甲胸甲": "荒漠拾荒铆接生漆板甲胸甲",
        "多節同軸彈簧尾刺導軌與配重重錘": "多节同轴弹簧尾刺导轨与配重重锤",
        "荒漠四角齒輪雕花黃銅發條鑰匙": "荒漠四角齿轮雕花黄铜发条钥匙",
        "沙丘穿棘機關鏢": "沙丘穿棘机关镖",
    },
    "en": {
        "伏影沙蠍": "The Duneshadow Scorpion",
        "沙蠍": "Scorpion",
        "荒漠沖壓馬口鐵沙蠍底盤": "Dune Tinplate Stamped Scorpion Chassis",
        "沖壓防沙折角金屬面盔": "Stamped Dune-Visor Metal Cowl",
        "雙聯高透琥珀金晶琉璃圓形目鏡": "Dual High-Clarity Amber Glass Round Goggles",
        "荒漠拾荒鉚接生漆板甲胸甲": "Wasteland Scavenger Riveted Plate Cuirass",
        "多節同軸彈簧尾刺導軌與配重重錘": "Articulated Spring Stinger Tail Rail",
        "荒漠四角齒輪雕花黃銅發條鑰匙": "Dune Cross-Cog Brass Key",
        "沙丘穿棘機關鏢": "Duneshadow Spike Dart",
    },
    "ja": {
        "伏影沙蠍": "影伏せサソリ (かげふせサソリ)",
        "沙蠍": "サソリ",
        "荒漠沖壓馬口鐵沙蠍底盤": "荒野プレスブリキサソリシャーシ",
        "沖壓防沙折角金屬面盔": "防砂折角プレス金属面甲",
        "雙聯高透琥珀金晶琉璃圓形目鏡": "双連高透琥珀金晶琉璃円形ゴーグル",
        "荒漠拾荒鉚接生漆板甲胸甲": "荒野廃品鋲留生漆板甲胸甲",
        "多節同軸彈簧尾刺導軌與配重重錘": "多節同軸発条尾＆重錘",
        "荒漠四角齒輪雕花黃銅發條鑰匙": "荒野の四角歯車ぜんまい鍵",
        "沙丘穿棘機關鏢": "砂丘貫き機關鏢",
    },
    "ko": {
        "伏影沙蠍": "모래그림자 전갈",
        "沙蠍": "전갈",
        "荒漠沖壓馬口鐵沙蠍底盤": "황야 프레스 양철 전갈 하판",
        "沖壓防沙折角金屬面盔": "방사 절각 프레스 금속 투구",
        "雙聯高透琥珀金晶琉璃圓形目鏡": "쌍련 고투명 호박 금정 유리 원형 접안경",
        "荒漠拾荒鉚接生漆板甲胸甲": "황야 고물수집 리벳 옻칠 판갑 흉갑",
        "多節同軸彈簧尾刺導軌與配重重錘": "다절 동축 용수철꼬리 & 평형추",
        "荒漠四角齒輪雕花黃銅發條鑰匙": "황야의 사각 톱니 태엽 열쇠",
        "沙丘穿棘機關鏢": "모래언덕 관통 기관비표",
    },
    "es": {
        "伏影沙蠍": "El Escorpión de las Dunas",
        "沙蠍": "Escorpión",
        "荒漠沖壓馬口鐵沙蠍底盤": "Chasis de Hojalata Estampada de Escorpión de Dunas",
        "沖壓防沙折角金屬面盔": "Caperuza Metálica con Visor Estampado de Dunas",
        "雙聯高透琥珀金晶琉璃圓形目鏡": "Gafas Redondas de Vidrio de Ámbar de Alta Claridad Doble",
        "荒漠拾荒鉚接生漆板甲胸甲": "Coraza de Placas Remachadas de Carroñero del Páramo",
        "多節同軸彈簧尾刺導軌與配重重錘": "Cola con Resorte Articulado y Riel de Aguijón",
        "荒漠四角齒輪雕花黃銅發條鑰匙": "Llave de Engranaje Cruzado de Dunas",
        "沙丘穿棘機關鏢": "Dardo Perforador de Dunas",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"File not found: {ui_path}")
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
    print(f"成功更新 {loc}/ui.json，新增 {added} 條目")
