import json
import os

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keys = {
    "zh_TW": {
        "shop.btn_go_soul_hall": "前往聚魂",
        "前往聚魂": "前往聚魂",
        "shop.btn_go_forge": "前往鍛造",
        "前往鍛造": "前往鍛造",
    },
    "zh_CN": {
        "shop.btn_go_soul_hall": "前往聚魂",
        "前往聚魂": "前往聚魂",
        "shop.btn_go_forge": "前往锻造",
        "前往鍛造": "前往锻造",
    },
    "en": {
        "shop.btn_go_soul_hall": "Go to Soul Hall",
        "前往聚魂": "Go to Soul Hall",
        "shop.btn_go_forge": "Go to Forge",
        "前往鍛造": "Go to Forge",
    },
    "ja": {
        "shop.btn_go_soul_hall": "聚魂殿へ進む",
        "前往聚魂": "聚魂殿へ進む",
        "shop.btn_go_forge": "鍛冶屋へ進む",
        "前往鍛造": "鍛冶屋へ進む",
    },
    "ko": {
        "shop.btn_go_soul_hall": "혼령전으로 이동",
        "前往聚魂": "혼령전으로 이동",
        "shop.btn_go_forge": "대장간으로 이동",
        "前往鍛造": "대장간으로 이동",
    },
    "es": {
        "shop.btn_go_soul_hall": "Ir a Sala de Almas",
        "前往聚魂": "Ir a Sala de Almas",
        "shop.btn_go_forge": "Ir a la Forja",
        "前往鍛造": "Ir a la Forja",
    },
}

for loc, kv in keys.items():
    p1 = os.path.join(repo, "game/data/i18n", f"{loc}.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p1)

    p2 = os.path.join(repo, "game/data/i18n/content", loc, "ui.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p2)
