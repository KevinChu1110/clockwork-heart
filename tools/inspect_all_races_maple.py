#!/usr/bin/env python3
import json
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"

for race in ["rabbit", "fox", "lion", "boar"]:
    json_path = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_{race}.json"
    if not os.path.exists(json_path):
        print(f"Missing {json_path}")
        continue
    with open(json_path) as f:
        data = json.load(f)
    print(f"\n================ Race: {race} ================")
    print("Canvas:", data.get("canvas_size"))
    print("Root Anchor:", data.get("root_anchor"))
    print("Anchors:", json.dumps(data.get("anchors"), indent=2))
    print("Default loadout:", data.get("default_loadout"))
    print("Parts summary:")
    parts = data.get("parts", {})
    for p_name, p_info in parts.items():
        anchor = p_info.get("anchor")
        z = p_info.get("z_index")
        items = list(p_info.get("items", {}).keys())
        first_item = items[0] if items else None
        item_data = p_info.get("items", {}).get(first_item, {})
        print(f"  {p_name} (anchor={anchor}, z={z}): items={items}, first_item_origin={item_data.get('origin')}, size=({item_data.get('width')}, {item_data.get('height')})")
