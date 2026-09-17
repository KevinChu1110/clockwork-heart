import os
import hashlib
from PIL import Image

files = [
    "proofs/qa_round13/proof_bear_lobby_1280x720.png",
    "proofs/qa_round13/proof_tiger_lobby_1280x720.png",
]

md5s = set()
for fn in files:
    im = Image.open(fn)
    print(f"File: {fn}")
    print(f"  Size: {im.size}, Mode: {im.mode}")
    assert im.size == (1280, 720), f"Size {im.size} is not 1280x720"
    
    # Check corners
    for coord in [(0,0), (1279,0), (0,719), (1279,719)]:
        pixel = im.getpixel(coord)
        if isinstance(pixel, tuple) and len(pixel) == 4:
            assert pixel[3] == 255, f"Corner alpha is not 255 at {coord}: {pixel}"
            
    size_kb = os.path.getsize(fn) / 1024
    print(f"  Filesize: {size_kb:.1f} KB")
    assert size_kb > 40, f"Filesize too small: {size_kb} KB"
    
    with open(fn, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
    print(f"  MD5: {h}")
    assert h not in md5s, f"Duplicate MD5: {h}"
    md5s.add(h)

print("\n✓ 0-QA15 & 0-QA18 verified successfully!")
