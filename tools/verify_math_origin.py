#!/usr/bin/env python3
import json
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
boar_json = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

with open(boar_json) as f:
    spec = json.load(f)

anchors = spec["anchors"]
# neck: (250, 176)
neck = anchors["neck"]
head_item = spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_brass"]
path = head_item["path"].replace("res://", f"{REPO_ROOT}/game/")
im = Image.open(path)
w, h = im.size
orig = head_item["origin"]
# 切片如果在 512 空間，左上角在 (neck[0] - orig[0], neck[1] - orig[1])
x0 = neck[0] - orig[0]
y0 = neck[1] - orig[1]
print(f"Boar head: neck={neck}, origin={orig}, size=({w}, {h}) -> placed at 512 pos: ({x0}, {y0}) to ({x0+w}, {y0+h})")
