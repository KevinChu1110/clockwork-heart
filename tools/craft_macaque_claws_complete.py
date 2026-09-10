import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"

# Colors
C_OUTLINE = (35, 22, 18, 255)
C_BRASS_HI = (255, 225, 80, 255)
C_BRASS_MID = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)
C_STEEL_SPEC = (255, 255, 250, 255)
C_STEEL_HI = (235, 235, 240, 255)
C_STEEL_MID = (180, 185, 195, 255)
C_STEEL_SHAD = (110, 115, 130, 255)
C_STEEL_DARK = (65, 68, 80, 255)

def build_idle_paperdoll_claws() -> Image.Image:
    """
    Builds the 128x128 weapon layer for macaque idle paperdoll:
    game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png
    """
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def draw_gauntlet(cx: int, cy: int, flip: bool = False):
        claw_offsets = [-5, 0, 5] if not flip else [5, 0, -5]
        
        # 1. Gauntlet bracket over wrist
        bx0, by0 = cx - 7, cy - 8
        bx1, by1 = cx + 7, cy + 1
        draw.rectangle([bx0, by0, bx1, by1], fill=C_BRASS_MID, outline=C_OUTLINE)
        draw.line([bx0 + 2, by0 + 1, bx1 - 2, by0 + 1], fill=C_BRASS_HI)
        draw.line([bx0 + 2, by1 - 1, bx1 - 2, by1 - 1], fill=C_BRASS_SHAD)
        # Clockwork spring mechanism housing
        draw.rectangle([cx - 3, cy - 6, cx + 3, cy - 2], fill=C_STEEL_MID, outline=C_OUTLINE)
        draw.point((cx - 1, cy - 4), fill=C_STEEL_SPEC)

        # 2. Draw 3 distinct curved claw blades
        for i, off in enumerate(claw_offsets):
            root_x = cx + off
            root_y = cy
            curve_dx = off * 1.3
            tip_x = int(root_x + curve_dx)
            tip_y = root_y + (23 if i == 1 else 20)

            # Curved claw blade polygon
            p1 = (root_x - 1, root_y)
            p2 = (root_x + 1, root_y)
            mid_x = root_x + int(curve_dx * 0.4)
            mid_y = root_y + 11
            p3 = (tip_x, tip_y)

            draw.polygon([p1, p2, p3], fill=C_STEEL_HI, outline=C_OUTLINE)
            draw.line([(root_x, root_y + 1), (mid_x, mid_y), (tip_x, tip_y - 1)], fill=C_STEEL_SPEC)
            # Brass claw socket bracket
            draw.rectangle([root_x - 2, root_y - 1, root_x + 2, root_y + 2], fill=C_BRASS_HI, outline=C_OUTLINE)

    # Left hand center: x=30, y=78
    draw_gauntlet(30, 78, flip=False)
    # Right hand center: x=71, y=78
    draw_gauntlet(71, 78, flip=True)

    return img

def build_attack_pose_with_claws() -> tuple[Image.Image, Image.Image]:
    """
    Builds the attack pose:
    Returns (composite_attack_pose, attack_weapon_layer_only)
    """
    base_atk = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
    weapon_layer = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw_wep = ImageDraw.Draw(weapon_layer)

    # 1. Forward punching hand (screen right, around x=85..101, y=52..68)
    # Wrist / gauntlet housing:
    gx0, gy0 = 84, 53
    gx1, gy1 = 98, 66
    draw_wep.rectangle([gx0, gy0, gx1, gy1], fill=C_BRASS_MID, outline=C_OUTLINE)
    draw_wep.line([gx0 + 2, gy0 + 1, gx1 - 2, gy0 + 1], fill=C_BRASS_HI)
    draw_wep.line([gx0 + 2, gy1 - 1, gx1 - 2, gy1 - 1], fill=C_BRASS_SHAD)
    # Clockwork spring chamber
    draw_wep.rectangle([88, 56, 94, 63], fill=C_STEEL_MID, outline=C_OUTLINE)
    draw_wep.line([91, 57, 91, 62], fill=C_STEEL_SPEC)

    # 3 Forward Curved Claw Blades:
    # Upper claw:
    # base: (97, 54), tip: (120, 51)
    # Middle claw:
    # base: (100, 59), tip: (122, 59)
    # Lower claw:
    # base: (97, 65), tip: (120, 69)

    # Claw 1 (Upper)
    c1_base_top = (97, 53)
    c1_base_bot = (97, 56)
    c1_mid = (109, 53)
    c1_tip = (120, 50)
    draw_wep.polygon([c1_base_top, c1_base_bot, (c1_mid[0], c1_mid[1] + 1), c1_tip, c1_mid], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.line([(98, 54), c1_mid, (119, 50)], fill=C_STEEL_SPEC)
    draw_wep.rectangle([96, 52, 99, 57], fill=C_BRASS_HI, outline=C_OUTLINE)

    # Claw 2 (Middle)
    c2_base_top = (100, 58)
    c2_base_bot = (100, 61)
    c2_mid = (111, 59)
    c2_tip = (122, 59)
    draw_wep.polygon([c2_base_top, c2_base_bot, (c2_mid[0], c2_mid[1] + 1), c2_tip, c2_mid], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.line([(101, 59), c2_mid, (121, 59)], fill=C_STEEL_SPEC)
    draw_wep.rectangle([98, 57, 102, 62], fill=C_BRASS_HI, outline=C_OUTLINE)

    # Claw 3 (Lower)
    c3_base_top = (97, 63)
    c3_base_bot = (97, 66)
    c3_mid = (109, 66)
    c3_tip = (120, 69)
    draw_wep.polygon([c3_base_top, c3_base_bot, (c3_mid[0], c3_mid[1] + 1), c3_tip, c3_mid], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.line([(98, 64), c3_mid, (119, 69)], fill=C_STEEL_SPEC)
    draw_wep.rectangle([96, 62, 99, 67], fill=C_BRASS_HI, outline=C_OUTLINE)

    # 2. Rear hand at waist (x=28..38, y=68..80)
    # Companion claw gauntlet
    draw_wep.rectangle([28, 69, 37, 78], fill=C_BRASS_MID, outline=C_OUTLINE)
    draw_wep.line([29, 70, 36, 70], fill=C_BRASS_HI)
    draw_wep.line([29, 77, 36, 77], fill=C_BRASS_SHAD)
    # Claws tucked along side
    draw_wep.polygon([(28, 71), (28, 73), (20, 70)], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.polygon([(28, 74), (28, 76), (19, 74)], fill=C_STEEL_HI, outline=C_OUTLINE)
    draw_wep.polygon([(28, 77), (28, 79), (20, 78)], fill=C_STEEL_HI, outline=C_OUTLINE)

    # Composite weapon layer onto base attack pose
    comp = base_atk.copy()
    comp.alpha_composite(weapon_layer)
    return comp, weapon_layer

if __name__ == "__main__":
    idle_claws = build_idle_paperdoll_claws()
    atk_pose, wep_layer = build_attack_pose_with_claws()

    print("Idle claws bbox:", idle_claws.getbbox())
    print("Attack pose bbox:", atk_pose.getbbox())
    print("Attack weapon layer bbox:", wep_layer.getbbox())

    # Measure silhouette visibility ratio and external ratio for attack pose
    base_atk = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/macaque/attack.png").convert("RGBA")
    w, h = atk_pose.size
    
    comp_px = atk_pose.load()
    wep_px = wep_layer.load()
    base_px = base_atk.load()
    assert comp_px is not None and wep_px is not None and base_px is not None

    wep_pixels = 0
    on_silhouette = 0
    external_pixels = 0

    for y in range(h):
        for x in range(w):
            wp = wep_px[x, y]
            if wp[3] > 8:
                wep_pixels += 1
                # Check external: was base_atk transparent?
                if base_px[x, y][3] <= 8:
                    external_pixels += 1
                # Check silhouette: does comp_px have a transparent neighbor in 8-neighborhood?
                has_trans_neighbor = False
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        if comp_px[nx, ny][3] <= 8:
                            has_trans_neighbor = True
                            break
                    else:
                        has_trans_neighbor = True
                        break
                if has_trans_neighbor:
                    on_silhouette += 1

    sil_ratio = (on_silhouette / float(wep_pixels)) * 100.0 if wep_pixels > 0 else 0.0
    ext_ratio = (external_pixels / float(wep_pixels)) * 100.0 if wep_pixels > 0 else 0.0

    print(f"Total attack weapon pixels: {wep_pixels}")
    print(f"Silhouette visibility ratio: {sil_ratio:.2f}% (threshold > 10%)")
    print(f"External ratio: {ext_ratio:.2f}% (threshold > 10%)")
    print(f"Max X of attack pose: {atk_pose.getbbox()[2]} (must be <= 123 for safe border)")
