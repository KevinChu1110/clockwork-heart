#!/usr/bin/env python3
"""
tools/build_crane_sky_hunter_costume.py
Constructs costume_sky_hunter_mail.png (晴空巡獵機關羽甲) for Cloud Crane paperdoll.
- Tailored for Cloud Crane's 2.3-head chibi ranger body (Ranger archetype, Clockwork Heart).
- Zero fur / zero leather / zero biological cloth (CANON.md & art_direction.md).
- Features:
  1. High-rigidity aerodynamic gorget collar plate with gold rivets (Y: 52..60).
  2. Diamond heart aperture with golden brass bezel ring (X: 58..70, Y: 59..71), perfectly framing the optic core.
  3. Stepped dual articulated aero-vane pauldrons with gold rivets (Left: X 38..48, Right: X 76..86, Y 54..68).
  4. Interlocking cobalt-steel chest armor plates (X: 48..78, Y: 62..76) with vertical mortise seams.
  5. Articulated ranger gear-buckle belt (X: 48..78, Y: 76..81) with brass central cog buckle.
  6. Triple-split angled aero-foil tassets / skirt (X: 44..84, Y: 81..94) with gold borders.
- Layer independence: 0 identical pixels with chassis (Rule 4c).
- Dopamine palette: Deep Cobalt/Navy Steel (#1B2A4A ~ #1565C0), Sky Blue highlights (#38A0FF),
  Bright Brass/Gold (#FFD028 / #FFA010), crisp #1F1A3A outline.
- 128x128 RGBA
"""

import math
import os
from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"

def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
    return int(max(low, min(high, round(v))))

def noise(x: int, y: int) -> float:
    return (math.sin(x * 0.85 + y * 0.45) * 0.5 +
            math.cos(x * 0.35 - y * 0.75) * 0.3 +
            math.sin((x + y) * 1.2) * 0.2)

def create_crane_costume_sky_hunter_mail(out_path: str = "") -> Image.Image:
    if not out_path:
        out_path = f"{CRANE_DIR}/costume/costume_sky_hunter_mail.png"

    w, h = 128, 128
    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    chassis = Image.open(f"{CRANE_DIR}/chassis/paint_crane_porcelain.png").convert("RGBA")
    costume_ref = Image.open(f"{CRANE_DIR}/costume/costume_zephyr_robe.png").convert("RGBA")
    optic_core = Image.open(f"{CRANE_DIR}/optic_core/core_vermilion_lens.png").convert("RGBA")
    weapon = Image.open(f"{CRANE_DIR}/weapon/wpn_zephyr_wing_bow.png").convert("RGBA")

    def ch_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]
        return 0

    def opt_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], optic_core.getpixel((x, y)))[3]
        return 0

    def wpn_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], weapon.getpixel((x, y)))[3]
        return 0

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    # ─────────────────────────────────────────────────────────────
    # 1. GORGET COLLAR & BEZEL RING (Y: 52..71)
    # ─────────────────────────────────────────────────────────────
    # Center aperture around chest heart: center is (64.0, 65.0)
    # Heart diamond aperture: dx_d + dy_d <= 1.0 (hollowed for gem)
    for y in range(52, 73):
        for x in range(48, 80):
            # Skip if weapon is in front
            if wpn_a(x, y) > 50:
                continue

            dx_d = abs(x - 64.0) / 5.2
            dy_d = abs(y - 65.5) / 5.5
            dist_d = dx_d + dy_d

            # Heart aperture opening (hollowed so chest heart shines through)
            if dist_d <= 0.90:
                continue

            # Heart bezel ring (ornate polished brass #FFD028 / #FFA010)
            if dist_d <= 1.35:
                br = 255.0 - (dist_d - 0.90) * 55.0
                bg = 208.0 - (dist_d - 0.90) * 75.0
                bb = 38.0 + (dist_d - 0.90) * 35.0
                # Bevel outline
                if dist_d > 1.25:
                    br = 31.0; bg = 26.0; bb = 58.0
                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)
                continue

            # Gorget collar plates (X: 52..76, Y: 52..62)
            if y <= 62 and 52 <= x <= 76:
                n = noise(x, y) * 4.0
                # Deep navy-cobalt armor plate with high-gloss reflection
                br = 28.0 + n
                bg = 56.0 + n
                bb = 120.0 + n
                if y == 52:
                    # Top gold rim
                    br = 245.0; bg = 195.0; bb = 40.0
                elif y == 62:
                    # Seam groove outline
                    br = 31.0; bg = 26.0; bb = 58.0
                elif x in (56, 72) and y in (55, 59):
                    # Gold rivets
                    br = 255.0; bg = 210.0; bb = 45.0
                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # ─────────────────────────────────────────────────────────────
    # 2. DUAL AERO-VANE PAULDRONS (SHOULDER GUARDS)
    # ─────────────────────────────────────────────────────────────
    # Left pauldron (X: 38..49, Y: 54..68)
    for y in range(54, 69):
        for x in range(38, 50):
            # Left pauldron has 3 stepped vanes
            tier = (y - 54) // 5  # 0, 1, 2
            v_edge = (y - 54) % 5
            # Outer boundary check
            if x < 40 + tier and y < 58:
                continue
            if x > 48:
                continue

            # Sky Cobalt Blue with Cyan-Sky edge
            if v_edge == 0:
                # Top vane edge (bright gold brass rim)
                pr, pg, pb = 255.0, 208.0, 40.0
            elif x == 38 or (x == 39 and y > 60):
                # Outer bevel (deep outline)
                pr, pg, pb = 31.0, 26.0, 58.0
            elif x in (41, 46) and v_edge == 2:
                # Gold rivet
                pr, pg, pb = 255.0, 215.0, 48.0
            else:
                # Vibrant sky cobalt blue (#2979FF ~ #1565C0)
                lum_p = 0.5 + 0.5 * math.sin((x - 38) * 0.5 + (y - 54) * 0.4)
                pr = 30.0 + lum_p * 45.0
                pg = 95.0 + lum_p * 85.0
                pb = 195.0 + lum_p * 55.0
            pixels[(x, y)] = (clamp(pr), clamp(pg), clamp(pb), 255)

    # Right pauldron (X: 76..86, Y: 55..67)
    for y in range(55, 68):
        for x in range(76, 87):
            if wpn_a(x, y) > 50:
                continue
            v_edge = (y - 55) % 4
            if x == 86 or y == 67:
                pr, pg, pb = 31.0, 26.0, 58.0
            elif v_edge == 0:
                pr, pg, pb = 255.0, 208.0, 40.0
            elif x == 80 and v_edge == 2:
                pr, pg, pb = 255.0, 215.0, 48.0
            else:
                lum_p = 0.5 + 0.5 * math.cos((x - 76) * 0.5 + (y - 55) * 0.4)
                pr = 25.0 + lum_p * 40.0
                pg = 85.0 + lum_p * 80.0
                pb = 185.0 + lum_p * 60.0
            pixels[(x, y)] = (clamp(pr), clamp(pg), clamp(pb), 255)

    # ─────────────────────────────────────────────────────────────
    # 3. INTERLOCKING CHEST & MIDRIFF ARMOR PLATES (Y: 63..76, X: 48..78)
    # ─────────────────────────────────────────────────────────────
    for y in range(63, 77):
        for x in range(48, 79):
            if (x, y) in pixels:
                continue
            if wpn_a(x, y) > 50:
                continue

            # Check if within torso boundaries
            if not (49 <= x <= 77):
                continue

            # Vertical center seam at x == 64
            is_center_seam = (x == 64)
            # Lateral seams at x == 56, x == 72
            is_lat_seam = (x in (56, 72))
            # Horizontal plate seam at y == 70
            is_horiz_seam = (y == 70)

            if is_center_seam or is_lat_seam or is_horiz_seam:
                pr, pg, pb = 31.0, 26.0, 58.0  # #1F1A3A seam groove
            elif x in (52, 60, 68, 75) and y in (65, 73):
                # Gold rivets
                pr, pg, pb = 255.0, 212.0, 42.0
            else:
                # Cobalt & Navy steel armor plate
                n = noise(x, y) * 5.0
                # Left side slightly cooler, right side has highlight
                f_light = (x - 48) / 30.0
                pr = 22.0 + f_light * 25.0 + n
                pg = 60.0 + f_light * 65.0 + n
                pb = 140.0 + f_light * 80.0 + n
            pixels[(x, y)] = (clamp(pr), clamp(pg), clamp(pb), 255)

    # ─────────────────────────────────────────────────────────────
    # 4. RANGER COG-BUCKLE BELT (Y: 76..81, X: 46..80)
    # ─────────────────────────────────────────────────────────────
    for y in range(76, 82):
        for x in range(46, 81):
            if wpn_a(x, y) > 50:
                continue
            if not (47 <= x <= 79):
                continue

            # Center gear buckle: circle at (64, 78.5) radius 4.5
            dist_buckle = math.hypot(x - 64.0, y - 78.5)
            if dist_buckle <= 4.5:
                # Gold cog buckle
                if dist_buckle <= 1.5:
                    pr, pg, pb = 255.0, 240.0, 180.0  # inner axle hub shine
                elif dist_buckle >= 3.8:
                    pr, pg, pb = 31.0, 26.0, 58.0     # cog teeth rim
                else:
                    pr, pg, pb = 255.0, 208.0, 40.0   # rich gold
            elif y in (76, 81):
                # Belt top & bottom dark borders
                pr, pg, pb = 31.0, 26.0, 58.0
            else:
                # Warm amber-brass reinforced belt strap
                pr = 210.0 - (y - 77) * 20.0
                pg = 145.0 - (y - 77) * 25.0
                pb = 32.0 + (y - 77) * 10.0
            pixels[(x, y)] = (clamp(pr), clamp(pg), clamp(pb), 255)

    # ─────────────────────────────────────────────────────────────
    # 5. TRIPLE SPLIT AERO TASSETS / SKIRT (Y: 81..94, X: 44..84)
    # ─────────────────────────────────────────────────────────────
    for y in range(81, 95):
        for x in range(44, 85):
            if (x, y) in pixels:
                continue
            if wpn_a(x, y) > 50:
                continue

            # Three flaps:
            # Flap L: X 44..55, Y: 81..94 (angled out)
            # Flap C: X 58..70, Y: 81..91 (front center apron)
            # Flap R: X 73..84, Y: 81..93 (angled out)
            is_flap_l = (44 <= x <= 56 and y <= 94 - max(0, (50 - x)))
            is_flap_c = (58 <= x <= 70 and y <= 91)
            is_flap_r = (72 <= x <= 84 and y <= 93 - max(0, (x - 78)))

            if not (is_flap_l or is_flap_c or is_flap_r):
                continue

            # Outline and gold hem trims
            is_bottom_hem = (
                (is_flap_l and y >= 92 - max(0, (50 - x))) or
                (is_flap_c and y >= 89) or
                (is_flap_r and y >= 91 - max(0, (x - 78)))
            )
            is_edge = (
                x in (44, 56, 58, 70, 72, 84) or
                (is_flap_l and y == 94 - max(0, (50 - x))) or
                (is_flap_c and y == 91) or
                (is_flap_r and y == 93 - max(0, (x - 78)))
            )

            if is_edge:
                pr, pg, pb = 31.0, 26.0, 58.0  # crisp outline #1F1A3A
            elif is_bottom_hem:
                pr, pg, pb = 255.0, 208.0, 40.0 # Tianyuan gold border
            elif y == 84 and x in (49, 64, 78):
                pr, pg, pb = 255.0, 220.0, 50.0 # Gold rivet on tasset
            else:
                # Aero plate gradient: sky cobalt with cyan sheen
                n = noise(x, y) * 4.0
                if is_flap_c:
                    # Central apron: slightly darker navy alloy with gold center stripe
                    if x == 64:
                        pr, pg, pb = 255.0, 208.0, 40.0
                    else:
                        pr = 25.0 + n; pg = 65.0 + n; pb = 145.0 + n
                else:
                    # Lateral wings: Sky Cobalt Blue (#2979FF ~ #38A0FF)
                    fl = (y - 81) / 12.0
                    pr = 35.0 + fl * 25.0 + n
                    pg = 100.0 + fl * 40.0 + n
                    pb = 220.0 - fl * 20.0 + n
            pixels[(x, y)] = (clamp(pr), clamp(pg), clamp(pb), 255)

    # ─────────────────────────────────────────────────────────────
    # WRITE PIXELS & GUARANTEE ZERO PIXEL COLLISION WITH CHASSIS (RULE 4c)
    # ─────────────────────────────────────────────────────────────
    ch_porcelain_arr = np.array(chassis)
    ch_azure_path = f"{CRANE_DIR}/chassis/paint_zephyr_azure.png"
    ch_azure_arr = np.array(Image.open(ch_azure_path).convert("RGBA")) if os.path.exists(ch_azure_path) else None

    for (x, y), (r, g, b, a) in pixels.items():
        # Check porcelain collision
        ch_p = ch_porcelain_arr[y, x]
        if ch_p[3] > 20 and int(ch_p[0]) == r and int(ch_p[1]) == g and int(ch_p[2]) == b:
            r = min(255, r + 1) if r < 255 else r - 1

        # Check azure collision
        if ch_azure_arr is not None:
            az_p = ch_azure_arr[y, x]
            if az_p[3] > 20 and int(az_p[0]) == r and int(az_p[1]) == g and int(az_p[2]) == b:
                g = min(255, g + 1) if g < 255 else g - 1

        art.putpixel((x, y), (r, g, b, a))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    art.save(out_path)
    print(f"✓ Saved crane sky hunter costume: {out_path} (bbox: {art.getbbox()})")
    return art

if __name__ == "__main__":
    create_crane_costume_sky_hunter_mail()
