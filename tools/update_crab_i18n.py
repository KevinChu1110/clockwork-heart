#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "熔砧石蟹": "熔砧石蟹",
        "熔矽石蟹": "熔矽石蟹",
        "石蟹": "石蟹",
        "蟹": "蟹",
        "黑曜衝壓熔岩拳套": "黑曜衝壓熔岩拳套",
        "四葉散熱鍛造發條鑰匙": "四葉散熱鍛造發條鑰匙",
        "雙聯氣動洩壓排煙煙囪": "雙聯氣動洩壓排煙煙囪",
        "鑄鐵鍛爐矮萌甲殼素體底盤": "鑄鐵鍛爐矮萌甲殼素體底盤",
        "雙向潛望測距護額頭盔": "雙向潛望測距護額頭盔",
        "熔爐工兵重裝石磚胸甲": "熔爐工兵重裝石磚胸甲",
        "雙聯壓力儀表石英凸透鏡": "雙聯壓力儀表石英凸透鏡",
    },
    "zh_CN": {
        "熔砧石蟹": "熔砧石蟹",
        "熔矽石蟹": "熔硅石蟹",
        "石蟹": "石蟹",
        "蟹": "蟹",
        "黑曜衝壓熔岩拳套": "黑曜冲压熔岩拳套",
        "四葉散熱鍛造發條鑰匙": "四叶散热锻造发条钥匙",
        "雙聯氣動洩壓排煙煙囪": "双联气动泄压排烟烟囱",
        "鑄鐵鍛爐矮萌甲殼素體底盤": "铸铁锻炉矮萌甲壳素体底盘",
        "雙向潛望測距護額頭盔": "双向潜望测距护额头盔",
        "熔爐工兵重裝石磚胸甲": "熔炉工兵重装石砖胸甲",
        "雙聯壓力儀表石英凸透鏡": "双联压力仪表石英凸透镜",
    },
    "en": {
        "熔砧石蟹": "The Anvil Crab",
        "熔矽石蟹": "The Silica Crab",
        "石蟹": "Stone Crab",
        "蟹": "Crab",
        "黑曜衝壓熔岩拳套": "Obsidian Stamping Magma Gauntlets",
        "四葉散熱鍛造發條鑰匙": "Quad-Flue Anvil Winding Key",
        "雙聯氣動洩壓排煙煙囪": "Pneumatic Dual Exhaust Chimneys",
        "鑄鐵鍛爐矮萌甲殼素體底盤": "Cast-Iron Crucible Crab Chassis",
        "雙向潛望測距護額頭盔": "Periscope Visor Cowl",
        "熔爐工兵重裝石磚胸甲": "Furnace Sapper Cuirass",
        "雙聯壓力儀表石英凸透鏡": "Dual-Gauge Convex Quartz Lenses",
    },
    "ja": {
        "熔砧石蟹": "熔砧の石蟹 (ヨウチンのイシガニ)",
        "熔矽石蟹": "熔ケイの石蟹 (ヨウケイノイシガニ)",
        "石蟹": "石蟹",
        "蟹": "蟹",
        "黑曜衝壓熔岩拳套": "黒曜衝圧熔岩拳套",
        "四葉散熱鍛造發條鑰匙": "四葉放熱鍛造ぜんまい鍵",
        "雙聯氣動洩壓排煙煙囪": "気動連装排煙煙突",
        "鑄鐵鍛爐矮萌甲殼素體底盤": "鋳鉄鍛炉矮萌甲殻素体",
        "雙向潛望測距護額頭盔": "双方向潜望測距額兜",
        "熔爐工兵重裝石磚胸甲": "熔炉工兵重装石煉瓦胸甲",
        "雙聯壓力儀表石英凸透鏡": "連装圧力計石英凸レンズ",
    },
    "ko": {
        "熔砧石蟹": "용침 석게",
        "熔矽石蟹": "용규 석게",
        "石蟹": "석게",
        "蟹": "게",
        "黑曜衝壓熔岩拳套": "흑요 충압 용암 권투",
        "四葉散熱鍛造發條鑰匙": "4엽 방열 단조 태엽 열쇠",
        "雙聯氣動洩壓排煙煙囪": "기동 2연장 감압 배연 굴뚝",
        "鑄鐵鍛爐矮萌甲殼素體底盤": "주철 단로 소체 하판",
        "雙向潛望測距護額頭盔": "양방향 잠망 측거 투구",
        "熔爐工兵重裝石磚胸甲": "용광로 공병 중장 석전 흉갑",
        "雙聯壓力儀表石英凸透鏡": "2연장 압력계 석영 볼록 렌즈",
    },
    "es": {
        "熔砧石蟹": "El Cangrejo Yunque",
        "熔矽石蟹": "El Cangrejo de Sílice",
        "石蟹": "Cangrejo de Piedra",
        "蟹": "Cangrejo",
        "黑曜衝壓熔岩拳套": "Guanteletes de Magma de Estampado de Obsidiana",
        "四葉散熱鍛造發條鑰匙": "Llave de Cuerda Yunque de Cuatro Aspas",
        "雙聯氣動洩壓排煙煙囪": "Chimeneas Neumáticas Dobles de Escape",
        "鑄鐵鍛爐矮萌甲殼素體底盤": "Chasis de Caparazón de Forja de Hierro Fundido",
        "雙向潛望測距護額頭盔": "Capucha Visor Periscópico",
        "熔爐工兵重裝石磚胸甲": "Coraza de Zapador de Forja",
        "雙聯壓力儀表石英凸透鏡": "Lentes Ópticas Convexas de Doble Manómetro",
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
    print(f"[{loc}] Updated {ui_path} (added {added})")
