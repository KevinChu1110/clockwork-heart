from PIL import Image

rdir = "game/assets/sprites/player/paperdoll/lion"
slots = [
    ("winding_key", "key_classic_brass.png"),
    ("back_curio", "curio_lion_fan_tail.png"),
    ("chassis", "paint_brass_gold.png"),
    ("head_unit", "ear_lion_gilded_mane.png"),
    ("costume", "costume_nutcracker_guard.png"),
    ("optic_core", "core_amber_sun.png"),
    ("weapon", "wpn_knight_lance.png"),
]
comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for slot, fn in slots:
    comp = Image.alpha_composite(comp, Image.open(f"{rdir}/{slot}/{fn}").convert("RGBA"))

comp.save(f"{rdir}/proof_paperdoll_lion_composite.png")

bg_mag = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
mag = Image.alpha_composite(bg_mag, comp)
mag.save(f"{rdir}/proof_paperdoll_lion_magenta.png")
print("Saved lion proof composite and magenta!")
