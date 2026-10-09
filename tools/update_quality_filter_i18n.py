import json
import os

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
script_dir = os.path.dirname(os.path.abspath(__file__))
wt_dir = os.path.dirname(script_dir)
base_dir = os.path.join(wt_dir, "game", "data", "i18n")
content_dir = os.path.join(base_dir, "content")

new_entries = {
    "精工": {
        "zh_TW": "精工", "zh_CN": "精工", "en": "Refined", "ja": "精工", "ko": "정공", "es": "Refinado"
    },
    "稀有": {
        "zh_TW": "稀有", "zh_CN": "稀有", "en": "Rare", "ja": "希少", "ko": "희귀", "es": "Raro"
    },
    "史詩": {
        "zh_TW": "史詩", "zh_CN": "史诗", "en": "Epic", "ja": "叙事詩", "ko": "서사", "es": "Épico"
    },
    "傳說": {
        "zh_TW": "傳說", "zh_CN": "传说", "en": "Legendary", "ja": "伝説", "ko": "전설", "es": "Legendario"
    },
    "尚無該品質可替換武器": {
        "zh_TW": "尚無該品質可替換武器", "zh_CN": "尚无该品质可替换武器",
        "en": "No weapons of this quality in inventory",
        "ja": "この品質の交換可能な武器がありません",
        "ko": "해당 등급의 교체 가능한 무기가 없습니다",
        "es": "No hay armas de esta calidad en el inventario"
    },
    "可嘗試切換其他品質或前往鍛造殿堂打造": {
        "zh_TW": "可嘗試切換其他品質或前往鍛造殿堂打造", "zh_CN": "可尝试切换其他品质或前往锻造殿堂打造",
        "en": "Try selecting another quality or forge in the Hall",
        "ja": "他の品質を選択するか鍛冶の殿堂で作成してください",
        "ko": "다른 등급을 선택하거나 대장간에서 제작해 보세요",
        "es": "Prueba otra calidad o forja en la Sala"
    },
    "尚無該流派與品質之可替換武器": {
        "zh_TW": "尚無該流派與品質之可替換武器", "zh_CN": "尚无该流派与品质之可替换武器",
        "en": "No weapons matching this class and quality",
        "ja": "この流派と品質に一致する武器がありません",
        "ko": "해당 유파 및 등급에 일치하는 무기가 없습니다",
        "es": "No hay armas que coincidan con esta clase y calidad"
    },
    "可嘗試調整篩選條件或前往鍛造殿堂打造": {
        "zh_TW": "可嘗試調整篩選條件或前往鍛造殿堂打造", "zh_CN": "可尝试调整筛选条件或前往锻造殿堂打造",
        "en": "Try adjusting filters or forge in the Hall",
        "ja": "フィルターを調整するか鍛冶の殿堂で作成してください",
        "ko": "필터를 조정하거나 대장간에서 제작해 보세요",
        "es": "Ajusta los filtros o forja en la Sala"
    }
}

for loc in locales:
    p = os.path.join(content_dir, loc, "ui.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        added = 0
        for k, trans in new_entries.items():
            if k not in data:
                data[k] = trans[loc]
                added += 1
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{loc}] added {added} to {p}")

    p2 = os.path.join(base_dir, f"{loc}.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            data2 = json.load(f)
        added2 = 0
        for k, trans in new_entries.items():
            if k not in data2:
                data2[k] = trans[loc]
                added2 += 1
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(data2, f, ensure_ascii=False, indent=2)
        print(f"[{loc}] added {added2} to {p2}")
