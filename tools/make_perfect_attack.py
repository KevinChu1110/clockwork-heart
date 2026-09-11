from PIL import Image
from typing import cast

battle_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")
bw, bh = battle_src.size
px = battle_src.load()
assert px is not None

# Clean ground halo
for y in range(116, bh):
    for x in range(bw):
        p = cast(tuple[int, int, int, int], px[x, y])
        if p[3] > 0:
            is_paw = (44 <= x <= 62 or 80 <= x <= 104) and y <= 122 and p[0] < 85 and p[1] < 85 and p[2] < 85
            if not is_paw:
                px[x, y] = (0, 0, 0, 0)

# Smoothly feather out rightmost magic blast at x >= 105
for y in range(bh):
    for x in range(bw):
        p = cast(tuple[int, int, int, int], px[x, y])
        if p[3] > 0 and x >= 102:
            fade = max(0.0, 1.0 - ((x - 102) / 14.0) ** 1.5)
            px[x, y] = (p[0], p[1], p[2], int(p[3] * fade))

# Scale to 1.02 to perfectly match idle proportion
target_w = int(round(bw * 1.02))
target_h = int(round(bh * 1.02))
scaled = battle_src.resize((target_w, target_h), Image.Resampling.LANCZOS)

out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
# Center placing
out.paste(scaled, (-2, 0), scaled)

# Clean shadow
from PIL import ImageDraw, ImageFilter
shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
draw = ImageDraw.Draw(shadow_canvas)
cx, cy, rx, ry = 62, 120, 44, 6
draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
shadow = shadow_canvas.filter(ImageFilter.GaussianBlur(0.8))

final_atk = Image.alpha_composite(shadow, out)
final_atk.save("/tmp/test_perfect_attack.png")
print("Saved /tmp/test_perfect_attack.png, bbox:", final_atk.getbbox())
