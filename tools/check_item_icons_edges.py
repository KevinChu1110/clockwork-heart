#!/usr/bin/env python3
import glob
from PIL import Image
import numpy as np

def main():
    files = sorted(glob.glob("/opt/side/bravesoul-game/game/assets/icons/items/*.png"))
    print(f"Checking {len(files)} files...")
    all_pass = True
    for f in files:
        im = Image.open(f).convert("RGBA")
        arr = np.array(im)
        alpha = arr[:, :, 3]
        h, w = alpha.shape
        top128 = int(np.sum(alpha[0, :] > 128))
        bottom128 = int(np.sum(alpha[h-1, :] > 128))
        left128 = int(np.sum(alpha[:, 0] > 128))
        right128 = int(np.sum(alpha[:, w-1] > 128))
        total_edge128 = top128 + bottom128 + left128 + right128

        top0 = int(np.sum(alpha[0, :] > 0))
        bottom0 = int(np.sum(alpha[h-1, :] > 0))
        left0 = int(np.sum(alpha[:, 0] > 0))
        right0 = int(np.sum(alpha[:, w-1] > 0))
        total_edge0 = top0 + bottom0 + left0 + right0

        bbox = im.getbbox()
        name = f.split("/")[-1]
        status = "OK" if total_edge128 == 0 else "FAIL"
        if total_edge128 != 0:
            all_pass = False
        if top0 > 0:
            print(f"  {name} top row alphas: {alpha[0, alpha[0, :] > 0].tolist()}")
        print(f"[{status}] {name:20s}: edge_opaque(>128)={total_edge128} (T:{top128} B:{bottom128} L:{left128} R:{right128}), edge_any(>0)={total_edge0} (T:{top0} B:{bottom0} L:{left0} R:{right0}), bbox={bbox}")

    if all_pass:
        print("\nALL 12 ICONS PASSED EDGE OPAQUE CHECK (0 edge pixels > 128)!")
        return 0
    else:
        print("\nFAILURES DETECTED!")
        return 1

if __name__ == "__main__":
    exit(main())
