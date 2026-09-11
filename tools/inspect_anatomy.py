from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")

# Let's inspect where the limbs are
# Head: y=42..70
# Torso: y=70..95
# Legs: y=95..124
# Wait, let's see what is at x=35..45, y=75..95 vs x=75..85, y=75..95
# Left arm (character's left, screen right): x=75..88, y=70..90
# Right arm (character's right, screen left): x=34..45, y=70..90

print("Chassis bbox:", ch_ivory.getbbox())
