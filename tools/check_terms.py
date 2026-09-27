import json, os, glob

langs = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
terms = ["換裝", "零件", "雜件", "黃銅齒輪", "發條游絲", "核心碎片", "小白 · 奶油便服", "獅 · 黃銅背心", "狐 · 圍巾長衫", "野豬 · 工匠工裙", "搪瓷碎屑"]
keys = ["drop_brass_gear", "drop_spring_coil", "drop_core_shard", "outfit_cream", "outfit_brass_vest", "outfit_scarf_tunic", "outfit_worker_apron", "junk_enamel_chip", "outfit", "part", "junk"]

for root, dirs, files in os.walk("/opt/side/bravesoul-game/game/data/i18n"):
    for file in files:
        if file.endswith(".json"):
            p = os.path.join(root, file)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read()
                    for t in terms + keys:
                        if t in content:
                            print(f"Found '{t}' in {p}")
            except Exception as e:
                pass
