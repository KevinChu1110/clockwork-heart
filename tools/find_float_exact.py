from PIL import Image

im_c = Image.open("proofs/combat_feel/frame_c_damage_float.png")
im_d = Image.open("proofs/combat_feel/frame_d_break_part.png")

# 在 im_c 中搜尋帶有紅色/橘色特徵的傷害跳字像素
# 傷害顏色為 Color(1.0, 0.4, 0.35) -> 約 R>200, G in [80, 150], B in [70, 130]
pixels = im_c.load()
w, h = im_c.size
dmg_pts = []
for y in range(h):
    for x in range(w):
        r, g, b = pixels[x, y][:3]
        if r > 220 and 80 <= g <= 160 and 60 <= b <= 140:
            dmg_pts.append((x, y))

if dmg_pts:
    min_x = min(p[0] for p in dmg_pts)
    max_x = max(p[0] for p in dmg_pts)
    min_y = min(p[1] for p in dmg_pts)
    max_y = max(p[1] for p in dmg_pts)
    print(f"Found damage float pixels in im_c: x in [{min_x}, {max_x}], y in [{min_y}, {max_y}]")
    crop_dmg = im_c.crop((min_x - 30, min_y - 30, max_x + 30, max_y + 30))
    crop_dmg.save("proofs/combat_feel/exact_damage_float_crop.png")
else:
    print("No matching damage float pixels found in im_c")

# 同理在 im_d 中搜尋 BREAK 金黃色像素 (Color(1.0, 0.85, 0.15) -> R>220, G>180, B<80)
pixels_d = im_d.load()
brk_pts = []
for y in range(h):
    for x in range(w):
        r, g, b = pixels_d[x, y][:3]
        if r > 220 and g > 180 and b < 80:
            brk_pts.append((x, y))

if brk_pts:
    min_x = min(p[0] for p in brk_pts)
    max_x = max(p[0] for p in brk_pts)
    min_y = min(p[1] for p in brk_pts)
    max_y = max(p[1] for p in brk_pts)
    print(f"Found BREAK float pixels in im_d: x in [{min_x}, {max_x}], y in [{min_y}, {max_y}]")
    crop_brk = im_d.crop((min_x - 30, min_y - 30, max_x + 30, max_y + 30))
    crop_brk.save("proofs/combat_feel/exact_break_float_crop.png")
else:
    print("No matching BREAK pixels found in im_d")
