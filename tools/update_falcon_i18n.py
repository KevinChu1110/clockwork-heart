#!/usr/bin/env python3
"""為第二十八族疾影神隼 (The Swift Falcon, falcon) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/SWIFT_FALCON_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "疾影神隼": "疾影神隼",
        "神隼": "神隼",
        "空境巡守·穿雲追風者": "空境巡守·穿雲追風者",
        "疾影穿雲機關爪": "疾影穿雲機關爪",
        "雙羽旋風發條鑰匙": "雙羽旋風發條鑰匙",
        "流線鷹喙沖壓金屬面罩": "流線鷹喙沖壓金屬面罩",
        "琥珀石英雙聯鷹眼目鏡": "琥珀石英雙聯鷹眼目鏡",
        "三聯空氣動力滑翔舵板尾羽": "三聯空氣動力滑翔舵板尾羽",
    },
    "zh_CN": {
        "疾影神隼": "疾影神隼",
        "神隼": "神隼",
        "空境巡守·穿雲追風者": "空境巡守·穿云追风者",
        "疾影穿雲機關爪": "疾影穿云机关爪",
        "雙羽旋風發條鑰匙": "双羽旋风发条钥匙",
        "流線鷹喙沖壓金屬面罩": "流线鹰喙冲压金属面罩",
        "琥珀石英雙聯鷹眼目鏡": "琥珀石英双联鹰眼目镜",
        "三聯空氣動力滑翔舵板尾羽": "三联空气动力滑翔舵板尾羽",
    },
    "en": {
        "疾影神隼": "The Swift Falcon",
        "神隼": "Falcon",
        "空境巡守·穿雲追風者": "Skyline Warden: Cloud Strider",
        "疾影穿雲機關爪": "Shadow-Talon Cloud Piercing Claw",
        "雙羽旋風發條鑰匙": "Aero Twin-Quill Winding Key",
        "流線鷹喙沖壓金屬面罩": "Streamlined Beak Visor",
        "琥珀石英雙聯鷹眼目鏡": "Amber Quartz Dual Hawk Optics",
        "三聯空氣動力滑翔舵板尾羽": "Aerodynamic Rudder Tail Flaps",
    },
    "ja": {
        "疾影神隼": "疾影の神隼",
        "神隼": "神隼",
        "空境巡守·穿雲追風者": "空境の巡守・雲追う風",
        "疾影穿雲機關爪": "疾影穿雲からくり爪",
        "雙羽旋風發條鑰匙": "双羽つむじ風ぜんまい鍵",
        "流線鷹喙沖壓金屬面罩": "流線鷹嘴プレス金属面頬",
        "琥珀石英雙聯鷹眼目鏡": "琥珀石英二連鷹眼レンズ",
        "三聯空氣動力滑翔舵板尾羽": "三連空力滑空舵板尾羽",
    },
    "ko": {
        "疾影神隼": "질영 신골",
        "神隼": "신골",
        "空境巡守·穿雲追風者": "공경 순찰·구름 가르는 바람",
        "疾影穿雲機關爪": "질영천운 기관 발톱",
        "雙羽旋風發條鑰匙": "쌍깃 선풍 태엽 키",
        "流線鷹喙沖壓金屬面罩": "유선형 매부리 프레스 금속 투구",
        "琥珀石英雙聯鷹眼目鏡": "호박 석영 2연 매의 눈 렌즈",
        "三聯空氣動力滑翔舵板尾羽": "3연 공기역학 활공 러더 꼬리깃",
    },
    "es": {
        "疾影神隼": "El Halcón Veloz",
        "神隼": "Halcón",
        "空境巡守·穿雲追風者": "Guardián del Cielo: Cazavientos",
        "疾影穿雲機關爪": "Garra Mecánica Cazadora de Nubes",
        "雙羽旋風發條鑰匙": "Llave Mecánica de Doble Pluma del Viento",
        "流線鷹喙沖壓金屬面罩": "Visera de Pico Estampada Aerodinámica",
        "琥珀石英雙聯鷹眼目鏡": "Óptica Dual de Cuarzo Ámbar Ojo de Halcón",
        "三聯空氣動力滑翔舵板尾羽": "Alerones de Cola Aerodinámicos de 3 Secciones",
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
