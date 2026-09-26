import json
import os

TRANSLATIONS_ZH_TW = {
    "戰鬥失敗": "戰鬥失敗",
    "發條動能耗盡，齒輪暫時停擺！": "發條動能耗盡，齒輪暫時停擺！",
    "二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！": "二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！",
    "二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！": "二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！",
    "若是選擇承認敗北，將返回城鎮整頓裝備與招式。": "若是選擇承認敗北，將返回城鎮整頓裝備與招式。",
    "若是選擇承認敗北，將返還 2 點能量並返回整頓。": "若是選擇承認敗北，將返還 2 點能量並返回整頓。",
    "觀看廣告立即復活  (%d/%d)": "觀看廣告立即復活  (%d/%d)",
    "已移除廣告，直接領取  (%d/%d)": "已移除廣告，直接領取  (%d/%d)",
    "今日復活次數已達上限 (0/%d)": "今日復活次數已達上限 (0/%d)",
    "結束戰鬥": "結束戰鬥",
    "木人樁": "木人樁",
    "木人樁不反擊 · 自由試刀 · 右上可結束": "木人樁不反擊 · 自由試刀 · 右上可結束",
    "小白": "小白",
    "鎖定": "鎖定",
    "換武": "換武",
    "技能": "技能",
    "暫停": "暫停",
    "攻擊": "攻擊",
    "結束試招": "結束試招"
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
