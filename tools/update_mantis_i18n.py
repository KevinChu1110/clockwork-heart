#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "翠刃螳螂": "翠刃螳螂",
        "螳螂": "螳螂",
        "蔓谷沖壓薄銅螳螂底盤": "蔓谷沖壓薄銅螳螂底盤",
        "沖壓林冠折角金屬面盔": "沖壓林冠折角金屬面盔",
        "雙聯高透翡翠石英琉璃球形目鏡": "雙聯高透翡翠石英琉璃球形目鏡",
        "蔓谷藤蔓鉚接生漆板甲胸甲": "蔓谷藤蔓鉚接生漆板甲胸甲",
        "多節同軸彈簧平衡背囊與微型排氣風箱": "多節同軸彈簧平衡背囊與微型排氣風箱",
        "蔓谷雙環藤蔓雕花黃銅發條鑰匙": "蔓谷雙環藤蔓雕花黃銅發條鑰匙",
        "翠刃連斬機關爪": "翠刃連斬機關爪",
    },
    "zh_CN": {
        "翠刃螳螂": "翠刃螳螂",
        "螳螂": "螳螂",
        "蔓谷沖壓薄銅螳螂底盤": "蔓谷冲压薄铜螳螂底盘",
        "沖壓林冠折角金屬面盔": "冲压林冠折角金属面盔",
        "雙聯高透翡翠石英琉璃球形目鏡": "双联高透翡翠石英琉璃球形目镜",
        "蔓谷藤蔓鉚接生漆板甲胸甲": "蔓谷藤蔓铆接生漆板甲胸甲",
        "多節同軸彈簧平衡背囊與微型排氣風箱": "多节同轴弹簧平衡背囊与微型排气风箱",
        "蔓谷雙環藤蔓雕花黃銅發條鑰匙": "蔓谷双环藤蔓雕花黄铜发条钥匙",
        "翠刃連斬機關爪": "翠刃连斩机关爪",
    },
    "en": {
        "翠刃螳螂": "The Jade Mantis",
        "螳螂": "Mantis",
        "蔓谷沖壓薄銅螳螂底盤": "Vine Valley Stamped Brass Mantis Chassis",
        "沖壓林冠折角金屬面盔": "Stamped Canopy Metal Cowl",
        "雙聯高透翡翠石英琉璃球形目鏡": "Dual High-Clarity Emerald Glass Round Goggles",
        "蔓谷藤蔓鉚接生漆板甲胸甲": "Vine-Laced Brass Plate Cuirass",
        "多節同軸彈簧平衡背囊與微型排氣風箱": "Segmented Spring Balance Pack & Micro Bellows",
        "蔓谷雙環藤蔓雕花黃銅發條鑰匙": "Vine-Filigree Brass Key",
        "翠刃連斬機關爪": "Jade Scythe Claw",
    },
    "ja": {
        "翠刃螳螂": "翠刃カマキリ (すいじん)",
        "螳螂": "カマキリ",
        "蔓谷沖壓薄銅螳螂底盤": "蔓谷プレス薄銅カマキリシャーシ",
        "沖壓林冠折角金屬面盔": "樹冠折角プレス金属面甲",
        "雙聯高透翡翠石英琉璃球形目鏡": "双連高透翡翠石英琉璃球形ゴーグル",
        "蔓谷藤蔓鉚接生漆板甲胸甲": "蔓谷唐草鋲留生漆板甲胸甲",
        "多節同軸彈簧平衡背囊與微型排氣風箱": "多節同軸発条背嚢＆排気風箱",
        "蔓谷雙環藤蔓雕花黃銅發條鑰匙": "蔓谷の二重環唐草ぜんまい鍵",
        "翠刃連斬機關爪": "翠刃連斬の機關爪",
    },
    "ko": {
        "翠刃螳螂": "비취날 사마귀",
        "螳螂": "사마귀",
        "蔓谷沖壓薄銅螳螂底盤": "덩굴골짜기 프레스 얇은 구리 사마귀 하판",
        "沖壓林冠折角金屬面盔": "수관 절각 프레스 금속 투구",
        "雙聯高透翡翠石英琉璃球形目鏡": "쌍련 고투명 비취 석영 유리 구형 접안경",
        "蔓谷藤蔓鉚接生漆板甲胸甲": "덩굴골짜기 덩굴 리벳 옻칠 판갑 흉갑",
        "多節同軸彈簧平衡背囊與微型排氣風箱": "다절 동축 용수철 배낭 & 배기 풍구",
        "蔓谷雙環藤蔓雕花黃銅發條鑰匙": "덩굴골짜기 이중고리 태엽 열쇠",
        "翠刃連斬機關爪": "비취연참 기관발톱",
    },
    "es": {
        "翠刃螳螂": "La Mantis de Cuchilla de Jade",
        "螳螂": "Mantis",
        "蔓谷沖壓薄銅螳螂底盤": "Chasis de Cobre Estampado de Mantis del Valle de Enredaderas",
        "沖壓林冠折角金屬面盔": "Caperuza Metálica Estampada de Dosel",
        "雙聯高透翡翠石英琉璃球形目鏡": "Gafas Esféricas de Vidrio de Cuarzo de Jade Doble",
        "蔓谷藤蔓鉚接生漆板甲胸甲": "Coraza de Placas Remachadas de Enredadera",
        "多節同軸彈簧平衡背囊與微型排氣風箱": "Mochila con Resorte Articulado y Fuelle de Escape",
        "蔓谷雙環藤蔓雕花黃銅發條鑰匙": "Llave de Bronce con Filigrana de Enredadera",
        "翠刃連斬機關爪": "Garra Guadaña de Jade",
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
