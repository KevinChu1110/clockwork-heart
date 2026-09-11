from PIL import Image

b_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar"
hammer = Image.open(f"{b_dir}/weapon/wpn_anvil_greathammer.png").convert("RGBA")
ch_ivory = Image.open(f"{b_dir}/chassis/paint_ivory_stock.png").convert("RGBA")
print("Boar hammer bbox:", hammer.getbbox())
print("Boar chassis bbox:", ch_ivory.getbbox())

comp = Image.new("RGBA", (128, 128), (0,0,0,0))
comp.alpha_composite(ch_ivory)
comp.alpha_composite(hammer)
comp.save("/tmp/test_boar_comp.png")
