#!/usr/bin/env python3
import json
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    spec = json.load(f)

# 依據 json 中的規格在 python 中合成
canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

slots = [
    ("winding_key", "key_classic_brass", spec["anchors"]["back_key"]),
    ("back_curio", "curio_spring_tail", spec["anchors"]["tail"]),
    ("body", "paint_brass_gold", [0, 0]),
    ("head_unit", "ear_boar_rivet_cowl_brass", spec["anchors"]["neck"]),
    ("costume", "costume_viking_harness", spec["anchors"]["navel"]),
    ("eyes", "eyes_cyan_emerald", [spec["anchors"]["neck"][0] + spec["anchors"]["brow_relative_to_neck"][0],
                                    spec["anchors"]["neck"][1] + spec["anchors"]["brow_relative_to_neck"][1]]),
    ("weapon", "wpn_anvil_greathammer", spec["anchors"]["hand"])
]

# 依 Z order
for s_name, item_id, anchor in slots:
    item_spec = spec["parts"][s_name]["items"][item_id]
    rel_path = item_spec["path"].replace("res://", "game/")
    im = Image.open(f"{REPO_ROOT}/{rel_path}").convert("RGBA")
    origin = item_spec["origin"]
    pos = (anchor[0] - origin[0], anchor[1] - origin[1])
    print(f"Slot {s_name:12}: anchor={anchor}, origin={origin} -> paste pos={pos}, size={im.size}")
    canvas.alpha_composite(im, pos)

canvas.save("/tmp/python_composite_direct.png")

# 檢查鼻吻正下方 (220..250, 175..205) 的 Alpha
arr = np.array(canvas)
snout_alpha = arr[175:205, 220:250, 3]
print("Snout alpha min:", np.min(snout_alpha), "zero count:", np.sum(snout_alpha == 0))
if np.sum(snout_alpha == 0) > 0:
    for y in range(175, 205):
        for x in range(220, 250):
            if arr[y, x, 3] == 0:
                print(f"  Empty at ({x}, {y})")
                break
