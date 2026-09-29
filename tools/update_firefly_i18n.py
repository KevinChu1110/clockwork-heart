#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "靈燈飛螢": "靈燈飛螢",
        "飛螢": "飛螢",
        "深林沖壓薄銅馬口鐵底盤": "深林沖壓薄銅馬口鐵底盤",
        "雙聯微調黃銅觸角調諧冠": "雙聯微調黃銅觸角調諧冠",
        "花蕾造型四瓣齒輪黃銅發條鑰匙": "花蕾造型四瓣齒輪黃銅發條鑰匙",
        "藤蔓工裝編織輕量背心胸甲": "藤蔓工裝編織輕量背心胸甲",
        "雙聯聚碳酸酯夜燈球形目鏡": "雙聯聚碳酸酯夜燈球形目鏡",
        "深林熒光藤蔓發條長杖": "深林熒光藤蔓發條長杖",
        "注塑樹脂熒光腹囊與沖壓透光薄翅": "注塑樹脂熒光腹囊與沖壓透光薄翅",
    },
    "zh_CN": {
        "靈燈飛螢": "灵灯飞萤",
        "飛螢": "飞萤",
        "深林沖壓薄銅馬口鐵底盤": "深林冲压薄铜马口铁底盘",
        "雙聯微調黃銅觸角調諧冠": "双联微调黄铜触角调谐冠",
        "花蕾造型四瓣齒輪黃銅發條鑰匙": "花蕾造型四瓣齿轮黄铜发条钥匙",
        "藤蔓工裝編織輕量背心胸甲": "藤蔓工装编织轻量背心胸甲",
        "雙聯聚碳酸酯夜燈球形目鏡": "双联聚碳酸酯夜灯球形目镜",
        "深林熒光藤蔓發條長杖": "深林荧光藤蔓发条长杖",
        "注塑樹脂熒光腹囊與沖壓透光薄翅": "注塑树脂荧光腹囊与冲压透光薄翅",
    },
    "en": {
        "靈燈飛螢": "The Lantern Firefly",
        "飛螢": "Firefly",
        "深林沖壓薄銅馬口鐵底盤": "Emerald Stamped Brass & Tinplate Chassis",
        "雙聯微調黃銅觸角調諧冠": "Dual Fine-Tuning Brass Antenna Tuner Cowl",
        "花蕾造型四瓣齒輪黃銅發條鑰匙": "Floral-Gear Four-Petal Brass Winding Key",
        "藤蔓工裝編織輕量背心胸甲": "Clockwork Vine Harness Woven Lightweight Cuirass",
        "雙聯聚碳酸酯夜燈球形目鏡": "Dual Spherical Lantern Quartz Night-Light Eyes",
        "深林熒光藤蔓發條長杖": "Emerald Luminescent Vine Clockwork Staff",
        "注塑樹脂熒光腹囊與沖壓透光薄翅": "Luminescent Resin Abdomen & Stamped Brass Elytra",
    },
    "ja": {
        "靈燈飛螢": "霊灯ホタル (ランタン・ファイアフライ)",
        "飛螢": "ホタル",
        "深林沖壓薄銅馬口鐵底盤": "深林プレス薄銅ブリキシャーシ",
        "雙聯微調黃銅觸角調諧冠": "双連微調整黄銅触角チューナーカウル",
        "花蕾造型四瓣齒輪黃銅發條鑰匙": "花蕾造形四弁歯車黄銅ぜんまい鍵",
        "藤蔓工裝編織輕量背心胸甲": "蔓ワーク編組軽量ベスト胸甲",
        "雙聯聚碳酸酯夜燈球形目鏡": "双連ポリカーボネート夜灯球形ゴーグル",
        "深林熒光藤蔓發條長杖": "深林蛍光蔓ぜんまい長杖",
        "注塑樹脂熒光腹囊與沖壓透光薄翅": "射出樹脂蛍光腹嚢とプレス透光薄翅",
    },
    "ko": {
        "靈燈飛螢": "영등 반딧불이 (랜턴 파이어플라이)",
        "飛螢": "반딧불이",
        "深林沖壓薄銅馬口鐵底盤": "깊은숲 프레스 박동 양철 하판",
        "雙聯微調黃銅觸角調諧冠": "쌍련 미세조정 황동 촉각 튜너 카울",
        "花蕾造型四瓣齒輪黃銅發條鑰匙": "꽃봉오리형 4엽 기어 황동 태엽 열쇠",
        "藤蔓工裝編織輕量背心胸甲": "덩굴 워크 편조 경량 조끼 흉갑",
        "雙聯聚碳酸酯夜燈球形目鏡": "쌍련 폴리카보네이트 야간등 구형 접안경",
        "深林熒光藤蔓發條長杖": "깊은숲 형광 덩굴 태엽 장봉",
        "注塑樹脂熒光腹囊與沖壓透光薄翅": "사출 수지 형광 복낭과 프레스 투광 박시",
    },
    "es": {
        "靈燈飛螢": "La Luciérnaga de Linterna",
        "飛螢": "Luciérnaga",
        "深林沖壓薄銅馬口鐵底盤": "Chasis de Hojalata y Latón Estampado de Bosque Profundo",
        "雙聯微調黃銅觸角調諧冠": "Caperuza Sintonizadora de Antena de Latón de Ajuste Fino Doble",
        "花蕾造型四瓣齒輪黃銅發條鑰匙": "Llave de Cuerda de Latón de Engranaje Floral de Cuatro Pétalos",
        "藤蔓工裝編織輕量背心胸甲": "Peto Ligero de Chaleco Tejido con Arnés de Enredadera Mecánica",
        "雙聯聚碳酸酯夜燈球形目鏡": "Ojos Esféricos de Luz Nocturna de Cuarzo de Linterna Doble",
        "深林熒光藤蔓發條長杖": "Bastón Mecánico de Enredadera Luminiscente de Bosque Profundo",
        "注塑樹脂熒光腹囊與沖壓透光薄翅": "Abdomen de Resina Luminiscente y Élitros de Latón Estampado",
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
