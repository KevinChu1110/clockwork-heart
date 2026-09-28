#!/usr/bin/env python3
"""為第四十六族破星蜜獾 (The Starbreaker Honey Badger, badger) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/STARBREAKER_BADGER_DESIGN_PROPOSAL.md。
"""

import json
import os

locales = {
    "zh_TW": {
        "破星蜜獾": "破星蜜獾",
        "蜜獾": "蜜獾",
        "逐星裂空機關爪": "逐星裂空機關爪",
        "四葉天線金黃發條鑰匙": "四葉天線金黃發條鑰匙",
        "雙聯冷氣反推推進背包": "雙聯冷氣反推推進背包",
        "高密度聚合物平頭抗衝擊素體": "高密度聚合物平頭抗衝擊素體",
        "平頭防暴沖壓護額": "平頭防暴沖壓護額",
        "軌道高抗衝擊防護工裝": "軌道高抗衝擊防護工裝",
        "琥珀點陣 LED 護目面罩": "琥珀點陣 LED 護目面罩",
    },
    "zh_CN": {
        "破星蜜獾": "破星蜜獾",
        "蜜獾": "蜜獾",
        "逐星裂空機關爪": "逐星裂空机关爪",
        "四葉天線金黃發條鑰匙": "四叶天线金黄发条钥匙",
        "雙聯冷氣反推推進背包": "双联冷气反推推进背包",
        "高密度聚合物平頭抗衝擊素體": "高密度聚合物平头抗冲击素体",
        "平頭防暴沖壓護額": "平头防暴冲压护额",
        "軌道高抗衝擊防護工裝": "轨道高抗冲击防护工装",
        "琥珀點陣 LED 護目面罩": "琥珀点阵 LED 护目面罩",
    },
    "en": {
        "破星蜜獾": "The Starbreaker Honey Badger",
        "蜜獾": "Honey Badger",
        "逐星裂空機關爪": "Star-Breaker Vacuum Ripper Claw",
        "四葉天線金黃發條鑰匙": "Four-Vane Antenna Gold Winding Key",
        "雙聯冷氣反推推進背包": "Dual Cold-Gas Reaction Thruster Pack",
        "高密度聚合物平頭抗衝擊素體": "High-Density Polymer Shock-Resistant Chassis",
        "平頭防暴沖壓護額": "Flathead Ballistic Visor Brow",
        "軌道高抗衝擊防護工裝": "EVA Heavy Orbital Harness",
        "琥珀點陣 LED 護目面罩": "Amber LED Matrix Visor",
    },
    "ja": {
        "破星蜜獾": "砕星のラーテル (サイセイノラーテル)",
        "蜜獾": "ラーテル",
        "逐星裂空機關爪": "逐星裂空機関爪",
        "四葉天線金黃發條鑰匙": "四葉アンテナ黄金ぜんまい鍵",
        "雙聯冷氣反推推進背包": "2連コールドガス反動推進パック",
        "高密度聚合物平頭抗衝擊素體": "高密度ポリマー平頭耐衝撃素体",
        "平頭防暴沖壓護額": "平頭防暴プレスバイザー",
        "軌道高抗衝擊防護工裝": "軌道高耐衝撃防護ハーネス",
        "琥珀點陣 LED 護目面罩": "琥珀ドットLEDバイザーマスク",
    },
    "ko": {
        "破星蜜獾": "파성의 라텔",
        "蜜獾": "라텔",
        "逐星裂空機關爪": "축성 열공 기관 발톱",
        "四葉天線金黃發條鑰匙": "4엽 안테나 황금 태엽 열쇠",
        "雙聯冷氣反推推進背包": "2연장 냉각 가스 반작용 추진 배낭",
        "高密度聚合物平頭抗衝擊素體": "고밀도 폴리머 평두 내충격 소체",
        "平頭防暴沖壓護額": "평두 방폭 프레스 이마 보호대",
        "軌道高抗衝擊防護工裝": "궤도 고내충격 방호 작업복",
        "琥珀點陣 LED 護目面罩": "호박색 도트 매트릭스 LED 고글 마스크",
    },
    "es": {
        "破星蜜獾": "El Tejón Melívoro Rompeestrellas",
        "蜜獾": "Tejón Melívoro",
        "逐星裂空機關爪": "Garra Mecánica Desgarradora del Vacío",
        "四葉天線金黃發條鑰匙": "Llave de Cuerda Dorada con Antena de Cuatro Aspas",
        "雙聯冷氣反推推進背包": "Mochila de Propulsión de Gas Frío Doble",
        "高密度聚合物平頭抗衝擊素體": "Chasis Antichoque de Polímero de Alta Densidad",
        "平頭防暴沖壓護額": "Visera Frontal Antidisturbios de Cabeza Plana",
        "軌道高抗衝擊防護工裝": "Arnés Orbital de Alta Resistencia",
        "琥珀點陣 LED 護目面罩": "Visera de Matriz LED Ámbar",
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
