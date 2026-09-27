import json

root = "/opt/side/bravesoul-game"
locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
fields = ["name", "desc", "lv2", "lv3", "unlock_hint"]

for loc in locales:
    p = f"{root}/game/data/i18n/content/{loc}/skill.json"
    data = json.load(open(p, encoding="utf-8"))
    assert len(data) == 54, f"{loc} length is {len(data)}"
    for sid, entry in data.items():
        for f in fields:
            assert f in entry and entry[f], f"{loc} missing {sid}.{f}"

print("All 6 locales have all 54 skills and all 5 fields!")
