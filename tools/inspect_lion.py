from PIL import Image

l_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/lion"
lance = Image.open(f"{l_dir}/weapon/wpn_knight_lance.png").convert("RGBA")
ch_ivory = Image.open(f"{l_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
print("Lance bbox:", lance.getbbox())
print("Lion chassis bbox:", ch_ivory.getbbox())

# Let's inspect where the lance is relative to lion's hand
comp = Image.new("RGBA", (128, 128), (0,0,0,0))
comp.alpha_composite(ch_ivory)
comp.alpha_composite(lance)
comp.save("/tmp/test_lion_comp.png")
print("Saved lion test comp")
