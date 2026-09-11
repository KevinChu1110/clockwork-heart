from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/boar_battle_idle.png")
arr = np.array(im.convert('L'))
dark = (arr < 70)
dark_counts = dark.sum(axis=1)
for y in range(im.size[1]):
    if dark_counts[y] > 50:
        print(f"y={y}: dark_pixels={dark_counts[y]} ({dark_counts[y]/im.size[0]*100:.1f}%)")
