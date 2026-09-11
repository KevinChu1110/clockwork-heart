from PIL import Image
import numpy as np

im = Image.open("screenshots/proof_battle_lion_full_screen.png").convert("L")
arr = np.array(im)
h, w = im.size[1], im.size[0]

for y in range(int(h * 0.35), int(h * 0.55)):
    streak = 0
    cur_max = 0
    start_x = 0
    best_start = 0
    for x in range(w):
        if arr[y, x] < 70:
            if streak == 0:
                start_x = x
            streak += 1
            if streak > cur_max:
                cur_max = streak
                best_start = start_x
        else:
            streak = 0
    if cur_max > 100:
        print(f"y={y}: streak={cur_max}, from x={best_start} to x={best_start+cur_max}")
