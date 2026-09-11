from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
m_im = Image.open(f"{r_dir}/composite_final_master.png").convert("RGBA")
p_im = Image.open(f"{r_dir}/composite_preview_nutcracker.png").convert("RGBA")

m_im.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/master_4x.png")
p_im.resize((512, 512), getattr(Image, 'Resampling', Image).NEAREST).save("/tmp/preview_nutcracker_4x.png")

print("Saved master and preview nutcracker!")
