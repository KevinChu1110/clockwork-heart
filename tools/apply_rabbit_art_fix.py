import os
import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"
w, h = 128, 128

print("=== 1. Processing ear_rabbit_straight.png ===")
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
ew, eh = ear.size
ear_data = ear.load()

OUTLINE = (44, 28, 22, 255) # #2C1C16 deep warm brown

# Wrap outer edge pixels with dark outline
ear_clean = ear.copy()
c_data = ear_clean.load()

# Step A: Find all transparent pixels adjacent to ear pixels (y < 65)
wrap_pixels = {}
for y in range(65):
    for x in range(ew):
        if ear_data[x, y][3] == 0:
            has_neighbor = False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < ew and 0 <= ny < eh:
                        if ear_data[nx, ny][3] > 64:
                            has_neighbor = True
                            break
                if has_neighbor:
                    break
            if has_neighbor:
                wrap_pixels[(x, y)] = OUTLINE

for pos, col in wrap_pixels.items():
    c_data[pos] = col

# Step B: Check any remaining edge pixel on ear that touches alpha=0 and is bright
for y in range(eh):
    for x in range(ew):
        r, g, b, a = c_data[x, y]
        if a > 0:
            touches_0 = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= ew or ny < 0 or ny >= eh or c_data[nx, ny][3] == 0:
                    touches_0 = True
                    break
            if touches_0:
                lum = (r + g + b) / 3
                if lum > 140:
                    c_data[x, y] = OUTLINE

ear_clean.save(f"{r_dir}/head_unit/ear_rabbit_straight.png")
print("  ✓ ear_rabbit_straight.png saved with clean dark contour and zero bright edge pixels.")

print("\n=== 2. Processing chassis paints (head crown contour) ===")
# Between ears (y: 42..45, x: 53..63), cap the skull plate with dark outline
for p_name in ["paint_ivory_stock.png", "paint_brass_gold.png", "paint_midnight_navy.png"]:
    ch_path = f"{r_dir}/chassis/{p_name}"
    ch = Image.open(ch_path).convert("RGBA")
    ch_data = ch.load()
    # Find outer edge pixels between x=52..64, y=42..46
    for y in range(42, 47):
        for x in range(52, 65):
            r, g, b, a = ch_data[x, y]
            if a > 0:
                touches_0 = False
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= w or ny < 0 or ny >= h or ch_data[nx, ny][3] == 0:
                        touches_0 = True
                        break
                if touches_0 and y <= 43:
                    ch_data[x, y] = OUTLINE
    ch.save(ch_path)
    print(f"  ✓ {p_name} head crown contour verified and saved.")

print("\n=== 3. Crafting 3D single-handed longsword wpn_dawn_blade.png ===")
# Colors
C_OUTLINE      = (35, 22, 18, 255)       # #231612
C_BRASS_SPEC   = (255, 255, 220, 255)
C_BRASS_HI     = (255, 225, 80, 255)
C_BRASS_MID    = (215, 160, 30, 255)
C_BRASS_SHAD   = (145, 95, 18, 255)
C_BRASS_DEEP   = (85, 52, 10, 255)

C_STEEL_SPEC   = (255, 255, 255, 255)
C_STEEL_HI     = (232, 244, 252, 255)
C_STEEL_MID    = (198, 218, 234, 255)
C_STEEL_RIDGE  = (140, 168, 190, 255)
C_STEEL_FULLER = (70, 92, 112, 255)
C_STEEL_SHAD   = (95, 120, 142, 255)
C_STEEL_DARK   = (62, 82, 100, 255)

C_DARK_GRIP    = (38, 24, 18, 255)
C_DARK_GRIP_D  = (24, 14, 10, 255)

# Contact drop shadow layer
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))

# Crossguard shadow on torso
for gx in range(41, 48):
    for gy in range(92, 97):
        shadow.putpixel((gx + 1, gy + 1), (18, 12, 26, 175))
        shadow.putpixel((gx + 2, gy + 1), (18, 12, 26, 130))

# Blade tight contact shadow along bottom edge
for step in range(0, 45):
    frac = step / 44.0
    bx = 43.0 + frac * 47.0
    by = 91.0 + frac * 34.0
    nx, ny = -0.59, 0.81
    
    width_mult = 1.0 if step < 38 else max(0.15, (44 - step) / 6.0)
    edge_x = int(round(bx + 2.5 * width_mult * nx))
    edge_y = int(round(by + 2.5 * width_mult * ny))
    
    if bx < 78:
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

shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(0.4))
combined_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
combined_shadow.alpha_composite(shadow_blurred)
combined_shadow.alpha_composite(shadow)

# Weapon layer
weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pix = weapon.load()

# Pommel: Golden brass ball at (32, 83)
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

# Grip: Dark leather handle running from (33, 85) to (41, 91)
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

# Crossguard: Brass bar running perpendicular from (44, 87) down to (37, 95)
cg_pixels = {
    (44, 86): C_OUTLINE, (45, 87): C_OUTLINE,
    (43, 87): C_OUTLINE, (44, 87): C_BRASS_SPEC, (45, 88): C_OUTLINE,
    (42, 88): C_OUTLINE, (43, 88): C_BRASS_HI, (44, 88): C_BRASS_MID, (45, 89): C_OUTLINE,
    (41, 89): C_OUTLINE, (42, 89): C_BRASS_SPEC, (43, 89): C_BRASS_HI, (44, 89): C_BRASS_SHAD, (45, 90): C_OUTLINE,
    (40, 90): C_OUTLINE, (41, 90): C_BRASS_HI, (42, 90): C_BRASS_MID, (43, 90): C_BRASS_SHAD, (44, 90): C_BRASS_DEEP, (45, 91): C_OUTLINE,
    (39, 91): C_OUTLINE, (40, 91): C_BRASS_HI, (41, 91): C_BRASS_MID, (42, 91): C_BRASS_SHAD, (43, 91): C_BRASS_DEEP, (44, 91): C_OUTLINE,
    (38, 92): C_OUTLINE, (39, 92): C_BRASS_MID, (40, 92): C_BRASS_SHAD, (41, 92): C_OUTLINE,
    (37, 93): C_OUTLINE, (38, 93): C_BRASS_SHAD, (39, 93): C_BRASS_DEEP, (40, 93): C_OUTLINE,
    (37, 94): C_OUTLINE, (38, 94): C_OUTLINE,
}
for pos, col in cg_pixels.items():
    pix[pos] = col

# Blade: Wide 6-pixel steel blade from (43, 91) to (90, 125)
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

wpn_path = f"{r_dir}/weapon/wpn_dawn_blade.png"
final_sword.save(wpn_path)
print(f"  ✓ wpn_dawn_blade.png saved successfully (bbox={final_sword.getbbox()})")

print("\n=== 4. Re-generating composite and proof images ===")
key = Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA")
pigeon = Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA")
head = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
core = Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA")
wpn = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")

# Build standard proof composite (ivory + nutcracker)
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
cost_nutcracker = Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA")

comp_standard = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp_standard.alpha_composite(key)
comp_standard.alpha_composite(pigeon)
comp_standard.alpha_composite(ch_ivory)
comp_standard.alpha_composite(head)
comp_standard.alpha_composite(cost_nutcracker)
comp_standard.alpha_composite(core)
comp_standard.alpha_composite(wpn)

comp_standard.save(f"{r_dir}/proof_paperdoll_rabbit_composite.png")
comp_standard.save(f"{r_dir}/proof_paperdoll_scene_composite.png")
comp_standard.save(f"{r_dir}/proof_race_switch_verified.png")
comp_standard.save(f"{r_dir}/composite_preview_nutcracker.png")
comp_standard.save(f"{r_dir}/composite_all_layers.png")
comp_standard.save(f"{r_dir}/composite_final_master.png")

# Magenta proof
magenta = Image.new("RGBA", (w, h), (255, 0, 255, 255))
magenta.alpha_composite(comp_standard)
magenta.save(f"{r_dir}/proof_paperdoll_rabbit_magenta.png")

# Proof royal navy
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")
cost_royal = Image.open(f"{r_dir}/costume/costume_royal_parade.png").convert("RGBA")
comp_royal_navy = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp_royal_navy.alpha_composite(key)
comp_royal_navy.alpha_composite(pigeon)
comp_royal_navy.alpha_composite(ch_navy)
comp_royal_navy.alpha_composite(head)
comp_royal_navy.alpha_composite(cost_royal)
comp_royal_navy.alpha_composite(core)
comp_royal_navy.alpha_composite(wpn)
comp_rn_mag = Image.new("RGBA", (w, h), (255, 0, 255, 255))
comp_rn_mag.alpha_composite(comp_royal_navy)
comp_rn_mag.save(f"{r_dir}/proof_paperdoll_rabbit_royal_navy_magenta.png")

# Proof nutcracker navy
comp_nut_navy = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp_nut_navy.alpha_composite(key)
comp_nut_navy.alpha_composite(pigeon)
comp_nut_navy.alpha_composite(ch_navy)
comp_nut_navy.alpha_composite(head)
comp_nut_navy.alpha_composite(cost_nutcracker)
comp_nut_navy.alpha_composite(core)
comp_nut_navy.alpha_composite(wpn)
comp_nn_mag = Image.new("RGBA", (w, h), (255, 0, 255, 255))
comp_nn_mag.alpha_composite(comp_nut_navy)
comp_nn_mag.save(f"{r_dir}/proof_paperdoll_rabbit_nutcracker_navy_magenta.png")

# Proof royal ivory
comp_royal_ivory = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp_royal_ivory.alpha_composite(key)
comp_royal_ivory.alpha_composite(pigeon)
comp_royal_ivory.alpha_composite(ch_ivory)
comp_royal_ivory.alpha_composite(head)
comp_royal_ivory.alpha_composite(cost_royal)
comp_royal_ivory.alpha_composite(core)
comp_royal_ivory.alpha_composite(wpn)
comp_ri_mag = Image.new("RGBA", (w, h), (255, 0, 255, 255))
comp_ri_mag.alpha_composite(comp_royal_ivory)
comp_ri_mag.save(f"{r_dir}/proof_paperdoll_rabbit_royal_ivory_magenta.png")

# Bare preview
comp_bare = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp_bare.alpha_composite(key)
comp_bare.alpha_composite(pigeon)
comp_bare.alpha_composite(ch_ivory)
comp_bare.alpha_composite(head)
comp_bare.alpha_composite(core)
comp_bare.alpha_composite(wpn)
comp_bare.save(f"{r_dir}/composite_preview_bare.png")
comp_bare.save(f"{r_dir}/composite_bare_master.png")

print("  ✓ All rabbit composite and proof images re-generated successfully!")
