import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"

# Colors according to CANON and Whitey/Macaque palette
C_OUTLINE = (35, 22, 18, 255)
C_BRASS_HI = (255, 225, 80, 255)
C_BRASS_MID = (215, 160, 30, 255)
C_BRASS_SHAD = (145, 95, 18, 255)
C_STEEL_SPEC = (255, 255, 250, 255)
C_STEEL_HI = (235, 235, 240, 255)
C_STEEL_MID = (180, 185, 195, 255)
C_STEEL_SHAD = (110, 115, 130, 255)
C_STEEL_DARK = (65, 68, 80, 255)

def build_paperdoll_idle_claws() -> Image.Image:
    """
    Builds the 128x128 weapon layer for macaque idle paperdoll:
    game/assets/sprites/player/paperdoll/macaque/weapon/wpn_spring_claws.png
    Left hand (screen left): around x=24..37, y=70..85 -> claws extend to y=104
    Right hand (screen right): around x=64..77, y=70..85 -> claws extend to y=104
    """
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Function to draw one 3-claw gauntlet facing downward/forward
    def draw_gauntlet(cx: int, cy: int, flip: bool = False):
        # cx, cy is the knuckle center
        # We draw 3 curved claws: outer, middle, inner
        claw_offsets = [-5, 0, 5] if not flip else [5, 0, -5]
        
        # 1. Gauntlet base / bracket over wrist
        bx0, by0 = cx - 7, cy - 8
        bx1, by1 = cx + 7, cy + 1
        # Housing base
        draw.rectangle([bx0, by0, bx1, by1], fill=C_BRASS_MID, outline=C_OUTLINE)
        # Highlight and rivets
        draw.line([bx0 + 2, by0 + 1, bx1 - 2, by0 + 1], fill=C_BRASS_HI)
        draw.line([bx0 + 2, by1 - 1, bx1 - 2, by1 - 1], fill=C_BRASS_SHAD)
        # Spring / coil detail
        draw.rectangle([cx - 3, cy - 6, cx + 3, cy - 2], fill=C_STEEL_MID, outline=C_OUTLINE)
        draw.point((cx - 1, cy - 4), fill=C_STEEL_SPEC)

        # 2. Draw 3 distinct curved claw blades
        for i, off in enumerate(claw_offsets):
            root_x = cx + off
            root_y = cy
            # Claw curve: curves down and slightly outward
            # claw length ~20px (1.5x hand width 13px)
            curve_dx = off * 1.2
            tip_x = int(root_x + curve_dx)
            tip_y = root_y + (22 if i == 1 else 19)

            # Blade polygon (base width 3px, tapering to 1px tip)
            p1 = (root_x - 1, root_y)
            p2 = (root_x + 1, root_y)
            mid_x = root_x + int(curve_dx * 0.4)
            mid_y = root_y + 10
            p3 = (tip_x, tip_y)

            # Draw blade with outline
            draw.polygon([p1, p2, p3], fill=C_STEEL_HI, outline=C_OUTLINE)
            # Blade edge specular highlight
            draw.line([(root_x, root_y + 1), (mid_x, mid_y), (tip_x, tip_y - 1)], fill=C_STEEL_SPEC)
            # Socket ring
            draw.rectangle([root_x - 2, root_y - 1, root_x + 2, root_y + 2], fill=C_BRASS_HI, outline=C_OUTLINE)

    # Draw left and right gauntlets
    # Left hand center: x=30, y=78
    draw_gauntlet(30, 78, flip=False)
    # Right hand center: x=71, y=78
    draw_gauntlet(71, 78, flip=True)

    return img

if __name__ == "__main__":
    claws_img = build_paperdoll_idle_claws()
    bbox = claws_img.getbbox()
    print("Idle claws bbox:", bbox)
    opaque = sum(1 for p in claws_img.getdata() if p[3] > 8)
    print("Idle claws opaque pixels:", opaque)
