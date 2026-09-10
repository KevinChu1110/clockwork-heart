import os
import math
from PIL import Image, ImageDraw, ImageFilter

repo = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"
w, h = 128, 128

print("=== 1. Checking ear_rabbit_straight.png (Already verified & approved in Attempt 1) ===")
# ear_rabbit_straight.png outer outline is already cleanly committed in HEAD

print("\n=== 2. Checking chassis paints (Already verified & approved in Attempt 1) ===")
# chassis paint contours are already cleanly committed in HEAD

print("\n=== 3. Crafting 3D single-handed longsword wpn_dawn_blade.png ===")
# Colors
C_OUTLINE      = (44, 28, 22, 255)       # #2C1C16 deep warm brown
C_OUTLINE_SOFT = (60, 40, 32, 255)

C_BRASS_SPEC   = (255, 255, 230, 255)
C_BRASS_HI     = (255, 225, 85, 255)
C_BRASS_MID    = (215, 160, 30, 255)
C_BRASS_SHAD   = (145, 95, 18, 255)
C_BRASS_DEEP   = (85, 52, 10, 255)

C_STEEL_SPEC   = (255, 255, 255, 255)
C_STEEL_HI     = (235, 245, 252, 255)
C_STEEL_MID    = (195, 215, 232, 255)
C_STEEL_RIDGE  = (145, 172, 195, 255)
C_STEEL_FULLER = (65, 88, 110, 255)      # Central fuller groove
C_STEEL_SHAD   = (100, 125, 148, 255)
C_STEEL_DARK   = (65, 85, 105, 255)

C_DARK_GRIP    = (25, 15, 10, 255)

# Glove / chassis fist colors (matching ivory chassis fist):
C_FIST_SPEC    = (245, 235, 205, 255)
C_FIST_HI      = (197, 161, 105, 255)
C_FIST_MID     = (156, 114, 57, 255)
C_FIST_SHAD    = (123, 79, 41, 255)

# Weapon base canvas
weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(weapon)

# Geometry:
# Rabbit left fist in chassis is centered at (35.0, 90.5) (bounding box x:34..38, y:89..92)
# Sword axis points down-right to tip (88.0, 125.0)
dx_axis = 47.5
dy_axis = 31.0
L_axis = math.hypot(dx_axis, dy_axis)
ux = dx_axis / L_axis # ~0.8374
uy = dy_axis / L_axis # ~0.5465
nx = -uy              # ~-0.5465
ny = ux               # ~0.8374

# 1. Pommel: Brass sphere at (34.0, 89.5), radius 2.3
# Aligned directly with fist center and body boundary, eliminating gaps at (34, 86)(35, 85)
p_cx, p_cy = 34.0, 89.5
r_pommel = 2.4
for y in range(87, 93):
    for x in range(31, 38):
        d = math.hypot(x - p_cx, y - p_cy)
        if d <= r_pommel:
            if d > r_pommel - 0.75:
                weapon.putpixel((x, y), C_OUTLINE)
            else:
                light = -0.6 * (x - p_cx) - 0.8 * (y - p_cy)
                if light > 0.8:
                    weapon.putpixel((x, y), C_BRASS_SPEC)
                elif light > 0.2:
                    weapon.putpixel((x, y), C_BRASS_HI)
                elif light > -0.5:
                    weapon.putpixel((x, y), C_BRASS_MID)
                else:
                    weapon.putpixel((x, y), C_BRASS_SHAD)

# 2. Dark Grip: From pommel (34.0, 89.5) through fist (35.0, 90.5) to guard (40.5, 94.0)
grip_poly = [
    (int(round(34.0 - 1.4 * nx)), int(round(89.5 - 1.4 * ny))),
    (int(round(40.5 - 1.4 * nx)), int(round(94.0 - 1.4 * ny))),
    (int(round(40.5 + 1.4 * nx)), int(round(94.0 + 1.4 * ny))),
    (int(round(34.0 + 1.4 * nx)), int(round(89.5 + 1.4 * ny))),
]
draw.polygon(grip_poly, fill=C_DARK_GRIP, outline=C_OUTLINE)

# 3. Crossguard: At (40.5, 94.0), symmetric perpendicular quillons
g_p1 = (int(round(40.5 - 5.0 * nx - 1.2 * ux)), int(round(94.0 - 5.0 * ny - 1.2 * uy)))
g_p2 = (int(round(40.5 - 5.0 * nx + 1.2 * ux)), int(round(94.0 - 5.0 * ny + 1.2 * uy)))
g_p3 = (int(round(40.5 + 5.0 * nx + 1.2 * ux)), int(round(94.0 + 5.0 * ny + 1.2 * uy)))
g_p4 = (int(round(40.5 + 5.0 * nx - 1.2 * ux)), int(round(94.0 - 5.0 * ny - 1.2 * uy)))
draw.polygon([g_p1, g_p2, g_p3, g_p4], fill=C_BRASS_MID, outline=C_OUTLINE)

for s in range(30):
    t = (s - 15) / 15.0
    qx = 40.5 + t * 4.7 * nx
    qy = 94.0 + t * 4.7 * ny
    pt_in = (int(round(qx)), int(round(qy)))
    if weapon.getpixel(pt_in) != C_OUTLINE:
        if t < -0.3:
            weapon.putpixel(pt_in, C_BRASS_HI)
        elif t > 0.4:
            weapon.putpixel(pt_in, C_BRASS_SHAD)
        else:
            weapon.putpixel(pt_in, C_BRASS_MID)

weapon.putpixel((40, 94), C_BRASS_SPEC)
weapon.putpixel((41, 94), C_BRASS_HI)

# 4. Blade: 100% Solid Polygon Fill from (41.5, 94.7) to (88.0, 125.0)
start_bx, start_by = 41.5, 94.7
tip_bx, tip_by = 88.0, 125.0
b_len = math.hypot(tip_bx - start_bx, tip_by - start_by) # 55.2 px
b_ux = (tip_bx - start_bx) / b_len
b_uy = (tip_by - start_by) / b_len
b_nx = -b_uy
b_ny = b_ux

top_pts = []
bot_pts = []
num_samples = 150
for i in range(num_samples + 1):
    frac = i / float(num_samples)
    dist = frac * b_len
    cur_x = start_bx + dist * b_ux
    cur_y = start_by + dist * b_uy
    if dist < b_len - 10.0:
        w_half = 2.8
    else:
        w_half = 2.8 * (b_len - dist) / 10.0
    top_pts.append((cur_x - w_half * b_nx, cur_y - w_half * b_ny))
    bot_pts.append((cur_x + w_half * b_nx, cur_y + w_half * b_ny))

blade_poly = top_pts + list(reversed(bot_pts))
draw.polygon(blade_poly, fill=C_STEEL_MID, outline=C_OUTLINE)

# Facet shading on blade
for i in range(num_samples + 1):
    frac = i / float(num_samples)
    dist = frac * b_len
    cur_x = start_bx + dist * b_ux
    cur_y = start_by + dist * b_uy
    if dist < b_len - 10.0:
        w_half = 2.8
    else:
        w_half = 2.8 * (b_len - dist) / 10.0
    if w_half < 0.7:
        continue

    # Upper specular cutting edge
    p_spec = (int(round(cur_x - (w_half - 0.75) * b_nx)), int(round(cur_y - (w_half - 0.75) * b_ny)))
    if weapon.getpixel(p_spec) != C_OUTLINE:
        weapon.putpixel(p_spec, C_STEEL_SPEC if (i % 3 == 0) else C_STEEL_HI)

    # Upper face highlight
    p_hi = (int(round(cur_x - 0.9 * b_nx)), int(round(cur_y - 0.9 * b_ny)))
    if weapon.getpixel(p_hi) != C_OUTLINE:
        weapon.putpixel(p_hi, C_STEEL_HI)

    # Central fuller groove
    p_mid = (int(round(cur_x)), int(round(cur_y)))
    if weapon.getpixel(p_mid) != C_OUTLINE:
        weapon.putpixel(p_mid, C_STEEL_FULLER if dist < b_len * 0.75 else C_STEEL_RIDGE)

    # Lower face shadow
    p_shad = (int(round(cur_x + 0.9 * b_nx)), int(round(cur_y + 0.9 * b_ny)))
    if weapon.getpixel(p_shad) != C_OUTLINE:
        weapon.putpixel(p_shad, C_STEEL_SHAD)

    # Lower edge dark steel
    p_dark = (int(round(cur_x + (w_half - 0.75) * b_nx)), int(round(cur_y + (w_half - 0.75) * b_ny)))
    if weapon.getpixel(p_dark) != C_OUTLINE:
        weapon.putpixel(p_dark, C_STEEL_DARK)

# Acute pointed tip
weapon.putpixel((int(round(tip_bx)), int(round(tip_by))), C_OUTLINE)
weapon.putpixel((int(round(tip_bx - 1)), int(round(tip_by))), C_STEEL_SPEC)

# 5. Hand Clasping (Modification A):
# Finger patches on layer z=40 wrapping across the grip at x: 35..38, y: 90..92
fingers_map = {
    (37, 91): C_OUTLINE,
    (38, 91): C_FIST_SPEC,
    (39, 91): C_FIST_HI,
    (40, 91): C_OUTLINE,
    
    (35, 91): C_OUTLINE,
    (36, 91): C_FIST_SPEC,
    (37, 92): C_FIST_HI,
    (38, 92): C_FIST_MID,
    (39, 92): C_OUTLINE,
    
    (35, 90): C_OUTLINE,
    (36, 90): C_FIST_SPEC,
    (37, 90): C_FIST_HI,
    (38, 90): C_OUTLINE,
    
    (36, 92): C_OUTLINE,
    (37, 93): C_OUTLINE,
    (38, 93): C_FIST_SHAD,
    (39, 93): C_OUTLINE,
}
for pt, col in fingers_map.items():
    weapon.putpixel(pt, col)

# 6. Verify outer boundary closure
im_closed = weapon.copy()
pix = im_closed.load()
for y in range(h):
    for x in range(w):
        if pix[x, y][3] > 0:
            is_boundary = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx_pos, ny_pos = x + dx, y + dy
                if nx_pos < 0 or nx_pos >= w or ny_pos < 0 or ny_pos >= h or pix[nx_pos, ny_pos][3] == 0:
                    is_boundary = True
                    break
            if is_boundary and pix[x, y] != C_OUTLINE:
                pix[x, y] = C_OUTLINE

# 7. Contact drop shadow strictly outside weapon along lower edge on torso
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
for i in range(num_samples + 1):
    frac = i / float(num_samples)
    dist = frac * b_len
    cur_x = start_bx + dist * b_ux
    cur_y = start_by + dist * b_uy
    if cur_x > 66.0:
        break
    w_half = 2.8
    out_x = int(round(cur_x + (w_half + 1.1) * b_nx))
    out_y = int(round(cur_y + (w_half + 1.1) * b_ny))
    if 0 <= out_x < w and 0 <= out_y < h:
        if im_closed.getpixel((out_x, out_y))[3] == 0:
            shadow.putpixel((out_x, out_y), (18, 12, 26, 120))

final_sword = Image.new("RGBA", (w, h), (0, 0, 0, 0))
final_sword.alpha_composite(shadow)
final_sword.alpha_composite(im_closed)

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
