import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys = [
    "能量不足",
    "當前能量：—",
    "當前能量：%d／%d",
    "自然回復：—",
    "能量恢復中……",
    "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！",
    "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是直接領取補充 3 點能量！",
    "觀看廣告回復能量 (+3)  (%d/%d)",
    "已移除廣告，直接領取 (+3)  (%d/%d)",
    "今日廣告次數已達上限 (0/%d)",
    "今日領取次數已達上限 (0/%d)",
    "稍後再來",
    "能量 %d／%d（已滿）",
    "能量 %d／%d（約 %d 分後＋1）",
]

for loc in locales:
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    print(f"=== {loc} ===")
    for k in keys:
        if k in d:
            print(f"  EXISTS: {repr(k)} -> {repr(d[k])}")
        else:
            print(f"  MISSING: {repr(k)}")
