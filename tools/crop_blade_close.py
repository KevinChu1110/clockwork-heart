from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")
crop = screen.crop((310, 350, 360, 410))
crop_3x = crop.resize((crop.width * 4, crop.height * 4), getattr(Image, 'Resampling', Image).NEAREST)
crop_3x.save("/tmp/rabbit_blade_close.png")
print("Saved /tmp/rabbit_blade_close.png")
