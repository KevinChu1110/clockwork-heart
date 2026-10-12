from PIL import Image
import numpy as np

im = Image.open('/opt/side/bravesoul-game/proofs/t_bfd13f08/proof_01_bubble_charging_4h.png')
w, h = im.size
arr = np.array(im, dtype=np.int32)

found = []
for y in range(0, h - 52, 2):
    for x in range(0, w - 160, 2):
        # check if (x+15, y+15) is dark bg (33, 25, 46)
        px = arr[y+15, x+15]
        if abs(px[0] - 33) < 10 and abs(px[1] - 25) < 10 and abs(px[2] - 46) < 10:
            # check if border at left (x+1, y+15) is gold (212, 173, 56)
            b_l = arr[y+15, x+1]
            b_r = arr[y+15, x+159]
            if b_l[0] > 170 and b_l[1] > 130 and b_l[2] < 90:
                if b_r[0] > 170 and b_r[1] > 130 and b_r[2] < 90:
                    found.append((x, y))

print("Found exact matches:", found)
