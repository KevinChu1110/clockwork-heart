import json

langs = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys = [
    "drop_brass_gear", "drop_spring_coil", "drop_core_shard",
    "outfit_cream", "outfit_brass_vest", "outfit_scarf_tunic", "outfit_worker_apron",
    "junk_enamel_chip",
    "outfit", "part", "junk",
    "換裝", "零件", "雜件",
    "黃銅齒輪", "發條游絲", "核心碎片",
    "小白 · 奶油便服", "獅 · 黃銅背心", "狐 · 圍巾長衫", "野豬 · 工匠工裙",
    "搪瓷碎屑"
]

for lang in langs:
    p = f"/opt/side/bravesoul-game/game/data/i18n/{lang}.json"
    print(f"=== {lang}.json ===")
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
        for k in keys:
            if k in d:
                print(f"  {k}: {repr(d[k])}")
