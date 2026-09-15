from PIL import Image
import numpy as np

img = Image.open("/opt/side/bravesoul-game/screenshots/qa_round2/proof_07_battle_macaque.png")
# Check what is around (x=100..300, y=140..220) in proof_07_battle_macaque.png
arr = np.array(img)
print("Image shape:", arr.shape)

# Let's inspect rows around y=150 to y=200
# Where are pixels with color close to pure white or high brightness?
for y in range(150, 180, 5):
    row = arr[y, 50:280]
    # find x where row is white or near white
    whites = np.where((row[:,0]>240) & (row[:,1]>240) & (row[:,2]>240))[0]
    if len(whites) > 0:
        print(f"y={y}: white x from {whites[0]+50} to {whites[-1]+50}, count={len(whites)}")

# Also inspect around monkey face: where is the monkey face?
# Let's check coordinates around x=200..260, y=160..240
print("\nMonkey face region sample:")
for y in range(160, 210, 5):
    face_row = arr[y, 180:260]
    print(f"y={y}: avg rgb={face_row.mean(axis=0)[:3].astype(int)}, max rgb={face_row.max(axis=0)[:3]}")
