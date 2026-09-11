from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/hud_dopamine/proof_explore_hud_hotbar.png')
print('Image size:', im.size)
# Let's crop around center
crop1 = im.crop((500, 350, 850, 600))
crop1.save('/tmp/crop_center.png')
print('Saved /tmp/crop_center.png')
