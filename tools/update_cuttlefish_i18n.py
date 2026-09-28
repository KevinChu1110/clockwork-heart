#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "墨影烏賊": "墨影烏賊",
        "墨紋烏賊": "墨紋烏賊",
        "烏賊": "烏賊",
        "海淵墨影雙鋒匕": "海淵墨影雙鋒匕",
        "三葉深海渦輪水流發條鑰匙": "三葉深海渦輪水流發條鑰匙",
        "氣動高壓發煙雙聯墨囊氣罐": "氣動高壓發煙雙聯墨囊氣罐",
        "鍍鈦合金與琉璃海藍搪瓷素體底盤": "鍍鈦合金與琉璃海藍搪瓷素體底盤",
        "深潛圓頂頭盔與氣動平衡側鰭": "深潛圓頂頭盔與氣動平衡側鰭",
        "海淵夜行輕量耐壓背心": "海淵夜行輕量耐壓背心",
        "雙聯水下耐壓石英探照目鏡": "雙聯水下耐壓石英探照目鏡",
    },
    "zh_CN": {
        "墨影烏賊": "墨影乌贼",
        "墨紋烏賊": "墨纹乌贼",
        "烏賊": "乌贼",
        "海淵墨影雙鋒匕": "海渊墨影双锋匕",
        "三葉深海渦輪水流發條鑰匙": "三叶深海涡轮水流发条钥匙",
        "氣動高壓發煙雙聯墨囊氣罐": "气动高压发烟双联墨囊气罐",
        "鍍鈦合金與琉璃海藍搪瓷素體底盤": "镀钛合金与琉璃海蓝搪瓷素体底盘",
        "深潛圓頂頭盔與氣動平衡側鰭": "深潜圆顶头盔与气动平衡侧鳍",
        "海淵夜行輕量耐壓背心": "海渊夜行轻量耐压背心",
        "雙聯水下耐壓石英探照目鏡": "双联水下耐压石英探照目镜",
    },
    "en": {
        "墨影烏賊": "The Inksmoke Cuttlefish",
        "墨紋烏賊": "The Ink-Marked Cuttlefish",
        "烏賊": "Cuttlefish",
        "海淵墨影雙鋒匕": "Abyssal Inksmoke Twin Daggers",
        "三葉深海渦輪水流發條鑰匙": "Tri-Vane Turbine Winding Key",
        "氣動高壓發煙雙聯墨囊氣罐": "Pneumatic High-Pressure Ink-Siphon Pack",
        "鍍鈦合金與琉璃海藍搪瓷素體底盤": "Titanium Cyan-Enamel Chassis",
        "深潛圓頂頭盔與氣動平衡側鰭": "Diving Cowl with Balance Fins",
        "海淵夜行輕量耐壓背心": "Abyssal Shinobi Cuirass",
        "雙聯水下耐壓石英探照目鏡": "Dual Quartz Optic Lenses",
    },
    "ja": {
        "墨影烏賊": "墨影の烏賊 (ボクエイノコウイカ)",
        "墨紋烏賊": "墨紋の烏賊 (ボクモンノコウイカ)",
        "烏賊": "烏賊",
        "海淵墨影雙鋒匕": "海淵墨影双鋒短匕",
        "三葉深海渦輪水流發條鑰匙": "三葉深海タービンぜんまい鍵",
        "氣動高壓發煙雙聯墨囊氣罐": "気動高圧発煙連装墨嚢タンク",
        "鍍鈦合金與琉璃海藍搪瓷素體底盤": "チタン合金瑠璃海藍エナメル素体",
        "深潛圓頂頭盔與氣動平衡側鰭": "深潜ドーム兜・気動バランス側鰭",
        "海淵夜行輕量耐壓背心": "海淵夜行耐圧ベスト",
        "雙聯水下耐壓石英探照目鏡": "連装水中耐圧石英探照レンズ",
    },
    "ko": {
        "墨影烏賊": "먹그림자 갑오징어",
        "墨紋烏賊": "먹무늬 갑오징어",
        "烏賊": "갑오징어",
        "海淵墨影雙鋒匕": "심연 묵영 쌍단검",
        "三葉深海渦輪水流發條鑰匙": "3엽 심해 터빈 태엽 열쇠",
        "氣動高壓發煙雙聯墨囊氣罐": "기동 고압 발연 2연장 먹물 탱크",
        "鍍鈦合金與琉璃海藍搪瓷素體底盤": "티타늄 합금 유리해람 에나멜 소체",
        "深潛圓頂頭盔與氣動平衡側鰭": "심잠 돔 투구와 기동 밸런스 지느러미",
        "海淵夜行輕量耐壓背心": "심연 야행 경량 내압 조끼",
        "雙聯水下耐壓石英探照目鏡": "2연장 수중 내압 석영 탐조 렌즈",
    },
    "es": {
        "墨影烏賊": "La Sepia de Tinta Abisal",
        "墨紋烏賊": "La Sepia de Patrones de Tinta",
        "烏賊": "Sepia",
        "海淵墨影雙鋒匕": "Dagas Gemelas de Tinta Abisal",
        "三葉深海渦輪水流發條鑰匙": "Llave de Cuerda de Turbina de Tres Palas",
        "氣動高壓發煙雙聯墨囊氣罐": "Mochila Neumática Doble de Tinta de Alta Presión",
        "鍍鈦合金與琉璃海藍搪瓷素體底盤": "Chasis de Esmalte Azul Abisal y Titanio",
        "深潛圓頂頭盔與氣動平衡側鰭": "Capucha de Buceo con Aletas de Equilibrio",
        "海淵夜行輕量耐壓背心": "Coraza Ligera Shinobi Abisal",
        "雙聯水下耐壓石英探照目鏡": "Lentes Ópticas Dobles de Cuarzo de Alta Presión",
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
