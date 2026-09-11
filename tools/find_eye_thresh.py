from PIL import Image

idle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
battle_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/fox_battle.png").convert("RGBA")

# Let's inspect eye area around (45..75, 40..65)
for name, im in [("fox_idle", idle_im), ("fox_battle", battle_im)]:
    px = im.load()
    assert px is not None
    # Let's check cyan lens pixels
    # Test different thresholds
    for thr_g, thr_r in [(150, 150), (140, 140), (130, 130), (160, 130)]:
        pts = []
        for y in range(im.height):
            for x in range(im.width):
                p = px[x, y]
                if p[3] > 80 and p[1] > thr_g and p[2] > thr_g and p[0] < thr_r:
                    pts.append((x, y))
        # split into left eye (x < 60) and right eye (x >= 60)
        l = sum(1 for x, y in pts if x < 60)
        r = sum(1 for x, y in pts if x >= 60)
        print(f"{name:10s} (G>{thr_g}, R<{thr_r}): total={len(pts)}, left={l}, right={r}")
