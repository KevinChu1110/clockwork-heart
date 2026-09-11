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

# Contact drop shadow layer (cast directly onto coat, belt, legs)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))

# 1-2px tight contact shadow directly abutting the blade bottom edge
# Crossguard shadow on torso (x: 41..49, y: 92..97)
for gx in range(41, 48):
    for gy in range(92, 97):
        shadow.putpixel((gx + 1, gy + 1), (18, 12, 26, 175))
        shadow.putpixel((gx + 2, gy + 1), (18, 12, 26, 130))

# Blade tight contact shadow along the bottom-right border
# From crossguard (x=43, y=91) across coat/belt down to knee (x=72, y=112)
for step in range(0, 45):
    frac = step / 44.0
    bx = 43.0 + frac * 47.0
    by = 91.0 + frac * 34.0
    nx, ny = -0.59, 0.81
    
    width_mult = 1.0 if step < 38 else max(0.15, (44 - step) / 6.0)
    # Bottom edge of blade is around (bx + 2.5 * nx, by + 2.5 * ny)
    edge_x = int(round(bx + 2.5 * width_mult * nx))
    edge_y = int(round(by + 2.5 * width_mult * ny))
    
    # Place 1-2px cast shadow directly below bottom edge
    # Strongest over the torso and coat (x < 74)
    if bx < 78:
        # 1px tight contact shadow
        p1 = (edge_x + 1, edge_y + 1)
        p2 = (edge_x, edge_y + 1)
        p3 = (edge_x + 1, edge_y + 2)
        if 0 <= p1[0] < w and 0 <= p1[1] < h:
            shadow.putpixel(p1, (16, 10, 24, 190))
        if 0 <= p2[0] < w and 0 <= p2[1] < h:
            cur_a = shadow.getpixel(p2)[3]
            shadow.putpixel(p2, (16, 10, 24, max(cur_a, 160)))
        if 0 <= p3[0] < w and 0 <= p3[1] < h:
            cur_a = shadow.getpixel(p3)[3]
            shadow.putpixel(p3, (16, 10, 24, max(cur_a, 125)))

# Soft blur on outer shadow edge only
shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(0.4))
# Blend tight shadow over blurred shadow for sharp contact + soft penumbra
combined_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
combined_shadow.alpha_composite(shadow_blurred)
combined_shadow.alpha_composite(shadow)

# Weapon layer
weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pix = weapon.load()

# --- POMMEL: Golden brass ball at (32, 83) ---
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
    nx, ny = -0.59, 0.81
    
    width_mult = 1.0 if step < 38 else max(0.15, (44 - step) / 6.0)
    
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
final_sword.alpha_composite(combined_shadow)
final_sword.alpha_composite(weapon)

final_sword.save("/tmp/hand_aligned_blade_shadow.png")

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
    comp.save(f"/tmp/aligned_shadow_comp_{tag}.png")
    
    dark = Image.new("RGBA", (w, h), (7, 6, 10, 255))
    dark.alpha_composite(comp)
    dark.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save(f"/tmp/aligned_shadow_comp_{tag}_4x.png")
    
    crop = dark.crop((24, 66, 100, 126)).resize((380, 300), getattr(Image, 'Resampling', Image).NEAREST)
    crop.save(f"/tmp/aligned_shadow_crop_{tag}.png")

print("Saved enhanced shadow weapon composites and crops!")
