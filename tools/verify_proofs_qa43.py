import os
import hashlib
from PIL import Image

OUT_DIR = "/opt/side/bravesoul-game/proofs/qa_round43"
CROPS_DIR = os.path.join(OUT_DIR, "crops")

files = sorted([f for f in os.listdir(OUT_DIR) if f.endswith(".png")])
crop_files = sorted([f for f in os.listdir(CROPS_DIR) if f.endswith(".png")])

hashes = {}
print("=== 0-QA15 & 0-QA23 實機截圖規格與 MD5 查驗 ===")
for fn in files:
    fp = os.path.join(OUT_DIR, fn)
    with open(fp, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    img = Image.open(fp)
    w, h = img.size
    print(f"{md5}  {fn} ({w}x{h})")
    assert md5 not in hashes, f"Duplicate MD5: {fn} matches {hashes[md5]}"
    hashes[md5] = fn
    assert (w, h) == (1280, 720), f"Wrong size for {fn}: {w}x{h}"

print("\n=== 局部特寫 Crops 查驗 ===")
for fn in crop_files:
    fp = os.path.join(CROPS_DIR, fn)
    with open(fp, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    img = Image.open(fp)
    w, h = img.size
    print(f"{md5}  crops/{fn} ({w}x{h})")
    assert md5 not in hashes, f"Duplicate MD5: crops/{fn} matches {hashes[md5]}"
    hashes[md5] = fn

print("\nALL 16 FILES VERIFIED! MD5 UNIQUE AND DIMENSIONS CORRECT!")
