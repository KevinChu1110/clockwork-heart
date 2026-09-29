from PIL import Image
SLICES=[("winding_key","winding_key/key_lynx_twin_ring_chime_brass"),
("back_curio","back_curio/curio_lynx_pendulum_bobtail_balance"),
("chassis","chassis/chassis_lynx_marionette_walnut_default"),
("head_unit","head_unit/head_lynx_bazaar_marionette_tufted_cowl"),
("costume","costume/costume_lynx_marionette_acrobat_vest"),
("optic_core","optic_core/face_lynx_emerald_quartz_eyemask"),
("weapon","weapon/weapon_lynx_dawn_marionette_steel_claws")]
B='game/assets/sprites/player/paperdoll/lynx'
rec=Image.new("RGBA",(128,128),(0,0,0,0))
for slot,rel in SLICES:
    rec.alpha_composite(Image.open(f"{B}/{rel}.png").convert("RGBA"))
rec.save(f"{B}/proof_paperdoll_lynx_composite.png")
print("composite rewritten from shipped slices")
