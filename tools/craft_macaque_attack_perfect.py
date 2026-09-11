import os
from PIL import Image, ImageDraw
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"

# Load the base attack pose
import subprocess
with open("/tmp/attack_base.png", "wb") as f:
    subprocess.run(["git", "show", "67101ed:game/assets/sprites/player/poses/macaque/attack.png"], stdout=f)

base = Image.open("/tmp/attack_base.png").convert("RGBA")

# Color palette:
C_OUTLINE = (35, 22, 18, 255)
C_OUTLINE_SOFT = (45, 30, 24, 200)

C_BRASS_HI = (255, 225, 80, 255)
C_BRASS_MID = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)
C_BRASS_DARK = (95, 60, 12, 255)

C_STEEL_SPEC = (255, 255, 250, 255)
C_STEEL_HI = (235, 238, 245, 255)
C_STEEL_MID = (195, 200, 215, 255)
C_STEEL_SHAD = (140, 145, 160, 255)

C_IVORY_HI = (252, 252, 248, 255)
C_IVORY_MID = (238, 238, 234, 255)
C_IVORY_SHAD = (212, 212, 208, 255)

atk = base.copy()
atk_px = atk.load()
assert atk_px is not None

# 1. Update body & limbs to ivory chassis
for y in range(atk.height):
    for x in range(atk.width):
        r, g, b, a = atk_px[x, y]
        if a > 80:
            # Check if this is body/limb/flesh/plate tone
            if r > 45 and g > 35 and b > 25 and r < 220 and (g - b) < 45 and (r - g) < 60:
                if 20 <= y <= 118:
                    bri = (r + g + b) / 3.0
                    if bri > 115:
                        atk_px[x, y] = C_IVORY_HI
                    elif bri > 80:
                        atk_px[x, y] = C_IVORY_MID
                    else:
                        atk_px[x, y] = C_IVORY_SHAD

# 2. Lower body & legs reinforcement with ivory/steel armor plates (y in 80..118, x in 25..95):
for y in range(80, 118):
    for x in range(25, 96):
        r, g, b, a = atk_px[x, y]
        if a > 60:
            if not (r < 45 and g < 35 and b < 30):
                if (x + y) % 2 == 0:
                    atk_px[x, y] = C_STEEL_SPEC
                else:
                    atk_px[x, y] = C_STEEL_HI

# 3. Build prominent mechanical claw gauntlets (ZERO STAFF / NO ROD)
wep = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw = ImageDraw.Draw(wep)
wep_px = wep.load()
assert wep_px is not None

# A. Forward Punching Gauntlet & Triple Steel Claws (Lead arm)
# Gauntlet bracket mounted on forward fist (x=82..97, y=50..70)
draw.rectangle([82, 50, 97, 69], fill=C_BRASS_MID, outline=C_OUTLINE)
draw.line([83, 51, 96, 51], fill=C_BRASS_HI)
draw.line([83, 68, 96, 68], fill=C_BRASS_SHAD)
# Spring chamber
draw.rectangle([86, 55, 93, 64], fill=C_STEEL_MID, outline=C_OUTLINE)
draw.line([89, 56, 89, 63], fill=C_STEEL_SPEC)
# Mounting claw sockets
draw.rectangle([96, 49, 100, 54], fill=C_BRASS_HI, outline=C_OUTLINE)
draw.rectangle([96, 57, 101, 62], fill=C_BRASS_HI, outline=C_OUTLINE)
draw.rectangle([96, 65, 100, 70], fill=C_BRASS_HI, outline=C_OUTLINE)

# THREE SOLID, GLEAMING STEEL CLAW BLADES:
# Upper Claw (x=98..124, y=48..55)
for x in range(98, 123):
    tip_decay = max(0, x - 115)
    y_top = 50 - (1 if x > 108 else 0)
    y_bot = 54 - tip_decay
    for y in range(y_top, y_bot + 1):
        if y == y_top or y == y_bot:
            wep_px[x, y] = C_OUTLINE
        elif y == y_top + 1:
            wep_px[x, y] = C_STEEL_SPEC
        elif y == y_top + 2:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
wep_px[123, 49] = C_STEEL_SPEC
wep_px[123, 50] = C_OUTLINE
wep_px[124, 49] = C_STEEL_SPEC

# Middle Claw (Main thrust blade, x=98..126, y=57..64)
for x in range(98, 125):
    tip_decay = max(0, x - 117)
    y_top = 58
    y_bot = 62 - tip_decay
    for y in range(y_top, y_bot + 1):
        if y == y_top or y == y_bot:
            wep_px[x, y] = C_OUTLINE
        elif y == y_top + 1:
            wep_px[x, y] = C_STEEL_SPEC
        elif y == y_top + 2:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
wep_px[125, 58] = C_STEEL_SPEC
wep_px[125, 59] = C_OUTLINE
wep_px[126, 58] = C_STEEL_SPEC

# Lower Claw (x=98..124, y=66..73)
for x in range(98, 123):
    tip_decay = max(0, x - 115)
    y_top = 66 + (1 if x > 108 else 0)
    y_bot = 70 - tip_decay
    for y in range(y_top, y_bot + 1):
        if y == y_top or y == y_bot:
            wep_px[x, y] = C_OUTLINE
        elif y == y_top + 1:
            wep_px[x, y] = C_STEEL_SPEC
        elif y == y_top + 2:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
wep_px[123, 67] = C_STEEL_SPEC
wep_px[123, 68] = C_OUTLINE
wep_px[124, 67] = C_STEEL_SPEC

# B. Rear hand gauntlet at hip/waist & downward pointing triple steel claws (x=24..48, y=68..112):
draw.rectangle([26, 68, 44, 80], fill=C_BRASS_MID, outline=C_OUTLINE)
draw.line([27, 69, 43, 69], fill=C_BRASS_HI)
draw.line([27, 79, 43, 79], fill=C_BRASS_SHAD)
# Rear spring chamber
draw.rectangle([30, 71, 40, 77], fill=C_STEEL_MID, outline=C_OUTLINE)
draw.line([35, 72, 35, 76], fill=C_STEEL_SPEC)

# Three solid downward claw blades (matching composite wpn_spring_claws exactly):
# Blade 1 (x=27..32, y=81..104)
for y in range(81, 104):
    for x in range(27, 33):
        if x == 27 or x == 32:
            wep_px[x, y] = C_OUTLINE
        elif x == 28:
            wep_px[x, y] = C_STEEL_SPEC
        elif x == 29:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
wep_px[28, 104] = C_STEEL_SPEC
wep_px[29, 104] = C_OUTLINE
wep_px[28, 105] = C_STEEL_SPEC

# Blade 2 (x=34..39, y=81..108 - central long blade)
for y in range(81, 108):
    for x in range(34, 40):
        if x == 34 or x == 39:
            wep_px[x, y] = C_OUTLINE
        elif x == 35:
            wep_px[x, y] = C_STEEL_SPEC
        elif x == 36:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
wep_px[35, 108] = C_STEEL_SPEC
wep_px[36, 108] = C_OUTLINE
wep_px[35, 109] = C_STEEL_SPEC

# Blade 3 (x=41..46, y=81..104)
for y in range(81, 104):
    for x in range(41, 47):
        if x == 41 or x == 46:
            wep_px[x, y] = C_OUTLINE
        elif x == 42:
            wep_px[x, y] = C_STEEL_SPEC
        elif x == 43:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
wep_px[42, 104] = C_STEEL_SPEC
wep_px[43, 104] = C_OUTLINE
wep_px[42, 105] = C_STEEL_SPEC

# Composite weapon onto attack
atk.alpha_composite(wep)

# Save to target path
target_path = f"{REPO_ROOT}/game/assets/sprites/player/poses/macaque/attack.png"
atk.save(target_path)
print(f"Successfully crafted and saved: {target_path}")
