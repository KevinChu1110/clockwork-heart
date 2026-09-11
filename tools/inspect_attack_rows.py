from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png")
pix = im.load()
for y in range(48, 72):
    xs = [x for x in range(102, 124) if pix[x, y][3] > 10]
    # calculate runs in xs
    runs = []
    if xs:
        cur_run = [xs[0]]
        for x in xs[1:]:
            if x == cur_run[-1] + 1:
                cur_run.append(x)
            else:
                runs.append(cur_run)
                cur_run = [x]
        runs.append(cur_run)
    run_lens = [len(r) for r in runs]
    print(f"y={y}: xs count={len(xs)}, xs={xs if len(xs)<=10 else [xs[0],'...',xs[-1]]}, runs={run_lens}")
