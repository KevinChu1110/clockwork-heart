import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

w, h = 128, 128
blade_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

# Palette constants
OUTLINE = (44, 28, 22, 255)         # #2C1C16
OUTLINE_TRANS = (44, 28, 22, 180)

# Golden brass (matching rabbit key and buttons)
GOLD_HI  = (255, 245, 175, 255)
GOLD_L1  = (255, 215, 60, 255)
GOLD_M   = (215, 160, 25, 255)
GOLD_D   = (145, 95, 15, 255)
GOLD_DK  = (85, 52, 10, 255)

# Polished steel blade (chibi stylized RPG steel)
STEEL_SPEC = (255, 255, 255, 255)
STEEL_HI   = (230, 242, 250, 255)
STEEL_M    = (195, 215, 230, 255)
STEEL_RIDGE= (75, 95, 115, 255)
STEEL_SHAD = (100, 125, 145, 255)
STEEL_DEEP = (60, 80, 100, 255)
STEEL_DARK = (42, 58, 75, 255)

# Grip (dark oxblood / worn leather wrap with gold wire)
GRIP_WRAP_L = (135, 75, 45, 255)
GRIP_WRAP_D = (75, 38, 22, 255)
GRIP_WIRE   = (240, 195, 50, 255)

# Rabbit hand/fingers (matching ivory chassis tone with clear definition)
PAW_HI   = (252, 248, 240, 255)
PAW_M    = (228, 216, 200, 255)
PAW_SHAD = (185, 168, 148, 255)
PAW_DARK = (135, 118, 100, 255)

# 1. Contact Shadow Layer (cast onto the body)
shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow_layer)

# Cast shadow follows the blade from crossguard (46, 86) to (86, 124)
# offset by (+2, +2)
for t in range(0, 42):
    frac = t / 41.0
    bx = 46.0 + frac * 40.0
    by = 86.0 + frac * 38.0
    # Width of shadow under blade: 3 pixels wide
    for dx in [1, 2, 3]:
        for dy in [1, 2, 3]:
            px = int(bx + dx)
            py = int(by + dy)
            if 0 <= px < w and 0 <= py < h:
                # Alpha between 70 and 120 (strongest near body center x=55..75)
                dist_factor = 1.0 - 0.5 * abs(frac - 0.4)
                a = int(dist_factor * 115)
                cur = shadow_layer.getpixel((px, py))[3]
                if a > cur:
                    shadow_layer.putpixel((px, py), (18, 12, 25, a))

# Also shadow under the crossguard
for cx in range(41, 48):
    for cy in range(85, 89):
        shadow_layer.putpixel((cx + 1, cy + 2), (18, 12, 25, 120))

# Soften shadow slightly
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(0.5))

# 2. Sword Structure Layer
sword_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pix = sword_layer.load()

# --- POMMEL: Spherical brass ball at (35, 75) ---
# Radius ~ 3px
pommel = {
    (35, 73): OUTLINE, (36, 73): OUTLINE,
    (34, 74): OUTLINE, (35, 74): GOLD_HI, (36, 74): GOLD_L1, (37, 74): OUTLINE,
    (33, 75): OUTLINE, (34, 75): GOLD_HI, (35, 75): GOLD_L1, (36, 75): GOLD_M,  (37, 75): OUTLINE,
    (33, 76): OUTLINE, (34, 76): GOLD_L1, (35, 76): GOLD_M,  (36, 76): GOLD_D,  (37, 76): OUTLINE,
    (34, 77): OUTLINE, (35, 77): GOLD_D,  (36, 77): GOLD_DK, (37, 77): OUTLINE,
    (35, 78): OUTLINE, (36, 78): OUTLINE,
}
for pos, col in pommel.items():
    pix[pos] = col

# --- GRIP: Cylindrical leather/brass wrap from pommel to crossguard ---
# y: 77..82, x: 37..42
grip = {
    (37, 77): OUTLINE, (38, 77): GRIP_WIRE,   (39, 77): GRIP_WRAP_D, (40, 77): OUTLINE,
    (37, 78): OUTLINE, (38, 78): GRIP_WRAP_L, (39, 78): GRIP_WRAP_D, (40, 78): OUTLINE,
    (38, 79): OUTLINE, (39, 79): GRIP_WIRE,   (40, 79): GRIP_WRAP_D, (41, 79): OUTLINE,
    (38, 80): OUTLINE, (39, 80): GRIP_WRAP_L, (40, 80): GRIP_WRAP_D, (41, 80): OUTLINE,
    (39, 81): OUTLINE, (40, 81): GRIP_WIRE,   (41, 81): GRIP_WRAP_D, (42, 81): OUTLINE,
    (39, 82): OUTLINE, (40, 82): GRIP_WRAP_L, (41, 82): GRIP_WRAP_D, (42, 82): OUTLINE,
}
for pos, col in grip.items():
    pix[pos] = col

# --- CROSSGUARD: Polished brass crossbar (y: 81..86, x: 41..48) ---
crossguard = {
    # Upper quill / finial
    (46, 79): OUTLINE,
    (45, 80): OUTLINE, (46, 80): GOLD_HI, (47, 80): OUTLINE,
    (44, 81): OUTLINE, (45, 81): GOLD_L1, (46, 81): GOLD_M,  (47, 81): OUTLINE,
    # Main bar
    (43, 82): OUTLINE, (44, 82): GOLD_HI, (45, 82): GOLD_L1, (46, 82): GOLD_D,  (47, 82): OUTLINE,
    (42, 83): OUTLINE, (43, 83): GOLD_HI, (44, 83): GOLD_L1, (45, 83): GOLD_M,  (46, 83): GOLD_D,  (47, 83): OUTLINE,
    (41, 84): OUTLINE, (42, 84): GOLD_L1, (43, 84): GOLD_M,  (44, 84): GOLD_M,  (45, 84): GOLD_D,  (46, 84): OUTLINE,
    (40, 85): OUTLINE, (41, 85): GOLD_M,  (42, 85): GOLD_D,  (43, 85): GOLD_DK, (44, 85): OUTLINE,
    # Lower quill / finial
    (39, 86): OUTLINE, (40, 86): GOLD_D,  (41, 86): OUTLINE,
    (39, 87): OUTLINE,
}
for pos, col in crossguard.items():
    pix[pos] = col

# --- BLADE: Double-edged steel blade with central ridge, gleaming highlight, and depth ---
# Start from crossguard center (x=46, y=84) down to (x=88, y=124)
# Blade length: ~58 px, width ~ 4-5 px tapering to acute tip
for step in range(0, 42):
    t = step / 41.0
    # Axis coordinate
    ax = 46.0 + t * 41.5
    ay = 84.5 + t * 39.5
    
    ix = int(round(ax))
    iy = int(round(ay))
    
    if step >= 39:
        # Acute tip
        if step == 41:
            pix[ix, iy] = OUTLINE
            pix[ix - 1, iy] = STEEL_SPEC
        elif step == 40:
            pix[ix - 1, iy] = STEEL_SPEC
            pix[ix, iy] = STEEL_HI
            pix[ix + 1, iy] = OUTLINE
            pix[ix, iy - 1] = STEEL_HI
            pix[ix - 1, iy - 1] = OUTLINE
            pix[ix, iy + 1] = OUTLINE
        else:
            pix[ix - 2, iy - 1] = OUTLINE
            pix[ix - 1, iy - 1] = STEEL_SPEC
            pix[ix, iy - 1] = STEEL_HI
            pix[ix - 1, iy] = STEEL_M
            pix[ix, iy] = STEEL_SHAD
            pix[ix + 1, iy] = OUTLINE
            pix[ix, iy + 1] = OUTLINE
    else:
        # Full blade body
        # Upper edge outline
        pix[ix - 2, iy - 1] = OUTLINE
        pix[ix - 1, iy - 2] = OUTLINE
        
        # Upper facet (specular & light facet)
        pix[ix - 1, iy - 1] = STEEL_SPEC if (step % 4 in [0, 1]) else STEEL_HI
        pix[ix, iy - 1] = STEEL_HI
        
        # Central spine / ridge
        pix[ix - 1, iy] = STEEL_M
        pix[ix, iy] = STEEL_RIDGE
        
        # Lower facet (shadow facet)
        pix[ix + 1, iy] = STEEL_SHAD
        pix[ix, iy + 1] = STEEL_DEEP
        
        # Lower edge outline
        pix[ix + 1, iy + 1] = OUTLINE
        pix[ix + 2, iy] = OUTLINE
        pix[ix, iy + 2] = OUTLINE

# --- HAND FINGERS GRIPPING THE HILT ---
# The rabbit's paw/gauntlet wraps AROUND the grip!
# Hand is located at (x: 37..44, y: 77..83).
# We render the curling fingers, knuckles, and thumb wrapped OVER the front of the hilt.
# This physically clamps the hilt between the palm and fingers!
fingers = {
    # Thumb pressing on top-left of grip
    (37, 76): OUTLINE, (38, 76): PAW_HI,   (39, 76): PAW_M,    (40, 76): OUTLINE,
    (36, 77): OUTLINE, (37, 77): PAW_HI,   (38, 77): PAW_M,    (39, 77): PAW_SHAD, (40, 77): OUTLINE,
    # Index finger wrapping over hilt at y=78..79
    (38, 78): OUTLINE, (39, 78): PAW_HI,   (40, 78): PAW_M,    (41, 78): PAW_SHAD, (42, 78): OUTLINE,
    (38, 79): OUTLINE, (39, 79): PAW_M,    (40, 79): PAW_SHAD, (41, 79): OUTLINE,
    # Middle finger wrapping over hilt at y=80..81
    (39, 80): OUTLINE, (40, 80): PAW_HI,   (41, 80): PAW_M,    (42, 80): PAW_SHAD, (43, 80): OUTLINE,
    (39, 81): OUTLINE, (40, 81): PAW_M,    (41, 81): PAW_SHAD, (42, 81): OUTLINE,
    # Ring finger / pinky wrapping near crossguard at y=82..83
    (40, 82): OUTLINE, (41, 82): PAW_HI,   (42, 82): PAW_M,    (43, 82): PAW_SHAD, (44, 82): OUTLINE,
    (40, 83): OUTLINE, (41, 83): PAW_SHAD, (42, 83): OUTLINE,
    # Knuckle segment lines (chibi mechanical toy joint details)
    (39, 77): (200, 185, 165, 255),
    (40, 79): (200, 185, 165, 255),
    (41, 81): (200, 185, 165, 255),
}
for pos, col in fingers.items():
    pix[pos] = col

# Combine shadow and sword into final weapon
final_weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
final_weapon.alpha_composite(shadow_layer)
final_weapon.alpha_composite(sword_layer)
final_weapon.save("/tmp/refined_dawn_blade.png")
print("Refined weapon created, bbox:", final_weapon.getbbox())

# Composite with rabbit costume, chassis (midnight navy and ivory), head, etc.
for chassis_name in ["paint_midnight_navy.png", "paint_ivory_stock.png"]:
    comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    comp.alpha_composite(Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/chassis/{chassis_name}").convert("RGBA"))
    comp.alpha_composite(Image.open("/tmp/ear_wrapped.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA"))
    comp.alpha_composite(final_weapon)
    
    tag = "navy" if "navy" in chassis_name else "ivory"
    comp.save(f"/tmp/full_comp_{tag}.png")
    
    dark = Image.new("RGBA", (w, h), (7, 6, 10, 255))
    dark.alpha_composite(comp)
    dark.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save(f"/tmp/full_comp_{tag}_4x.png")
    
    crop = dark.crop((28, 65, 96, 126)).resize((340, 305), getattr(Image, 'Resampling', Image).NEAREST)
    crop.save(f"/tmp/crop_weapon_{tag}.png")

print("Saved full comps and weapon crops for vision inspection!")
