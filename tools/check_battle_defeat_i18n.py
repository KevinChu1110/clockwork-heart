import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys = [
    "戰鬥失敗",
    "發條動能耗盡，齒輪暫時停擺！",
    "二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！",
    "二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！",
    "若是選擇承認敗北，將返回城鎮整頓裝備與招式。",
    "若是選擇承認敗北，將返還 2 點能量並返回整頓。",
    "觀看廣告立即復活  (%d/%d)",
    "已移除廣告，直接領取  (%d/%d)",
    "今日復活次數已達上限 (0/%d)",
    "結束戰鬥"
]

base_path = "/opt/side/bravesoul-game/game/data/i18n/content"
for k in keys:
    print(f"=== Key: {k} ===")
    for loc in locales:
        p = f"{base_path}/{loc}/ui.json"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        val = data.get(k, "<MISSING>")
        print(f"  [{loc}]: {val}")
