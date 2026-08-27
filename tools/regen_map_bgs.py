#!/usr/bin/env python3
"""照 docs/MAP_ART_SPEC.md 重生成違規底圖（2026-08-27 體檢：13 張）。

違規類型：帶天空地平線的遠景、平視鏡頭、畫框卷軸圖。
產後仍需：pixelize_env → 重描 walkmask → verify_capture（見 SPEC「產後三件事」）。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_GEN = ROOT / ".agents/skills/asset-gen/tools/asset_gen.py"
PY = ROOT / ".venv-asset/bin/python"
GEN = ROOT / "game/assets/sprites/_gen_r2/maps_spec"
MAPS = ROOT / "game/assets/sprites/maps"

TEMPLATE = (
    "top-down 3/4 isometric RPG map background, camera looking down at 45 degrees, "
    "consistent scale: a single-story house is about 1/4 of image height and a doorway "
    "about 1/12 of image height, ground terrain fills the entire canvas edge to edge, "
    "no sky, no horizon, no clouds, no border, no frame, no text, clear walkable dirt "
    "paths about twice door width connecting to the edges, at least forty percent open "
    "walkable ground, warm muted painted game art, "
)

BRIEFS = {
    "cross_east": "barren ash wasteland crossroads, dead trees along the sides, weathered stone arches and old milestones, a forked dirt road, dark cracks in the scorched ground",
    "cross_north": "misty highland crossroads with mossy standing stones, pine clusters, a wide mountain path forking northward",
    "road": "rolling green countryside with a wide winding dirt road, hedges, a stone milestone, scattered trees and grass fields",
    "road_bridge": "an old stone bridge crossing a modest river, riverbanks with reeds and rocks, the road continuing on both sides",
    "road_inn": "a half-collapsed roadside inn with an open-walled shed, a stable yard with wooden troughs, a dirt courtyard and the road passing through",
    "road_ruins": "overgrown stone ruins beside the road, fallen columns, a cracked mosaic floor, wildflowers among rubble",
    "starfall_plain": "a night-lit grassy plain dotted with faintly glowing meteor stones and shallow impact craters, rune-carved standing stones, a small stargazer camp with tents and a campfire",
    "village_mill": "a windmill farmstead among golden wheat fields, fenced plots, a barn and a well, dirt lanes between the fields",
    "wild": "scorched wild borderlands, ruined burnt watchtower, blackened ground patches, sparse dead shrubs, a broken war road",
    "wild_leo_court": "a ruined castle forecourt, cracked flagstone plaza flanked by five stone lion statues, a grand staircase leading to a fortified gate, rubble piles along the walls",
    "wild_ravine": "a rocky ravine crossing with a wooden rope bridge, cliff ledges with small campfires, the gorge as a clear boundary through the middle",
    "mist_cliff": "a foggy clifftop plateau with twisted pines and stone lanterns along a winding path, mist banks marking the plateau edges",
    "dojo_peak": "a mountaintop stone training platform with banners and practice dummies, rock gardens, cloud-mist only at the very image edges as a boundary",
}


def main() -> int:
    if not os.environ.get("GOOGLE_API_KEY"):
        print("no GOOGLE_API_KEY", file=sys.stderr)
        return 2
    from PIL import Image

    GEN.mkdir(parents=True, exist_ok=True)
    (GEN / ".gdignore").write_text("# gen sources — not loaded by game\n")
    ok = fail = cost = 0
    for name, brief in BRIEFS.items():
        print(f"==> {name}", flush=True)
        raw = GEN / f"{name}.png"
        if not (raw.exists() and raw.stat().st_size > 50000):
            cmd = [
                str(PY if PY.exists() else sys.executable), str(ASSET_GEN), "image",
                "--model", "gemini", "--size", "2K", "--aspect-ratio", "16:9",
                "--prompt", TEMPLATE + brief, "-o", str(raw),
            ]
            done = False
            for attempt in range(1, 4):
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
                if r.returncode == 0 and raw.exists():
                    done = True
                    break
                if "503" in (r.stderr or ""):
                    time.sleep(6 * attempt)
            if not done:
                fail += 1
                print("  FAIL", flush=True)
                continue
            cost += 7
        im = Image.open(raw).convert("RGB")
        im.thumbnail((2633, 1469), Image.LANCZOS)
        im.save(MAPS / f"{name}_bg.webp", quality=90, method=6)
        ok += 1
        print("  OK", flush=True)
        time.sleep(1.0)
    print(json.dumps({"ok": ok, "fail": fail, "cost_cents_est": cost}))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
