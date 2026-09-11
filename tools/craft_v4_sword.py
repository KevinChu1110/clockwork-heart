import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"
w, h = 128, 128

# Colors
C_OUTLINE      = (35, 22, 18, 255)       # #231612
C_OUTLINE_SOFT = (55, 38, 30, 180)

# Golden brass (pommel & crossguard)
C_BRASS_SPEC = (255, 255, 220, 255)
C_BRASS_HI   = (255, 225, 80, 255)
C_BRASS_MID  = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)
C_BRASS_DEEP = (85, 52, 10, 255)

# Steel blade
C_STEEL_SPEC = (255, 255, 255, 255)
C_STEEL_HI   = (232, 244, 252, 255)
C_STEEL_MID  = (198, 218, 234, 255)
C_STEEL_RIDGE= (140, 168, 190, 255)
C_STEEL_FULLER=(70, 92, 112, 255)
C_STEEL_SHAD = (95, 120, 142, 255)
C_STEEL_DARK = (62, 82, 100, 255)

# DARK EBONY / LEATHER GRIP (Stark contrast against ivory fingers!)
C_DARK_GRIP   = (38, 24, 18, 255)
C_DARK_GRIP_D = (24, 14, 10, 255)

# IVORY WHITE PAW / FINGERS (Matching Whitey's official color!)
C_FINGER_SPEC = (255, 255, 255, 255)
C_FINGER_HI   = (250, 246, 238, 255)
C_FINGER_MID  = (226, 214, 196, 255)
C_FINGER_SHAD = (176, 158, 136, 255)
C_FINGER_DEEP = (128, 110, 90, 255)
C_FINGER_CREASE = (45, 28, 20, 255)

# 1. Contact shadow layer (cast onto rabbit body)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
blade_pts = []
for t in range(0, 42):
    frac = t / 41.0
    bx = 45.0 + frac * 42.0
    by = 84.0 + frac * 39.0
    blade_pts.append((bx, by))

for (bx, by) in blade_pts:
    for ox in range(2, 7):
        for oy in range(2, 6):
            px, py = int(bx + ox), int(by + oy)
            if 0 <= px < w and 0 <= py < h:
                base_a = int(140 * (1.0 - (by - 84) / 55.0))
                cur_a = shadow.getpixel((px, py))[3]
                if base_a > cur_a:
                    shadow.putpixel((px, py), (15, 10, 22, base_a))

for gx in range(40, 52):
    for gy in range(85, 92):
        cur_a = shadow.getpixel((gx, gy))[3]
        shadow.putpixel((gx, gy), (15, 10, 22, max(cur_a, 150)))

shadow = shadow.filter(ImageFilter.GaussianBlur(0.8))

# 2. Weapon layer
weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pix = weapon.load()

# --- POMMEL: Golden brass ball at (35, 73) ---
for dy in range(-3, 4):
    for dx in range(-3, 4):
        dist = math.sqrt(dx*dx + dy*dy)
        px, py = 35 + dx, 73 + dy
        if dist <= 3.2:
            if dist > 2.5:
                pix[px, py] = C_OUTLINE
            else:
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

# --- DARK GRIP: Pure dark leather handle ---
# Axis: (36, 75) to (43, 82)
for step in range(0, 9):
    gt = step / 8.0
    gx = 36.5 + gt * 6.5
    gy = 75.5 + gt * 6.5
    for w_off in range(-2, 3):
        qx = int(round(gx - w_off * 0.7))
        qy = int(round(gy + w_off * 0.7))
        if w_off in [-2, 2]:
            pix[qx, qy] = C_OUTLINE
        else:
            pix[qx, qy] = C_DARK_GRIP if w_off <= 0 else C_DARK_GRIP_D

# --- CROSSGUARD: Golden brass crossbar ---
cg_pixels = {
    # Upper finial (47..49, 78..81)
    (48, 78): C_OUTLINE, (49, 79): C_OUTLINE,
    (47, 79): C_OUTLINE, (48, 79): C_BRASS_SPEC, (49, 80): C_OUTLINE,
    (46, 80): C_OUTLINE, (47, 80): C_BRASS_HI, (48, 80): C_BRASS_MID, (49, 81): C_OUTLINE,
    (45, 81): C_OUTLINE, (46, 81): C_BRASS_SPEC, (47, 81): C_BRASS_HI, (48, 81): C_BRASS_SHAD, (49, 82): C_OUTLINE,
    
    # Center block / hub (x: 43..48, y: 82..85)
    (44, 82): C_OUTLINE, (45, 82): C_BRASS_SPEC, (46, 82): C_BRASS_HI, (47, 82): C_BRASS_MID, (48, 82): C_BRASS_SHAD, (49, 83): C_OUTLINE,
    (43, 83): C_OUTLINE, (44, 83): C_BRASS_HI, (45, 83): C_BRASS_MID, (46, 83): C_BRASS_MID, (47, 83): C_BRASS_SHAD, (48, 83): C_OUTLINE,
    (42, 84): C_OUTLINE, (43, 84): C_BRASS_HI, (44, 84): C_BRASS_MID, (45, 84): C_BRASS_SHAD, (46, 84): C_BRASS_DEEP, (47, 84): C_OUTLINE,
    (41, 85): C_OUTLINE, (42, 85): C_BRASS_MID, (43, 85): C_BRASS_SHAD, (44, 85): C_BRASS_DEEP, (45, 85): C_OUTLINE,
    
    # Lower finial (38..41, 86..88)
    (40, 86): C_OUTLINE, (41, 86): C_BRASS_MID, (42, 86): C_BRASS_SHAD, (43, 86): C_OUTLINE,
    (39, 87): C_OUTLINE, (40, 87): C_BRASS_SHAD, (41, 87): C_BRASS_DEEP, (42, 87): C_OUTLINE,
    (39, 88): C_OUTLINE, (40, 88): C_OUTLINE,
}
for pos, col in cg_pixels.items():
    pix[pos] = col

# --- BLADE: Wide 6-px volumetric steel blade ---
for step in range(0, 42):
    frac = step / 41.0
    bx = 45.0 + frac * 42.0
    by = 84.0 + frac * 39.0
    nx, ny = -0.68, 0.73
    
    width_mult = 1.0
    if step >= 35:
        width_mult = max(0.2, (41 - step) / 6.0)
    
    if step == 41:
        pix[int(round(bx)), int(round(by))] = C_OUTLINE
        pix[int(round(bx - 1)), int(round(by))] = C_STEEL_SPEC
    elif step >= 39:
        t_ix, t_iy = int(round(bx)), int(round(by))
        pix[t_ix - 1, t_iy - 1] = C_OUTLINE
        pix[t_ix, t_iy - 1] = C_STEEL_SPEC
        pix[t_ix - 1, t_iy] = C_STEEL_HI
        pix[t_ix, t_iy] = C_STEEL_SHAD
        pix[t_ix + 1, t_iy] = C_OUTLINE
        pix[t_ix, t_iy + 1] = C_OUTLINE
    else:
        p_out_top = (int(round(bx - 2.5 * width_mult * nx)), int(round(by - 2.5 * width_mult * ny)))
        pix[p_out_top] = C_OUTLINE
        
        p_spec = (int(round(bx - 1.8 * width_mult * nx)), int(round(by - 1.8 * width_mult * ny)))
        pix[p_spec] = C_STEEL_SPEC if (step % 5 in [0, 1, 2]) else C_STEEL_HI
        
        p_hi = (int(round(bx - 1.0 * width_mult * nx)), int(round(by - 1.0 * width_mult * ny)))
        pix[p_hi] = C_STEEL_HI
        
        p_ridge = (int(round(bx)), int(round(by)))
        pix[p_ridge] = C_STEEL_FULLER if step < 30 else C_STEEL_MID
        
        p_shad = (int(round(bx + 1.0 * width_mult * nx)), int(round(by + 1.0 * width_mult * ny)))
        pix[p_shad] = C_STEEL_SHAD
        
        p_deep = (int(round(bx + 1.8 * width_mult * nx)), int(round(by + 1.8 * width_mult * ny)))
        pix[p_deep] = C_STEEL_DARK
        
        p_out_bot = (int(round(bx + 2.5 * width_mult * nx)), int(round(by + 2.5 * width_mult * ny)))
        pix[p_out_bot] = C_OUTLINE

# --- WHITE IVORY FINGERS WRAPPING ACROSS THE DARK GRIP ---
# This creates unmistakable, crystal-clear finger occlusion!
# Four chubby white rabbit fingers + thumb wrapping over the dark handle:
fingers_ivory = {
    # Palm base & Thumb pressing on top (x: 35..38, y: 75..77)
    (35, 76): C_OUTLINE, (36, 76): C_FINGER_SPEC, (37, 76): C_FINGER_HI, (38, 76): C_OUTLINE,
    (35, 77): C_OUTLINE, (36, 77): C_FINGER_HI,   (37, 77): C_FINGER_MID, (38, 77): C_FINGER_SHAD, (39, 77): C_OUTLINE,
    (35, 78): C_OUTLINE, (36, 78): C_FINGER_MID,  (37, 78): C_FINGER_SHAD, (38, 78): C_OUTLINE,
    
    # FINGER 1 - Index finger wrapping across hilt at y=78..79 (x: 38..43)
    (38, 78): C_OUTLINE, (39, 78): C_FINGER_SPEC, (40, 78): C_FINGER_HI, (41, 78): C_FINGER_MID, (42, 78): C_OUTLINE,
    (38, 79): C_OUTLINE, (39, 79): C_FINGER_HI,   (40, 79): C_FINGER_MID, (41, 79): C_FINGER_SHAD, (42, 79): C_FINGER_SHAD, (43, 79): C_OUTLINE,
    (39, 80): C_FINGER_CREASE, (40, 80): C_FINGER_CREASE, (41, 80): C_FINGER_CREASE, (42, 80): C_OUTLINE,
    
    # FINGER 2 - Middle finger wrapping across hilt at y=80..81 (x: 39..44)
    (39, 80): C_OUTLINE, (40, 80): C_FINGER_SPEC, (41, 80): C_FINGER_HI, (42, 80): C_FINGER_MID, (43, 80): C_OUTLINE,
    (39, 81): C_OUTLINE, (40, 81): C_FINGER_HI,   (41, 81): C_FINGER_MID, (42, 81): C_FINGER_SHAD, (43, 81): C_FINGER_SHAD, (44, 81): C_OUTLINE,
    (40, 82): C_FINGER_CREASE, (41, 82): C_FINGER_CREASE, (42, 82): C_FINGER_CREASE, (43, 82): C_OUTLINE,
    
    # FINGER 3 - Ring/Pinky finger wrapping at y=82..83 (x: 40..45)
    (40, 82): C_OUTLINE, (41, 82): C_FINGER_SPEC, (42, 82): C_FINGER_HI, (43, 82): C_FINGER_MID, (44, 82): C_OUTLINE,
    (40, 83): C_OUTLINE, (41, 83): C_FINGER_HI,   (42, 83): C_FINGER_MID, (43, 83): C_FINGER_SHAD, (44, 83): C_FINGER_SHAD, (45, 83): C_OUTLINE,
    (41, 84): C_OUTLINE, (42, 84): C_OUTLINE, (43, 84): C_OUTLINE, (44, 84): C_OUTLINE,
}
for pos, col in fingers_ivory.items():
    pix[pos] = col

# Final composite of shadow + weapon
final_v4 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
final_v4.alpha_composite(shadow)
final_v4.alpha_composite(weapon)
final_v4.save("/tmp/v4_dawn_blade.png")

# Composite with both navy and ivory
for c_name in ["paint_midnight_navy.png", "paint_ivory_stock.png"]:
    comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    comp.alpha_composite(Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/chassis/{c_name}").convert("RGBA"))
    comp.alpha_composite(Image.open("/tmp/ear_wrapped.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA"))
    comp.alpha_composite(final_v4)
    
    tag = "navy" if "navy" in c_name else "ivory"
    comp.save(f"/tmp/v4_comp_{tag}.png")
    
    dark = Image.new("RGBA", (w, h), (7, 6, 10, 255))
    dark.alpha_composite(comp)
    dark.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save(f"/tmp/v4_comp_{tag}_4x.png")
    
    crop = dark.crop((26, 64, 98, 126)).resize((360, 310), getattr(Image, 'Resampling', Image).NEAREST)
    crop.save(f"/tmp/v4_crop_{tag}.png")

print("Saved V4 weapon, composites and crops successfully!")
