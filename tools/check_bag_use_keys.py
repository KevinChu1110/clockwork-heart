import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys_to_check = [
    "使用【%s】· %s",
    "使用【%s】%s",
    "使用【%s】",
    "賣出【%s】· 金 +%d",
    "【%s】是重要物品，不能消耗。",
    "使用失敗。",
    "使用失敗",
    "賣出失敗。",
    "賣出失敗",
    "沒有這個道具。",
    "無法使用。",
    "無法使用",
    "第 %d 格是空的。開 I 背包指派道具。",
    "沒有可賣的材料。",
    "賣出材料 %d 件 · 金 +%d",
    "星屑 +%d",
    "HP +%d",
]

for loc in locales:
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"=== {loc} ===")
    for k in keys_to_check:
        if k in data:
            print(f"  EXISTS: {k!r} -> {data[k]!r}")
        else:
            print(f"  MISSING: {k!r}")
