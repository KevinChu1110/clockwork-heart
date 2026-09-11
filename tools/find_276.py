from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")
idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/idle.png").convert("RGBA")

scale = 200.0 / 128.0
ox = 224.0
oy = 248.0 # 223 + 25

# Let's search for a bounding box or set of pixels in idle that:
# when mapped to screen or counted in idle gives ~276 pixels and matching stats
# Look at the numbers from task:
# silver: 31, brown: 223 -> 31 / 276 = 11.2%, 223 / 276 = 80.8%

# Let's test all candidate bounding boxes in screen or idle:
for y_min in range(70, 85):
    for y_max in range(88, 100):
        for x_min in range(55, 68):
            for x_max in range(72, 85):
                pts = []
                for sy in range(int(oy + y_min * scale), int(oy + y_max * scale)):
                    for sx in range(int(ox + x_min * scale), int(ox + x_max * scale)):
                        # corresponding source pixel
                        tx = int((sx - ox) / scale)
                        ty = int((sy - oy) / scale)
                        if 0 <= tx < 128 and 0 <= ty < 128:
                            ir, ig, ib, ia = idle.getpixel((tx, ty))
                            if ia > 128 and ir > 195 and ig > 195 and ib > 195 and abs(ir - ib) < 40:
                                pts.append((sx, sy))
                if len(pts) == 276:
                    # check silver and brown
                    silvers = 0
                    browns = 0
                    rgbs = []
                    for sx, sy in pts:
                        sr, sg, sb = screen.getpixel((sx, sy))
                        rgbs.append((sr, sg, sb))
                        if sr > 185 and sg > 185 and sb > 185 and abs(sr - sb) < 40:
                            silvers += 1
                        if sr - sb > 50:
                            browns += 1
                    ar = sum(c[0] for c in rgbs) / 276
                    ag = sum(c[1] for c in rgbs) / 276
                    ab = sum(c[2] for c in rgbs) / 276
                    print(f"FOUND 276! box: y[{y_min},{y_max}], x[{x_min},{x_max}]: silver={silvers}, brown={browns}, avg=({ar:.1f}, {ag:.1f}, {ab:.1f})")
                    break
