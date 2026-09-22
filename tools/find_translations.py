import json
import glob
import os

terms = [
    "星屑", "手藝工坊", "演武競技", "冒險委託", "前往出征",
    "品質轉化", "三合一熔煉", "雙倍抽獎", "懸賞領獎",
    "當前主線", "出發吧", "外裝", "發條", "奇玩", "未裝備"
]

all_files = glob.glob("/opt/side/bravesoul-game/game/data/i18n/**/*.json", recursive=True)

for term in terms:
    print(f"=== TERM: {term} ===")
    found = 0
    for path in all_files:
        rel = os.path.relpath(path, "/opt/side/bravesoul-game/game/data/i18n")
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
                if isinstance(d, dict):
                    # check if term is key
                    for k, v in d.items():
                        if term in k:
                            print(f"  [{rel}] KEY '{k}': '{v}'")
                            found += 1
                            if found >= 5:
                                break
        except Exception:
            pass
