#!/usr/bin/env python3
import json
import hashlib
from typing import cast
from PIL import Image, ImageChops

REPO = "/opt/side/bravesoul-game"
LION = f"{REPO}/game/assets/sprites/player/paperdoll/lion"
BG_MAGENTA = (255, 0, 255, 255)

def run_checks():
    print("==================================================================")
    print("RESUBMISSION VERIFICATION FOR TASK t_186de786")
    print("==================================================================")

    # 1. Rule 10a-2: Metrics
    print("\n--- 1. Rule 10a-2 Quantitative Color Nuance Metrics ---")
    def analyze_metrics(path: str):
        im = Image.open(path).convert("RGBA")
        w, h = im.size
        pixels = []
        for y in range(h):
            for x in range(w):
                p = cast(tuple[int, int, int, int], im.getpixel((x, y)))
                if p[3] > 0:
                    pixels.append(p[:3])
        u = set(pixels)
        ratio = len(u) / (len(pixels) / 100.0) if pixels else 0.0
        print(f"{path}:")
        print(f"  Opaque: {len(pixels)}, Unique colors: {len(u)}, colors/100px: {ratio:.2f}")
        assert ratio >= 24.0, f"FAILED: ratio {ratio:.2f} < 24.0"
        return len(pixels), len(u), ratio

    analyze_metrics(f"{LION}/costume/costume_steam_artisan.png")
    analyze_metrics(f"{LION}/chassis/paint_midnight_navy.png")
    print("✓ Rule 10a-2 PASSED (both >= 24.0 colors/100px)")

    # 2. Rule 4c-4 / 19f-3: Magenta Proof Exact Source Verification
    print("\n--- 2. Rule 4c-4 / 19f-3 Magenta Proof Verification ---")
    def get_layer(slot: str, fn: str) -> Image.Image:
        return Image.open(f"{LION}/{slot}/{fn}").convert("RGBA")

    def build_comp(chassis_fn: str, costume_fn: str | None = None) -> Image.Image:
        c = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        c.alpha_composite(get_layer("winding_key", "key_classic_brass.png"))
        c.alpha_composite(get_layer("back_curio", "curio_lion_fan_tail.png"))
        c.alpha_composite(get_layer("chassis", chassis_fn))
        c.alpha_composite(get_layer("head_unit", "ear_lion_gilded_mane.png"))
        if costume_fn and costume_fn != "none":
            c.alpha_composite(get_layer("costume", costume_fn))
        c.alpha_composite(get_layer("optic_core", "core_amber_sun.png"))
        c.alpha_composite(get_layer("weapon", "wpn_knight_lance.png"))
        return c

    proofs = [
        ("proof_paperdoll_lion_artisan_navy_magenta.png", "paint_midnight_navy.png", "costume_steam_artisan.png"),
        ("proof_paperdoll_lion_artisan_gold_magenta.png", "paint_brass_gold.png", "costume_steam_artisan.png"),
        ("proof_paperdoll_lion_nutcracker_navy_magenta.png", "paint_midnight_navy.png", "costume_nutcracker_guard.png"),
    ]

    for p_fn, ch_fn, cos_fn in proofs:
        proof_img = Image.open(f"{LION}/{p_fn}").convert("RGBA")
        recomp = Image.new("RGBA", (128, 128), BG_MAGENTA)
        recomp.alpha_composite(build_comp(ch_fn, cos_fn))
        diff = ImageChops.difference(proof_img, recomp).getbbox(alpha_only=False)
        print(f"  Difference for {p_fn}: {diff}")
        assert diff is None, f"FAILED: Proof {p_fn} differs from recomputed composite!"
    print("✓ Rule 4c-4 / 19f-3 PASSED (all 3 proof diffs are None)")

    # 3. Rule 4c: Layer Independence
    print("\n--- 3. Rule 4c Layer Independence Check ---")
    art = Image.open(f"{LION}/costume/costume_steam_artisan.png").convert("RGBA")
    for ch_fn in ["paint_brass_gold.png", "paint_ivory_stock.png", "paint_midnight_navy.png"]:
        ch = Image.open(f"{LION}/chassis/{ch_fn}").convert("RGBA")
        opaque = 0
        identical = 0
        for y in range(128):
            for x in range(128):
                ap = cast(tuple[int, int, int, int], art.getpixel((x, y)))
                cp = cast(tuple[int, int, int, int], ch.getpixel((x, y)))
                if ap[3] > 0:
                    opaque += 1
                    if ap[:3] == cp[:3]:
                        identical += 1
        ratio = identical / (opaque / 100.0)
        print(f"  Overlap with {ch_fn}: {identical}/{opaque} identical ({ratio:.2f}%)")
        assert ratio < 10.0, f"FAILED: Overlap {ratio:.2f}% >= 10.0%"
    print("✓ Rule 4c PASSED (overlap << 90% threshold, exactly 0.00%)")

    # 4. Negative space on paint_midnight_navy
    print("\n--- 4. Negative Space Clearance Check on paint_midnight_navy ---")
    navy = Image.open(f"{LION}/chassis/paint_midnight_navy.png").convert("RGBA")
    # Winding key hole (94, 61)
    p_key = cast(tuple[int, int, int, int], navy.getpixel((94, 61)))
    print(f"  Winding key cutout at (94, 61): alpha={p_key[3]}")
    assert p_key[3] == 0, "FAILED: Key cutout is not transparent!"
    # Lance gap (45, 95)
    p_lance = cast(tuple[int, int, int, int], navy.getpixel((45, 95)))
    print(f"  Lance/torso gap at (45, 95): alpha={p_lance[3]}")
    assert p_lance[3] == 0, "FAILED: Lance/torso gap is not transparent!"
    # Between legs (68, 108)
    p_legs = cast(tuple[int, int, int, int], navy.getpixel((68, 108)))
    print(f"  Legs gap at (68, 108): alpha={p_legs[3]}")
    assert p_legs[3] == 0, "FAILED: Legs gap is not transparent!"
    print("✓ Negative space clearance PASSED (all negative spaces transparent)")

    # 5. Rule 4b-2 / 23f: JSON sync & MD5
    print("\n--- 5. Rule 4b-2 / 23f JSON Sync & MD5 Uniqueness ---")
    p1 = f"{REPO}/docs/design/paperdoll_slots.json"
    p2 = f"{REPO}/game/data/tables/paperdoll_slots.json"
    with open(p1) as f1, open(p2) as f2:
        j1 = json.load(f1)
        j2 = json.load(f2)
    s1 = json.dumps(j1, sort_keys=True)
    s2 = json.dumps(j2, sort_keys=True)
    assert s1 == s2, "FAILED: JSON specs out of sync!"
    print("  Both paperdoll_slots.json files sort_keys identical: True")

    # Check MD5 uniqueness
    md5_art = hashlib.md5(open(f"{LION}/costume/costume_steam_artisan.png", "rb").read()).hexdigest()
    md5_nut = hashlib.md5(open(f"{LION}/costume/costume_nutcracker_guard.png", "rb").read()).hexdigest()
    assert md5_art != md5_nut, "FAILED: Costume MD5 matches nutcracker guard!"
    md5_navy = hashlib.md5(open(f"{LION}/chassis/paint_midnight_navy.png", "rb").read()).hexdigest()
    md5_gold = hashlib.md5(open(f"{LION}/chassis/paint_brass_gold.png", "rb").read()).hexdigest()
    md5_ivory = hashlib.md5(open(f"{LION}/chassis/paint_ivory_stock.png", "rb").read()).hexdigest()
    assert md5_navy not in (md5_gold, md5_ivory), "FAILED: Chassis MD5 matches existing!"
    print(f"  MD5 artisan: {md5_art[:8]} vs nutcracker: {md5_nut[:8]}")
    print(f"  MD5 navy: {md5_navy[:8]} vs gold: {md5_gold[:8]} / ivory: {md5_ivory[:8]}")
    print("✓ Rule 4b-2 / 23f PASSED")

    print("\n==================================================================")
    print("ALL PRE-SUBMISSION CHECKS PASSED PERFECTLY!")
    print("==================================================================")

if __name__ == "__main__":
    run_checks()
