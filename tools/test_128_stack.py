#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

key = Image.open(f"{BOAR_DIR}/winding_key/key_classic_brass.png").convert("RGBA")
tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
chassis = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold.png").convert("RGBA")
head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass.png").convert("RGBA")
costume = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad.png").convert("RGBA")
weapon = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer.png").convert("RGBA")
core = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald.png").convert("RGBA")
comp_target = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")

# 依照 Z order 合成 128
test_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
test_128.alpha_composite(key)
test_128.alpha_composite(tail)
test_128.alpha_composite(chassis)
test_128.alpha_composite(head)
test_128.alpha_composite(costume)
test_128.alpha_composite(core)
test_128.alpha_composite(weapon)

test_128.save("/tmp/boar_128_stack_test.png")

# 比對與 proof_paperdoll_boar_composite.png 的差異
diff_cnt = 0
for y in range(128):
    for x in range(128):
        p1 = test_128.getpixel((x, y))
        p2 = comp_target.getpixel((x, y))
        if p1 != p2:
            diff_cnt += 1

print(f"Diff between stacked 128 and target composite: {diff_cnt} pixels")
