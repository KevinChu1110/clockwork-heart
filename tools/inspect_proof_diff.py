from PIL import Image, ImageChops

proof = Image.open("game/assets/sprites/player/paperdoll/lion/proof_paperdoll_lion_composite.png").convert("RGBA")
comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
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
for slot, fn in slots:
    comp = Image.alpha_composite(comp, Image.open(f"{rdir}/{slot}/{fn}").convert("RGBA"))

diff = ImageChops.difference(comp, proof)
print("BBox diff:", diff.getbbox())
cnt = 0
for y in range(128):
    for x in range(128):
        dp = diff.getpixel((x, y))
        if dp != (0, 0, 0, 0):
            cnt += 1
            if cnt <= 5:
                print(f"Diff at ({x}, {y}): comp={comp.getpixel((x, y))}, proof={proof.getpixel((x, y))}")
print("Total differing pixels:", cnt)
