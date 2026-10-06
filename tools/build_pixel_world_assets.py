"""
tools/build_pixel_world_assets.py
Generates:
1. game/assets/sprites/maps/sky_lobby_layer1_far.png (1280x720)
2. game/assets/sprites/maps/sky_lobby_layer2_mid.png (1280x720, RGBA)
3. game/assets/sprites/maps/sky_lobby_layer3_near.png (1280x720, RGBA)
4. game/assets/sprites/maps/battle_ruins_pixel.png (1280x720)
5. composite preview of lobby (layers 1 + 2 + 3)
"""

import math
import os
from PIL import Image, ImageDraw

WIDTH = 1280
HEIGHT = 720

# ── Palette Definitions ───────────────────────────────────────────
CREAM = (255, 253, 248, 255)          # #FFFDF8
CREAM_DARK = (242, 235, 220, 255)
CREAM_SHADOW = (222, 212, 195, 255)

GOLD = (255, 208, 40, 255)            # #FFD028
GOLD_LIGHT = (255, 232, 120, 255)
GOLD_DARK = (218, 165, 20, 255)
GOLD_SHADOW = (180, 130, 15, 255)
BRASS_DARK = (180, 135, 55, 255)

ORANGE = (255, 160, 16, 255)          # #FFA010
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_DARK = (210, 115, 10, 255)
ORANGE_SHADOW = (165, 80, 5, 255)

SKY_BLUE = (56, 160, 255, 255)        # #38A0FF
SKY_LIGHT = (145, 210, 255, 255)
SKY_PALE = (210, 235, 255, 255)
SKY_DEEP = (30, 110, 210, 255)
SKY_TOP = (20, 85, 185, 255)

OUTLINE = (31, 26, 58, 255)           # #1F1A3A
OUTLINE_SOFT = (55, 48, 92, 255)

EMERALD = (78, 216, 106, 255)         # #4ED86A
EMERALD_LIGHT = (140, 240, 160, 255)
EMERALD_DARK = (38, 148, 65, 255)

CYAN_CORE = (60, 240, 220, 255)
CYAN_GLOW = (160, 255, 245, 180)

WOOD_LIGHT = (245, 205, 140, 255)
WOOD_MED = (220, 165, 95, 255)
WOOD_DARK = (175, 115, 55, 255)
WOOD_DEEP = (125, 75, 35, 255)
WOOD_GROOVE = (65, 38, 20, 255)

TRANSPARENT = (0, 0, 0, 0)


# ── Pixel Drawing Primitives ──────────────────────────────────────
def draw_pixel_rect(draw, x0, y0, x1, y1, fill_col, outline_col=OUTLINE):
    if fill_col:
        draw.rectangle([x0, y0, x1, y1], fill=fill_col)
    if outline_col:
        draw.rectangle([x0, y0, x1, y1], outline=outline_col, width=1)


def draw_pixel_circle(draw, cx, cy, radius, fill_col, outline_col=OUTLINE):
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    if fill_col:
        draw.ellipse(bbox, fill=fill_col)
    if outline_col:
        draw.ellipse(bbox, outline=outline_col, width=1)


def draw_gear(draw, cx, cy, r_outer, r_inner, num_teeth, tooth_depth, fill_col=GOLD, shade_col=GOLD_DARK, outline_col=OUTLINE):
    points = []
    total_steps = num_teeth * 2
    for i in range(total_steps):
        angle = (i * 2.0 * math.pi) / total_steps
        r = r_outer if (i % 2 == 0) else (r_outer - tooth_depth)
        px = int(cx + r * math.cos(angle))
        py = int(cy + r * math.sin(angle))
        points.append((px, py))
    
    draw.polygon(points, fill=fill_col, outline=outline_col)
    
    # Internal ring with bevel
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], outline=outline_col, width=1)
    draw.ellipse([cx - r_inner + 2, cy - r_inner + 2, cx + r_inner - 2, cy + r_inner - 2], fill=shade_col)
    
    # Spoke cutouts
    num_spokes = 4
    spoke_r = max(4, (r_inner - 6) // 2)
    for s in range(num_spokes):
        s_ang = s * (2.0 * math.pi / num_spokes)
        spx = int(cx + (r_inner - spoke_r - 2) * math.cos(s_ang))
        spy = int(cy + (r_inner - spoke_r - 2) * math.sin(s_ang))
        draw.ellipse([spx - spoke_r, spy - spoke_r, spx + spoke_r, spy + spoke_r], fill=outline_col)
        draw.ellipse([spx - spoke_r + 1, spy - spoke_r + 1, spx + spoke_r - 1, spy + spoke_r - 1], fill=fill_col)
    
    # Axle
    r_axle = max(4, r_inner // 3)
    draw.ellipse([cx - r_axle, cy - r_axle, cx + r_axle, cy + r_axle], fill=outline_col)
    draw.ellipse([cx - r_axle + 1, cy - r_axle + 1, cx + r_axle - 1, cy + r_axle - 1], fill=CREAM)


def draw_winding_key(draw, cx, cy, size, angle_deg=0, fill_col=GOLD, outline_col=OUTLINE):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    shaft_len = int(size * 1.5)
    shaft_w = max(3, size // 4)
    
    def rot(dx, dy):
        return int(cx + dx * cos_a - dy * sin_a), int(cy + dx * sin_a + dy * cos_a)
    
    # Key loops (wings)
    loop_r = max(4, size // 2)
    p1 = rot(-int(size * 0.55), -int(shaft_len * 0.35))
    p2 = rot(int(size * 0.55), -int(shaft_len * 0.35))
    
    # Wing 1
    draw.ellipse([p1[0] - loop_r, p1[1] - loop_r, p1[0] + loop_r, p1[1] + loop_r], fill=fill_col, outline=outline_col)
    hole_r = max(2, loop_r // 2)
    draw.ellipse([p1[0] - hole_r, p1[1] - hole_r, p1[0] + hole_r, p1[1] + hole_r], fill=outline_col)
    
    # Wing 2
    draw.ellipse([p2[0] - loop_r, p2[1] - loop_r, p2[0] + loop_r, p2[1] + loop_r], fill=fill_col, outline=outline_col)
    draw.ellipse([p2[0] - hole_r, p2[1] - hole_r, p2[0] + hole_r, p2[1] + hole_r], fill=outline_col)
    
    # Key shaft
    stem_top = rot(0, -int(shaft_len * 0.45))
    stem_bot = rot(0, int(shaft_len * 0.55))
    draw.line([stem_top, stem_bot], fill=outline_col, width=shaft_w + 2)
    draw.line([stem_top, stem_bot], fill=fill_col, width=shaft_w)
    
    # Key base collar / teeth
    b1 = rot(-shaft_w, int(shaft_len * 0.45))
    b2 = rot(shaft_w, int(shaft_len * 0.45))
    draw.line([b1, b2], fill=outline_col, width=3)


def draw_cloud(draw, cx, cy, w, h):
    # Under-shadow
    draw.ellipse([cx - w//2 - 2, cy - h//3 + 4, cx + w//2 + 2, cy + h//2 + 4], fill=SKY_DEEP)
    # Cloud base
    draw.ellipse([cx - w//2, cy - h//3, cx + w//2, cy + h//2], fill=CREAM, outline=OUTLINE)
    # Puffy bubbles
    draw.ellipse([cx - int(w*0.35), cy - int(h*0.48), cx - int(w*0.05), cy + int(h*0.25)], fill=CREAM, outline=OUTLINE)
    draw.ellipse([cx - int(w*0.15), cy - int(h*0.58), cx + int(w*0.25), cy + int(h*0.3)], fill=CREAM, outline=OUTLINE)
    draw.ellipse([cx + int(w*0.1), cy - int(h*0.42), cx + int(w*0.42), cy + int(h*0.28)], fill=CREAM, outline=OUTLINE)
    # Sunlight highlight along top arc
    draw.arc([cx - int(w*0.15), cy - int(h*0.58), cx + int(w*0.25), cy + int(h*0.3)], 200, 340, fill=GOLD, width=2)
    draw.arc([cx - int(w*0.35), cy - int(h*0.48), cx - int(w*0.05), cy + int(h*0.25)], 200, 330, fill=GOLD_LIGHT, width=2)


# ── BUILD LAYER 1: 遠空浮島 ───────────────────────────────────────
def build_sky_lobby_layer1_far():
    img = Image.new("RGBA", (WIDTH, HEIGHT), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    
    # 1. Sky Gradient (Vertical stepped bands for pure pixel aesthetic)
    for y in range(HEIGHT):
        t = y / (HEIGHT * 0.8)
        t = min(1.0, max(0.0, t))
        # Gradient from SKY_TOP -> SKY_BLUE -> SKY_LIGHT -> SKY_PALE -> CREAM
        if t < 0.25:
            f = t / 0.25
            r = int(SKY_TOP[0] + (SKY_BLUE[0] - SKY_TOP[0]) * f)
            g = int(SKY_TOP[1] + (SKY_BLUE[1] - SKY_TOP[1]) * f)
            b = int(SKY_TOP[2] + (SKY_BLUE[2] - SKY_TOP[2]) * f)
        elif t < 0.6:
            f = (t - 0.25) / 0.35
            r = int(SKY_BLUE[0] + (SKY_LIGHT[0] - SKY_BLUE[0]) * f)
            g = int(SKY_BLUE[1] + (SKY_LIGHT[1] - SKY_BLUE[1]) * f)
            b = int(SKY_BLUE[2] + (SKY_LIGHT[2] - SKY_BLUE[2]) * f)
        elif t < 0.85:
            f = (t - 0.6) / 0.25
            r = int(SKY_LIGHT[0] + (SKY_PALE[0] - SKY_LIGHT[0]) * f)
            g = int(SKY_LIGHT[1] + (SKY_PALE[1] - SKY_LIGHT[1]) * f)
            b = int(SKY_LIGHT[2] + (SKY_PALE[2] - SKY_LIGHT[2]) * f)
        else:
            f = (t - 0.85) / 0.15
            r = int(SKY_PALE[0] + (CREAM[0] - SKY_PALE[0]) * f)
            g = int(SKY_PALE[1] + (CREAM[1] - SKY_PALE[1]) * f)
            b = int(SKY_PALE[2] + (CREAM[2] - SKY_PALE[2]) * f)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))
    
    # 2. Distant Whimsical Clouds
    clouds = [
        (160, 110, 140, 48),
        (380, 160, 200, 60),
        (720, 90, 160, 50),
        (960, 140, 180, 56),
        (1180, 100, 150, 46),
        (80, 260, 220, 68),
        (560, 220, 250, 72),
        (860, 270, 240, 70),
        (1120, 250, 210, 64),
    ]
    for cx, cy, w, h in clouds:
        draw_cloud(draw, cx, cy, w, h)
        
    # 3. Distant Toy Airship (Flying Winding Balloon) at x=830, y=105
    # Airship envelope
    draw.ellipse([800, 90, 880, 130], fill=ORANGE, outline=OUTLINE)
    draw.ellipse([815, 96, 865, 124], fill=CREAM, outline=OUTLINE)
    draw.line([(800, 110), (880, 110)], fill=GOLD, width=2)
    # Gondola
    draw_pixel_rect(draw, 825, 136, 855, 146, GOLD, OUTLINE)
    # Suspension ropes
    draw.line([(815, 125), (828, 136)], fill=OUTLINE, width=1)
    draw.line([(865, 125), (852, 136)], fill=OUTLINE, width=1)
    # Propeller / Winding key on back
    draw_winding_key(draw, 792, 110, 16, angle_deg=90, fill_col=GOLD)
    
    # 4. Distant Floating Islands (遠景小浮島)
    def draw_distant_island(ix, iy, iw, ih, has_tower=True, has_tree=True):
        # Island body (inverted triangle/arc)
        pts = [
            (ix - iw//2, iy),
            (ix + iw//2, iy),
            (ix + iw//3, iy + ih//2),
            (ix + 6, iy + ih),
            (ix - 8, iy + ih - 4),
            (ix - iw//3, iy + ih//2 + 4)
        ]
        # Underside rock
        draw.polygon(pts, fill=CREAM_SHADOW, outline=OUTLINE)
        # Hanging chain / brass pendulum
        draw.line([(ix, iy + ih), (ix, iy + ih + 18)], fill=OUTLINE, width=1)
        draw.ellipse([ix - 3, iy + ih + 16, ix + 3, iy + ih + 22], fill=GOLD, outline=OUTLINE)
        
        # Island grass plateau
        draw_pixel_rect(draw, ix - iw//2 - 2, iy - 6, ix + iw//2 + 2, iy + 4, EMERALD, OUTLINE)
        draw_pixel_rect(draw, ix - iw//2 + 2, iy - 4, ix + iw//2 - 2, iy - 1, EMERALD_LIGHT, None)
        
        # Miniature architectural features
        if has_tower:
            # Clock tower
            tx = ix - 8
            ty = iy - 42
            draw_pixel_rect(draw, tx, ty, tx + 16, iy - 6, CREAM, OUTLINE)
            # Conical roof
            draw.polygon([(tx - 3, ty), (tx + 8, ty - 22), (tx + 19, ty)], fill=ORANGE, outline=OUTLINE)
            # Clock face
            draw.ellipse([tx + 3, ty + 6, tx + 13, ty + 16], fill=GOLD, outline=OUTLINE)
            draw.point((tx + 8, ty + 11), fill=OUTLINE)
            # Tiny winding key on spire
            draw_winding_key(draw, tx + 8, ty - 26, 10, angle_deg=0, fill_col=GOLD)
            
        if has_tree:
            # Toy spherical trees
            trx = ix + iw//4
            try_ = iy - 20
            draw.line([(trx, iy - 6), (trx, try_ + 8)], fill=WOOD_DARK, width=2)
            draw.ellipse([trx - 10, try_ - 10, trx + 10, try_ + 10], fill=EMERALD, outline=OUTLINE)
            draw.ellipse([trx - 6, try_ - 7, trx + 2, try_ + 1], fill=EMERALD_LIGHT)
    
    # Island 1: Left distance (x=160, y=280)
    draw_distant_island(160, 290, 110, 48, has_tower=True, has_tree=True)
    # Island 2: Mid-left high (x=380, y=230)
    draw_distant_island(380, 240, 90, 40, has_tower=False, has_tree=True)
    # Island 3: Mid-right (x=910, y=260)
    draw_distant_island(910, 270, 120, 52, has_tower=True, has_tree=True)
    # Island 4: Far-right (x=1120, y=300)
    draw_distant_island(1120, 310, 100, 44, has_tower=False, has_tree=True)
    
    # 5. Distant Toy Pinwheels / Windmills on Island 2
    draw.line([(380, 234), (380, 210)], fill=OUTLINE, width=2)
    draw_gear(draw, 380, 210, 12, 5, 6, 3, fill_col=GOLD, shade_col=GOLD_DARK)
    
    return img


# ── BUILD LAYER 2: 中景城與齒輪 ───────────────────────────────────
def build_sky_lobby_layer2_mid():
    img = Image.new("RGBA", (WIDTH, HEIGHT), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    
    # 1. Grand Center Gear Halo (Behind Character, x=640, y=320)
    # Outer decorative teeth ring
    cx, cy = 640, 310
    draw_gear(draw, cx, cy, 140, 110, 24, 10, fill_col=GOLD, shade_col=GOLD_DARK, outline_col=OUTLINE)
    # Inner glowing cyan halo ring
    draw.ellipse([cx - 106, cy - 106, cx + 106, cy + 106], outline=GOLD, width=3)
    draw.ellipse([cx - 102, cy - 102, cx + 102, cy + 102], outline=CYAN_CORE, width=2)
    # Radiating radial gear spokes
    for a in range(8):
        rad = a * (math.pi / 4.0)
        p1 = (int(cx + 80 * math.cos(rad)), int(cy + 80 * math.sin(rad)))
        p2 = (int(cx + 106 * math.cos(rad)), int(cy + 106 * math.sin(rad)))
        draw.line([p1, p2], fill=OUTLINE, width=3)
        draw.line([p1, p2], fill=GOLD_LIGHT, width=1)
    # Inner clear opening so center character silhouette remains completely clear and unoccluded
    draw.ellipse([cx - 78, cy - 78, cx + 78, cy + 78], fill=TRANSPARENT)
    
    # 2. Left Side: Classical Greco-Roman Toy Pavilion & Clockwork (x=40 to 420, y=200 to 540)
    # Floating foundation landmass
    left_land = [
        (40, 420), (440, 420), (410, 480), (320, 530), (180, 520), (60, 470)
    ]
    draw.polygon(left_land, fill=CREAM_DARK, outline=OUTLINE)
    # Foundation brass gear teeth protruding from rock
    draw_gear(draw, 120, 480, 38, 16, 12, 6, fill_col=ORANGE, shade_col=ORANGE_DARK)
    draw_gear(draw, 220, 510, 28, 12, 10, 5, fill_col=GOLD, shade_col=GOLD_DARK)
    draw_gear(draw, 340, 490, 32, 14, 10, 5, fill_col=BRASS_DARK if 'BRASS_DARK' in globals() else GOLD_DARK, shade_col=GOLD_DARK)
    
    # Pavilion top base platform
    draw_pixel_rect(draw, 60, 408, 420, 422, GOLD, OUTLINE)
    
    # Greco-Roman Columns (4 fluted columns)
    col_x_list = [90, 180, 270, 360]
    for col_x in col_x_list:
        # Capital
        draw_pixel_rect(draw, col_x - 14, 286, col_x + 14, 296, GOLD, OUTLINE)
        # Column shaft
        draw_pixel_rect(draw, col_x - 10, 296, col_x + 10, 408, CREAM, OUTLINE)
        # Column vertical fluting lines
        draw.line([(col_x - 4, 297), (col_x - 4, 407)], fill=CREAM_SHADOW, width=1)
        draw.line([(col_x + 4, 297), (col_x + 4, 407)], fill=CREAM_SHADOW, width=1)
        # Base
        draw_pixel_rect(draw, col_x - 13, 400, col_x + 13, 408, GOLD, OUTLINE)
        
    # Architrave / Entablature
    draw_pixel_rect(draw, 70, 274, 380, 286, CREAM, OUTLINE)
    draw_pixel_rect(draw, 64, 266, 386, 274, GOLD, OUTLINE)
    # Triangular Classical Pediment
    pediment = [(60, 266), (225, 195), (390, 266)]
    draw.polygon(pediment, fill=CREAM, outline=OUTLINE)
    # Pediment brass trim & central clockwork emblem
    draw.line([(66, 262), (225, 199), (384, 262)], fill=GOLD, width=3)
    draw_gear(draw, 225, 238, 22, 10, 8, 4, fill_col=GOLD, shade_col=GOLD_DARK)
    draw_winding_key(draw, 225, 180, 24, angle_deg=0, fill_col=GOLD)
    
    # Interlocking Gears on Left (between columns)
    draw_gear(draw, 140, 360, 34, 15, 12, 6, fill_col=ORANGE, shade_col=ORANGE_DARK)
    draw_gear(draw, 225, 335, 42, 18, 14, 7, fill_col=GOLD, shade_col=GOLD_DARK)
    draw_gear(draw, 315, 365, 30, 14, 10, 5, fill_col=ORANGE_LIGHT, shade_col=ORANGE)
    
    # 3. Right Side: Toy Kingdom Fairytale Castle & Towers (x=840 to 1240, y=170 to 540)
    # Floating foundation landmass
    right_land = [
        (840, 420), (1240, 420), (1220, 480), (1110, 535), (960, 520), (860, 470)
    ]
    draw.polygon(right_land, fill=CREAM_DARK, outline=OUTLINE)
    # Foundation gears
    draw_gear(draw, 920, 490, 36, 16, 12, 6, fill_col=GOLD, shade_col=GOLD_DARK)
    draw_gear(draw, 1040, 515, 32, 14, 10, 5, fill_col=ORANGE, shade_col=ORANGE_DARK)
    draw_gear(draw, 1160, 475, 42, 18, 14, 7, fill_col=GOLD, shade_col=GOLD_DARK)
    
    # Main Castle Wall & Battlements
    draw_pixel_rect(draw, 880, 320, 1200, 420, CREAM, OUTLINE)
    # Brick pattern
    for by in range(330, 410, 16):
        draw.line([(882, by), (1198, by)], fill=CREAM_SHADOW, width=1)
    for bx in range(890, 1190, 32):
        draw.line([(bx, 330), (bx, 346)], fill=CREAM_SHADOW, width=1)
        draw.line([(bx + 16, 346), (bx + 16, 362)], fill=CREAM_SHADOW, width=1)
        draw.line([(bx, 362), (bx, 378)], fill=CREAM_SHADOW, width=1)
    
    # Castle Battlements (Crenellations)
    for cx_b in range(880, 1200, 24):
        draw_pixel_rect(draw, cx_b, 308, cx_b + 14, 320, CREAM, OUTLINE)
        
    # Left Spire Tower (x=900 to 950)
    draw_pixel_rect(draw, 895, 230, 945, 320, CREAM, OUTLINE)
    # Arched window
    draw_pixel_rect(draw, 912, 255, 928, 280, OUTLINE, OUTLINE)
    draw_pixel_rect(draw, 914, 257, 926, 278, SKY_BLUE, None)
    # Conical Roof (Sky Blue with Gold Trim)
    draw.polygon([(890, 230), (920, 145), (950, 230)], fill=SKY_BLUE, outline=OUTLINE)
    draw.line([(890, 230), (950, 230)], fill=GOLD, width=3)
    # Winding key finial on spire
    draw_winding_key(draw, 920, 132, 20, angle_deg=0, fill_col=GOLD)
    
    # Right Main Clock Tower (x=1120 to 1190)
    draw_pixel_rect(draw, 1115, 200, 1185, 320, CREAM, OUTLINE)
    # Giant Clock Face on tower
    draw.ellipse([1122, 215, 1178, 271], fill=CREAM, outline=OUTLINE)
    draw.ellipse([1126, 219, 1174, 267], fill=GOLD_LIGHT, outline=GOLD)
    # Clock hands
    draw.line([(1150, 243), (1150, 226)], fill=OUTLINE, width=2)
    draw.line([(1150, 243), (1162, 243)], fill=OUTLINE, width=2)
    # Tower Roof (Warm Orange Conical Spire)
    draw.polygon([(1110, 200), (1150, 110), (1190, 200)], fill=ORANGE, outline=OUTLINE)
    draw.line([(1110, 200), (1190, 200)], fill=GOLD, width=3)
    # Winding key finial on clock tower
    draw_winding_key(draw, 1150, 95, 24, angle_deg=0, fill_col=GOLD)
    
    # Waving Pennant Flags
    draw.polygon([(920, 145), (945, 155), (920, 165)], fill=ORANGE, outline=OUTLINE)
    draw.polygon([(1150, 110), (1180, 120), (1150, 130)], fill=SKY_BLUE, outline=OUTLINE)
    
    # Interlocking Gears on Right Castle
    draw_gear(draw, 1030, 360, 48, 22, 16, 8, fill_col=GOLD, shade_col=GOLD_DARK)
    draw_gear(draw, 975, 410, 34, 15, 12, 6, fill_col=ORANGE, shade_col=ORANGE_DARK)
    draw_gear(draw, 1105, 395, 30, 14, 10, 5, fill_col=GOLD_LIGHT, shade_col=GOLD)
    
    return img


# ── BUILD LAYER 3: 近景木地板 ───────────────────────────────────
def build_sky_lobby_layer3_near():
    img = Image.new("RGBA", (WIDTH, HEIGHT), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    
    # 1. Hardwood Stage Floorboards (y=530 to 720)
    floor_top_y = 535
    
    # Top brass edging rail
    draw_pixel_rect(draw, 0, floor_top_y - 6, WIDTH, floor_top_y, GOLD, OUTLINE)
    draw_pixel_rect(draw, 0, floor_top_y - 4, WIDTH, floor_top_y - 2, GOLD_LIGHT, None)
    # Screw rivets along the brass rail
    for rx in range(20, WIDTH, 36):
        draw.ellipse([rx - 2, floor_top_y - 5, rx + 2, floor_top_y - 1], fill=OUTLINE)
        draw.point((rx, floor_top_y - 3), fill=CREAM)
        
    # Horizontal wooden planks
    plank_heights = [24, 28, 32, 36, 42, 48]
    cur_y = floor_top_y
    plank_idx = 0
    
    colors_plank = [
        WOOD_LIGHT, WOOD_MED, WOOD_LIGHT, WOOD_MED, WOOD_DARK, WOOD_MED
    ]
    
    for ph in plank_heights:
        ny = min(HEIGHT, cur_y + ph)
        p_col = colors_plank[plank_idx % len(colors_plank)]
        
        # Draw plank body
        draw.rectangle([0, cur_y, WIDTH, ny], fill=p_col)
        # Groove seam line
        draw.line([(0, ny - 1), (WIDTH, ny - 1)], fill=WOOD_GROOVE, width=2)
        draw.line([(0, ny), (WIDTH, ny)], fill=OUTLINE, width=1)
        
        # Wood grain streaks (subtle parallel lines)
        grain_col = WOOD_DARK if p_col == WOOD_LIGHT else WOOD_DEEP
        for gx in range(40, WIDTH, 120):
            gy = cur_y + ph // 2
            draw.line([(gx, gy), (gx + 60, gy)], fill=grain_col, width=1)
            draw.line([(gx + 75, gy + 3), (gx + 110, gy + 3)], fill=grain_col, width=1)
            
        # Vertical board butt joints with nails
        stagger = (plank_idx * 210) % 320
        for jx in range(stagger, WIDTH, 320):
            if jx > 10:
                draw.line([(jx, cur_y), (jx, ny - 1)], fill=WOOD_GROOVE, width=2)
                draw.line([(jx, cur_y), (jx, ny - 1)], fill=OUTLINE, width=1)
                # Nails
                draw.ellipse([jx - 5, cur_y + 4, jx - 1, cur_y + 8], fill=OUTLINE)
                draw.ellipse([jx + 2, cur_y + 4, jx + 6, cur_y + 8], fill=OUTLINE)
                draw.ellipse([jx - 5, ny - 9, jx - 1, ny - 5], fill=OUTLINE)
                draw.ellipse([jx + 2, ny - 9, jx + 6, ny - 5], fill=OUTLINE)
                
        cur_y = ny
        plank_idx += 1
        if cur_y >= HEIGHT:
            break

    # 2. Stage Corner Ornaments (Brass Corner Plates with Clockwork Trim)
    # Bottom Left Corner (x=0 to 180, y=620 to 720)
    bl_poly = [(0, 720), (0, 620), (140, 720)]
    draw.polygon(bl_poly, fill=GOLD_DARK, outline=OUTLINE)
    draw.polygon([(0, 720), (0, 635), (120, 720)], fill=GOLD, outline=OUTLINE)
    draw_gear(draw, 35, 685, 24, 10, 8, 4, fill_col=GOLD_LIGHT, shade_col=GOLD)
    draw_winding_key(draw, 75, 695, 18, angle_deg=-45, fill_col=ORANGE)
    
    # Bottom Right Corner (x=1100 to 1280, y=620 to 720)
    br_poly = [(1280, 720), (1280, 620), (1140, 720)]
    draw.polygon(br_poly, fill=GOLD_DARK, outline=OUTLINE)
    draw.polygon([(1280, 720), (1280, 635), (1160, 720)], fill=GOLD, outline=OUTLINE)
    draw_gear(draw, 1245, 685, 24, 10, 8, 4, fill_col=GOLD_LIGHT, shade_col=GOLD)
    draw_winding_key(draw, 1205, 695, 18, angle_deg=45, fill_col=ORANGE)
    
    # 3. Top Stage Valance / Toy Theater Border (Corners only, subtle framing)
    # Top-Left Valance
    tl_curtain = [(0, 0), (140, 0), (110, 50), (60, 45), (0, 70)]
    draw.polygon(tl_curtain, fill=SKY_DEEP, outline=OUTLINE)
    draw.polygon([(0, 0), (125, 0), (98, 42), (52, 38), (0, 60)], fill=SKY_BLUE, outline=None)
    draw.line([(0, 60), (52, 38), (98, 42), (125, 0)], fill=GOLD, width=3)
    
    # Top-Right Valance
    tr_curtain = [(1280, 0), (1140, 0), (1170, 50), (1220, 45), (1280, 70)]
    draw.polygon(tr_curtain, fill=SKY_DEEP, outline=OUTLINE)
    draw.polygon([(1280, 0), (1155, 0), (1182, 42), (1228, 38), (1280, 60)], fill=SKY_BLUE, outline=None)
    draw.line([(1280, 60), (1228, 38), (1182, 42), (1155, 0)], fill=GOLD, width=3)

    return img


# ── BUILD BATTLE RUINS: 石徑廢墟 ──────────────────────────────────
def build_battle_ruins_pixel():
    img = Image.new("RGBA", (WIDTH, HEIGHT), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    
    # 1. Sky Gradient (Warm clear dopamine sky)
    for y in range(HEIGHT):
        t = y / (HEIGHT * 0.75)
        t = min(1.0, max(0.0, t))
        if t < 0.3:
            f = t / 0.3
            r = int(SKY_TOP[0] + (SKY_BLUE[0] - SKY_TOP[0]) * f)
            g = int(SKY_TOP[1] + (SKY_BLUE[1] - SKY_TOP[1]) * f)
            b = int(SKY_TOP[2] + (SKY_BLUE[2] - SKY_TOP[2]) * f)
        elif t < 0.7:
            f = (t - 0.3) / 0.4
            r = int(SKY_BLUE[0] + (SKY_LIGHT[0] - SKY_BLUE[0]) * f)
            g = int(SKY_BLUE[1] + (SKY_LIGHT[1] - SKY_BLUE[1]) * f)
            b = int(SKY_BLUE[2] + (SKY_LIGHT[2] - SKY_BLUE[2]) * f)
        else:
            f = (t - 0.7) / 0.3
            r = int(SKY_LIGHT[0] + (CREAM[0] - SKY_LIGHT[0]) * f)
            g = int(SKY_LIGHT[1] + (CREAM[1] - SKY_LIGHT[1]) * f)
            b = int(SKY_LIGHT[2] + (CREAM[2] - SKY_LIGHT[2]) * f)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))
        
    # Clouds
    draw_cloud(draw, 220, 110, 180, 54)
    draw_cloud(draw, 640, 90, 220, 60)
    draw_cloud(draw, 1060, 120, 190, 56)
    
    # 2. Distant Classical Ruins & Broken Pillars (y=160 to 480)
    # Background distant archway (Center, x=540 to 740, y=180 to 420)
    arch_pts = [(560, 420), (560, 240), (640, 180), (720, 240), (720, 420)]
    draw.polygon(arch_pts, fill=CREAM_DARK, outline=OUTLINE)
    # Inner opening
    inner_arch = [(590, 420), (590, 260), (640, 220), (690, 260), (690, 420)]
    draw.polygon(inner_arch, fill=SKY_LIGHT, outline=OUTLINE)
    # Gold decorative Keystone
    draw_pixel_rect(draw, 626, 172, 654, 202, GOLD, OUTLINE)
    draw_gear(draw, 640, 187, 10, 4, 6, 2, fill_col=GOLD_LIGHT, shade_col=GOLD)
    
    # Weathered Columns (Left & Right)
    # Left intact column (x=160, y=170 to 460)
    draw_pixel_rect(draw, 140, 170, 180, 182, GOLD, OUTLINE) # capital
    draw_pixel_rect(draw, 145, 182, 175, 460, CREAM, OUTLINE) # shaft
    draw.line([(152, 183), (152, 459)], fill=CREAM_SHADOW, width=1)
    draw.line([(168, 183), (168, 459)], fill=CREAM_SHADOW, width=1)
    draw_pixel_rect(draw, 138, 450, 182, 465, GOLD, OUTLINE) # base
    # Brass reinforcement ring on column
    draw_pixel_rect(draw, 143, 290, 177, 302, GOLD, OUTLINE)
    draw_gear(draw, 160, 296, 14, 6, 8, 3, fill_col=ORANGE, shade_col=ORANGE_DARK)
    
    # Left broken column (x=290, y=260 to 470)
    draw_pixel_rect(draw, 275, 270, 305, 470, CREAM, OUTLINE)
    draw.line([(282, 271), (282, 469)], fill=CREAM_SHADOW, width=1)
    draw.line([(298, 271), (298, 469)], fill=CREAM_SHADOW, width=1)
    # Jagged sheared top
    draw.polygon([(270, 270), (285, 250), (298, 274), (305, 258), (310, 270)], fill=CREAM, outline=OUTLINE)
    draw_pixel_rect(draw, 270, 456, 310, 472, GOLD, OUTLINE)
    
    # Right column cluster (x=980 to 1160)
    # Tall Column (x=1020, y=160 to 470)
    draw_pixel_rect(draw, 1000, 160, 1040, 172, GOLD, OUTLINE)
    draw_pixel_rect(draw, 1005, 172, 1035, 470, CREAM, OUTLINE)
    draw.line([(1012, 173), (1012, 469)], fill=CREAM_SHADOW, width=1)
    draw.line([(1028, 173), (1028, 469)], fill=CREAM_SHADOW, width=1)
    draw_pixel_rect(draw, 998, 455, 1042, 470, GOLD, OUTLINE)
    # Brass gear ring
    draw_pixel_rect(draw, 1003, 310, 1037, 322, GOLD, OUTLINE)
    draw_gear(draw, 1020, 316, 14, 6, 8, 3, fill_col=GOLD_LIGHT, shade_col=GOLD)
    
    # Far right broken pillar (x=1140, y=230 to 470)
    draw_pixel_rect(draw, 1125, 240, 1155, 470, CREAM, OUTLINE)
    draw.polygon([(1120, 240), (1135, 220), (1148, 244), (1160, 230)], fill=CREAM, outline=OUTLINE)
    draw_pixel_rect(draw, 1120, 455, 1160, 470, GOLD, OUTLINE)
    
    # 3. Midground Exposed Gear Mechanisms & Fallen Clockwork Relics
    # Large gear partially embedded in broken stone plinth (x=420, y=410)
    draw_gear(draw, 420, 410, 52, 22, 14, 8, fill_col=GOLD, shade_col=GOLD_DARK)
    draw_gear(draw, 490, 435, 36, 15, 12, 6, fill_col=ORANGE, shade_col=ORANGE_DARK)
    
    # Massive Fallen Antique Brass Winding Key (Center-Right, x=750, y=410)
    draw_winding_key(draw, 750, 410, 56, angle_deg=35, fill_col=GOLD)
    
    # Another smaller gear on right (x=880, y=430)
    draw_gear(draw, 880, 430, 42, 18, 12, 6, fill_col=ORANGE_LIGHT, shade_col=ORANGE)
    
    # Overgrown Toy Vines & Cheerful Flowers
    def draw_vine_cluster(vx, vy, vlen):
        draw.line([(vx, vy), (vx + 8, vy + vlen//2), (vx - 4, vy + vlen)], fill=EMERALD_DARK, width=3)
        draw.line([(vx, vy), (vx + 8, vy + vlen//2), (vx - 4, vy + vlen)], fill=EMERALD, width=2)
        # Leaves
        for lv in range(vy + 10, vy + vlen, 14):
            draw.ellipse([vx + 6, lv - 3, vx + 14, lv + 3], fill=EMERALD, outline=OUTLINE)
            # Orange/gold blossom
            if lv % 28 == 0:
                draw.ellipse([vx + 14, lv - 4, vx + 22, lv + 4], fill=ORANGE, outline=OUTLINE)
                draw.point((vx + 18, lv), fill=GOLD)
    
    draw_vine_cluster(140, 260, 90)
    draw_vine_cluster(1040, 220, 110)
    draw_vine_cluster(270, 310, 80)
    draw_vine_cluster(560, 300, 70)
    
    # 4. Foreground Paved Cobblestone Road (石徑) (y=490 to 720)
    road_top_y = 500
    
    # Transition dirt/stone verge
    draw_pixel_rect(draw, 0, road_top_y - 8, WIDTH, road_top_y, GOLD_DARK, OUTLINE)
    # Grass tufts along the road edge
    for gx in range(15, WIDTH, 32):
        draw.polygon([(gx, road_top_y), (gx + 4, road_top_y - 12), (gx + 8, road_top_y)], fill=EMERALD, outline=OUTLINE)
        draw.polygon([(gx + 6, road_top_y), (gx + 10, road_top_y - 16), (gx + 14, road_top_y)], fill=EMERALD_LIGHT, outline=OUTLINE)
        if gx % 64 == 0:
            draw.ellipse([gx + 8, road_top_y - 20, gx + 16, road_top_y - 12], fill=ORANGE, outline=OUTLINE)
            draw.point((gx + 12, road_top_y - 16), fill=GOLD)
            
    # Cobblestone Pavers Grid (Interlocking, clean, 1px outline)
    # Stone row heights increase towards foreground for perspective
    row_heights = [26, 30, 34, 40, 44, 48]
    cur_y = road_top_y
    row_idx = 0
    
    stone_colors = [
        CREAM, CREAM_DARK, CREAM_SHADOW, GOLD_LIGHT, CREAM, CREAM_DARK
    ]
    
    for rh in row_heights:
        ny = min(HEIGHT, cur_y + rh)
        # Shift stones in alternating rows
        x_shift = (row_idx * 55) % 110
        stone_w = 90 + (row_idx * 6)
        
        for sx in range(-stone_w + x_shift, WIDTH + stone_w, stone_w):
            c_idx = (row_idx * 3 + int(sx // stone_w)) % len(stone_colors)
            s_col = stone_colors[c_idx]
            
            # Rounded rectangular cobblestone
            draw.rounded_rectangle([sx + 3, cur_y + 3, sx + stone_w - 3, ny - 3], radius=6, fill=s_col, outline=OUTLINE, width=1)
            # Subtle top bevel highlight
            draw.line([(sx + 8, cur_y + 5), (sx + stone_w - 8, cur_y + 5)], fill=CREAM, width=1)
            # Subtle bottom shadow
            draw.line([(sx + 8, ny - 5), (sx + stone_w - 8, ny - 5)], fill=CREAM_SHADOW, width=1)
            
            # Scattered brass rivets and decorative gear inlays in cobblestones
            if (row_idx == 2 and sx == 420) or (row_idx == 3 and sx == 840):
                draw_gear(draw, sx + stone_w//2, cur_y + rh//2, 16, 7, 8, 3, fill_col=GOLD, shade_col=GOLD_DARK)
            elif (sx + row_idx * 17) % 73 == 0:
                # Brass screw in stone
                bx = sx + stone_w // 2
                by = cur_y + rh // 2
                draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=GOLD, outline=OUTLINE)
                draw.line([(bx - 2, by), (bx + 2, by)], fill=OUTLINE, width=1)
                
        cur_y = ny
        row_idx += 1
        if cur_y >= HEIGHT:
            break
            
    # Bottom brass road barrier/curb
    draw_pixel_rect(draw, 0, HEIGHT - 8, WIDTH, HEIGHT, GOLD, OUTLINE)
    for bx in range(24, WIDTH, 48):
        draw.ellipse([bx - 2, HEIGHT - 6, bx + 2, HEIGHT - 2], fill=OUTLINE)
        
    return img


def main():
    os.makedirs("/opt/side/bravesoul-game/game/assets/sprites/maps", exist_ok=True)
    os.makedirs("/opt/side/bravesoul-game/proofs", exist_ok=True)
    
    print("Generating Lobby Layer 1 (遠空浮島)...")
    l1 = build_sky_lobby_layer1_far()
    l1_path = "/opt/side/bravesoul-game/game/assets/sprites/maps/sky_lobby_layer1_far.png"
    l1.save(l1_path)
    print("Saved:", l1_path, l1.size)
    
    print("Generating Lobby Layer 2 (中景城與齒輪)...")
    l2 = build_sky_lobby_layer2_mid()
    l2_path = "/opt/side/bravesoul-game/game/assets/sprites/maps/sky_lobby_layer2_mid.png"
    l2.save(l2_path)
    print("Saved:", l2_path, l2.size)
    
    print("Generating Lobby Layer 3 (近景木地板)...")
    l3 = build_sky_lobby_layer3_near()
    l3_path = "/opt/side/bravesoul-game/game/assets/sprites/maps/sky_lobby_layer3_near.png"
    l3.save(l3_path)
    print("Saved:", l3_path, l3.size)
    
    print("Generating Battle Ruins (石徑廢墟)...")
    battle = build_battle_ruins_pixel()
    battle_path = "/opt/side/bravesoul-game/game/assets/sprites/battle/battle_ruins_pixel.png"
    battle.save(battle_path)
    stone_path = "/opt/side/bravesoul-game/game/assets/sprites/maps/stone_path_ruins_bg.png"
    battle.save(stone_path)
    print("Saved:", battle_path, battle.size)
    
    # Also create a combined lobby preview image
    lobby_comp = Image.alpha_composite(l1, l2)
    lobby_comp = Image.alpha_composite(lobby_comp, l3)
    comp_path = "/opt/side/bravesoul-game/proofs/test_lobby_composite_pixel.png"
    lobby_comp.save(comp_path)
    print("Saved composite lobby:", comp_path)
    
    print("ALL_PIXEL_BACKGROUNDS_BUILT_SUCCESSFULLY")

if __name__ == "__main__":
    main()
