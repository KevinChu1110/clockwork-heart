import json
import os

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys = ["能量", "金幣", "星屑", "發條新村", "角色裝備", "四區出征", "聚魂殿堂", "冒險背包"]

base_dir = "game/data/i18n/content"

for loc in locales:
    fpath = os.path.join(base_dir, loc, "ui.json")
    if not os.path.exists(fpath):
        print(f"File not found: {fpath}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"=== {loc} ===")
    for k in keys:
        if k in data:
            print(f"  [OK] {k} -> {data[k]}")
        else:
            print(f"  [MISSING] {k}")
