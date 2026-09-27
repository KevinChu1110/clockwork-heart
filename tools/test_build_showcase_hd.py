from PIL import Image, ImageDraw, ImageFilter

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

comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for name, path in slots:
    img = Image.open(path).convert("RGBA")
    comp512.alpha_composite(img)

char_crop_512 = comp512.crop(comp512.getbbox())
w_orig, h_orig = char_crop_512.size
print(f"Original char_crop_512: {w_orig}x{h_orig}")

# We want sc_w <= 784 so that paste_x >= 8 (margin >= 8px on left and right)
# 800 - 2 * 8 = 784 max width!
max_w = 784
max_scale_by_w = max_w / float(w_orig)
target_scale = max_scale_by_w # ~ 1.7578

sc_w = int(round(w_orig * target_scale))
sc_h = int(round(h_orig * target_scale))
print(f"Scaled size: ({sc_w}, {sc_h})")

scaled_showcase = char_crop_512.resize((sc_w, sc_h), Image.Resampling.LANCZOS)
sc_paste_x = (800 - sc_w) // 2
sc_paste_y = 1120 - sc_h

print(f"Paste at: ({sc_paste_x}, {sc_paste_y})")
print(f"Margins: Left={sc_paste_x}, Right={800 - sc_paste_x - sc_w}, Top={sc_paste_y}, Bottom={1200 - sc_paste_y - sc_h}")

showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
sc_sdraw = ImageDraw.Draw(sc_shadow)
sc_sdraw.ellipse((400 - 180, 1120 - 18, 400 + 180, 1120 + 18), fill=(31, 26, 58, 110))
sc_shadow = sc_shadow.filter(ImageFilter.GaussianBlur(radius=10))

showcase_hd.alpha_composite(sc_shadow)
showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

showcase_hd.save("proofs/test_hedgehog_showcase_hd.png")
bbox = showcase_hd.getbbox()
print("New showcase bbox:", bbox)

# Check left crop of new showcase
crop_l = showcase_hd.crop((0, 400, 150, 750))
crop_l.save("proofs/test_hedgehog_left_edge_after.png")
