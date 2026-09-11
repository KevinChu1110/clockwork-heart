from PIL import Image

repo = "/opt/side/bravesoul-game"
r_dir = f"{repo}/game/assets/sprites/player/paperdoll/rabbit"

# Let's load the composite image used in wardrobe_dialog
# When wardrobe_dialog opens with rabbit + costume_nutcracker_guard + paint_midnight_navy:
chassis = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")
head = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
key = Image.open(f"{r_dir}/winding_key/key_classic_brass.png").convert("RGBA")
costume = Image.open(f"{r_dir}/costume/costume_nutcracker_guard.png").convert("RGBA")
optic = Image.open(f"{r_dir}/optic_core/core_cyan_emerald.png").convert("RGBA")
weapon = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")
curio = Image.open(f"{r_dir}/back_curio/curio_clockwork_pigeon.png").convert("RGBA")

# Layer order from paperdoll_slots.json:
# winding_key (5)
# back_curio (8)
# chassis (10)
# head_unit (20)
# costume (25)
# optic_core (30)
# weapon (40)

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
comp.alpha_composite(key)
comp.alpha_composite(curio)
comp.alpha_composite(chassis)
comp.alpha_composite(head)
comp.alpha_composite(costume)
comp.alpha_composite(optic)
comp.alpha_composite(weapon)

comp.save("/tmp/test_rabbit_composite.png")

# Now let's put it on the wardrobe dialog background color (OBSIDIAN_DEEP = Color(0.027, 0.024, 0.039) -> RGB(7, 6, 10))
bg = Image.new("RGBA", (128, 128), (7, 6, 10, 255))
bg.alpha_composite(comp)
bg.save("/tmp/test_rabbit_on_dark_bg.png")

# 4x zoom
zoom = bg.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST)
zoom.save("/tmp/test_rabbit_4x.png")

# Crop ears and head
ears_crop = bg.crop((35, 5, 95, 65)).resize((240, 240), getattr(Image, 'Resampling', Image).NEAREST)
ears_crop.save("/tmp/test_ears_crop.png")

# Crop hand and weapon
weapon_crop = bg.crop((30, 65, 95, 125)).resize((260, 240), getattr(Image, 'Resampling', Image).NEAREST)
weapon_crop.save("/tmp/test_weapon_crop.png")

print("Saved inspection crops successfully!")
