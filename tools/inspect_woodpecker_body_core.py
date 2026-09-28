#!/usr/bin/env python3
"""
Inspect woodpecker body_core and landmark features.
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"

curio = Image.open(f"{BASE_DIR}/back_curio/curio_woodpecker_riveted_tinplate_prop_tail.png").convert("RGBA")
chassis = Image.open(f"{BASE_DIR}/chassis/chassis_woodpecker_tinplate_brass_default.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_woodpecker_scarlet_crest_cowl.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_woodpecker_skyspire_inspector_harness.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_woodpecker_precision_gauge_monocle.png").convert("RGBA")

body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio)
body_core.alpha_composite(chassis)
body_core.alpha_composite(head)
body_core.alpha_composite(costume)
body_core.alpha_composite(optic)

bbox = body_core.getbbox()
print("Body core bbox:", bbox)

arr = np.array(body_core)
alpha = arr[:, :, 3]

# Check feet & tail in rows 110..120
for y in [112, 114, 116, 118]:
    xs = np.where(alpha[y, :] > 20)[0]
    print(f"y={y}: min_x={xs[0]}, max_x={xs[-1]}, count={len(xs)}")
