#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "黑曜金龜": "黑曜金龜",
        "金龜": "金龜",
        "黑曜耐火鑄鐵矮萌底盤": "黑曜耐火鑄鐵矮萌底盤",
        "黑曜淬火雙叉金角面罩": "黑曜淬火雙叉金角面罩",
        "熔金琥珀透鏡耐火面甲": "熔金琥珀透鏡耐火面甲",
        "赤焰熔爐隔熱工匠護裙": "赤焰熔爐隔熱工匠護裙",
        "雙聯微型高壓洩壓排煙管短尾": "雙聯微型高壓洩壓排煙管短尾",
        "四葉鍛造十字火紋黃銅發條鑰匙": "四葉鍛造十字火紋黃銅發條鑰匙",
        "赤焰黑曜護體靈晶": "赤焰黑曜護體靈晶",
    },
    "zh_CN": {
        "黑曜金龜": "黑曜金龟",
        "金龜": "金龟",
        "黑曜耐火鑄鐵矮萌底盤": "黑曜耐火铸铁矮萌底盘",
        "黑曜淬火雙叉金角面罩": "黑曜淬火双叉金角面罩",
        "熔金琥珀透鏡耐火面甲": "熔金琥珀透镜耐火面甲",
        "赤焰熔爐隔熱工匠護裙": "赤焰熔炉隔热工匠护裙",
        "雙聯微型高壓洩壓排煙管短尾": "双联微型高压泄压排烟管短尾",
        "四葉鍛造十字火紋黃銅發條鑰匙": "四叶锻造十字火纹黄铜发条钥匙",
        "赤焰黑曜護體靈晶": "赤焰黑曜护体灵晶",
    },
    "en": {
        "黑曜金龜": "The Obsidian Scarab",
        "金龜": "Scarab",
        "黑曜耐火鑄鐵矮萌底盤": "Obsidian Refractory Cast Iron Chibi Chassis",
        "黑曜淬火雙叉金角面罩": "Obsidian Quenched Twin-Horn Visor Cowl",
        "熔金琥珀透鏡耐火面甲": "Molten Amber Refractory Visor Lens",
        "赤焰熔爐隔熱工匠護裙": "Crucible Furnace Heat-Resistant Artisan Apron",
        "雙聯微型高壓洩壓排煙管短尾": "Twin Micro-Vent Exhaust Tail",
        "四葉鍛造十字火紋黃銅發條鑰匙": "Four-Leaf Forge Cross-Fire Brass Winding Key",
        "赤焰黑曜護體靈晶": "Crucible Obsidian Shield-Focus",
    },
    "ja": {
        "黑曜金龜": "黒曜金亀 (オブシディアン・スカラベ)",
        "金龜": "金亀",
        "黑曜耐火鑄鐵矮萌底盤": "黒曜耐火鋳鉄矮萌素体",
        "黑曜淬火雙叉金角面罩": "黒曜焼入れ双角バイザー兜",
        "熔金琥珀透鏡耐火面甲": "溶金琥珀レンズ耐火面甲",
        "赤焰熔爐隔熱工匠護裙": "赤炎炉遮熱職人エプロン",
        "雙聯微型高壓洩壓排煙管短尾": "二連超小型減圧排煙管短尾",
        "四葉鍛造十字火紋黃銅發條鑰匙": "四葉鍛造十字火紋黄銅ぜんまい鍵",
        "赤焰黑曜護體靈晶": "赤炎黒曜護身霊晶",
    },
    "ko": {
        "黑曜金龜": "흑요석 풍뎅이 (옵시디언 스카라베)",
        "金龜": "풍뎅이",
        "黑曜耐火鑄鐵矮萌底盤": "흑요 내화 주철 꼬마 소체 하판",
        "黑曜淬火雙叉金角面罩": "흑요 담금질 쌍각 바이저 두건",
        "熔金琥珀透鏡耐火面甲": "용금 호박 렌즈 내화 면갑",
        "赤焰熔爐隔熱工匠護裙": "화염용광로 단열 장인 앞치마",
        "雙聯微型高壓洩壓排煙管短尾": "2연 마이크로 감압 배연관 단미",
        "四葉鍛造十字火紋黃銅發條鑰匙": "4엽 단조 십자 화문 황동 태엽 열쇠",
        "赤焰黑曜護體靈晶": "화염 흑요 호신 영정",
    },
    "es": {
        "黑曜金龜": "El Escarabajo de Obsidiana",
        "金龜": "Escarabajo",
        "黑曜耐火鑄鐵矮萌底盤": "Chasis Chibi de Hierro Fundido Refractario de Obsidiana",
        "黑曜淬火雙叉金角面罩": "Capucha de Visera Templada de Doble Cuerno de Obsidiana",
        "熔金琥珀透鏡耐火面甲": "Máscara Facial Refractaria con Lente de Ámbar Fundido",
        "赤焰熔爐隔熱工匠護裙": "Delantal de Artesano Aislante del Horno Crisol",
        "雙聯微型高壓洩壓排煙管短尾": "Cola Corta de Tubo de Escape Doble de Alivio de Presión",
        "四葉鍛造十字火紋黃銅發條鑰匙": "Llave de Cuerda de Latón Forjada de Cuatro Hojas con Cruz de Fuego",
        "赤焰黑曜護體靈晶": "Cristal Espiritual Protector de Obsidiana del Crisol",
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
