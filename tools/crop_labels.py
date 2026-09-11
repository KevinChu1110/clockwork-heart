from PIL import Image

im = Image.open('/opt/side/bravesoul-game/proofs/hud_dopamine/proof_explore_hud_hotbar.png')
crop = im.crop((610, 350, 760, 420))
crop.save('/tmp/crop_sword_maisui.png')

# Also crop each label separately:
# Let's inspect pixel colors in this region
print("Cropped /tmp/crop_sword_maisui.png")
