import json
import os

keys = {
    "zh_TW": {"暴擊+%.1f%%": "暴擊+%.1f%%", "暴傷+%.0f%%": "暴傷+%.0f%%"},
    "zh_CN": {"暴擊+%.1f%%": "暴击+%.1f%%", "暴傷+%.0f%%": "暴伤+%.0f%%"},
    "en": {"暴擊+%.1f%%": "Crit+%.1f%%", "暴傷+%.0f%%": "CritDmg+%.0f%%"},
    "ja": {"暴擊+%.1f%%": "会心+%.1f%%", "暴傷+%.0f%%": "会心ダメ+%.0f%%"},
    "ko": {"暴擊+%.1f%%": "치명+%.1f%%", "暴傷+%.0f%%": "치명피해+%.0f%%"},
    "es": {"暴擊+%.1f%%": "Crít+%.1f%%", "暴傷+%.0f%%": "DañoCrít+%.0f%%"}
}

for loc, d in keys.items():
    p1 = f"game/data/i18n/content/{loc}/ui.json"
    p2 = f"game/data/i18n/{loc}.json"
    for p in [p1, p2]:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.update(d)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {p}")

print("All i18n updated successfully!")
