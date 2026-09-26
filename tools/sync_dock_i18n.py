import json
import os

ENTRIES_TO_ENSURE = {
    "能量": {
        "zh_TW": "能量",
        "zh_CN": "能量",
        "en": "Energy",
        "ja": "エネルギー",
        "ko": "에너지",
        "es": "Energía"
    },
    "金幣": {
        "zh_TW": "金幣",
        "zh_CN": "金币",
        "en": "Gold",
        "ja": "金",
        "ko": "골드",
        "es": "Oro"
    },
    "星屑": {
        "zh_TW": "星屑",
        "zh_CN": "星屑",
        "en": "Stardust",
        "ja": "星屑",
        "ko": "별가루",
        "es": "Polvo estelar"
    },
    "發條新村": {
        "zh_TW": "發條新村",
        "zh_CN": "发条新村",
        "en": "Cogwheel Hamlet",
        "ja": "ぜんまい新村",
        "ko": "태엽 신촌",
        "es": "Aldea Mecánica"
    },
    "角色裝備": {
        "zh_TW": "角色裝備",
        "zh_CN": "角色装备",
        "en": "Hero Gear",
        "ja": "キャラ装備",
        "ko": "캐릭터 장비",
        "es": "Equipo de héroe"
    },
    "四區出征": {
        "zh_TW": "四區出征",
        "zh_CN": "四区出征",
        "en": "Four Regions",
        "ja": "四区出征",
        "ko": "4구역 출정",
        "es": "Cuatro Regiones"
    },
    "聚魂殿堂": {
        "zh_TW": "聚魂殿堂",
        "zh_CN": "聚魂殿堂",
        "en": "Soul Hall",
        "ja": "聚魂殿",
        "ko": "영혼의 전당",
        "es": "Salón del Alma"
    },
    "冒險背包": {
        "zh_TW": "冒險背包",
        "zh_CN": "冒险背包",
        "en": "Adventure Bag",
        "ja": "冒険バッグ",
        "ko": "모험 배낭",
        "es": "Bolsa de aventura"
    }
}

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "game/data/i18n/content"

for loc in locales:
    fpath = os.path.join(base_dir, loc, "ui.json")
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, v_map in ENTRIES_TO_ENSURE.items():
        if k not in data:
            data[k] = v_map[loc]
            added += 1
            print(f"[{loc}] Added {k} -> {v_map[loc]}")
        else:
            # Check if value matches
            pass
    if added > 0:
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"[{loc}] Successfully saved with {added} new entries.")
    else:
        print(f"[{loc}] All entries already present.")
