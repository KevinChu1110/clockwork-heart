from PIL import Image

screen_off = Image.open("/tmp/player_drawn_crop_grade_off.png").convert("RGB")
# Note: player_drawn_crop_grade_off is crop((224, 248, 424, 448))
# So in screen coordinates, (sx, sy) corresponds to (sx - 224, sy - 248) in screen_off!

idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0

y_min, y_max, x_min, x_max = 70, 96, 64, 78

pts = []
for sy in range(int(oy + y_min * scale), int(oy + y_max * scale)):
    for sx in range(int(ox + x_min * scale), int(ox + x_max * scale)):
        tx = int((sx - ox) / scale)
        ty = int((sy - oy) / scale)
        if 0 <= tx < 128 and 0 <= ty < 128:
            ir, ig, ib, ia = idle.getpixel((tx, ty))
            if ia > 128 and ir > 195 and ig > 195 and ib > 195 and abs(ir - ib) < 40:
                pts.append((sx, sy))

print(f"Points count: {len(pts)}")
silvers = 0
browns = 0
rgbs = []
for sx, sy in pts:
    # in screen_off
    lx = sx - int(ox)
    ly = sy - int(oy)
    sr, sg, sb = screen_off.getpixel((lx, ly))
    rgbs.append((sr, sg, sb))
    if sr > 185 and sg > 185 and sb > 185 and abs(sr - sb) < 40:
        silvers += 1
    if sr - sb > 50:
        browns += 1

ar = sum(c[0] for c in rgbs) / len(pts)
ag = sum(c[1] for c in rgbs) / len(pts)
ab = sum(c[2] for c in rgbs) / len(pts)
print(f"When Grade is OFF: silver={silvers}/{len(pts)} ({silvers/len(pts)*100:.1f}%), brown={browns}/{len(pts)} ({browns/len(pts)*100:.1f}%), avg=({ar:.1f}, {ag:.1f}, {ab:.1f})")
