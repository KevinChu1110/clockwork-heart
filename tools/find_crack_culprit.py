#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

ear = Image.open(f"{BASE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
core = Image.open(f"{BASE_DIR}/optic_core/core_cyan_emerald.png").convert("RGBA")
chassis = Image.open(f"{BASE_DIR}/chassis/paint_bamboo_bronze.png").convert("RGBA")

# Let's check non-zero pixels around the right eye in each:
# Right eye in 128x128 sprite is around x: 55..75, y: 30..45
print("=== Checking ear layer at x: 55..75, y: 30..45 ===")
ear_px = [(x, y, ear.getpixel((x, y))) for y in range(30, 46) for x in range(55, 76) if ear.getpixel((x, y))[3] > 0]
print(f"Ear non-transparent pixels in eye region: {len(ear_px)}")
for p in ear_px[:20]:
    print(f"  {p}")

print("\n=== Checking core layer at x: 55..75, y: 30..45 ===")
core_px = [(x, y, core.getpixel((x, y))) for y in range(30, 46) for x in range(55, 76) if core.getpixel((x, y))[3] > 0]
print(f"Core non-transparent pixels in eye region: {len(core_px)}")
for p in core_px[:20]:
    print(f"  {p}")

print("\n=== Checking chassis layer at x: 55..75, y: 30..45 ===")
chassis_px = [(x, y, chassis.getpixel((x, y))) for y in range(30, 46) for x in range(55, 76) if chassis.getpixel((x, y))[3] > 0 and chassis.getpixel((x, y))[0] < 80 and chassis.getpixel((x, y))[1] < 80]
print(f"Chassis dark pixels in eye region: {len(chassis_px)}")
for p in chassis_px[:20]:
    print(f"  {p}")
