from PIL import Image
import numpy as np

im = Image.open("screenshots/proof_battle_lion_full_screen.png").convert("L")
arr = np.array(im)
h, w = im.size[1], im.size[0]

max_streak = 0
for y in range(int(h * 0.35), int(h * 0.55)):
    streak = 0
    cur_max = 0
    for x in range(w):
        if arr[y, x] < 70:
            streak += 1
            if streak > cur_max:
                cur_max = streak
        else:
            streak = 0
    if cur_max > max_streak:
        max_streak = cur_max

print(f"Max dark streak across any row in 35%-55% height: {max_streak} px")
