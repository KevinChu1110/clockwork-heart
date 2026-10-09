import json
import os

repo_dir = "/opt/side/bravesoul-game"

locales = {
    "zh_TW": "上緊發條，啟動！",
    "zh_CN": "上紧发条，启动！",
    "en": "Wind up tight, engage!",
    "ja": "ゼンマイを巻いて、起動！",
    "ko": "태엽을 감고, 기동!",
    "es": "¡Cuerda al máximo, activar!",
}

# 1. Update top-level i18n
for loc, text in locales.items():
    p = os.path.join(repo_dir, f"game/data/i18n/{loc}.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["battle.pre_windup"] = text
    data["上緊發條，啟動！"] = text
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {p}")

# 2. Update content/*/ui.json
for loc, text in locales.items():
    p = os.path.join(repo_dir, f"game/data/i18n/content/{loc}/ui.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["上緊發條，啟動！"] = text
        data["battle.pre_windup"] = text
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {p}")
