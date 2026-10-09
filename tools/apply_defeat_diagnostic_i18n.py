import json
import os

DIAGNOSTIC_I18N = {
    "zh_TW": {
        "戰力診斷": "戰力診斷",
        "武器階數": "武器階數",
        "天宮鐵匠鍛造強化": "天宮鐵匠鍛造強化",
        "裝備副詞條": "裝備副詞條",
        "調整機芯優化屬性": "調整機芯優化屬性",
        "招式調整": "招式調整",
        "武術館自訂招式順序": "武術館自訂招式順序",
        "前往整頓": "前往整頓",
    },
    "zh_CN": {
        "戰力診斷": "战力诊断",
        "武器階數": "武器阶数",
        "天宮鐵匠鍛造強化": "天宫铁匠锻造强化",
        "裝備副詞條": "装备副词条",
        "調整機芯優化屬性": "调整机芯优化属性",
        "招式調整": "招式调整",
        "武術館自訂招式順序": "武术馆自订招式顺序",
        "前往整頓": "前往整顿",
    },
    "en": {
        "戰力診斷": "Combat Diagnostics",
        "武器階數": "Weapon Tier",
        "天宮鐵匠鍛造強化": "Forge at Celestial Smith",
        "裝備副詞條": "Gear Affixes",
        "調整機芯優化屬性": "Tune Cores & Attributes",
        "招式調整": "Skill Setup",
        "武術館自訂招式順序": "Set Priority at Dojo",
        "前往整頓": "Gear Up",
    },
    "ja": {
        "戰力診斷": "戦力診断",
        "武器階數": "武器ランク",
        "天宮鐵匠鍛造強化": "天宮の鍛冶屋で強化",
        "裝備副詞條": "装備サブステ",
        "調整機芯優化屬性": "コアを調整し属性強化",
        "招式調整": "技の調整",
        "武術館自訂招式順序": "武術館で技順を設定",
        "前往整頓": "装備強化へ",
    },
    "ko": {
        "戰力診斷": "전투력 진단",
        "武器階數": "무기 등급",
        "天宮鐵匠鍛造強化": "천궁 대장간에서 강화",
        "裝備副詞條": "장비 보조옵션",
        "調整機芯優化屬性": "코어 조정 및 속성 최적화",
        "招式調整": "기술 조정",
        "武術館自訂招式順序": "무술관에서 기술 순서 조정",
        "前往整頓": "정비하러 가기",
    },
    "es": {
        "戰力診斷": "Diagnóstico de combate",
        "武器階數": "Rango de arma",
        "天宮鐵匠鍛造強化": "Forjar en la Forja Celestial",
        "裝備副詞條": "Subatributos de equipo",
        "調整機芯優化屬性": "Ajustar núcleos y atributos",
        "招式調整": "Ajuste de técnicas",
        "武術館自訂招式順序": "Ajustar orden en el dojo",
        "前往整頓": "Equiparse",
    },
}

base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"
for loc, trans in DIAGNOSTIC_I18N.items():
    p = os.path.join(base_dir, loc, "ui.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in trans.items():
        data[k] = v
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {loc}/ui.json with {len(trans)} keys.")
