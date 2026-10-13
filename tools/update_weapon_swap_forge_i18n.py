import json
import os

repo = "/opt/side/bravesoul-game"
content_dir = os.path.join(repo, "game/data/i18n/content")
root_i18n_dir = os.path.join(repo, "game/data/i18n")

trans = {
    "zh_TW": "前往鍛造",
    "zh_CN": "前往锻造",
    "en": "Go to Forge",
    "ja": "鍛造へ進む",
    "ko": "단조로 이동",
    "es": "Ir a Forja"
}

# 1. Update content/<loc>/ui.json
for loc, text in trans.items():
    p = os.path.join(content_dir, loc, "ui.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["前往鍛造"] = text
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"content/{loc}/ui.json updated with 前往鍛造 -> {text}")

# 2. Update <loc>.json
for loc, text in trans.items():
    p = os.path.join(root_i18n_dir, f"{loc}.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["前往鍛造"] = text
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{loc}.json updated with 前往鍛造 -> {text}")
