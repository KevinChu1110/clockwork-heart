import json, os

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_77530648/game/data/i18n"

translations = {
    "zh_TW": {
        "核心機芯": "核心機芯",
        "普通": "普通",
        "稀有": "稀有",
        "史詩": "史詩",
        "傳奇": "傳奇",
        "彩": "彩",
    },
    "zh_CN": {
        "核心機芯": "核心机芯",
        "普通": "普通",
        "稀有": "稀有",
        "史詩": "史诗",
        "傳奇": "传奇",
        "彩": "彩",
    },
    "en": {
        "核心機芯": "Core Movement",
        "普通": "Common",
        "稀有": "Rare",
        "史詩": "Epic",
        "傳奇": "Legendary",
        "彩": "Rainbow",
    },
    "ja": {
        "核心機芯": "コアムーブメント",
        "普通": "コモン",
        "稀有": "レア",
        "史詩": "エピック",
        "傳奇": "レジェンド",
        "彩": "虹",
    },
    "ko": {
        "核心機芯": "코어 무브먼트",
        "普通": "일반",
        "稀有": "희귀",
        "史詩": "에픽",
        "傳奇": "전설",
        "彩": "무지개",
    },
    "es": {
        "核心機芯": "Mecanismo central",
        "普通": "Común",
        "稀有": "Raro",
        "史詩": "Épico",
        "傳奇": "Legendario",
        "彩": "Arcoíris",
    },
}

for loc, entries in translations.items():
    p1 = os.path.join(base_dir, f"content/{loc}/ui.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(entries)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Updated {p1}")

    p2 = os.path.join(base_dir, f"{loc}.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(entries)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Updated {p2}")

print("i18n update complete.")
