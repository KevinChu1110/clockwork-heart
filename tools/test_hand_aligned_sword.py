import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"
w, h = 128, 128

# Colors
C_OUTLINE      = (35, 22, 18, 255)       # #231612
C_OUTLINE_SOFT = (55, 38, 30, 200)

# Golden brass (pommel & crossguard)
C_BRASS_SPEC = (255, 255, 220, 255)
C_BRASS_HI   = (255, 225, 80, 255)
C_BRASS_MID  = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)
C_BRASS_DEEP = (85, 52, 10, 255)

# Steel blade (3D volumetric steel)
C_STEEL_SPEC = (255, 255, 255, 255)
C_STEEL_HI   = (232, 244, 252, 255)
C_STEEL_MID  = (198, 218, 234, 255)
C_STEEL_RIDGE= (140, 168, 190, 255)
C_STEEL_FULLER=(70, 92, 112, 255)
C_STEEL_SHAD = (95, 120, 142, 255)
C_STEEL_DARK = (62, 82, 100, 255)

# Dark grip
C_DARK_GRIP   = (38, 24, 18, 255)
C_DARK_GRIP_D = (24, 14, 10, 255)

# Strong visible cast shadow (alpha 140..190)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))

# Blade axis: from (44, 92) to (90, 125)
# Cast shadow is cast to the right/down (+2..+5) onto the legs and feet
for t in range(0, 45):
    frac = t / 44.0
    bx = 44.0 + frac * 46.0
    by = 92.0 + frac * 33.0
    for ox in range(2, 6):
        for oy in range(2, 5):
            px, py = int(bx + ox), int(by + oy)
            if 0 <= px < w and 0 <= py < h:
                a = int(170 * (1.0 - frac * 0.35))
                cur = shadow.getpixel((px, py))[3]
                if a > cur:
                    shadow.putpixel((px, py), (14, 10, 22, a))

# Shadow under crossguard (at body x=42..48, y=93..97)
for gx in range(41, 48):
    for gy in range(92, 98):
        shadow.putpixel((gx + 2, gy + 2), (14, 10, 22, 180))

shadow = shadow.filter(ImageFilter.GaussianBlur(0.7))

# Weapon layer
weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pix = weapon.load()

# --- POMMEL: Golden brass ball at (32, 83) ---
# Behind the wrist/hand at hip level
for dy in range(-3, 4):
    for dx in range(-3, 4):
        dist = math.sqrt(dx*dx + dy*dy)
        px, py = 32 + dx, 83 + dy
        if dist <= 3.2:
            if dist > 2.4:
                pix[px, py] = C_OUTLINE
            else:
                light = -0.6 * dx - 0.8 * dy
                if light > 1.6:
                    pix[px, py] = C_BRASS_SPEC
                elif light > 0.6:
                    pix[px, py] = C_BRASS_HI
                elif light > -0.6:
                    pix[px, py] = C_BRASS_MID
                elif light > -1.6:
                    pix[px, py] = C_BRASS_SHAD
                else:
                    pix[px, py] = C_BRASS_DEEP

# --- GRIP: Dark leather handle running from (33, 85) to (41, 91) ---
for step in range(0, 8):
    gt = step / 7.0
    gx = 34.0 + gt * 6.5
    gy = 85.0 + gt * 5.5
    for w_off in range(-2, 3):
        qx = int(round(gx - w_off * 0.6))
        qy = int(round(gy + w_off * 0.8))
        if w_off in [-2, 2]:
            pix[qx, qy] = C_OUTLINE
        else:
            pix[qx, qy] = C_DARK_GRIP if w_off <= 0 else C_DARK_GRIP_D

# --- CROSSGUARD: Brass bar running perpendicular from (44, 87) down to (37, 95) ---
cg_pixels = {
    # Upper finial
    (44, 86): C_OUTLINE, (45, 87): C_OUTLINE,
    (43, 87): C_OUTLINE, (44, 87): C_BRASS_SPEC, (45, 88): C_OUTLINE,
    (42, 88): C_OUTLINE, (43, 88): C_BRASS_HI, (44, 88): C_BRASS_MID, (45, 89): C_OUTLINE,
    # Center hub
    (41, 89): C_OUTLINE, (42, 89): C_BRASS_SPEC, (43, 89): C_BRASS_HI, (44, 89): C_BRASS_SHAD, (45, 90): C_OUTLINE,
    (40, 90): C_OUTLINE, (41, 90): C_BRASS_HI, (42, 90): C_BRASS_MID, (43, 90): C_BRASS_SHAD, (44, 90): C_BRASS_DEEP, (45, 91): C_OUTLINE,
    (39, 91): C_OUTLINE, (40, 91): C_BRASS_HI, (41, 91): C_BRASS_MID, (42, 91): C_BRASS_SHAD, (43, 91): C_BRASS_DEEP, (44, 91): C_OUTLINE,
    # Lower finial
    (38, 92): C_OUTLINE, (39, 92): C_BRASS_MID, (40, 92): C_BRASS_SHAD, (41, 92): C_OUTLINE,
    (37, 93): C_OUTLINE, (38, 93): C_BRASS_SHAD, (39, 93): C_BRASS_DEEP, (40, 93): C_OUTLINE,
    (37, 94): C_OUTLINE, (38, 94): C_OUTLINE,
}
for pos, col in cg_pixels.items():
    pix[pos] = col

# --- BLADE: Wide 6-pixel steel blade from (43, 91) to (90, 125) ---
for step in range(0, 45):
    frac = step / 44.0
    bx = 43.0 + frac * 47.0
    by = 91.0 + frac * 34.0
    
    # Normal to blade: direction is roughly (47, 34) -> normal is (-34, 47) / 58 = (-0.59, 0.81)
    nx, ny = -0.59, 0.81
    
    width_mult = 1.0
    if step >= 38:
        width_mult = max(0.15, (44 - step) / 6.0)
    
    if step == 44:
        pix[int(round(bx)), int(round(by))] = C_OUTLINE
        pix[int(round(bx - 1)), int(round(by))] = C_STEEL_SPEC
    elif step >= 41:
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
        pix[p_spec] = C_STEEL_SPEC if (step % 4 in [0, 1]) else C_STEEL_HI
        
        p_hi = (int(round(bx - 1.0 * width_mult * nx)), int(round(by - 1.0 * width_mult * ny)))
        pix[p_hi] = C_STEEL_HI
        
        p_ridge = (int(round(bx)), int(round(by)))
        pix[p_ridge] = C_STEEL_FULLER if step < 32 else C_STEEL_MID
        
        p_shad = (int(round(bx + 1.0 * width_mult * nx)), int(round(by + 1.0 * width_mult * ny)))
        pix[p_shad] = C_STEEL_SHAD
        
        p_deep = (int(round(bx + 1.8 * width_mult * nx)), int(round(by + 1.8 * width_mult * ny)))
        pix[p_deep] = C_STEEL_DARK
        
        p_out_bot = (int(round(bx + 2.5 * width_mult * nx)), int(round(by + 2.5 * width_mult * ny)))
        pix[p_out_bot] = C_OUTLINE

# Combine shadow and weapon
final_sword = Image.new("RGBA", (w, h), (0, 0, 0, 0))
final_sword.alpha_composite(shadow)
final_sword.alpha_composite(weapon)

final_sword.save("/tmp/hand_aligned_blade.png")

# Now composite with rabbit!
for c_name in ["paint_midnight_navy.png", "paint_ivory_stock.png"]:
    comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    comp.alpha_composite(Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/chassis/{c_name}").convert("RGBA"))
    comp.alpha_composite(Image.open("/tmp/ear_wrapped.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA"))
    comp.alpha_composite(final_sword)
    
    tag = "navy" if "navy" in c_name else "ivory"
    comp.save(f"/tmp/aligned_comp_{tag}.png")
    
    dark = Image.new("RGBA", (w, h), (7, 6, 10, 255))
    dark.alpha_composite(comp)
    dark.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save(f"/tmp/aligned_comp_{tag}_4x.png")
    
    crop = dark.crop((24, 66, 100, 126)).resize((380, 300), getattr(Image, 'Resampling', Image).NEAREST)
    crop.save(f"/tmp/aligned_crop_{tag}.png")

print("Saved aligned weapon composites and crops!")
