from PIL import Image

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

c_bbox = comp.getbbox()
print("comp512 bbox:", c_bbox)
char_crop = comp.crop(c_bbox)
print("char_crop size:", char_crop.size)

sh_scale = 1000.0 / char_crop.height
sc_w = int(round(char_crop.width * sh_scale))
sc_h = int(round(char_crop.height * sh_scale))
print(f"sh_scale={sh_scale:.4f}, sc_w={sc_w}, sc_h={sc_h}")

sc_paste_x = (800 - sc_w) // 2
sc_paste_y = 1120 - sc_h
print(f"sc_paste_x={sc_paste_x}, sc_paste_y={sc_paste_y}")
print(f"Right edge reaches: {sc_paste_x + sc_w}")
