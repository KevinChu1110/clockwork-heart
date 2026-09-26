import json
import os

TRANSLATIONS_ZH_TW = {
    "能量不足": "能量不足",
    "當前能量：—": "當前能量：—",
    "當前能量：%d／%d": "當前能量：%d／%d",
    "自然回復：—": "自然回復：—",
    "能量恢復中……": "能量恢復中……",
    "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！": "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！",
    "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是直接領取補充 3 點能量！": "出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是直接領取補充 3 點能量！",
    "觀看廣告回復能量 (+3)  (%d/%d)": "觀看廣告回復能量 (+3)  (%d/%d)",
    "已移除廣告，直接領取 (+3)  (%d/%d)": "已移除廣告，直接領取 (+3)  (%d/%d)",
    "今日廣告次數已達上限 (0/%d)": "今日廣告次數已達上限 (0/%d)",
    "今日領取次數已達上限 (0/%d)": "今日領取次數已達上限 (0/%d)",
    "稍後再來": "稍後再來",
    "能量 %d／%d（已滿）": "能量 %d／%d（已滿）",
    "能量 %d／%d（約 %d 分後＋1）": "能量 %d／%d（約 %d 分後＋1）",
}

base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"
tw_path = os.path.join(base_dir, "zh_TW", "ui.json")

with open(tw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for k, v in TRANSLATIONS_ZH_TW.items():
    data[k] = v

sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))

with open(tw_path, "w", encoding="utf-8") as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Updated zh_TW/ui.json with {len(TRANSLATIONS_ZH_TW)} keys.")
