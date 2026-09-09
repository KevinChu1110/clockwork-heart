#!/usr/bin/env python3
from PIL import Image, ImageChops

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar"
BG_MAGENTA = (255, 0, 255, 255)

def build_comp(ch_fn, cos_fn):
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    comp.alpha_composite(Image.open(f"{BASE}/winding_key/key_classic_brass.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{BASE}/back_curio/curio_spring_tail.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{BASE}/chassis/{ch_fn}").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{BASE}/head_unit/ear_boar_rivet_cowl.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{BASE}/costume/{cos_fn}").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{BASE}/optic_core/core_cyan_emerald.png").convert("RGBA"))
    comp.alpha_composite(Image.open(f"{BASE}/weapon/wpn_anvil_greathammer.png").convert("RGBA"))
    mag = Image.new("RGBA", (128, 128), BG_MAGENTA)
    mag.alpha_composite(comp)
    return mag

combos = [
    ("proof_paperdoll_boar_ironclad_crimson_magenta.png", "paint_molten_crimson.png", "costume_viking_ironclad.png"),
    ("proof_paperdoll_boar_ironclad_gold_magenta.png", "paint_brass_gold.png", "costume_viking_ironclad.png"),
    ("proof_paperdoll_boar_harness_crimson_magenta.png", "paint_molten_crimson.png", "costume_viking_harness.png"),
]

all_ok = True
for out_fn, ch_fn, cos_fn in combos:
    fresh = build_comp(ch_fn, cos_fn)
    saved = Image.open(f"{BASE}/{out_fn}").convert("RGBA")
    diff = ImageChops.difference(fresh, saved)
    bbox = diff.getbbox()
    print(f"Diff test for {out_fn}: bbox = {bbox}")
    if bbox is not None:
        all_ok = False

if all_ok:
    print("ALL MAGENTA PROOFS 100% IDENTICAL TO FRESH COMPOSITE (Rule 19f-3 PASS)")
else:
    print("MAGENTA PROOF MISMATCH!")
