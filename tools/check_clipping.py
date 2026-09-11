from typing import cast
from PIL import Image

for name in [
    "pos14_deg-65_h96_64",
    "pos14_deg-70_h98_60",
    "pos14_deg-60_h96_58",
    "pos14_deg-75_h98_62",
    "pos14_deg-65_h94_70",
    "pos14_deg-55_h95_55",
]:
    im = Image.open(f"/tmp/fox_hit_candidates/{name}.png")
    px = im.load()
    assert px is not None
    x0 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], px[0, y])[3] > 0)
    x127 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], px[127, y])[3] > 0)
    y0 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], px[x, 0])[3] > 0)
    y127 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], px[x, 127])[3] > 0)
    print(f"{name}: x0={x0}, x127={x127}, y0={y0}, y127={y127}")
