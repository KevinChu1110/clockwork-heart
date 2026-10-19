from PIL import Image

OUT_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts"

# Check the source pieces in lion/
p_body = f"{OUT_DIR}/body/paint_brass_gold.png"
p_head = f"{OUT_DIR}/head_unit/ear_lion_gilded_mane_brass.png"
p_eyes_amber = f"{OUT_DIR}/eyes/eyes_amber_gold.png"
p_eyes_cyan = f"{OUT_DIR}/eyes/eyes_cyan_emerald.png"
p_costume_nut = f"{OUT_DIR}/costume/costume_nutcracker_guard.png"
p_costume_art = f"{OUT_DIR}/costume/costume_steam_artisan.png"
p_weapon = f"{OUT_DIR}/weapon/wpn_knight_lance.png"
p_key = f"{OUT_DIR}/winding_key/key_classic_brass.png"

im_body = Image.open(p_body)
im_head = Image.open(p_head)
im_eyes = Image.open(p_eyes_amber)

# Composite just body + head
c_bh = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
# Head is placed at (131, 51)
c_bh.alpha_composite(im_body)
c_bh.alpha_composite(im_head, (131, 51))
c_bh.save("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/comp_body_head.png")

# Now let's see where the eyes in core_amber_sun_512 were in 512 canvas:
# In core_amber_sun_512.png, eyes were at x=186..270, y=162..184
# When eyes sprite is 120x60 cropped from (168, 143, 288, 203):
# Placing eyes at (168, 143):
c_bhe = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
c_bhe.alpha_composite(c_bh)
c_bhe.alpha_composite(im_eyes, (168, 143))
c_bhe.save("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/comp_body_head_eyes.png")

print("Saved comp_body_head.png and comp_body_head_eyes.png")
