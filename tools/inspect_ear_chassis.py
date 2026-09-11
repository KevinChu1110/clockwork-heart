from PIL import Image

r_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit"
ear = Image.open(f"{r_dir}/head_unit/ear_rabbit_straight.png").convert("RGBA")
ch_ivory = Image.open(f"{r_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
ch_navy = Image.open(f"{r_dir}/chassis/paint_midnight_navy.png").convert("RGBA")

print("ear bbox:", ear.getbbox())
print("ch_ivory bbox:", ch_ivory.getbbox())
print("ch_navy bbox:", ch_navy.getbbox())

# Where does ear overlap with chassis?
# In rabbit, ear bbox is (41, 7, 83, 72).
# Chassis bbox is (34, 42, 93, 124).
# So ear is y=7..72, chassis starts at y=42!
# They overlap between y=42 and y=72!
