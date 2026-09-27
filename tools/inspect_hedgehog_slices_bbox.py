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

for name, path in slots:
    img = Image.open(path)
    bbox = img.getbbox()
    print(f"{name:10s}: bbox={bbox}")
