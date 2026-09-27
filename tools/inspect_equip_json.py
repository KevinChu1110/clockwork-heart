import json

with open("game/data/tables/equipment.json", "r", encoding="utf-8") as f:
    bases = json.load(f)["bases"]

for idx, (bid, b) in enumerate(bases.items(), 1):
    print(f"{idx:2d}. {bid:18s} | {b.get('slot'):9s} | T{b.get('tier', 1)} | {b.get('line', ''):8s} | {b.get('name')}")
