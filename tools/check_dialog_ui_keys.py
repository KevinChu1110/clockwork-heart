import json

root = "/opt/side/bravesoul-game"
keys = [
    "旅途 · 招式心法",
    "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉",
    "戰鬥優先",
    "平常出招：%s",
    "危急治療：%s",
    "可體悟",
    "未解鎖",
    "熟練 %d/%d",
    "下級預覽：%s",
    "解鎖條件：%s",
    "關閉",
    "Lv.%d · 極階"
]

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
for loc in locales:
    p = f"{root}/game/data/i18n/content/{loc}/ui.json"
    data = json.load(open(p, encoding="utf-8"))
    missing = [k for k in keys if k not in data]
    print(f"[{loc}] missing: {missing}")
