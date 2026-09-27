import json
import os

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"

ui_data = {}
for loc in locales:
    fpath = os.path.join(base_dir, loc, "ui.json")
    with open(fpath, "r", encoding="utf-8") as f:
        ui_data[loc] = json.load(f)

with open("/opt/side/bravesoul-game/game/data/tables/paperdoll_slots.json", "r", encoding="utf-8") as f:
    slots_spec = json.load(f)

# Collect all sample variants from slots
all_variants = {}
for slot in slots_spec.get("paperdoll_specification", {}).get("slots", []):
    sid = slot.get("slot_id")
    for v in slot.get("sample_variants", []):
        vid = v.get("id")
        vname = v.get("name")
        all_variants[vid] = {"slot": sid, "name": vname}

print(f"Total sample variants in paperdoll_slots: {len(all_variants)}")

# Check each variant name in ui_data
missing_summary = []
for vid, info in all_variants.items():
    name_zh = info["name"]
    missing = [loc for loc in locales if loc != "zh_TW" and name_zh not in ui_data[loc]]
    if missing:
        missing_summary.append((vid, info["slot"], name_zh, missing))

print(f"\nVariants missing translation: {len(missing_summary)}")
for vid, slot, name_zh, missing in missing_summary:
    print(f"[{slot}] {vid} -> '{name_zh}' missing in {missing}")
