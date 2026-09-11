from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
m_im = Image.open(f"{r_dir}/composite_final_master.png").convert("RGBA")
p_im = Image.open(f"{r_dir}/composite_preview_nutcracker.png").convert("RGBA")
dawn = Image.open(f"{r_dir}/weapon/wpn_dawn_blade.png").convert("RGBA")

# Let's crop x: 30..90, y: 70..126
m_crop = m_im.crop((30, 70, 90, 126)).resize((300, 280), getattr(Image, 'Resampling', Image).NEAREST)
m_crop.save("/tmp/master_weapon_hand.png")

p_crop = p_im.crop((30, 70, 90, 126)).resize((300, 280), getattr(Image, 'Resampling', Image).NEAREST)
p_crop.save("/tmp/preview_weapon_hand.png")

d_crop = dawn.crop((30, 70, 90, 126)).resize((300, 280), getattr(Image, 'Resampling', Image).NEAREST)
d_crop.save("/tmp/dawn_crop.png")

print("Saved weapon hand crops successfully!")
