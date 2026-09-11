#!/usr/bin/env python3
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

def measure():
    chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
    head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
    tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")
    striker = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker.png").convert("RGBA")

    # Bare body
    bare = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    bare = Image.alpha_composite(bare, chassis)
    bare = Image.alpha_composite(bare, head)

    # 1. Dark outline scan: a>150 and r<110 and g<90 and b<80
    dark_pts: list[tuple[int, int]] = []
    for y in range(128):
        for x in range(128):
            px = cast(tuple[int, int, int, int], bare.getpixel((x, y)))
            r, g, b, a = px
            if a > 150 and r < 110 and g < 90 and b < 80:
                dark_pts.append((x, y))

    # In chin / mouth area (x around 48..66, y around 60..78)
    chin_pts = [(x, y) for (x, y) in dark_pts if 48 <= x <= 66 and 60 <= y <= 76]
    chin_pts_y = sorted(set(y for (x, y) in chin_pts))

    # Collar top edge y in neck center (x: 50..65)
    tunic_collar_ys = [y for x in range(50, 65) for y in range(128) if cast(tuple[int, int, int, int], tunic.getpixel((x, y)))[3] > 30]
    striker_collar_ys = [y for x in range(50, 65) for y in range(128) if cast(tuple[int, int, int, int], striker.getpixel((x, y)))[3] > 30]

    tunic_collar_y = min(tunic_collar_ys) if tunic_collar_ys else None
    striker_collar_y = min(striker_collar_ys) if striker_collar_ys else None

    # Altered dark line pixels count:
    comp_tunic = Image.alpha_composite(bare, tunic)
    comp_striker = Image.alpha_composite(bare, striker)

    tunic_altered_pts = [pt for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt)]
    striker_altered_pts = [pt for pt in dark_pts if comp_striker.getpixel(pt) != bare.getpixel(pt)]

    tunic_altered = len(tunic_altered_pts)
    striker_altered = len(striker_altered_pts)

    print(f"=== 4c-9 MEASUREMENTS ===")
    print(f"1. Chin/mouth dark line y-coords: {chin_pts_y}")
    print(f"2. costume_dawn_monk_tunic collar top y: {tunic_collar_y}")
    print(f"3. costume_zen_striker collar top y: {striker_collar_y}")
    print(f"4. Altered bare dark line pixels: Old (tunic) = {tunic_altered}, New (striker) = {striker_altered}")
    if tunic_altered > 0:
        print(f"   Ratio: {striker_altered / tunic_altered:.2f}x (threshold: <= 1.0x, fail if >= 2.0x)")

    # Breakdown by y of altered pixels
    print("\nAltered pixels breakdown by Y:")
    for y_range in [(50, 58), (59, 65), (66, 75), (76, 85), (86, 110)]:
        t_c = sum(1 for (x, y) in tunic_altered_pts if y_range[0] <= y <= y_range[1])
        s_c = sum(1 for (x, y) in striker_altered_pts if y_range[0] <= y <= y_range[1])
        print(f"  Y {y_range[0]:2d}..{y_range[1]:2d}: tunic={t_c:3d}, striker={s_c:3d}")

if __name__ == "__main__":
    measure()
