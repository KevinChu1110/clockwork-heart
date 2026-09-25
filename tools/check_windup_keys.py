import json
import glob

keys_to_check = [
    "冒險委託 · 今天誰需要上發條",
    "今天誰需要上發條",
    "【個案委託】",
    "委託描述",
    "對話提示",
    "累計上發條 0 次",
    "累計上發條 %d 次 · %s",
    "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1",
    "今日委託獎勵已領取：金幣 +25、星塵 +1、發條碎片 +1（明日輪替新個案）",
    "離開委託",
    "前往出征",
    "今日委託已完成（當日不可再領）",
    "這截發條輕輕咬合，發出溫柔的運轉聲。",
    "請選擇行動為發條玩具轉緊發條：",
    "委託完成！",
    "已獲得獎勵！",
    "領取失敗",
    "未命名個案",
    "釘釘", "灰鼬", "小芽", "星讀", "獅子殘件", "狐狸殘件"
]

for p in sorted(glob.glob("/opt/side/bravesoul-game/game/data/i18n/content/*/ui.json")):
    loc = p.split("/")[-2]
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    print(f"=== {loc} ({len(d)} keys) ===")
    found = 0
    for k in keys_to_check:
        if k in d:
            print(f"  [FOUND] {k} -> {d[k]}")
            found += 1
    if found == 0:
        print("  (None found)")
