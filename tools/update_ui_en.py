import json

path = "/opt/side/bravesoul-game/game/data/i18n/content/en/ui.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = {
    "凡品": "Common",
    "良品": "Uncommon",
    "上品": "Rare",
    "極品": "Epic",
    "秘寶": "Legendary"
}

for k, v in new_entries.items():
    data[k] = v

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Saved with newline", path)
