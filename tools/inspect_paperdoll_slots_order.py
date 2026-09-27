import json

with open("game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sa = data["slots_architecture"]
print("slots_architecture keys:", list(sa.keys()))
slots = sa.get("slots", [])
print("slots count:", len(slots))
slots_sorted = sorted(slots, key=lambda s: s.get("layer_z_index", 0))
for s in slots_sorted:
    print(f"  z={s.get('layer_z_index'):2d}: slot_id={s.get('slot_id'):<12} name={s.get('name_zh')}")
    for v in s.get("sample_variants", []):
        if v.get("race") == "squirrel" or "squirrel" in v.get("id", ""):
            print(f"    -> id={v.get('id')} name={v.get('name')}")
