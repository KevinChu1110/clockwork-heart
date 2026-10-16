import json
from pathlib import Path

locales = {
    "zh_TW": "前往心法",
    "zh_CN": "前往心法",
    "en": "To Skills",
    "ja": "心法へ",
    "ko": "심법으로",
    "es": "A Habilidades"
}

base_dir = Path("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_4116f7d6/game/data/i18n")

for loc, text in locales.items():
    # 1. game/data/i18n/{loc}.json
    p1 = base_dir / f"{loc}.json"
    with open(p1, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["shop.btn_go_skill"] = text
    with open(p1, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {p1} -> {text}")

    # 2. game/data/i18n/content/{loc}/ui.json
    p2 = base_dir / "content" / loc / "ui.json"
    with open(p2, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["shop.btn_go_skill"] = text
    with open(p2, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {p2} -> {text}")

print("All 12 i18n files updated successfully.")
