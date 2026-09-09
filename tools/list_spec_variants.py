import json

with open("game/data/tables/paperdoll_slots.json") as f:
    d = json.load(f)

for s in d["slots_architecture"]["slots"]:
    print("Slot:", s["slot_id"])
    for v in s.get("sample_variants", []):
        print(f"  {v['id']}: {v['name']}")
