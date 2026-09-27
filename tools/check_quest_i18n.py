import json
import os

root = "/opt/side/bravesoul-game/game/data/i18n/content"
for lc in ["en", "ja", "zh_CN", "ko", "es"]:
    path = os.path.join(root, lc, "quest.json")
    if os.path.exists(path):
        data = json.load(open(path, encoding="utf-8"))
        print(lc, "entries:", len(data))
        print("  d_train:", data.get("d_train"))
        print("  m_first_boss:", data.get("m_first_boss"))
