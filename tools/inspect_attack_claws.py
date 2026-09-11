from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png")
pix = im.load()
print(f"Image size: {im.size}")
total_pts = 0
for x in range(100, 125):
    ys = [y for y in range(128) if pix[x, y][3] > 10]
    total_pts += len(ys)
    # calculate runs in ys
    runs = []
    if ys:
        cur_run = [ys[0]]
        for y in ys[1:]:
            if y == cur_run[-1] + 1:
                cur_run.append(y)
            else:
                runs.append(cur_run)
                cur_run = [y]
        runs.append(cur_run)
    run_lens = [len(r) for r in runs]
    print(f"x={x}: ys={ys}, runs={run_lens}")
print("Total points in x=100..124:", total_pts)
