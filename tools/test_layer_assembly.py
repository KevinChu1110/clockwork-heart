import os
from PIL import Image, ImageChops

fox_pd = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox"

# Check standard composite
shadow = Image.open(f"{fox_pd}/chassis/paint_fox_orange.png").convert("RGBA") # or build shadow
tail = Image.open(f"{fox_pd}/back_curio/curio_fox_astral_tail.png").convert("RGBA")
key = Image.open(f"{fox_pd}/winding_key/key_classic_brass.png").convert("RGBA")
chassis = Image.open(f"{fox_pd}/chassis/paint_fox_orange.png").convert("RGBA")
costume = Image.open(f"{fox_pd}/costume/costume_astral_observer.png").convert("RGBA")
core = Image.open(f"{fox_pd}/optic_core/core_cyan_emerald.png").convert("RGBA")
head = Image.open(f"{fox_pd}/head_unit/ear_fox_radar.png").convert("RGBA")
weapon = Image.open(f"{fox_pd}/weapon/wpn_astral_staff.png").convert("RGBA")

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
# Order in paperdoll: shadow -> tail -> key -> chassis -> costume -> core -> head -> weapon
comp.alpha_composite(tail)
comp.alpha_composite(key)
comp.alpha_composite(chassis)
comp.alpha_composite(costume)
comp.alpha_composite(core)
comp.alpha_composite(head)
comp.alpha_composite(weapon)

party_idle = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")

diff = ImageChops.difference(party_idle, comp)
bbox = diff.getbbox()
print("Composite bbox:", comp.getbbox())
print("Party idle bbox:", party_idle.getbbox())
print("Diff bbox:", bbox)
if bbox:
    diff_data = list(diff.convert("L").getdata())
    diff_px = sum(1 for x in diff_data if x > 10)
    print("Diff pixels (>10):", diff_px)
comp.save("/tmp/fox_layer_comp.png")
