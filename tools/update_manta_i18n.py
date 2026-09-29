#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "潮汐蝠魟": "潮汐蝠魟",
        "蝠魟": "蝠魟",
        "深海沖壓耐蝕鍍鈦金屬底盤": "深海沖壓耐蝕鍍鈦金屬底盤",
        "雙聯微型導流頭角導航冠": "雙聯微型導流頭角導航冠",
        "海星造型五齒輪黃銅發條鑰匙": "海星造型五齒輪黃銅發條鑰匙",
        "深海潛水工裝編織輕量胸甲": "深海潛水工裝編織輕量胸甲",
        "雙聯耐高壓深海石英泡罩目鏡": "雙聯耐高壓深海石英泡罩目鏡",
        "海淵流體脈衝複合機關弓": "海淵流體脈衝複合機關弓",
        "柔性鈦合金滑翔翼翅與天線平衡細尾": "柔性鈦合金滑翔翼翅與天線平衡細尾",
    },
    "zh_CN": {
        "潮汐蝠魟": "潮汐蝠魟",
        "蝠魟": "蝠魟",
        "深海沖壓耐蝕鍍鈦金屬底盤": "深海冲压耐蚀镀钛金属底盘",
        "雙聯微型導流頭角導航冠": "双联微型导流头角导航冠",
        "海星造型五齒輪黃銅發條鑰匙": "海星造型五齿轮黄铜发条钥匙",
        "深海潛水工裝編織輕量胸甲": "深海潜水工装编织轻量胸甲",
        "雙聯耐高壓深海石英泡罩目鏡": "双联耐高压深海石英泡罩目镜",
        "海淵流體脈衝複合機關弓": "海渊流体脉冲复合机关弓",
        "柔性鈦合金滑翔翼翅與天線平衡細尾": "柔性钛合金滑翔翼翅与天线平衡细尾",
    },
    "en": {
        "潮汐蝠魟": "The Tidal Manta",
        "蝠魟": "Manta",
        "深海沖壓耐蝕鍍鈦金屬底盤": "Abyssal Stamped Corrosion-Resistant Titanium Chassis",
        "雙聯微型導流頭角導航冠": "Dual Micro Hydrofoil Horn Navigation Cowl",
        "海星造型五齒輪黃銅發條鑰匙": "Starfish-Gear Five-Tooth Brass Winding Key",
        "深海潛水工裝編織輕量胸甲": "Deepsea Diver Harness Woven Lightweight Cuirass",
        "雙聯耐高壓深海石英泡罩目鏡": "Dual High-Pressure Quartz Bubble Goggles",
        "海淵流體脈衝複合機關弓": "Abyssal Hydro-Pulse Compound Bow",
        "柔性鈦合金滑翔翼翅與天線平衡細尾": "Flexible Titanium Gliding Wings & Antenna Tail Curio",
    },
    "ja": {
        "潮汐蝠魟": "潮汐マンタ (タイダル・マンタ)",
        "蝠魟": "マンタ",
        "深海沖壓耐蝕鍍鈦金屬底盤": "深海プレス耐食チタンシャーシ",
        "雙聯微型導流頭角導航冠": "双連超小型整流頭角ナビゲーションカウル",
        "海星造型五齒輪黃銅發條鑰匙": "ヒトデ造形五歯車黄銅ぜんまい鍵",
        "深海潛水工裝編織輕量胸甲": "深海ダイバーハーネス編組軽量胸甲",
        "雙聯耐高壓深海石英泡罩目鏡": "双連耐高圧深海石英バブルゴーグル",
        "海淵流體脈衝複合機關弓": "海淵流体パルス複合からくり弓",
        "柔性鈦合金滑翔翼翅與天線平衡細尾": "フレキシブルチタン滑翔翼とアンテナ細尾",
    },
    "ko": {
        "潮汐蝠魟": "조석 쥐가오리 (타이달 만타)",
        "蝠魟": "쥐가오리",
        "深海沖壓耐蝕鍍鈦金屬底盤": "심해 프레스 내식 티타늄 하판",
        "雙聯微型導流頭角導航冠": "쌍련 마이크로 유도두각 내비게이션 카울",
        "海星造型五齒輪黃銅發條鑰匙": "불가사리형 5엽 기어 황동 태엽 열쇠",
        "深海潛水工裝編織輕量胸甲": "심해 다이버 하네스 편조 경량 흉갑",
        "雙聯耐高壓深海石英泡罩目鏡": "쌍련 내고압 심해 석영 버블 접안경",
        "海淵流體脈衝複合機關弓": "해연 유체 펄스 복합 기믹 활",
        "柔性鈦合金滑翔翼翅與天線平衡細尾": "연성 티타늄 활공 날개와 안테나 미세꼬리",
    },
    "es": {
        "潮汐蝠魟": "La Manta de Marea",
        "蝠魟": "Manta",
        "深海沖壓耐蝕鍍鈦金屬底盤": "Chasis de Titanio Estampado Resistente a la Corrosión Abisal",
        "雙聯微型導流頭角導航冠": "Caperuza de Navegación de Cuernos Hidroala Micro Doble",
        "海星造型五齒輪黃銅發條鑰匙": "Llave de Cuerda de Latón de Engranaje de Estrella de Mar de Cinco Dientes",
        "深海潛水工裝編織輕量胸甲": "Peto Ligero Tejido con Arnés de Buceo de Profundidad",
        "雙聯耐高壓深海石英泡罩目鏡": "Gafas de Burbuja de Cuarzo Abisal de Alta Presión Doble",
        "海淵流體脈衝複合機關弓": "Arco Compuesto Mecánico de Pulso Hidráulico Abisal",
        "柔性鈦合金滑翔翼翅與天線平衡細尾": "Alas Planeadoras de Titanio Flexible y Cola de Antena Fina",
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
