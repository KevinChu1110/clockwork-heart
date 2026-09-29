#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "闢道頑驢": "闢道頑驢",
        "頑驢": "頑驢",
        "集市工兵沖壓馬口鐵金屬底盤": "集市工兵沖壓馬口鐵金屬底盤",
        "雙聯棘輪立體折疊長耳面盔": "雙聯棘輪立體折疊長耳面盔",
        "雙聯高透青石琉璃圓形目鏡": "雙聯高透青石琉璃圓形目鏡",
        "集市工兵鉚接生漆板甲胸甲": "集市工兵鉚接生漆板甲胸甲",
        "雙聯天軌木榫馱架與分節配重平衡尾": "雙聯天軌木榫馱架與分節配重平衡尾",
        "晨曦三葉雕花黃銅發條鑰匙": "晨曦三葉雕花黃銅發條鑰匙",
        "集市天軌闢道重斧": "集市天軌闢道重斧",
    },
    "zh_CN": {
        "闢道頑驢": "辟道顽驴",
        "頑驢": "顽驴",
        "集市工兵沖壓馬口鐵金屬底盤": "集市工兵冲压马口铁金属底盘",
        "雙聯棘輪立體折疊長耳面盔": "双联棘轮立体折叠长耳面盔",
        "雙聯高透青石琉璃圓形目鏡": "双联高透青石琉璃圆形目镜",
        "集市工兵鉚接生漆板甲胸甲": "集市工兵铆接生漆板甲胸甲",
        "雙聯天軌木榫馱架與分節配重平衡尾": "双联天轨木榫驮架与分节配重平衡尾",
        "晨曦三葉雕花黃銅發條鑰匙": "晨曦三叶雕花黄铜发条钥匙",
        "集市天軌闢道重斧": "集市天轨辟道重斧",
    },
    "en": {
        "闢道頑驢": "The Sapper Donkey",
        "頑驢": "Donkey",
        "集市工兵沖壓馬口鐵金屬底盤": "Bazaar Sapper Tinplate Stamped Chassis",
        "雙聯棘輪立體折疊長耳面盔": "Dual Ratchet Foldable Long Ears Cowl",
        "雙聯高透青石琉璃圓形目鏡": "Dual High-Clarity Slate Glass Round Goggles",
        "集市工兵鉚接生漆板甲胸甲": "Sapper Riveted Brass Cuirass",
        "雙聯天軌木榫馱架與分節配重平衡尾": "Dual Cograil Timber Pack & Counterweight Tail",
        "晨曦三葉雕花黃銅發條鑰匙": "Dawn Three-Leaf Clover Brass Key",
        "集市天軌闢道重斧": "Bazaar Cograil Clearing Axe",
    },
    "ja": {
        "闢道頑驢": "道拓きロバ (みちひらきロバ)",
        "頑驢": "ロバ",
        "集市工兵沖壓馬口鐵金屬底盤": "バザール工兵プレスブリキ金属シャーシ",
        "雙聯棘輪立體折疊長耳面盔": "双連ラチェット立体折畳長耳面甲",
        "雙聯高透青石琉璃圓形目鏡": "双連高透青石琉璃円形ゴーグル",
        "集市工兵鉚接生漆板甲胸甲": "バザール工兵鋲留生漆板甲胸甲",
        "雙聯天軌木榫馱架與分節配重平衡尾": "天軌木組荷鞍＆節動重錘尾",
        "晨曦三葉雕花黃銅發條鑰匙": "暁の三つ葉黄銅ぜんまい鍵",
        "集市天軌闢道重斧": "バザール軌道開拓重斧",
    },
    "ko": {
        "闢道頑驢": "길개척 당나귀",
        "頑驢": "당나귀",
        "集市工兵沖壓馬口鐵金屬底盤": "바자르 공병 프레스 양철 금속 하판",
        "雙聯棘輪立體折疊長耳面盔": "쌍련 라챗 입체 접이식 긴귀 투구",
        "雙聯高透青石琉璃圓形目鏡": "쌍련 고투명 청석 유리 원형 접안경",
        "集市工兵鉚接生漆板甲胸甲": "바자르 공병 리벳 옻칠 판갑 흉갑",
        "雙聯天軌木榫馱架與分節配重平衡尾": "천궤 목조 안장 & 다절 추꼬리",
        "晨曦三葉雕花黃銅發條鑰匙": "여명의 세잎 황동 태엽 열쇠",
        "集市天軌闢道重斧": "바자르 궤도 개척 중도끼",
    },
    "es": {
        "闢道頑驢": "El Asno Zapador",
        "頑驢": "Asno",
        "集市工兵沖壓馬口鐵金屬底盤": "Chasis de Hojalata Estampada de Zapador de Bazar",
        "雙聯棘輪立體折疊長耳面盔": "Caperuza de Orejas Largas Plegables con Trinquete Doble",
        "雙聯高透青石琉璃圓形目鏡": "Gafas Redondas de Vidrio de Pizarra de Alta Claridad Doble",
        "集市工兵鉚接生漆板甲胸甲": "Coraza Remachada de Laca de Zapador de Bazar",
        "雙聯天軌木榫馱架與分節配重平衡尾": "Albarda de Riel de Bazar y Cola con Contrapeso",
        "晨曦三葉雕花黃銅發條鑰匙": "Llave de Trébol de Latón del Alba",
        "集市天軌闢道重斧": "Gran Hacha Despejadora de Riel de Bazar",
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
