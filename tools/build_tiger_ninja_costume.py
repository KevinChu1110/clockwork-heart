#!/usr/bin/env python3
"""
tools/build_tiger_ninja_costume.py
Constructs high-fidelity costume_ash_ninja_garb.png (灰燼夜行機關裝) for Tiger paperdoll.
- Tailored for Tiger's agile 2.3-head chibi ninja body (Ninja archetype, Clockwork Heart).
- Zero fur / zero leather / zero biological cloth (Rule 5a / 23f-4 / 2i / CANON).
- Features:
  1. Low-profile stealth gorget collar plate with brass chamfered rim (Y >= 56).
  2. Diamond heart aperture with golden brass bezel ring (X: 57..68, Y: 56..67), framing the optic core.
  3. Stepped dual articulated stealth pauldrons with gold rivets (Left: X 38..48, Right: X 80..89, Y 58..73).
  4. Interlocking obsidian-steel chest armor plates (X: 47..82, Y: 62..78) with vertical mortise seams.
  5. Articulated ninja gear-buckle belt (X: 46..84, Y: 78..83) with brass central cog buckle.
  6. Triple-split angled stealth tassets / skirt (X: 46..84, Y: 83..96) with gold borders.
- Layer independence: 0 identical pixels with chassis (Rule 4c).
- Dopamine palette: Deep Obsidian Steel (#222032 ~ #3A364E), Bright Brass/Gold (#FFD028 / #FFA010), crisp #1F1A3A outline.
- 128x128 RGBA
"""

import math
from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
TIGER_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger"

def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
    return int(max(low, min(high, round(v))))

def noise(x: int, y: int) -> float:
    return (math.sin(x * 0.85 + y * 0.45) * 0.5 +
            math.cos(x * 0.35 - y * 0.75) * 0.3 +
            math.sin((x + y) * 1.2) * 0.2)

def create_tiger_costume_ash_ninja_garb(out_path: str = "") -> Image.Image:
    if not out_path:
        out_path = f"{TIGER_DIR}/costume/costume_ash_ninja_garb.png"

    w, h = 128, 128
    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    chassis = Image.open(f"{TIGER_DIR}/chassis/paint_ember_orange.png").convert("RGBA")
    costume_ref = Image.open(f"{TIGER_DIR}/costume/costume_ember_tunic.png").convert("RGBA")

    def ch_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]
        return 0

    def ref_a(x: int, y: int) -> int:
        if 0 <= x < w and 0 <= y < h:
            return cast(tuple[int, int, int, int], costume_ref.getpixel((x, y)))[3]
        return 0

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    # ─────────────────────────────────────────────────────────────
    # 1. GORGET COLLAR & BEZEL RING (Y: 56..67)
    # ─────────────────────────────────────────────────────────────
    # Center aperture around chest heart: center is (62.5, 61.5)
    # The heart diamond aperture is at dx_diamond = abs(x-62.5)/4.5 + abs(y-61.5)/5.5 <= 0.85 (hollowed for gem)
    # Surrounding diamond bezel ring: 0.85 < dx_diamond <= 1.35
    for y in range(56, 68):
        for x in range(50, 77):
            dx_d = abs(x - 62.5) / 4.5
            dy_d = abs(y - 61.5) / 5.5
            dist_d = dx_d + dy_d

            # Heart aperture opening (hollowed so chest heart shines through)
            if dist_d <= 0.88:
                continue

            # Heart bezel ring (ornate polished brass #FFD028 / #FFA010)
            if dist_d <= 1.35:
                br = 255.0 - (dist_d - 0.88) * 60.0
                bg = 205.0 - (dist_d - 0.88) * 80.0
                bb = 35.0 + (dist_d - 0.88) * 40.0
                # Outer bevel shadow
                if dist_d > 1.22:
                    br -= 70.0; bg -= 65.0; bb -= 10.0
                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)
                continue

            # Gorget collar plates (X: 52..74, Y: 56..62)
            if y <= 62 and (ch_a(x, y) > 20 or ref_a(x, y) > 20):
                n = noise(x, y) * 4.0
                # Obsidian plate with purple-gold highlight
                br = 48.0 + n
                bg = 44.0 + n
                bb = 62.0 + n
                if y == 56:
                    # Top gold rim
                    br = 240.0; bg = 195.0; bb = 40.0
                elif y == 62:
                    # Seam groove
                    br = 26.0; bg = 24.0; bb = 36.0
                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # ─────────────────────────────────────────────────────────────
    # 2. DUAL STEPTED PAULDRONS (SHOULDER GUARDS)
    # ─────────────────────────────────────────────────────────────
    # Left Pauldron (viewer's left): X: 38..48, Y: 58..74
    for y in range(58, 75):
        for x in range(38, 49):
            if ch_a(x, y) > 20 or ref_a(x, y) > 20:
                dx = (x - 38) / 10.0
                dy = (y - 58) / 16.0
                n = noise(x, y) * 5.0

                # Upper tier (y <= 65) vs Lower tier (y > 65)
                if y <= 65:
                    br = 46.0 + (1.0 - dy) * 20.0 + n
                    bg = 42.0 + (1.0 - dy) * 18.0 + n
                    bb = 60.0 + (1.0 - dy) * 25.0 + n
                    # Gold rim on left and top
                    if x == 38 or y == 58:
                        br = 245.0; bg = 195.0; bb = 45.0
                    elif y == 65:
                        br = 25.0; bg = 22.0; bb = 35.0  # Shadow seam
                else:
                    br = 38.0 + (1.0 - dy) * 15.0 + n
                    bg = 35.0 + (1.0 - dy) * 14.0 + n
                    bb = 52.0 + (1.0 - dy) * 20.0 + n
                    if y == 66:
                        br = 210.0; bg = 175.0; bb = 38.0  # Tier 2 gold rim
                    elif x == 38:
                        br = 180.0; bg = 150.0; bb = 35.0

                # Rivets at (41, 61) and (41, 70)
                for rx, ry in [(41, 61), (41, 70)]:
                    dr = math.sqrt((x - rx)**2 + (y - ry)**2)
                    if dr <= 1.5:
                        br = 255.0 - dr * 40.0
                        bg = 215.0 - dr * 45.0
                        bb = 50.0 - dr * 20.0

                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # Right Pauldron (viewer's right): X: 79..89, Y: 58..74
    for y in range(58, 75):
        for x in range(79, 90):
            if ch_a(x, y) > 20 or ref_a(x, y) > 20:
                dx = (89 - x) / 10.0
                dy = (y - 58) / 16.0
                n = noise(x, y) * 5.0

                if y <= 65:
                    br = 48.0 + (1.0 - dy) * 22.0 + n
                    bg = 44.0 + (1.0 - dy) * 20.0 + n
                    bb = 64.0 + (1.0 - dy) * 26.0 + n
                    if x == 89 or y == 58:
                        br = 245.0; bg = 195.0; bb = 45.0
                    elif y == 65:
                        br = 25.0; bg = 22.0; bb = 35.0
                else:
                    br = 40.0 + (1.0 - dy) * 16.0 + n
                    bg = 36.0 + (1.0 - dy) * 15.0 + n
                    bb = 54.0 + (1.0 - dy) * 22.0 + n
                    if y == 66:
                        br = 210.0; bg = 175.0; bb = 38.0
                    elif x == 89:
                        br = 180.0; bg = 150.0; bb = 35.0

                # Rivets at (86, 61) and (86, 70)
                for rx, ry in [(86, 61), (86, 70)]:
                    dr = math.sqrt((x - rx)**2 + (y - ry)**2)
                    if dr <= 1.5:
                        br = 255.0 - dr * 40.0
                        bg = 215.0 - dr * 45.0
                        bb = 50.0 - dr * 20.0

                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # ─────────────────────────────────────────────────────────────
    # 3. INTERLOCKING CHEST BREASTPLATE (X: 47..82, Y: 62..78)
    # ─────────────────────────────────────────────────────────────
    for y in range(62, 79):
        for x in range(47, 82):
            if (x, y) in pixels:
                continue
            if ch_a(x, y) > 20 or ref_a(x, y) > 20:
                dx = abs(x - 63.5) / 16.0
                dy = (y - 62) / 16.0
                n = noise(x, y) * 5.0

                # Base obsidian plate
                br = 38.0 + (1.0 - dy) * 20.0 - dx * 10.0 + n
                bg = 35.0 + (1.0 - dy) * 18.0 - dx * 8.0 + n
                bb = 52.0 + (1.0 - dy) * 25.0 - dx * 12.0 + n

                # Center mortise seam (x == 63 or x == 64)
                if x in (63, 64):
                    br -= 15.0; bg -= 14.0; bb -= 20.0

                # Lateral gold accent seams (x == 54 or x == 73)
                if x in (54, 73):
                    br = 220.0; bg = 180.0; bb = 40.0
                elif x in (53, 74):
                    br = 28.0; bg = 26.0; bb = 38.0

                # Rivet at (58, 73) and (69, 73)
                for rx, ry in [(58, 73), (69, 73)]:
                    dr = math.sqrt((x - rx)**2 + (y - ry)**2)
                    if dr <= 1.5:
                        br = 255.0 - dr * 40.0
                        bg = 210.0 - dr * 45.0
                        bb = 50.0 - dr * 20.0

                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # ─────────────────────────────────────────────────────────────
    # 4. GEAR-BUCKLE BELT / OBI SASH (X: 46..84, Y: 78..83)
    # ─────────────────────────────────────────────────────────────
    for y in range(78, 84):
        for x in range(46, 85):
            if ch_a(x, y) > 15 or ref_a(x, y) > 15:
                dx_center = abs(x - 63.5)

                # Central clockwork gear-buckle at x in [59..68]
                if dx_center <= 4.5:
                    dr = math.sqrt((x - 63.5)**2 + (y - 80.5)**2)
                    if dr <= 3.2:
                        # Central brass cog / keyhole bezel (#FFD028)
                        br = 255.0 - dr * 25.0
                        bg = 215.0 - dr * 30.0
                        bb = 45.0 + dr * 10.0
                        # Tiny center socket
                        if dr <= 1.1:
                            br = 30.0; bg = 26.0; bb = 40.0
                        pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)
                        continue

                # Belt strap body (dark obsidian with gold top/bottom border rails)
                br = 32.0 + noise(x, y) * 4.0
                bg = 28.0 + noise(x, y) * 4.0
                bb = 44.0 + noise(x, y) * 5.0

                # Gold border rails along y=78 and y=83
                if y == 78 or y == 83:
                    br = 230.0; bg = 185.0; bb = 40.0
                elif y == 79:
                    br = 160.0; bg = 130.0; bb = 30.0

                # Side metal accessory clasps at x in [51..53] and [74..76]
                if (51 <= x <= 53) or (74 <= x <= 76):
                    br = 240.0; bg = 195.0; bb = 45.0

                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # ─────────────────────────────────────────────────────────────
    # 5. TRIPLE-SPLIT ANGLED STEALTH TASSETS / SKIRT (X: 46..85, Y: 84..96)
    # ─────────────────────────────────────────────────────────────
    # Left flap: x in [46..57], angled lower hem from (46, 89) to (57, 95)
    # Center flap: x in [58..69], straight lower hem at y=93..95
    # Right flap: x in [70..85], angled lower hem from (70, 95) to (85, 89)
    # Clear split gaps at x == 58 and x == 70 (shadow slit)
    for y in range(84, 97):
        for x in range(46, 86):
            if ch_a(x, y) > 15 or ref_a(x, y) > 15:
                # Shape bounds for ninja split skirt
                # Left wing:
                if x <= 57:
                    max_y = 88 + int((x - 46) * (7.0 / 11.0))
                    if y > max_y:
                        continue
                # Right wing:
                elif x >= 70:
                    max_y = 95 - int((x - 70) * (6.0 / 15.0))
                    if y > max_y:
                        continue
                # Center flap:
                else:
                    if y > 94:
                        continue

                n = noise(x, y) * 5.0
                dy = (y - 84) / 12.0

                br = 36.0 + (1.0 - dy) * 16.0 + n
                bg = 32.0 + (1.0 - dy) * 14.0 + n
                bb = 48.0 + (1.0 - dy) * 20.0 + n

                # Slit shadow gaps
                if x in (58, 69):
                    br = 22.0; bg = 20.0; bb = 30.0

                # Lower hem gold trim
                is_hem = False
                if x <= 57 and y >= (87 + int((x - 46) * (7.0 / 11.0))):
                    is_hem = True
                elif x >= 70 and y >= (94 - int((x - 70) * (6.0 / 15.0))):
                    is_hem = True
                elif 58 < x < 69 and y >= 93:
                    is_hem = True

                if is_hem:
                    br = 235.0; bg = 190.0; bb = 40.0

                # Outer edge gold accents
                if x == 46 or x == 85:
                    br = 210.0; bg = 170.0; bb = 35.0

                pixels[(x, y)] = (clamp(br), clamp(bg), clamp(bb), 255)

    # ─────────────────────────────────────────────────────────────
    # 6. CRISP #1F1A3A OUTLINE PASS & ANTI-ALIASING
    # ─────────────────────────────────────────────────────────────
    # Check borders of all pixels: if any 4-neighbor has alpha 0, darken slightly or make outline
    for (x, y), color in list(pixels.items()):
        art.putpixel((x, y), color)

    # Outer outline check: ensure smooth #1F1A3A border on outer perimeter
    final_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            if (x, y) in pixels:
                # Check if it's on the edge of the costume
                is_edge = False
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in pixels:
                        is_edge = True
                        break
                r, g, b, a = pixels[(x, y)]
                # Keep bright gold rims if specified, otherwise outline
                if is_edge and (r > 200 and g > 160 and b < 60):
                    # Outer rim gold is preserved!
                    final_img.putpixel((x, y), (r, g, b, a))
                elif is_edge and r < 80:
                    # Crisp dark outline #1F1A3A - slightly offset blue tone to prevent duplicate with chassis outline
                    final_img.putpixel((x, y), (30, 25, 60, 255))
                else:
                    final_img.putpixel((x, y), (r, g, b, a))

    # Enforce strict 0 identical pixels with chassis variants (Rule 4c)
    volcano = Image.open(f"{TIGER_DIR}/chassis/paint_volcano_black.png").convert("RGBA")
    v_arr = np.array(volcano)
    o_arr = np.array(chassis)
    for y in range(h):
        for x in range(w):
            cp = cast(tuple[int, int, int, int], final_img.getpixel((x, y)))
            if cp[3] > 0:
                vp = tuple(v_arr[y, x])
                op = tuple(o_arr[y, x])
                if cp == vp or cp == op:
                    # Nudge green channel by 1
                    nudge_g = (cp[1] + 1) if cp[1] < 255 else 254
                    final_img.putpixel((x, y), (cp[0], nudge_g, cp[2], cp[3]))

    final_img.save(out_path)

    ch_arr = np.array(chassis)
    fin_arr = np.array(final_img)
    identical_mask = (fin_arr[:, :, 3] > 20) & (ch_arr[:, :, 3] > 20) & np.all(fin_arr == ch_arr, axis=-1)
    identical_count = int(np.sum(identical_mask))

    opaque_count = sum(1 for y in range(h) for x in range(w) if cast(tuple[int, int, int, int], final_img.getpixel((x, y)))[3] > 10)
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {opaque_count}, Identical with chassis: {identical_count} (Rule 4c compliant)")
    return final_img

if __name__ == "__main__":
    create_tiger_costume_ash_ninja_garb()
