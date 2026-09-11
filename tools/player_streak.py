from PIL import Image
import numpy as np

im = Image.open("screenshots/proof_battle_lion_full_screen.png").convert("L")
arr = np.array(im)
h, w = im.size[1], im.size[0]

player_streaks = []
for y in range(int(h * 0.35), int(h * 0.55)):
    streak = 0
    cur_max = 0
    for x in range(260, 450):
        if arr[y, x] < 70:
            streak += 1
            if streak > cur_max:
                cur_max = streak
        else:
            streak = 0
    player_streaks.append(cur_max)

print(f"Max streak across player region (x=260..450): {max(player_streaks)} px")
