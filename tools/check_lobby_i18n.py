import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys = [
    "能量", "金幣", "星屑", "商城", "設置", "戰力", "戰力 %d", "戰力 %s",
    "天宮鐵匠", "品質轉化 · 裝備鍛造",
    "手藝工坊", "紅黃藍石 · 三合一熔煉",
    "演武競技", "挑戰對手 · 雙倍抽獎",
    "冒險委託", "每日簽到 · 懸賞領獎",
    "外裝", "武器", "發條", "奇玩", "未裝備",
    "冒險出征 · 當前主線", "第二地區 · 白霧之地 (2-4 BOSS)", "前往出征",
    "發條新村", "角色裝備", "四區出征", "聚魂殿堂", "冒險背包",
    "背後的發條上得剛剛好，出發吧！",
    "更衣 · 發條衣櫥", "機體外觀 · 發條紙娃娃", "武器輪替配置", "點擊切換輪替順位 · 三段作戰序列", "機體戰鬥屬性",
    "聚魂殿 · 封靈罐四階", "綠階封靈罐", "藍階封靈罐", "紫階封靈罐", "橙階封靈罐",
    "冒險者背包", "道具與戰魂倉庫 · 點選格子查看詳情"
]

data = {}
for loc in locales:
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    try:
        with open(p, "r", encoding="utf-8") as f:
            data[loc] = json.load(f)
    except Exception as e:
        print(f"Error loading {loc}: {e}")
        data[loc] = {}

for k in keys:
    missing = [loc for loc in locales if loc != "zh_TW" and k not in data[loc]]
    found = {loc: data[loc].get(k) for loc in locales if k in data[loc]}
    print(f"KEY: {k}")
    if missing:
        print(f"  MISSING in: {missing}")
    if found:
        print(f"  FOUND: {found}")
