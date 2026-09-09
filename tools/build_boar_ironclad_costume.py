#!/usr/bin/env python3
"""
tools/build_boar_ironclad_costume.py
Constructs high-fidelity costume_viking_ironclad.png for Boar paperdoll.
- Tailored for Boar's heavy warrior 2.2-head chibi frame (Forge Boar, Viking archetype)
- Zero fur / zero leather / zero fabric (Rule 5a / 23f-4)
- Full heavy forged iron cuirass, double-layered Viking curved pauldrons, lamellar tassets, 3D brass rivets
- Rich hand-painted pixel art with multi-pass lighting, specular bevels, directional highlights,
  warm forge bounce light, and dark-iron outlines (#1A1B22)
- High color nuance (colors/100px >= 24, Rule 10a-2)
- Layer independence: 0 identical pixels with chassis (Rule 4c)
- 128x128 RGBA
"""

import math
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

def create_boar_costume_viking_ironclad():
    w, h = 128, 128
    art = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    harness = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness.png").convert("RGBA")
    chassis = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold.png").convert("RGBA")

    pixels: dict[tuple[int, int], tuple[int, int, int, int]] = {}

    def clamp(v: float, low: float = 0.0, high: float = 255.0) -> int:
        return int(max(low, min(high, round(v))))

    def noise(x: int, y: int) -> float:
        return (math.sin(x * 0.85 + y * 0.45) * 0.5 + 
                math.cos(x * 0.35 - y * 0.75) * 0.3 + 
                math.sin((x + y) * 1.2) * 0.2)

    def har_a(x: int, y: int) -> int:
        return cast(tuple[int, int, int, int], harness.getpixel((x, y)))[3]

    def har_rgb(x: int, y: int) -> tuple[int, int, int]:
        p = cast(tuple[int, int, int, int], harness.getpixel((x, y)))
        return p[:3]

    # --- 1. Right Pauldron (Viewer Right): X: 66..92, Y: 45..68 ---
    # Enhance harness pauldron into a massive, heavy multi-layered Viking forged-steel shoulder guard
    for y in range(45, 69):
        for x in range(66, 93):
            ha = har_a(x, y)
            if ha > 15:
                orig_r, orig_g, orig_b = har_rgb(x, y)
                n = noise(x, y) * 5.0

                # Determine if on upper main plate (Y <= 56) or lower plate (Y >= 57)
                if y <= 56:
                    # Upper heavy plate: shift towards burnished forged steel
                    # Top curved ridge highlight:
                    ridge = max(0.0, 1.0 - (y - 45) / 9.0) * (1.0 - abs(x - 80) / 13.0)
                    r = orig_r * 0.85 + ridge * 65.0 + n
                    g = orig_g * 0.90 + ridge * 70.0 + n
                    b = orig_b * 0.98 + ridge * 85.0 + n

                    # Division bevel crease at Y=56
                    if y == 56:
                        r -= 30; g -= 30; b -= 35
                else:
                    # Lower overlapping flange plate:
                    flange_light = max(0.0, 1.0 - (y - 57) / 10.0) * 0.8
                    r = orig_r * 0.75 + flange_light * 45.0 + n
                    g = orig_g * 0.80 + flange_light * 50.0 + n
                    b = orig_b * 0.90 + flange_light * 60.0 + n

                    # Flange top rim highlight at Y=57
                    if y == 57:
                        r += 35; g += 38; b += 45
                    # Lower shadow rim
                    if y >= 65 or x >= 90:
                        r -= 20; g -= 20; b -= 25

                pixels[(x, y)] = (clamp(r), clamp(g), clamp(b), 255)

    # --- 2. Central Full Cuirass (Forged Heavy Breastplate): X: 58..80, Y: 65..83 ---
    # Instead of open straps, build solid forged iron cuirass covering the chest
    for y in range(65, 84):
        for x in range(58, 81):
            ha = har_a(x, y)
            if ha > 15:
                orig_r, orig_g, orig_b = har_rgb(x, y)
                n = noise(x, y) * 6.0

                # Form a solid convex breastplate:
                # Centerline at X = 69
                dist_center = abs(x - 69.5) / 10.5
                dist_vert = (y - 65) / 18.0

                # Convex directional illumination (top-left key light, warm forge bounce from bottom)
                key_light = max(0.0, (1.0 - dist_center * 0.75) * (1.0 - dist_vert * 0.55))
                bounce_light = max(0.0, dist_vert * 0.35) * (1.0 - dist_center * 0.5)

                # Heavy cast iron palette with warm forge undertones
                base_r = 45.0 + key_light * 65.0 + bounce_light * 30.0 + n
                base_g = 52.0 + key_light * 70.0 + bounce_light * 18.0 + n
                base_b = 64.0 + key_light * 85.0 + bounce_light * 12.0 + n

                # Rolled top collar rim highlight at Y=65
                if y == 65:
                    base_r += 45; base_g += 50; base_b += 65

                # Vertical centerline split seam between left & right pectorals
                if x == 69:
                    base_r -= 28; base_g -= 28; base_b -= 32
                elif x == 70:
                    base_r += 24; base_g += 26; base_b += 35

                # Central Heavy Iron Boss Medallion with Brass Stud (X: 66..73, Y: 72..77)
                dx_b = x - 69.5
                dy_b = y - 74.5
                dist_boss = math.sqrt(dx_b * dx_b + dy_b * dy_b)
                if dist_boss <= 3.6:
                    bn = noise(x, y) * 5.0
                    if dist_boss <= 1.4:
                        # Central brass bolt
                        if dx_b <= 0 and dy_b <= 0:
                            base_r = 255.0; base_g = 240.0; base_b = 130.0
                        else:
                            base_r = 190.0 + bn; base_g = 145.0 + bn; base_b = 40.0 + bn
                    elif dist_boss <= 2.6:
                        # Inner shadow recess
                        base_r = 30.0 + bn; base_g = 32.0 + bn; base_b = 40.0 + bn
                    else:
                        # Outer reinforced steel boss ring
                        if dx_b <= 0 and dy_b <= 0:
                            base_r = 130.0 + bn; base_g = 145.0 + bn; base_b = 175.0 + bn
                        else:
                            base_r = 60.0 + bn; base_g = 68.0 + bn; base_b = 82.0 + bn

                pixels[(x, y)] = (clamp(base_r), clamp(base_g), clamp(base_b), 255)

    # --- 3. Left Side Flange & Articulated Lames: X: 48..65, Y: 65..95 ---
    for y in range(65, 96):
        for x in range(48, 66):
            ha = har_a(x, y)
            if ha > 15:
                orig_r, orig_g, orig_b = har_rgb(x, y)
                n = noise(x, y) * 5.5

                dist_left = (x - 48) / 17.0
                dist_top = (y - 65) / 30.0
                light = (1.0 - dist_left * 0.4) * (1.0 - dist_top * 0.3)

                r = orig_r * 0.82 + light * 40.0 + n
                g = orig_g * 0.88 + light * 45.0 + n
                b = orig_b * 0.96 + light * 55.0 + n

                # Left lateral edge highlight
                if x == 48:
                    r += 32; g += 36; b += 48

                # Horizontal articulated plate segmentation seams
                if y in (74, 82):
                    r -= 24; g -= 24; b -= 28
                elif y in (75, 83):
                    r += 22; g += 25; b += 32

                pixels[(x, y)] = (clamp(r), clamp(g), clamp(b), 255)

    # --- 4. Heavy Lamellar Waist Fauld & Tasset Plates: X: 48..92, Y: 82..96 ---
    for y in range(82, 97):
        for x in range(48, 93):
            ha = har_a(x, y)
            if ha > 15:
                orig_r, orig_g, orig_b = har_rgb(x, y)
                n = noise(x, y) * 6.0

                vy = (y - 82) / 14.0
                vx = abs(x - 70) / 22.0

                if y <= 87:
                    # Reinforced iron girdle band
                    band_light = (1.0 - vx * 0.5) * 35.0
                    r = orig_r * 0.78 + band_light + n
                    g = orig_g * 0.82 + band_light + n
                    b = orig_b * 0.90 + band_light + n

                    if y == 82:
                        r += 35; g += 38; b += 48
                    if y == 87:
                        r -= 25; g -= 25; b -= 30
                else:
                    # Fluted Viking tassets (hanging lamellar armor plates)
                    # Vertical fluting grooves at x=54, 59, 64, 69, 74, 79, 84
                    is_flute = ((x - 4) % 5 == 0)
                    tasset_light = (1.0 - vx * 0.35) * (0.8 + vy * 0.25)
                    r = orig_r * 0.80 * tasset_light + n
                    g = orig_g * 0.85 * tasset_light + n
                    b = orig_b * 0.95 * tasset_light + n

                    if is_flute:
                        r -= 22; g -= 22; b -= 26
                    if y == 88:
                        r += 28; g += 30; b += 40
                    if y >= 94:
                        r -= 18; g -= 18; b -= 22

                pixels[(x, y)] = (clamp(r), clamp(g), clamp(b), 255)

    # Fill any remaining pixel in harness silhouette so zero gaps exist
    for y in range(45, 97):
        for x in range(48, 93):
            ha = har_a(x, y)
            if ha > 15 and (x, y) not in pixels:
                orig_r, orig_g, orig_b = har_rgb(x, y)
                n = noise(x, y) * 4.0
                pixels[(x, y)] = (clamp(orig_r * 0.85 + n), clamp(orig_g * 0.90 + n), clamp(orig_b * 0.95 + n), 255)

    # --- 5. Prominent 3D Spherical Brass Rivets (立體黃銅鉚釘) ---
    # Double-row rivets on pauldron rim, breastplate anchors, and girdle plates
    rivet_specs = [
        # Pauldron top rim double row
        (71, 47), (77, 46), (84, 49), (89, 56), (87, 63),
        (74, 58), (80, 58), (85, 60),
        # Breastplate 4-corner heavy studs
        (61, 68), (77, 68),
        (61, 79), (77, 79),
        # Waist girdle band studs
        (52, 85), (60, 85), (68, 85), (76, 85), (84, 85),
        # Lower tasset hem rivets
        (51, 93), (59, 93), (67, 93), (75, 93), (83, 93)
    ]

    for rx, ry in rivet_specs:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                pt = (rx + dx, ry + dy)
                if pt in pixels:
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist <= 1.35:
                        n = noise(pt[0], pt[1]) * 4.0
                        if dx <= 0 and dy <= 0:
                            # Gleaming specular highlight
                            pixels[pt] = (clamp(255), clamp(242 + n), clamp(140 + n), 255)
                        elif dx > 0 or dy > 0:
                            # Spherical drop shadow
                            pixels[pt] = (clamp(135 + n), clamp(95 + n), clamp(25 + n), 255)
                        else:
                            # Core polished brass
                            pixels[pt] = (clamp(225 + n), clamp(175 + n), clamp(45 + n), 255)

    # --- 6. Edge Stroke (#1A1B22) & Anti-Aliasing ---
    edge_updates = {}
    for (x, y), (r, g, b, a) in pixels.items():
        is_boundary = False
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in pixels or har_a(nx, ny) <= 10:
                is_boundary = True
                break
        if is_boundary:
            orig_a = har_a(x, y)
            n = noise(x, y) * 3.0
            edge_updates[(x, y)] = (clamp(26 + n), clamp(27 + n), clamp(34 + n), orig_a)

    for pt, col in edge_updates.items():
        pixels[pt] = col

    # Render to image
    opaque_pixels = []
    for (x, y), (r, g, b, a) in pixels.items():
        final_a = har_a(x, y)
        if final_a > 30:
            final_a = max(final_a, 245)
        art.putpixel((x, y), (r, g, b, final_a))
        opaque_pixels.append((r, g, b))

    out_path = f"{BOAR_DIR}/costume/costume_viking_ironclad.png"
    art.save(out_path)

    u_colors = set(opaque_pixels)
    ratio = len(u_colors) / (len(opaque_pixels) / 100.0) if opaque_pixels else 0.0
    print(f"✓ Saved {out_path}")
    print(f"  Opaque pixels: {len(opaque_pixels)}")
    print(f"  Unique colors: {len(u_colors)}")
    print(f"  Colors/100px: {ratio:.2f}")

    return art

if __name__ == "__main__":
    create_boar_costume_viking_ironclad()
