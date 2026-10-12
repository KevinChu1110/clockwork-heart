from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/t_5c2f9a55/proof_04_char_weapon_auto_equip_en.png')
print('Image size:', im.size)
# Find non-background pixels on the rightmost columns
# Background is dark or cream. Let's see what is at x > 1200
w, h = im.size
print('Width:', w, 'Height:', h)
