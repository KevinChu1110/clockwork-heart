from PIL import Image, ImageChops

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
master = Image.open(f"{r_dir}/composite_final_master.png").convert("RGBA")
bare = Image.open(f"{r_dir}/composite_bare_master.png").convert("RGBA")

diff = ImageChops.difference(master, bare)
print("Difference bbox between master and bare:", diff.getbbox())
diff.save("/tmp/master_bare_diff.png")
