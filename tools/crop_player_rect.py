from PIL import Image

screen = Image.open("/opt/side/bravesoul-game/proofs/combat_feel/rabbit_battle_idle.png").convert("RGB")
# Crop player drawn rect: x in [224, 424], y in [248, 448]
crop = screen.crop((224, 248, 424, 448))
crop.save("/tmp/player_drawn_crop_grade_off.png")
print("Saved /tmp/player_drawn_crop_grade_off.png")
