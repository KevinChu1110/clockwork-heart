#!/usr/bin/env python3
"""為第三十四族鋼臂巨猩 (The Steelarm Gorilla, gorilla) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/world/STEELARM_GORILLA_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "鋼臂巨猩": "鋼臂巨猩",
        "巨猩": "巨猩",
        "高壓蒸氣鍛打拳套": "高壓蒸氣鍛打拳套",
        "巨輪鍛工重型T字鍛鐵發條鑰匙": "巨輪鍛工重型T字鍛鐵發條鑰匙",
        "雙渦輪過熱洩壓排氣煙囪": "雙渦輪過熱洩壓排氣煙囪",
        "鋼臂巨猩重型沖壓黃銅素體": "鋼臂巨猩重型沖壓黃銅素體",
        "五聯鉚釘沖壓防撞重額甲": "五聯鉚釘沖壓防撞重額甲",
        "巨輪鍛工高壓鍋爐背帶胸甲": "巨輪鍛工高壓鍋爐背帶胸甲",
        "雙聯石英蒸氣壓力表目鏡": "雙聯石英蒸氣壓力表目鏡",
    },
    "zh_CN": {
        "鋼臂巨猩": "钢臂巨猩",
        "巨猩": "巨猩",
        "高壓蒸氣鍛打拳套": "高压蒸气锻打拳套",
        "巨輪鍛工重型T字鍛鐵發條鑰匙": "巨轮锻工重型T字锻铁发条钥匙",
        "雙渦輪過熱洩壓排氣煙囪": "双涡轮过热泄压排气烟囱",
        "鋼臂巨猩重型沖壓黃銅素體": "钢臂巨猩重型冲压黄铜素体",
        "五聯鉚釘沖壓防撞重額甲": "五联铆钉冲压防撞重额甲",
        "巨輪鍛工高壓鍋爐背帶胸甲": "巨轮锻工高压锅炉背带胸甲",
        "雙聯石英蒸氣壓力表目鏡": "双联石英蒸气压力表目镜",
    },
    "en": {
        "鋼臂巨猩": "The Steelarm Gorilla",
        "巨猩": "Gorilla",
        "高壓蒸氣鍛打拳套": "High-Pressure Steam Forging Gauntlets",
        "巨輪鍛工重型T字鍛鐵發條鑰匙": "Metropolis Heavy T-Forged Winding Key",
        "雙渦輪過熱洩壓排氣煙囪": "Twin-Turbo Overheat Exhaust Chimneys",
        "鋼臂巨猩重型沖壓黃銅素體": "Heavy Stamped Brass Gorilla Chassis",
        "五聯鉚釘沖壓防撞重額甲": "Five-Rivet Stamped Brow Crest",
        "巨輪鍛工高壓鍋爐背帶胸甲": "Metropolis Boiler Forging Harness",
        "雙聯石英蒸氣壓力表目鏡": "Dual Quartz Steam Gauge Optics",
    },
    "ja": {
        "鋼臂巨猩": "鋼臂ゴリラ (こうひゴリラ)",
        "巨猩": "ゴリラ",
        "高壓蒸氣鍛打拳套": "高圧蒸気鍛造ナックル",
        "巨輪鍛工重型T字鍛鐵發條鑰匙": "巨輪鍛工重型T字ぜんまい鍵",
        "雙渦輪過熱洩壓排氣煙囪": "ツインターボ過熱排気煙突",
        "鋼臂巨猩重型沖壓黃銅素體": "鋼臂ゴリラ重型プレス真鍮素体",
        "五聯鉚釘沖壓防撞重額甲": "五連リベットプレス防衝額甲",
        "巨輪鍛工高壓鍋爐背帶胸甲": "巨輪鍛工高圧ボイラーハーネス",
        "雙聯石英蒸氣壓力表目鏡": "双連石英蒸気圧力計レンズ",
    },
    "ko": {
        "鋼臂巨猩": "강비 고릴라 (강비 고릴라)",
        "巨猩": "고릴라",
        "高壓蒸氣鍛打拳套": "고압 증기 단조 너클",
        "巨輪鍛工重型T字鍛鐵發條鑰匙": "거륜 단공 중형 T자 태엽 열쇠",
        "雙渦輪過熱洩壓排氣煙囪": "트윈 터보 과열 배기 굴뚝",
        "鋼臂巨猩重型沖壓黃銅素體": "강비 고릴라 중형 프레스 황동 소체",
        "五聯鉚釘沖壓防撞重額甲": "5연 리벳 프레스 방호 이마 갑옷",
        "巨輪鍛工高壓鍋爐背帶胸甲": "거륜 단공 고압 보일러 하네스",
        "雙聯石英蒸氣壓力表目鏡": "쌍련 석영 증기 압력계 렌즈",
    },
    "es": {
        "鋼臂巨猩": "El Gorila de Brazos de Acero",
        "巨猩": "Gorila",
        "高壓蒸氣鍛打拳套": "Guanteletes de Forja a Vapor de Alta Presión",
        "巨輪鍛工重型T字鍛鐵發條鑰匙": "Llave de Cuerda en T Forjada Pesada",
        "雙渦輪過熱洩壓排氣煙囪": "Chimeneas de Escape de Doble Turbo",
        "鋼臂巨猩重型沖壓黃銅素體": "Chasis Pesado de Latón Estampado de Gorila",
        "五聯鉚釘沖壓防撞重額甲": "Cresta Frontal Remachada Antichoque",
        "巨輪鍛工高壓鍋爐背帶胸甲": "Arnés de Caldera de Forja de la Metrópoli",
        "雙聯石英蒸氣壓力表目鏡": "Ópticas de Manómetro de Vapor de Cuarzo Dobles",
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
