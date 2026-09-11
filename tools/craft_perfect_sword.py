import math
from PIL import Image, ImageDraw, ImageFilter

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

# Canvas 128x128 RGBA
w, h = 128, 128
blade_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

# Colors
C_OUTLINE = (44, 28, 22, 255)       # #2C1C16
C_STEEL_HI = (255, 255, 255, 255)   # Specular
C_STEEL_L1 = (235, 244, 250, 255)   # Bright facet
C_STEEL_L2 = (205, 222, 235, 255)   # Mid facet
C_STEEL_L3 = (165, 185, 202, 255)   # Lower bright
C_STEEL_D1 = (112, 136, 154, 255)   # Shadow facet
C_STEEL_D2 = (84, 108, 126, 255)    # Deep shadow
C_STEEL_D3 = (56, 76, 92, 255)      # Core shadow

C_GOLD_HI = (255, 236, 150, 255)    # Gold specular
C_GOLD_M1 = (240, 196, 50, 255)     # Gold light
C_GOLD_M2 = (210, 156, 28, 255)     # Gold mid
C_GOLD_D1 = (150, 102, 18, 255)     # Gold dark
C_GOLD_D2 = (95, 60, 14, 255)       # Gold shadow

C_LEATHER_L = (140, 95, 55, 255)    # Grip wrap
C_LEATHER_D = (75, 48, 28, 255)     # Grip shadow

# Gauntlet fingers holding hilt (matching Whitey's hand colors):
C_GAUNTLET_HI = (250, 246, 240, 255)
C_GAUNTLET_M  = (225, 212, 195, 255)
C_GAUNTLET_D  = (175, 155, 135, 255)
C_GAUNTLET_GOLD = (230, 185, 45, 255)

# 1. Contact shadow under the sword onto torso/costume
# Shadow layer will be drawn first
shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow_layer)

# Shadow line along the sword blade offset by (dx=1, dy=2)
# Blade axis: from (47, 85) to (88, 124)
for t in range(0, 42):
    frac = t / 41.0
    bx = 47.0 + frac * (87.0 - 47.0)
    by = 85.0 + frac * (123.0 - 85.0)
    # Cast shadow under blade onto chest/hip
    # Radius ~ 2-3px, soft alpha
    for sx in range(-1, 3):
        for sy in range(1, 4):
            px, py = int(bx + sx), int(by + sy)
            if 0 <= px < w and 0 <= py < h:
                # deeper shadow near crossguard, softer near tip
                alpha = int((1.0 - frac * 0.4) * 110)
                cur_a = shadow_layer.getpixel((px, py))[3]
                if alpha > cur_a:
                    shadow_layer.putpixel((px, py), (20, 14, 28, alpha))

# Blur shadow slightly for natural contact shadow
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(0.6))

# 2. Main sword drawing
sword_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
s_pix = sword_layer.load()

# Pommel: spherical golden brass at (36, 73)
# Draw 5x5 spherical brass ball
pommel_pixels = {
    (36, 71): C_OUTLINE, (37, 71): C_OUTLINE, (38, 71): C_OUTLINE,
    (35, 72): C_OUTLINE, (36, 72): C_GOLD_HI, (37, 72): C_GOLD_M1, (38, 72): C_GOLD_M2, (39, 72): C_OUTLINE,
    (34, 73): C_OUTLINE, (35, 73): C_GOLD_HI, (36, 73): C_GOLD_HI, (37, 73): C_GOLD_M1, (38, 73): C_GOLD_D1, (39, 73): C_OUTLINE,
    (34, 74): C_OUTLINE, (35, 74): C_GOLD_M1, (36, 74): C_GOLD_M1, (37, 74): C_GOLD_M2, (38, 74): C_GOLD_D1, (39, 74): C_OUTLINE,
    (35, 75): C_OUTLINE, (36, 75): C_GOLD_M2, (37, 75): C_GOLD_D1, (38, 75): C_GOLD_D2, (39, 75): C_OUTLINE,
    (36, 76): C_OUTLINE, (37, 76): C_OUTLINE, (38, 76): C_OUTLINE,
}
for (px, py), col in pommel_pixels.items():
    s_pix[px, py] = col

# Grip: between pommel and crossguard (y: 76..81, x: 38..42)
# Wrapped grip with segments
grip_pixels = {
    (38, 76): C_OUTLINE, (39, 76): C_LEATHER_L, (40, 76): C_LEATHER_D, (41, 76): C_OUTLINE,
    (39, 77): C_OUTLINE, (40, 77): C_GOLD_M1,   (41, 77): C_LEATHER_L, (42, 77): C_OUTLINE,
    (39, 78): C_OUTLINE, (40, 78): C_LEATHER_L, (41, 78): C_LEATHER_D, (42, 78): C_OUTLINE,
    (40, 79): C_OUTLINE, (41, 79): C_GOLD_M1,   (42, 79): C_LEATHER_L, (43, 79): C_OUTLINE,
    (40, 80): C_OUTLINE, (41, 80): C_LEATHER_L, (42, 80): C_LEATHER_D, (43, 80): C_OUTLINE,
    (41, 81): C_OUTLINE, (42, 81): C_GOLD_M1,   (43, 81): C_LEATHER_D, (44, 81): C_OUTLINE,
}
for (px, py), col in grip_pixels.items():
    s_pix[px, py] = col

# Crossguard: straight brass bar perpendicular to blade (y: 81..85, x: 42..48)
crossguard_pixels = {
    # Upper quill / tip
    (45, 78): C_OUTLINE,
    (44, 79): C_OUTLINE, (45, 79): C_GOLD_HI, (46, 79): C_OUTLINE,
    (44, 80): C_OUTLINE, (45, 80): C_GOLD_M1, (46, 80): C_GOLD_M2, (47, 80): C_OUTLINE,
    (43, 81): C_OUTLINE, (44, 81): C_GOLD_HI, (45, 81): C_GOLD_M1, (46, 81): C_GOLD_D1, (47, 81): C_OUTLINE,
    # Center block
    (43, 82): C_OUTLINE, (44, 82): C_GOLD_HI, (45, 82): C_GOLD_M1, (46, 82): C_GOLD_D1, (47, 82): C_OUTLINE,
    (42, 83): C_OUTLINE, (43, 83): C_GOLD_HI, (44, 83): C_GOLD_M1, (45, 83): C_GOLD_D1, (46, 83): C_GOLD_D2, (47, 83): C_OUTLINE,
    (41, 84): C_OUTLINE, (42, 84): C_GOLD_M1, (43, 84): C_GOLD_M1, (44, 84): C_GOLD_D1, (45, 84): C_GOLD_D2, (46, 84): C_OUTLINE,
    # Lower quill / tip
    (41, 85): C_OUTLINE, (42, 85): C_GOLD_M2, (43, 85): C_GOLD_D2, (44, 85): C_OUTLINE,
    (40, 86): C_OUTLINE, (41, 86): C_GOLD_D2, (42, 86): C_OUTLINE,
    (40, 87): C_OUTLINE,
}
for (px, py), col in crossguard_pixels.items():
    s_pix[px, py] = col

# Blade: 3-4 px wide with upper bright facet, central ridge, lower shadow facet, dark outline
# Extends from crossguard (x=46, y=85) to tip (x=88, y=124)
# Let's map out the blade precisely along the diagonal:
for step in range(0, 42):
    t = step / 41.0
    # Centerline of the blade:
    cx = 47.0 + t * 40.5
    cy = 85.0 + t * 38.5
    
    # Normal vector perpendicular to diagonal (approx (-0.69, 0.72))
    # Upper-left is (cx - 1.4, cy - 1.4) or similar
    # In pixel grid along diagonal (dx ~ 1, dy ~ 1):
    # Perpendicular direction is roughly (-1, 1) or (+1, -1)
    ix, iy = int(round(cx)), int(round(cy))
    
    # Near the tip, taper down to 1 point
    if step >= 39:
        # Tip
        if step == 41:
            s_pix[ix, iy] = C_OUTLINE
            s_pix[ix-1, iy] = C_STEEL_HI
        elif step == 40:
            s_pix[ix, iy] = C_STEEL_HI
            s_pix[ix+1, iy] = C_OUTLINE
            s_pix[ix, iy-1] = C_STEEL_L1
            s_pix[ix-1, iy] = C_OUTLINE
        else:
            s_pix[ix-1, iy-1] = C_OUTLINE
            s_pix[ix, iy-1] = C_STEEL_HI
            s_pix[ix+1, iy-1] = C_STEEL_L1
            s_pix[ix-1, iy] = C_STEEL_L2
            s_pix[ix, iy] = C_STEEL_D1
            s_pix[ix+1, iy] = C_OUTLINE
    else:
        # Normal blade section:
        # Top-left outline
        s_pix[ix - 2, iy - 1] = C_OUTLINE
        s_pix[ix - 1, iy - 2] = C_OUTLINE
        
        # Upper facet (specular & bright steel)
        s_pix[ix - 1, iy - 1] = C_STEEL_HI
        s_pix[ix, iy - 1] = C_STEEL_L1
        
        # Centerline / ridge
        s_pix[ix - 1, iy] = C_STEEL_L2
        s_pix[ix, iy] = C_STEEL_D1
        
        # Lower facet (shadow & steel depth)
        s_pix[ix + 1, iy] = C_STEEL_D2
        s_pix[ix, iy + 1] = C_STEEL_D2
        
        # Bottom-right outline
        s_pix[ix + 1, iy + 1] = C_OUTLINE
        s_pix[ix + 2, iy] = C_OUTLINE

# 3. Hand fingers wrapping around the grip!
# Hand position is at x=38..44, y=76..82
# The rabbit's mechanical paw fingers wrap OVER the front of the hilt
# Curling fingers grasping the hilt firmly:
finger_pixels = {
    # Index finger curling around hilt at y=77..78
    (39, 77): C_OUTLINE, (40, 77): C_GAUNTLET_HI, (41, 77): C_GAUNTLET_M, (42, 77): C_OUTLINE,
    # Middle finger curling around hilt at y=79..80
    (40, 79): C_OUTLINE, (41, 79): C_GAUNTLET_HI, (42, 79): C_GAUNTLET_M, (43, 79): C_OUTLINE,
    # Ring/little finger at y=81
    (41, 81): C_OUTLINE, (42, 81): C_GAUNTLET_HI, (43, 81): C_GAUNTLET_M, (44, 81): C_OUTLINE,
    # Thumb pressing from the side/top at y=76..77, x=37..39
    (37, 76): C_OUTLINE, (38, 76): C_GAUNTLET_HI, (39, 76): C_GAUNTLET_M, (40, 76): C_OUTLINE,
    # Brass joint accent on knuckles
    (41, 78): C_GAUNTLET_GOLD,
    (42, 80): C_GAUNTLET_GOLD,
}
for (px, py), col in finger_pixels.items():
    s_pix[px, py] = col

# Merge shadow and sword
final_weapon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
final_weapon.alpha_composite(shadow_layer)
final_weapon.alpha_composite(sword_layer)

final_weapon.save("/tmp/new_crafted_blade.png")
print("Crafted new weapon successfully, bbox:", final_weapon.getbbox())

# Test composite with rabbit chassis, costume, head, optic, key
comp_ivory = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp_ivory.alpha_composite(Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA"))
comp_ivory.alpha_composite(Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA"))
comp_ivory.alpha_composite(Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA"))
comp_ivory.alpha_composite(Image.open("/tmp/ear_wrapped.png").convert("RGBA"))
comp_ivory.alpha_composite(Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA"))
comp_ivory.alpha_composite(Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA"))
comp_ivory.alpha_composite(final_weapon)

dark_comp = Image.new("RGBA", (w, h), (7, 6, 10, 255))
dark_comp.alpha_composite(comp_ivory)
dark_comp.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/new_rabbit_composite_4x.png")

# Crop weapon area for close-up vision inspection
crop = dark_comp.crop((30, 65, 95, 125)).resize((325, 300), getattr(Image, 'Resampling', Image).NEAREST)
crop.save("/tmp/new_weapon_hand_crop.png")

print("Saved new composite and crop for vision analysis!")
