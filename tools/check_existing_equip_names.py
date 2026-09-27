import json
import glob
import os

with open("game/data/tables/equipment.json", "r", encoding="utf-8") as f:
    bases = json.load(f)["bases"]

names = {b["name"]: bid for bid, b in bases.items()}

json_files = glob.glob("game/data/**/*.json", recursive=True)

print("Checking existing occurrences in game/data/:")
for jf in json_files:
    if "equipment.json" in jf:
        continue
    try:
        with open(jf, "r", encoding="utf-8") as f:
            content = f.read()
        found = [n for n in names if n in content]
        if found:
            print(f"  {jf}: {found}")
    except Exception as e:
        pass
