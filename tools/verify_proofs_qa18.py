from PIL import Image
import os

proof_files = [
    "proofs/costume_512_unique/proof_wardrobe_rabbit_royal_parade.png",
    "proofs/costume_512_unique/proof_wardrobe_fox_astral_observer.png",
    "proofs/costume_512_unique/proof_wardrobe_macaque_zen_striker.png",
    "proofs/costume_512_unique/proof_wardrobe_bear_berserker_cuirass.png",
]

for p in proof_files:
    assert os.path.exists(p), f"Missing {p}"
    im = Image.open(p).convert("RGBA")
    w, h = im.size
    print(f"\n--- Checking {p} ---")
    print(f"Size: {w}x{h}")
    assert (w, h) == (1280, 720), f"Incorrect dimensions: {w}x{h}"
    
    # Check 4 corners alpha
    c_tl = im.getpixel((0, 0))
    c_tr = im.getpixel((w - 1, 0))
    c_bl = im.getpixel((0, h - 1))
    c_br = im.getpixel((w - 1, h - 1))
    print(f"Corners: TL={c_tl}, TR={c_tr}, BL={c_bl}, BR={c_br}")
    assert c_tl[3] > 0 and c_tr[3] > 0 and c_bl[3] > 0 and c_br[3] > 0, "Corner transparent!"
    
    # Check alpha ratio
    alpha_channel = im.split()[3]
    zero_alpha = sum(1 for a in alpha_channel.getdata() if a == 0)
    zero_ratio = zero_alpha / (w * h)
    print(f"Zero alpha ratio: {zero_ratio:.2%}")
    assert zero_ratio < 0.05, f"Too much transparency: {zero_ratio:.2%}"

print("\nALL 4 PROOFS PASS 0-QA18 STANDARDS!")
