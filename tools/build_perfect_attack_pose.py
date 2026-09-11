import os
from PIL import Image, ImageDraw
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"

# Load the base attack pose (kinematic lunge)
# In git history 67101ed, we have the clean base lunge silhouette
import subprocess
with open("/tmp/attack_base.png", "wb") as f:
    subprocess.run(["git", "show", "67101ed:game/assets/sprites/player/poses/macaque/attack.png"], stdout=f)

base = Image.open("/tmp/attack_base.png").convert("RGBA")
comp = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")

# Let's inspect base colors
# base has the lunge silhouette:
# head at x: 45..85, y: 15..55
# torso at x: 50..80, y: 45..75
# lead arm punching at x: 75..100, y: 48..68
# rear arm at x: 30..45, y: 55..75
# legs at x: 40..85, y: 75..108

# Color Palette:
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

# Ivory chassis colors:
C_IVORY_HI = (250, 250, 245, 255)
C_IVORY_MID = (235, 235, 230, 255)
C_IVORY_SHAD = (210, 210, 205, 255)

# Emerald core:
C_CORE_HI = (120, 255, 180, 255)
C_CORE_MID = (30, 190, 120, 255)

atk = base.copy()
atk_px = atk.load()
assert atk_px is not None

# 1. Update the body/limbs to match the ivory chassis paint_ivory_stock!
# Any brown body pixels (not outline, not brass armor, not tail) should be ivory white!
for y in range(atk.height):
    for x in range(atk.width):
        r, g, b, a = atk_px[x, y]
        if a > 100:
            # Check if this is brown body/flesh tone (e.g. r in 90..180, g in 70..140, b in 50..100)
            # but NOT dark outline (r<50, g<40, b<35) and NOT green gem (g > r + 30)
            if r > 65 and g > 55 and b > 40 and r < 200 and (g - b) < 45 and (r - g) < 55:
                # Is it torso/belly or arm/leg?
                if 25 <= y <= 105:
                    # Map to ivory tone with proper shading
                    bri = (r + g + b) / 3.0
                    if bri > 125:
                        atk_px[x, y] = C_IVORY_HI
                    elif bri > 95:
                        atk_px[x, y] = C_IVORY_MID
                    else:
                        atk_px[x, y] = C_IVORY_SHAD

# 2. Build the prominent 3-blade steel mechanical claw gauntlets
wep = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw = ImageDraw.Draw(wep)
wep_px = wep.load()
assert wep_px is not None

# A. Lead (punching) arm gauntlet & claw blades:
# Fist is at x=82..98, y=50..68
# Gauntlet base (heavy brass frame mounted over fist)
draw.rectangle([82, 50, 97, 68], fill=C_BRASS_MID, outline=C_OUTLINE)
draw.line([83, 51, 96, 51], fill=C_BRASS_HI)
draw.line([83, 67, 96, 67], fill=C_BRASS_SHAD)
# Center clockwork spring housing
draw.rectangle([86, 55, 93, 63], fill=C_STEEL_MID, outline=C_OUTLINE)
draw.line([89, 56, 89, 62], fill=C_STEEL_SPEC)
# Three brass sockets at the front of gauntlet
draw.rectangle([96, 50, 100, 55], fill=C_BRASS_HI, outline=C_OUTLINE)
draw.rectangle([96, 56, 101, 62], fill=C_BRASS_HI, outline=C_OUTLINE)
draw.rectangle([96, 63, 100, 68], fill=C_BRASS_HI, outline=C_OUTLINE)

# THREE SOLID STEEL CLAW BLADES (Large, thick, gleaming, razor-sharp):
# Blade 1: Upper Claw (x=99..123, y=49..55)
for x in range(99, 122):
    # solid blade body (4-5px thick tapering to tip)
    tip_decay = max(0, (x - 114))
    y_top = 51 - (1 if x > 108 else 0)
    y_bot = 55 - tip_decay
    for y in range(y_top, y_bot + 1):
        if y == y_top or y == y_bot:
            wep_px[x, y] = C_OUTLINE
        elif y == y_top + 1:
            wep_px[x, y] = C_STEEL_SPEC
        elif y == y_top + 2:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
# Razor tip
wep_px[122, 50] = C_STEEL_SPEC
wep_px[122, 51] = C_OUTLINE
wep_px[123, 50] = C_STEEL_SPEC

# Blade 2: Middle Claw (Center thrust, longest, x=99..125, y=57..63)
for x in range(99, 124):
    tip_decay = max(0, (x - 116))
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
# Razor tip
wep_px[124, 58] = C_STEEL_SPEC
wep_px[124, 59] = C_OUTLINE
wep_px[125, 58] = C_STEEL_SPEC

# Blade 3: Lower Claw (x=99..122, y=64..70)
for x in range(99, 122):
    tip_decay = max(0, (x - 114))
    y_top = 65 + (1 if x > 108 else 0)
    y_bot = 69 - tip_decay
    for y in range(y_top, y_bot + 1):
        if y == y_top or y == y_bot:
            wep_px[x, y] = C_OUTLINE
        elif y == y_top + 1:
            wep_px[x, y] = C_STEEL_SPEC
        elif y == y_top + 2:
            wep_px[x, y] = C_STEEL_HI
        else:
            wep_px[x, y] = C_STEEL_MID
# Razor tip
wep_px[122, 66] = C_STEEL_SPEC
wep_px[122, 67] = C_OUTLINE
wep_px[123, 66] = C_STEEL_SPEC

# B. Rear hand gauntlet at hip/waist (x=30..44, y=62..78):
draw.rectangle([32, 62, 43, 72], fill=C_BRASS_MID, outline=C_OUTLINE)
draw.line([33, 63, 42, 63], fill=C_BRASS_HI)
draw.line([33, 71, 42, 71], fill=C_BRASS_SHAD)
# Rear claws extending downward and back
for x in range(22, 33):
    wep_px[x, 64] = C_OUTLINE
    wep_px[x, 65] = C_STEEL_SPEC
    wep_px[x, 66] = C_STEEL_HI
    wep_px[x, 67] = C_OUTLINE

    wep_px[x, 70] = C_OUTLINE
    wep_px[x, 71] = C_STEEL_SPEC
    wep_px[x, 72] = C_STEEL_HI
    wep_px[x, 73] = C_OUTLINE

# Composite weapon onto attack pose
atk.alpha_composite(wep)

# Save test result
out_test = "/tmp/test_new_attack.png"
atk.save(out_test)
print(f"Saved {out_test}, bbox: {atk.getbbox()}")

# Measure steel pixels in atk:
arr_atk = np.array(atk)
steel_atk = (arr_atk[:, :, 3] > 128) & (arr_atk[:, :, 0] > 185) & (arr_atk[:, :, 1] > 185) & (arr_atk[:, :, 2] > 185) & (np.abs(arr_atk[:, :, 0].astype(int) - arr_atk[:, :, 2].astype(int)) < 40)
print("Total steel pixels in new attack.png:", np.count_nonzero(steel_atk))
print("Steel pixels in lower region y >= 96:", np.count_nonzero(steel_atk[96:, :]))
