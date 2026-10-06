from PIL import Image

im = Image.open("/opt/side/bravesoul-game/proof_sky_lobby_hero_centered_fixed.png")
w, h = im.size

# Let's inspect x around center (550 to 730), y from 0 to 300
# Look for where non-background pixels start
# The top HUD bar is at y=0 to 80.
# Let's check y from 80 to 200 around x=640
print("Header is at y=0 to 80.")
# Let's find highest pixel of hero ear or nameplate
# Let's crop y=60 to 250, x=500 to 780
crop = im.crop((500, 60, 780, 300))
crop.save("/opt/side/bravesoul-game/tools/hero_head_crop.png")
print("Saved hero_head_crop.png")
