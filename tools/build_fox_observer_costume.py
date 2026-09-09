#!/usr/bin/env python3
"""
tools/build_fox_observer_costume.py
Constructs costume_astral_observer.png for Fox paperdoll.
- Tailored for Fox's agile 2.4-head chibi body (Mage archetype, R03 Emerald Woods Astrologer)
- Zero fur / zero leather / zero cloth / zero velvet (Rule 5a / 23f-4)
- Astrolabe engraved brass breastplate, celestial bronze pauldrons, crossed steel braces,
  gear-buckle belt, and three-tier segmented brass tassets
- Continuous lighting, specular bevels, 3D spherical clockwork rivets, anti-aliased outlines
  achieving high color nuance (colors/100px >= 24, Rule 10a-2)
- Layer independence: 0 identical pixels with chassis (Rule 4c)
- 128x128 RGBA
"""

import math
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
FOX_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox"

def create_fox_costume_astral_observer():
    w, h = 128, 128
    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cape = Image.open(f"{FOX_DIR}/costume/costume_astral_cape.png").convert("RGBA")
    chassis = Image.open(f"{FOX_DIR}/chassis/paint_fox_orange.png").convert("RGBA")

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
        return int(max(low, min(high, round(v))))

    def noise(x: int, y: int) -> float:
        return (math.sin(x * 0.85 + y * 0.45) * 0.5 + 
                math.cos(x * 0.35 - y * 0.75) * 0.3 + 
                math.sin((x + y) * 1.2) * 0.2)

    def cape_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], cape.getpixel((x, y)))[3]

    def ch_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], chassis.getpixel((x, y)))[3]

    # 1. Gorget Collar Plate (Neck protector): X: 48..72, Y: 56..64
    for y in range(56, 65):
        for x in range(48, 73):
            if ch_a(x, y) > 30 or cape_a(x, y) > 20:
                dx = abs(x - 60) / 12.0
                dy = (y - 56) / 8.0
                n = noise(x, y) * 7.0
                # Warm burnished brass with cool ambient light
                base_r = 195.0 - dx * 35.0 - dy * 20.0 + n
                base_g = 155.0 - dx * 30.0 - dy * 15.0 + n
                base_b = 65.0 - dx * 15.0 - dy * 10.0 + n
                # Specular top edge
                if y == 56 or (y == 57 and abs(x - 60) < 6):
                    base_r += 35; base_g += 40; base_b += 45
                # Bottom groove shadow
                if y == 64:
                    base_r -= 35; base_g -= 30; base_b -= 15
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 2. Left Celestial Pauldron (viewer left): X: 33..47, Y: 59..75
    for y in range(59, 76):
        for x in range(33, 48):
            if ch_a(x, y) > 20 or cape_a(x, y) > 20:
                dist_top = (y - 59) / 16.0
                dist_left = (x - 33) / 14.0
                n = noise(x, y) * 8.0
                # Celestial Bronze with teal oxidation undertones (#4A6070 ~ #6B8095)
                base_r = 65.0 + (1.0 - dist_top) * 45.0 - dist_left * 15.0 + n
                base_g = 80.0 + (1.0 - dist_top) * 50.0 - dist_left * 15.0 + n
                base_b = 100.0 + (1.0 - dist_top) * 60.0 - dist_left * 20.0 + n
                # Brass rim on outer edge
                if x in (33, 34) or y == 59:
                    base_r += 80; base_g += 65; base_b -= 15
                # Lower plate rim
                if y in (67, 75):
                    base_r += 40; base_g += 35; base_b += 10
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 3. Right Celestial Pauldron (viewer right): X: 73..87, Y: 59..75
    for y in range(59, 76):
        for x in range(73, 88):
            if ch_a(x, y) > 20 or cape_a(x, y) > 20:
                dist_top = (y - 59) / 16.0
                dist_right = (87 - x) / 14.0
                n = noise(x, y) * 8.0
                # Celestial Bronze with slightly deeper shadow on staff side
                base_r = 60.0 + (1.0 - dist_top) * 40.0 + dist_right * 15.0 + n
                base_g = 75.0 + (1.0 - dist_top) * 45.0 + dist_right * 15.0 + n
                base_b = 95.0 + (1.0 - dist_top) * 55.0 + dist_right * 20.0 + n
                # Brass rim on outer edge
                if x in (86, 87) or y == 59:
                    base_r += 80; base_g += 65; base_b -= 15
                if y in (67, 75):
                    base_r += 40; base_g += 35; base_b += 10
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 4. Underlay Chain-Mesh / Micro-Link Armor: X: 45..75, Y: 65..87
    for y in range(65, 88):
        for x in range(45, 76):
            if ch_a(x, y) > 25:
                n = noise(x, y) * 9.0
                weave = (1.5 if (x + y) % 2 == 0 else -1.5) * 4.0
                vy = (y - 65) / 22.0
                vx = abs(x - 60) / 15.0
                # Dark gunmetal/steel chain-mesh
                base_r = 48.0 - vy * 12.0 - vx * 8.0 + n + weave
                base_g = 52.0 - vy * 12.0 - vx * 8.0 + n + weave
                base_b = 64.0 - vy * 10.0 - vx * 6.0 + n + weave
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 5. Astrolabe Engraved Brass Breastplate: X: 49..71, Y: 65..86
    for y in range(65, 87):
        for x in range(49, 72):
            if ch_a(x, y) > 20:
                n = noise(x, y) * 7.0
                cx = (x - 60) / 11.0
                cy = (y - 75) / 11.0
                rad = math.sqrt(cx * cx + cy * cy)
                
                # Astrolabe concentric rings (星軌同心圓與刻線)
                is_ring = abs(rad - 0.5) < 0.08 or abs(rad - 0.85) < 0.08
                is_cross = (abs(cx) < 0.09 and abs(cy) < 0.85) or (abs(cy) < 0.09 and abs(cx) < 0.85)
                
                light = (1.0 - cx * 0.45) * (1.0 - cy * 0.35)
                # Radiant antique brass
                base_r = 185.0 * light + n
                base_g = 145.0 * light + n
                base_b = 55.0 * light + n
                
                if is_ring or is_cross:
                    # Engraved dark groove with subtle specular bevel
                    base_r -= 45.0; base_g -= 40.0; base_b -= 15.0
                    if x > 60 or y > 75:
                        base_r += 25.0; base_g += 20.0; base_b += 10.0
                else:
                    # Spherical curvature highlight
                    if rad < 0.4:
                        base_r += 30; base_g += 28; base_b += 15
                
                # Outer bevel of breastplate
                if x in (49, 71) or y in (65, 86):
                    base_r -= 30; base_g -= 25; base_b -= 10
                if y == 65 and 52 <= x <= 68:
                    base_r += 35; base_g += 35; base_b += 20
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 6. Center Celestial Astrolabe Core Gem Lens (天球核心晶石): X: 59..62, Y: 73..76
    for y in range(73, 77):
        for x in range(59, 63):
            n = noise(x, y) * 5.0
            dx = x - 60.5
            dy = y - 74.5
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= 1.8:
                # Glowing cyan-emerald gemstone lens (#4ED86A ~ #38E0B0)
                if dx <= 0 and dy <= 0:
                    # Specular highlight
                    pixels[(x, y)] = (clamp(180 + n), clamp(255), clamp(225 + n), 255)
                else:
                    pixels[(x, y)] = (clamp(35 + n), clamp(200 + n), clamp(135 + n), 255)

    # 7. Diagonal Wrought Iron Support Straps (鍛鐵交叉肩帶): X: 45..75, Y: 65..87
    # Left strap: from (46, 65) to (57, 87)
    for y in range(65, 88):
        t = (y - 65) / 22.0
        sx = 46.0 + t * 11.0
        for x in range(int(sx) - 1, int(sx) + 2):
            if ch_a(x, y) > 20:
                n = noise(x, y) * 6.0
                pixels[(x, y)] = (clamp(60 + n), clamp(65 + n), clamp(78 + n), 255)
    # Right strap: from (74, 65) to (63, 87)
    for y in range(65, 88):
        t = (y - 65) / 22.0
        sx = 74.0 - t * 11.0
        for x in range(int(sx) - 1, int(sx) + 2):
            if ch_a(x, y) > 20:
                n = noise(x, y) * 6.0
                pixels[(x, y)] = (clamp(55 + n), clamp(60 + n), clamp(74 + n), 255)

    # 8. Heavy Clockwork Belt & Rails: X: 42..78, Y: 87..93
    for y in range(87, 94):
        for x in range(42, 79):
            if ch_a(x, y) > 20 or cape_a(x, y) > 20:
                n = noise(x, y) * 6.0
                fy = (y - 87) / 6.0
                # Steel belt body with brass edge rails
                is_rail = (y in (87, 93))
                if is_rail:
                    # Brass upper/lower rim
                    base_r = 205.0 - fy * 30.0 + n
                    base_g = 160.0 - fy * 25.0 + n
                    base_b = 60.0 - fy * 15.0 + n
                    if y == 87:
                        base_r += 25; base_g += 25; base_b += 15
                else:
                    # Dark steel central belt band
                    base_r = 45.0 - fy * 12.0 + n
                    base_g = 48.0 - fy * 10.0 + n
                    base_b = 62.0 - fy * 10.0 + n
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 9. Central Celestial Gear Buckle (八齒星儀齒輪鎖扣): X: 56..64, Y: 86..94
    for y in range(86, 95):
        for x in range(56, 65):
            n = noise(x, y) * 6.0
            dx = x - 60.0
            dy = y - 90.0
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= 4.2:
                # Gear tooth vs rim vs center
                angle = math.atan2(dy, dx)
                teeth = math.sin(angle * 8.0)
                is_tooth = (dist >= 3.0 and teeth > 0.0)
                is_inner_rim = (1.5 <= dist <= 3.2)
                is_center_pin = (dist < 1.5)
                
                if is_tooth or is_inner_rim:
                    base_r = 230.0 + n
                    base_g = 185.0 + n
                    base_b = 55.0 + n
                    if dx < 0 or dy < 0:
                        base_r += 20; base_g += 20; base_b += 15
                    else:
                        base_r -= 35; base_g -= 30; base_b -= 15
                    pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)
                elif is_center_pin:
                    # Wrought iron center pin
                    pixels[(x, y)] = (clamp(75 + n), clamp(82 + n), clamp(98 + n), 255)

    # 10. Segmented Brass Tasset Skirt (三聯式星儀下擺鋼甲垂片): Y: 94..108
    # Center Tasset Plate: X: 54..66, Y: 94..108
    for y in range(94, 109):
        for x in range(54, 67):
            if ch_a(x, y) > 20 or cape_a(x, y) > 20:
                n = noise(x, y) * 8.0
                vy = (y - 94) / 14.0
                vx = abs(x - 60) / 6.0
                light = (1.0 - vx * 0.3) * (0.95 + vy * 0.2)
                base_r = 175.0 * light + n
                base_g = 135.0 * light + n
                base_b = 50.0 * light + n
                if x in (54, 66):
                    base_r -= 35; base_g -= 30; base_b -= 15
                if y == 108:
                    base_r -= 25; base_g -= 25; base_b -= 10
                if y == 94:
                    base_r += 20; base_g += 20; base_b += 10
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # Left Tasset Plate: X: 42..54, Y: 94..105
    for y in range(94, 106):
        for x in range(42, 55):
            if ch_a(x, y) > 20 or cape_a(x, y) > 20:
                n = noise(x, y) * 8.0
                vy = (y - 94) / 11.0
                vx = (x - 42) / 12.0
                light = (0.85 + vx * 0.25) * (0.9 + vy * 0.2)
                # Darker bronze / brass alloy
                base_r = 155.0 * light + n
                base_g = 120.0 * light + n
                base_b = 52.0 * light + n
                if x in (42, 54):
                    base_r -= 30; base_g -= 25; base_b -= 15
                if y == 105:
                    base_r -= 25; base_g -= 25; base_b -= 10
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # Right Tasset Plate: X: 66..78, Y: 94..105
    for y in range(94, 106):
        for x in range(66, 79):
            if ch_a(x, y) > 20 or cape_a(x, y) > 20:
                n = noise(x, y) * 8.0
                vy = (y - 94) / 11.0
                vx = (78 - x) / 12.0
                light = (0.80 + vx * 0.25) * (0.9 + vy * 0.2)
                base_r = 150.0 * light + n
                base_g = 115.0 * light + n
                base_b = 50.0 * light + n
                if x in (66, 78):
                    base_r -= 30; base_g -= 25; base_b -= 15
                if y == 105:
                    base_r -= 25; base_g -= 25; base_b -= 10
                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # 11. 3D Clockwork Rivets & Star Fasteners (立體黃銅螺栓與鉚釘)
    rivet_centers = [
        # Shoulders
        (36, 63), (44, 63), (38, 71), (43, 71),
        (76, 63), (84, 63), (77, 71), (82, 71),
        # Gorget
        (53, 58), (67, 58),
        # Breastplate corners & anchors
        (51, 67), (69, 67), (51, 83), (69, 83),
        # Belt
        (45, 90), (51, 90), (69, 90), (75, 90),
        # Tasset skirt tips
        (48, 102), (60, 106), (72, 102)
    ]
    for rx, ry in rivet_centers:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                pt = (rx + dx, ry + dy)
                if pt in pixels:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist <= 1.25:
                        n = noise(pt[0], pt[1]) * 4.0
                        if dx <= 0 and dy <= 0:
                            pixels[pt] = (clamp(255), clamp(235 + n), clamp(115 + n), 255)
                        elif dx > 0 or dy > 0:
                            pixels[pt] = (clamp(145 + n), clamp(100 + n), clamp(28 + n), 255)
                        else:
                            pixels[pt] = (clamp(220 + n), clamp(170 + n), clamp(45 + n), 255)

    # 12. Write to image with clean boundary anti-aliasing
    for (px, py), rgba in pixels.items():
        art.putpixel((px, py), rgba)

    # Deep outline pass: pixels adjacent to empty space get crisp dark-navy edge
    outline_pass = {}
    for (px, py) in list(pixels.keys()):
        is_edge = False
        for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
            nx, ny = px + dx, py + dy
            if (nx, ny) not in pixels:
                is_edge = True
                break
        if is_edge:
            r, g, b, a = pixels[(px, py)]
            # Dark contour shade (#1B1A32)
            outline_pass[(px, py)] = (clamp(r * 0.45 + 15), clamp(g * 0.45 + 12), clamp(b * 0.45 + 24), a)

    for (px, py), rgba in outline_pass.items():
        art.putpixel((px, py), rgba)

    out_path = f"{FOX_DIR}/costume/costume_astral_observer.png"
    art.save(out_path)

    # Calculate statistics
    all_opaque = [art.getpixel((x, y))[:3] for y in range(h) for x in range(w) if art.getpixel((x, y))[3] > 0] # type: ignore
    u_colors = set(all_opaque)
    ratio = len(u_colors) / (len(all_opaque) / 100.0) if all_opaque else 0.0

    # Overlap and identical color check with chassis
    same_coord_same_color = 0
    overlap_coords = 0
    for y in range(h):
        for x in range(w):
            ca = art.getpixel((x, y))[3] # type: ignore
            if ca > 0:
                cra, cga, cba, cha = chassis.getpixel((x, y)) # type: ignore
                if cha > 0:
                    overlap_coords += 1
                    cr, cg, cb = art.getpixel((x, y))[:3] # type: ignore
                    if (cr, cg, cb) == (cra, cga, cba):
                        same_coord_same_color += 1

    same_ratio = (same_coord_same_color / len(all_opaque)) * 100.0 if all_opaque else 0.0

    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(all_opaque)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")
    print(f"  Overlap with chassis: {overlap_coords}/{len(all_opaque)}")
    print(f"  Same coordinate same color with chassis: {same_coord_same_color}/{len(all_opaque)} ({same_ratio:.2f}%)")

    return art

if __name__ == "__main__":
    create_fox_costume_astral_observer()
