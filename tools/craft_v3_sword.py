import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

w, h = 128, 128

# Colors
C_OUTLINE    = (35, 22, 18, 255)       # #231612 deep warm contour
C_OUTLINE_SOFT = (55, 38, 30, 200)

# Golden brass (3D volumetric brass palette)
C_BRASS_SPEC = (255, 255, 220, 255)   # Specular spark
C_BRASS_HI   = (255, 225, 90, 255)    # High gloss
C_BRASS_MID  = (220, 168, 35, 255)    # Base gold
C_BRASS_SHAD = (150, 105, 20, 255)    # Shadow
C_BRASS_DEEP = (95, 62, 12, 255)      # Deep shadow

# Polished steel (3D volumetric steel blade)
C_STEEL_SPEC = (255, 255, 255, 255)   # Edge highlight glint
C_STEEL_HI   = (232, 244, 252, 255)   # Light bevel
C_STEEL_MID  = (198, 218, 234, 255)   # Mid tone
C_STEEL_RIDGE= (140, 168, 190, 255)   # Ridge accent
C_STEEL_FULLER=(70, 92, 112, 255)     # Blood groove/fuller
C_STEEL_SHAD = (95, 120, 142, 255)    # Shadow bevel
C_STEEL_DARK = (62, 82, 100, 255)     # Deep shadow bevel

# Dark textured leather grip
C_GRIP_BASE  = (58, 34, 24, 255)      # Dark leather
C_GRIP_HI    = (92, 56, 38, 255)      # Leather highlight
C_GRIP_WIRE  = (210, 160, 40, 255)    # Gold wire wrap

# Knightly gauntlet fingers gripping the hilt (polished toy brass gauntlet):
C_FINGER_HI   = (255, 235, 130, 255)  # Knuckle highlight
C_FINGER_MID  = (225, 175, 45, 255)   # Finger body
C_FINGER_SHAD = (155, 110, 25, 255)   # Finger shadow
C_FINGER_LINE = (40, 25, 16, 255)     # Finger crease / segment line

# 1. Contact shadow layer (cast onto rabbit torso/tunic)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow)

# Blade centerline: from (46, 84) to (88, 124)
# Cast shadow is cast to the right/down (dx=+3..+7, dy=+2..+6)
blade_pts = []
for t in range(0, 42):
    frac = t / 41.0
    bx = 45.0 + frac * 42.0
    by = 84.0 + frac * 39.0
    blade_pts.append((bx, by))

# Draw soft contact shadow under blade
for (bx, by) in blade_pts:
    # 5-pixel wide shadow underneath
    for ox in range(2, 7):
        for oy in range(2, 6):
            px, py = int(bx + ox), int(by + oy)
            if 0 <= px < w and 0 <= py < h:
                # stronger near body (t < 0.7), softer near tip
                base_a = int(140 * (1.0 - (by - 84) / 55.0))
                cur_a = shadow.getpixel((px, py))[3]
                if base_a > cur_a:
                    shadow.putpixel((px, py), (15, 10, 22, base_a))

# Shadow under crossguard
for gx in range(40, 52):
    for gy in range(85, 92):
        cur_a = shadow.getpixel((gx, gy))[3]
        shadow.putpixel((gx, gy), (15, 10, 22, max(cur_a, 150)))

shadow = shadow.filter(ImageFilter.GaussianBlur(0.8))

# 2. Main weapon layer
weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(weapon)
pix = weapon.load()

# --- POMMEL: Solid 7x7 spherical golden brass knob at center (35, 73) ---
# Spherical 3D shading
for dy in range(-3, 4):
    for dx in range(-3, 4):
        dist = math.sqrt(dx*dx + dy*dy)
        px, py = 35 + dx, 73 + dy
        if dist <= 3.2:
            if dist > 2.5:
                pix[px, py] = C_OUTLINE
            else:
                # 3D spherical light from upper-left (dx < 0, dy < 0)
                light = -0.6 * dx - 0.8 * dy
                if light > 1.8:
                    pix[px, py] = C_BRASS_SPEC
                elif light > 0.8:
                    pix[px, py] = C_BRASS_HI
                elif light > -0.5:
                    pix[px, py] = C_BRASS_MID
                elif light > -1.8:
                    pix[px, py] = C_BRASS_SHAD
                else:
                    pix[px, py] = C_BRASS_DEEP

# --- GRIP: Cylindrical leather wrap with golden wire rings (from pommel to crossguard) ---
# Axis runs from (36, 75) to (43, 82)
# Width ~ 4-5px, dark rich brown with gold wire rings
for step in range(0, 9):
    gt = step / 8.0
    gx = 36.5 + gt * 6.5
    gy = 75.5 + gt * 6.5
    # Perpendicular vector to (1, 1) is (-1, 1) / sqrt(2)
    for w_off in range(-2, 3):
        qx = int(round(gx - w_off * 0.7))
        qy = int(round(gy + w_off * 0.7))
        if w_off in [-2, 2]:
            pix[qx, qy] = C_OUTLINE
        else:
            if step in [2, 5, 8]:
                # Gold wire ring
                pix[qx, qy] = C_BRASS_HI if w_off <= 0 else C_BRASS_SHAD
            else:
                # Dark leather
                pix[qx, qy] = C_GRIP_HI if w_off < 0 else (C_GRIP_BASE if w_off == 0 else C_GRIP_BASE)

# --- CROSSGUARD: Heavy volumetric knightly brass crossbar (y: 80..87, x: 41..49) ---
# Crossguard bar runs perpendicular to blade (from (48, 79) down-left to (39, 87))
# Bar thickness: ~4-5 pixels, with rounded end caps and volumetric bevels
cg_poly = [
    # Rounded upper finial at (48, 79)
    (48, 79), (49, 80), (49, 81), (48, 82),
    # Center section
    (45, 85),
    # Lower finial at (39, 87)
    (41, 88), (39, 88), (38, 87), (39, 86),
    # Back to center
    (42, 83), (45, 80), (47, 79)
]
# Let's paint crossguard with crisp volumetric lighting
cg_pixels = {
    # Upper finial / quillon (47..49, 78..81)
    (48, 78): C_OUTLINE, (49, 79): C_OUTLINE,
    (47, 79): C_OUTLINE, (48, 79): C_BRASS_SPEC, (49, 80): C_OUTLINE,
    (46, 80): C_OUTLINE, (47, 80): C_BRASS_HI, (48, 80): C_BRASS_MID, (49, 81): C_OUTLINE,
    (45, 81): C_OUTLINE, (46, 81): C_BRASS_SPEC, (47, 81): C_BRASS_HI, (48, 81): C_BRASS_SHAD, (49, 82): C_OUTLINE,
    
    # Center block / hub (x: 43..48, y: 82..85)
    (44, 82): C_OUTLINE, (45, 82): C_BRASS_SPEC, (46, 82): C_BRASS_HI, (47, 82): C_BRASS_MID, (48, 82): C_BRASS_SHAD, (49, 83): C_OUTLINE,
    (43, 83): C_OUTLINE, (44, 83): C_BRASS_HI, (45, 83): C_BRASS_MID, (46, 83): C_BRASS_MID, (47, 83): C_BRASS_SHAD, (48, 83): C_OUTLINE,
    (42, 84): C_OUTLINE, (43, 84): C_BRASS_HI, (44, 84): C_BRASS_MID, (45, 84): C_BRASS_SHAD, (46, 84): C_BRASS_DEEP, (47, 84): C_OUTLINE,
    (41, 85): C_OUTLINE, (42, 85): C_BRASS_MID, (43, 85): C_BRASS_SHAD, (44, 85): C_BRASS_DEEP, (45, 85): C_OUTLINE,
    
    # Lower finial / quillon (38..41, 86..88)
    (40, 86): C_OUTLINE, (41, 86): C_BRASS_MID, (42, 86): C_BRASS_SHAD, (43, 86): C_OUTLINE,
    (39, 87): C_OUTLINE, (40, 87): C_BRASS_SHAD, (41, 87): C_BRASS_DEEP, (42, 87): C_OUTLINE,
    (39, 88): C_OUTLINE, (40, 88): C_OUTLINE,
}
for pos, col in cg_pixels.items():
    pix[pos] = col

# --- BLADE: Wide 6-pixel chibi toy longsword blade with 3D volume ---
# Extends from crossguard (45, 84) to acute tip at (88, 124)
# Total length: ~58 px.
# Profile:
#   Outline top-left
#   Bevel 1: Gleaming specular steel highlight (pure white / light cyan)
#   Bevel 2: High light steel
#   Fuller / spine ridge: Deep accent groove
#   Bevel 3: Shadow steel
#   Bevel 4: Deep ambient shadow steel
#   Outline bottom-right

for step in range(0, 42):
    frac = step / 41.0
    bx = 45.0 + frac * 42.0
    by = 84.0 + frac * 39.0
    
    # Perpendicular offsets for 6-px wide blade:
    # Vector along blade is roughly (42, 39) -> unit is (0.73, 0.68)
    # Perpendicular normal is (-0.68, 0.73)
    nx, ny = -0.68, 0.73
    
    # Taper near tip:
    width_mult = 1.0
    if step >= 35:
        width_mult = max(0.2, (41 - step) / 6.0)
    
    # Sample points across width: w from -3 to +3
    # Left side (negative w): upper-left facing light
    # Right side (positive w): lower-right in shadow
    if step == 41:
        # Extreme tip pixel
        pix[int(round(bx)), int(round(by))] = C_OUTLINE
        pix[int(round(bx - 1)), int(round(by))] = C_STEEL_SPEC
    elif step >= 39:
        # Sharp acute tip
        t_ix, t_iy = int(round(bx)), int(round(by))
        pix[t_ix - 1, t_iy - 1] = C_OUTLINE
        pix[t_ix, t_iy - 1] = C_STEEL_SPEC
        pix[t_ix - 1, t_iy] = C_STEEL_HI
        pix[t_ix, t_iy] = C_STEEL_SHAD
        pix[t_ix + 1, t_iy] = C_OUTLINE
        pix[t_ix, t_iy + 1] = C_OUTLINE
    else:
        # Full blade body (width ~ 5-6px)
        # Outline upper edge
        p_out_top = (int(round(bx - 2.5 * width_mult * nx)), int(round(by - 2.5 * width_mult * ny)))
        p_out_top2 = (int(round(bx - 2.0 * width_mult * nx - 1)), int(round(by - 2.0 * width_mult * ny)))
        pix[p_out_top] = C_OUTLINE
        
        # Specular light edge (white gleam)
        p_spec = (int(round(bx - 1.8 * width_mult * nx)), int(round(by - 1.8 * width_mult * ny)))
        pix[p_spec] = C_STEEL_SPEC if (step % 5 in [0, 1, 2]) else C_STEEL_HI
        
        # Light facet
        p_hi = (int(round(bx - 1.0 * width_mult * nx)), int(round(by - 1.0 * width_mult * ny)))
        pix[p_hi] = C_STEEL_HI
        
        # Fuller / central groove (dark steel line)
        p_ridge = (int(round(bx)), int(round(by)))
        pix[p_ridge] = C_STEEL_FULLER if step < 30 else C_STEEL_MID
        
        # Shadow facet
        p_shad = (int(round(bx + 1.0 * width_mult * nx)), int(round(by + 1.0 * width_mult * ny)))
        pix[p_shad] = C_STEEL_SHAD
        
        # Deep shadow facet
        p_deep = (int(round(bx + 1.8 * width_mult * nx)), int(round(by + 1.8 * width_mult * ny)))
        pix[p_deep] = C_STEEL_DARK
        
        # Outline bottom edge
        p_out_bot = (int(round(bx + 2.5 * width_mult * nx)), int(round(by + 2.5 * width_mult * ny)))
        pix[p_out_bot] = C_OUTLINE

# --- HAND: POLISHED BRASS KNIGHT GAUNTLET FINGERS WRAPPING OVER HILT ---
# The rabbit's hand is holding the hilt at (x: 37..44, y: 77..84).
# In chibi art, armored brass fingers (knuckles) securely wrap OVER the front of the grip:
# 4 distinct fingers + thumb clamping the hilt:
gauntlet_fingers = {
    # THUMB (pressing from top/side at y=76..78, x=36..39)
    (36, 76): C_OUTLINE, (37, 76): C_BRASS_HI, (38, 76): C_BRASS_MID, (39, 76): C_OUTLINE,
    (35, 77): C_OUTLINE, (36, 77): C_BRASS_SPEC, (37, 77): C_BRASS_HI, (38, 77): C_BRASS_SHAD, (39, 77): C_OUTLINE,
    (36, 78): C_OUTLINE, (37, 78): C_BRASS_MID, (38, 78): C_BRASS_SHAD, (39, 78): C_OUTLINE,
    
    # FINGER 1 - INDEX (wrapping over grip at y=78..79, x=38..43)
    (38, 78): C_OUTLINE, (39, 78): C_FINGER_HI, (40, 78): C_FINGER_MID, (41, 78): C_FINGER_SHAD, (42, 78): C_OUTLINE,
    (38, 79): C_OUTLINE, (39, 79): C_FINGER_MID, (40, 79): C_FINGER_MID, (41, 79): C_FINGER_SHAD, (42, 79): C_OUTLINE,
    (39, 80): C_FINGER_LINE, (40, 80): C_FINGER_LINE, (41, 80): C_FINGER_LINE, # Crease line between fingers
    
    # FINGER 2 - MIDDLE (wrapping over grip at y=80..81, x=39..44)
    (39, 80): C_OUTLINE, (40, 80): C_FINGER_HI, (41, 80): C_FINGER_MID, (42, 80): C_FINGER_SHAD, (43, 80): C_OUTLINE,
    (39, 81): C_OUTLINE, (40, 81): C_FINGER_MID, (41, 81): C_FINGER_MID, (42, 81): C_FINGER_SHAD, (43, 81): C_OUTLINE,
    (40, 82): C_FINGER_LINE, (41, 82): C_FINGER_LINE, (42, 82): C_FINGER_LINE, # Crease line
    
    # FINGER 3 - RING / PINKY (wrapping near crossguard at y=82..84, x=40..45)
    (40, 82): C_OUTLINE, (41, 82): C_FINGER_HI, (42, 82): C_FINGER_MID, (43, 82): C_FINGER_SHAD, (44, 82): C_OUTLINE,
    (40, 83): C_OUTLINE, (41, 83): C_FINGER_MID, (42, 83): C_FINGER_SHAD, (43, 83): C_BRASS_DEEP, (44, 83): C_OUTLINE,
    (41, 84): C_OUTLINE, (42, 84): C_OUTLINE, (43, 84): C_OUTLINE,
}
for pos, col in gauntlet_fingers.items():
    pix[pos] = col

# Combine shadow and sword into final deliverable
final_blade = Image.new("RGBA", (w, h), (0, 0, 0, 0))
final_blade.alpha_composite(shadow)
final_blade.alpha_composite(weapon)

final_blade.save("/tmp/v3_dawn_blade.png")
print("V3 Dawn Blade created, bbox:", final_blade.getbbox())

# Composite with all rabbit layers
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"
for c_name in ["paint_midnight_navy.png", "paint_ivory_stock.png"]:
    comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    comp.alpha_composite(Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/chassis/{c_name}").convert("RGBA"))
    comp.alpha_composite(Image.open("/tmp/ear_wrapped.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA"))
    comp.alpha_composite(final_blade)
    
    tag = "navy" if "navy" in c_name else "ivory"
    comp.save(f"/tmp/v3_comp_{tag}.png")
    
    dark = Image.new("RGBA", (w, h), (7, 6, 10, 255))
    dark.alpha_composite(comp)
    dark.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save(f"/tmp/v3_comp_{tag}_4x.png")
    
    crop = dark.crop((26, 64, 98, 126)).resize((360, 310), getattr(Image, 'Resampling', Image).NEAREST)
    crop.save(f"/tmp/v3_crop_{tag}.png")

print("Saved V3 composites and crops!")
