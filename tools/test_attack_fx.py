from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from scipy.ndimage import binary_fill_holes, label

# Let's test different arcs for attack fx
from build_chameleon_combat_poses import key_attack, warped_attack, bow_attack, enforce_ground_shadow

base_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
base_canvas = Image.alpha_composite(base_canvas, key_attack)
base_canvas = Image.alpha_composite(base_canvas, warped_attack)
base_canvas = Image.alpha_composite(base_canvas, bow_attack)

for test_start, test_end in [(295, 65), (300, 60), (310, 50), (280, 45)]:
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    a_draw.line([(48, 65), (122, 56)], fill=(56, 160, 255, 245), width=2)
    a_draw.line([(58, 64), (122, 55)], fill=(255, 255, 255, 255), width=1)
    a_draw.arc([72, 38, 122, 84], start=test_start, end=test_end, fill=(255, 94, 138, 230), width=2)
    a_draw.arc([78, 42, 120, 80], start=test_start+10, end=test_end-10, fill=(255, 208, 40, 240), width=2)
    a_draw.arc([84, 46, 118, 76], start=test_start+20, end=test_end-20, fill=(78, 216, 106, 255), width=1)
    for pt in [(118, 42), (122, 54), (120, 68), (114, 78), (106, 36), (98, 30)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))
    canvas = Image.alpha_composite(base_canvas, atk_fx)
    res = enforce_ground_shadow(canvas)
    arr = np.array(res)
    alpha = arr[:, :, 3]
    filled = binary_fill_holes(alpha > 10)
    holes = filled & (alpha <= 10)
    lbl, num = label(holes)
    max_c = 0
    for i in range(1, num + 1):
        cnt = np.sum(lbl == i)
        if cnt > max_c:
            max_c = cnt
    print(f"Angles ({test_start}, {test_end}): total_holes={np.sum(holes):3d}, max_cluster={max_c:3d}")
