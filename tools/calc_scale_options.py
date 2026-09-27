from PIL import Image
import numpy as np

p512 = "game/assets/sprites/player/paperdoll/hedgehog"
slots = [
    ("key", f"{p512}/winding_key/key_hedgehog_ratchet_and_pawl_cross_512.png"),
    ("curio", f"{p512}/back_curio/curio_hedgehog_spring_steel_quill_pack_512.png"),
    ("chassis", f"{p512}/chassis/chassis_hedgehog_amber_brass_default_512.png"),
    ("head", f"{p512}/head_unit/head_hedgehog_brass_tuning_fork_ears_512.png"),
    ("costume", f"{p512}/costume/costume_hedgehog_marionette_tailor_vest_512.png"),
    ("core", f"{p512}/optic_core/face_hedgehog_watchmaker_precision_loupe_512.png"),
    ("weapon", f"{p512}/weapon/weapon_hedgehog_ratchet_needle_dart_512.png"),
]

comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for name, path in slots:
    img = Image.open(path).convert("RGBA")
    comp.alpha_composite(img)

char_crop = comp.crop(comp.getbbox())
w, h = char_crop.size

for scale_target_w in [760, 780, 784, 750, 700]:
    scale_w = scale_target_w / w
    sc_w = int(round(w * scale_w))
    sc_h = int(round(h * scale_w))
    paste_x = (800 - sc_w) // 2
    paste_y = 1120 - sc_h
    print(f"target_w={scale_target_w}: sc_w={sc_w}, sc_h={sc_h}, paste_x={paste_x}, paste_y={paste_y}, margin_L={paste_x}, margin_R={800 - paste_x - sc_w}")

print("\nIf target_h:")
for scale_target_h in [950, 900, 850, 820, 800]:
    scale_h = scale_target_h / h
    sc_w = int(round(w * scale_h))
    sc_h = int(round(h * scale_h))
    paste_x = (800 - sc_w) // 2
    paste_y = 1120 - sc_h
    margin_L = paste_x
    margin_R = 800 - paste_x - sc_w
    print(f"target_h={scale_target_h}: sc_w={sc_w}, sc_h={sc_h}, paste_x={paste_x}, paste_y={paste_y}, margin_L={margin_L}, margin_R={margin_R}")
