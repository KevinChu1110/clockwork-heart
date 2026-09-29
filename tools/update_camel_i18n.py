#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "日晷駱駝": "日晷駱駝",
        "駱駝": "駱駝",
        "廢土日晷折射短杖": "廢土日晷折射短杖",
        "黃銅日晷雙環刻度發條鑰匙": "黃銅日晷雙環刻度發條鑰匙",
        "雙聯散熱油壺金屬駝峰": "雙聯散熱油壺金屬駝峰",
        "磨砂馬口鐵雙峰矮萌素體底盤": "磨砂馬口鐵雙峰矮萌素體底盤",
        "日晷晷針折光觀測兜帽": "日晷晷針折光觀測兜帽",
        "廢土觀星學者帆布補丁長袍": "廢土觀星學者帆布補丁長袍",
        "雙聯光譜分折石英目鏡": "雙聯光譜分折石英目鏡",
    },
    "zh_CN": {
        "日晷駱駝": "日晷骆驼",
        "駱駝": "骆驼",
        "廢土日晷折射短杖": "废土日晷折射短杖",
        "黃銅日晷雙環刻度發條鑰匙": "黄铜日晷双环刻度发条钥匙",
        "雙聯散熱油壺金屬駝峰": "双联散热油壶金属驼峰",
        "磨砂馬口鐵雙峰矮萌素體底盤": "磨砂马口铁双峰矮萌素体底盘",
        "日晷晷針折光觀測兜帽": "日晷晷针折光观测兜帽",
        "廢土觀星學者帆布補丁長袍": "废土观星学者帆布补丁长袍",
        "雙聯光譜分折石英目鏡": "双联光谱分折石英目镜",
    },
    "en": {
        "日晷駱駝": "The Sundial Camel",
        "駱駝": "Camel",
        "廢土日晷折射短杖": "Wasteland Sundial Refraction Rod",
        "黃銅日晷雙環刻度發條鑰匙": "Armillary Dial Brass Winding Key",
        "雙聯散熱油壺金屬駝峰": "Twin Condenser Oil Humps",
        "磨砂馬口鐵雙峰矮萌素體底盤": "Sanded Tinplate Camel Chassis",
        "日晷晷針折光觀測兜帽": "Sundial Gnomon Cowl",
        "廢土觀星學者帆布補丁長袍": "Scavenger Astronomer Robe",
        "雙聯光譜分折石英目鏡": "Dual Spectroscope Quartz Lenses",
    },
    "ja": {
        "日晷駱駝": "日晷の駱駝 (ニッキのラクダ)",
        "駱駝": "ラクダ",
        "廢土日晷折射短杖": "廃土日晷屈折短杖",
        "黃銅日晷雙環刻度發條鑰匙": "黄銅日晷二重環刻度ぜんまい鍵",
        "雙聯散熱油壺金屬駝峰": "連装放熱油壺金属瘤",
        "磨砂馬口鐵雙峰矮萌素體底盤": "研磨ブリキ二重瘤矮萌素体",
        "日晷晷針折光觀測兜帽": "日晷晷針屈折観測頭巾",
        "廢土觀星學者帆布補丁長袍": "廃土観星学者帆布継ぎ当て長袍",
        "雙聯光譜分折石英目鏡": "連装分光石英接眼レンズ",
    },
    "ko": {
        "日晷駱駝": "일구 낙타",
        "駱駝": "낙타",
        "廢土日晷折射短杖": "폐토 일구 굴절 단장",
        "黃銅日晷雙環刻度發條鑰匙": "황동 일구 2중환 눈금 태엽 열쇠",
        "雙聯散熱油壺金屬駝峰": "2연장 방열 유호 금속 혹",
        "磨砂馬口鐵雙峰矮萌素體底盤": "연마 양철 2개혹 소체 하판",
        "日晷晷針折光觀測兜帽": "일구 규침 굴절 관측 두건",
        "廢土觀星學者帆布補丁長袍": "폐토 관성학자 캔버스 누비 로브",
        "雙聯光譜分折石英目鏡": "2연장 분광 석영 접안렌즈",
    },
    "es": {
        "日晷駱駝": "El Camello Reloj de Sol",
        "駱駝": "Camello",
        "廢土日晷折射短杖": "Vara de Refracción Reloj de Sol del Yermo",
        "黃銅日晷雙環刻度發條鑰匙": "Llave de Cuerda Armilar de Latón",
        "雙聯散熱油壺金屬駝峰": "Jorobas Metálicas de Aceite de Doble Condensador",
        "磨砂馬口鐵雙峰矮萌素體底盤": "Chasis de Camello de Hojalata Pulida",
        "日晷晷針折光觀測兜帽": "Capucha de Observación Gnomon de Reloj de Sol",
        "廢土觀星學者帆布補丁長袍": "Túnica de Astrónomo Chatarrero",
        "雙聯光譜分折石英目鏡": "Lentes de Cuarzo de Doble Espectroscopio",
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
