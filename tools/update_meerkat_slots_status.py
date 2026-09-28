#!/usr/bin/env python3
import json

paths = [
    "/opt/side/bravesoul-game/docs/design/paperdoll_slots.json",
    "/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json"
]

for p in paths:
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)

    races = data.get("races_specification", {}).get("races", [])
    for r in races:
        if r.get("race_id") == "meerkat":
            anc = r.get("asset_naming_conventions", {})
            status = anc.get("status", {})
            existing = status.get("existing", [])
            pending = status.get("pending", [])

            item_str = "game/assets/sprites/player/paperdoll/meerkat/{slot_id}/{item_id}.png (紙娃娃切片圖層)"
            if item_str in pending:
                pending.remove(item_str)
            if item_str not in existing:
                existing.append(item_str)

            anc["paperdoll_slices_dir"] = "game/assets/sprites/player/paperdoll/meerkat/{slot_id}/{item_id}.png [既有]"

    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("✓ Both paperdoll_slots.json updated with meerkat paperdoll slices [既有]")
