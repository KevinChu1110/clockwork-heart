from PIL import Image
import numpy as np

im = Image.open("screenshots/proof_battle_full_screen.png")
lim = im.convert("L")
arr = np.array(lim)
h, w = im.size[1], im.size[0]
for y in range(h):
    cnt = (arr[y, :] < 70).sum()
    if cnt > w * 0.35 and 0.35 <= y / float(h) <= 0.55:
        print(f"Rabbit full screen y={y}: count={cnt}")
print("Rabbit check done. Max count in 35-55%:", max((arr[y, :] < 70).sum() for y in range(int(h*0.35), int(h*0.55))))
