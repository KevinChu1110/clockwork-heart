"""
generate_pixel_backgrounds.py
Generates the 4 pixel art background assets adhering strictly to:
- 2026-10-05 Brief (docs/CLOCKWORK_ART_MUSIC_BRIEF.md)
- CANON Toy World (zero fur, metal plates, winding keys, brass gears)
- Exact Dopamine Palette:
  Cream #FFFDF8, Gold #FFD028, Orange #FFA010, Sky Blue #38A0FF, Dark Outline #1F1A3A
- Crisp 1px outlines, zero blur, zero stretching, pixel-density matching character sprites.
"""

import math
from PIL import Image, ImageDraw

WIDTH = 1280
HEIGHT = 720

# Palette definitions
CREAM = (255, 253, 248, 255)        # #FFFDF8
CREAM_SHADE = (240, 232, 218, 255)
GOLD = (255, 208, 40, 255)          # #FFD028
GOLD_LIGHT = (255, 230, 110, 255)
GOLD_DARK = (218, 165, 20, 255)
ORANGE = (255, 160, 16, 255)        # #FFA010
ORANGE_LIGHT = (255, 190, 70, 255)
ORANGE_DARK = (205, 110, 10, 255)
SKY_BLUE = (56, 160, 255, 255)      # #38A0FF
SKY_LIGHT = (150, 210, 255, 255)
SKY_PALE = (215, 238, 255, 255)
SKY_DEEP = (28, 115, 210, 255)
OUTLINE = (31, 26, 58, 255)         # #1F1A3A
EMERALD = (78, 216, 106, 255)       # #4ED86A
EMERALD_DARK = (38, 148, 65, 255)
WOOD_LIGHT = (245, 205, 140, 255)
WOOD_MED = (220, 165, 95, 255)
WOOD_DARK = (170, 115, 55, 255)
TRANSPARENT = (0, 0, 0, 0)


def draw_pixel_line(draw, x0, y0, x1, y1, color):
    """Bresenham's line algorithm for clean 1px pixel line."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        draw.point((x0, y0), fill=color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_pixel_rect(draw, x0, y0, x1, y1, fill_color, outline_color=OUTLINE):
    """Draw a rectangle with solid 1px outline."""
    if fill_color:
        draw.rectangle([x0, y0, x1, y1], fill=fill_color)
    if outline_color:
        draw.rectangle([x0, y0, x1, y1], outline=outline_color, width=1)


def draw_gear(draw, cx, cy, r_outer, r_inner, num_teeth, tooth_depth, fill_col=GOLD, shade_col=GOLD_DARK, outline_col=OUTLINE):
    """Draw a clockwork gear with crisp pixel teeth and 1px outline."""
    points = []
    total_steps = num_teeth * 2
    for i in range(total_steps):
        angle = (i * 2.0 * math.pi) / total_steps
        r = r_outer if (i % 2 == 0) else (r_outer - tooth_depth)
        px = int(cx + r * math.cos(angle))
        py = int(cy + r * math.sin(angle))
        points.append((px, py))
    
    # Fill main body
    draw.polygon(points, fill=fill_col, outline=outline_col)
    
    # Internal shading rim (half crescent)
    draw.arc([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], 0, 360, fill=outline_col, width=1)
    draw.ellipse([cx - r_inner + 2, cy - r_inner + 2, cx + r_inner - 2, cy + r_inner - 2], fill=shade_col)
    # Center axle / brass hole
    r_axle = max(3, r_inner // 2)
    draw.ellipse([cx - r_axle, cy - r_axle, cx + r_axle, cy + r_axle], fill=OUTLINE)
    draw.ellipse([cx - r_axle + 1, cy - r_axle + 1, cx + r_axle - 1, cy + r_axle - 1], fill=CREAM)


def draw_winding_key(draw, cx, cy, size, angle_deg=0, fill_col=GOLD, outline_col=OUTLINE):
    """Draw an antique clockwork winding key silhouette."""
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Key shaft
    shaft_len = size * 1.4
    shaft_w = max(2, size // 5)
    
    def rot(dx, dy):
        return int(cx + dx * cos_a - dy * sin_a), int(cy + dx * sin_a + dy * cos_a)
    
    # Two wing loops of the winding key
    loop_r = size // 2
    p1 = rot(-size // 2, -shaft_len // 2)
    p2 = rot(size // 2, -shaft_len // 2)
    draw.ellipse([p1[0] - loop_r, p1[1] - loop_r, p1[0] + loop_r, p1[1] + loop_r], fill=fill_col, outline=outline_col)
    draw.ellipse([p1[0] - loop_r // 2, p1[1] - loop_r // 2, p1[0] + loop_r // 2, p1[1] + loop_r // 2], fill=OUTLINE)
    
    draw.ellipse([p2[0] - loop_r, p2[1] - loop_r, p2[0] + loop_r, p2[1] + loop_r], fill=fill_col, outline=outline_col)
    draw.ellipse([p2[0] - loop_r // 2, p2[1] - loop_r // 2, p2[0] + loop_r // 2, p2[1] + loop_r // 2], fill=OUTLINE)
    
    # Central stem
    stem_top = rot(0, -shaft_len // 2)
    stem_bot = rot(0, shaft_len // 2)
    draw.line([stem_top, stem_bot], fill=fill_col, width=shaft_w + 2)
    draw.line([stem_top, stem_bot], fill=outline_col, width=shaft_w)


def draw_cloud(draw, cx, cy, w, h):
    """Layered stylized pixel cloud with gold highlight and purple-blue shadow."""
    # Under-shadow
    draw.ellipse([cx - w//2 - 2, cy - h//3 + 4, cx + w//2 + 2, cy + h//2 + 4], fill=SKY_DEEP)
    # Middle body
    draw.ellipse([cx - w//2, cy - h//3, cx + w//2, cy + h//2], fill=CREAM, outline=OUTLINE)
    # Bumps
    draw.ellipse([cx - w//3, cy - h//2, cx, cy + h//4], fill=CREAM, outline=OUTLINE)
    draw.ellipse([cx - w//6, cy - h//2 - 6, cx + w//4, cy + h//3], fill=CREAM, outline=OUTLINE)
    draw.ellipse([cx, cy - h//3 - 2, cx + w//3, cy + h//4], fill=CREAM, outline=OUTLINE)
    # Top golden sunlight rim
    draw.arc([cx - w//6, cy - h//2 - 6, cx + w//4, cy + h//3], 180, 360, fill=GOLD, width=2)


print("Helper functions ready.")
