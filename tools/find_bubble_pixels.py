from PIL import Image
import numpy as np

im = Image.open('/opt/side/bravesoul-game/proofs/t_bfd13f08/proof_01_bubble_charging_4h.png')
# Bubble button has dark background Color(0.13, 0.10, 0.18) = (33, 25, 46) and size around 160x52
# Let's find contiguous dark patch of ~160x52 surrounded by golden border (212, 173, 56)
arr = np.array(im)
# Search rows where bubble might be:
for y in range(0, 720, 20):
    for x in range(0, 1280, 20):
        patch = arr[y:y+50, x:x+150]
        if patch.shape[0] == 50 and patch.shape[1] == 150:
            # Check if interior has dark background
            center = patch[10:40, 10:140]
            if (np.mean(center[:,:,0]) < 50 and np.mean(center[:,:,1]) < 40 and np.mean(center[:,:,2]) < 60):
                # Check top border
                top_b = patch[0:3, 10:140]
                if np.mean(top_b[:,:,0]) > 150 and np.mean(top_b[:,:,1]) > 120:
                    print(f"Candidate bubble at x={x}, y={y}")
