import json
import os
import re

root = "/opt/side/bravesoul-game"
skills_gd = open(f"{root}/game/scripts/systems/skill_system.gd", encoding="utf-8").read()

catalog_start = skills_gd.index("const CATALOG: Array[Dictionary] = [")
catalog_end = skills_gd.index("func _path_id()", catalog_start)
catalog_block = skills_gd[catalog_start:catalog_end]

skills_tw = {}
current = {}
fields = ["name", "desc", "lv2", "lv3", "unlock_hint"]

for line in catalog_block.split("\n"):
    line = line.strip()
    if line == "{":
        current = {}
    elif line.startswith("}"):
        if "id" in current:
            sid = current["id"]
            skills_tw[sid] = {f: current.get(f, "") for f in fields if f in current}
        current = {}
    else:
        m = re.match(r'"(\w+)":\s*(?:"([^"]*)"|([0-9.]+)),?', line)
        if m:
            k, v_str = m.group(1), m.group(2)
            if v_str is not None:
                current[k] = v_str

print(f"Extracted {len(skills_tw)} skills for zh_TW")

# 寫入 zh_TW/skill.json
tw_path = f"{root}/game/data/i18n/content/zh_TW/skill.json"
os.makedirs(os.path.dirname(tw_path), exist_ok=True)
with open(tw_path, "w", encoding="utf-8") as f:
    json.dump(skills_tw, f, ensure_ascii=False, indent=2, sort_keys=True)
    f.write("\n")
print("Written zh_TW/skill.json")

# 補齊六語系 ui.json 裡的職業名稱
prof_i18n = {
    "zh_TW": {"維京": "維京", "武鬥家": "武鬥家"},
    "zh_CN": {"維京": "维京", "武鬥家": "武斗家"},
    "en":    {"維京": "Viking", "武鬥家": "Monk"},
    "ja":    {"維京": "ヴァイキング", "武鬥家": "武闘家"},
    "ko":    {"維京": "바이킹", "武鬥家": "무투가"},
    "es":    {"維京": "Vikingo", "武鬥家": "Monje"},
}

for loc, trans in prof_i18n.items():
    uipath = f"{root}/game/data/i18n/content/{loc}/ui.json"
    if os.path.exists(uipath):
        uidata = json.load(open(uipath, encoding="utf-8"))
        changed = False
        for k, v in trans.items():
            if k not in uidata:
                uidata[k] = v
                changed = True
        if changed:
            with open(uipath, "w", encoding="utf-8") as f:
                json.dump(uidata, f, ensure_ascii=False, indent=2, sort_keys=True)
                f.write("\n")
            print(f"Updated {loc}/ui.json with missing profs")
