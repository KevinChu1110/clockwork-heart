from PIL import Image

for target_scale, max_w, label in [(784/446, 784, "margin 8px"), (780/446, 780, "margin 10px"), (768/446, 768, "margin 16px")]:
    sc_w = int(round(446 * target_scale))
    sc_h = int(round(457 * target_scale))
    paste_x = (800 - sc_w) // 2
    paste_y = 1120 - sc_h
    print(f"{label:12s}: size=({sc_w}, {sc_h}), paste=({paste_x}, {paste_y}), margin_L={paste_x}, margin_R={800-paste_x-sc_w}")
