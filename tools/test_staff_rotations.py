from PIL import Image, ImageDraw

staff_src = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = s_px[x, y]

# Bridge shaft
draw_cs = ImageDraw.Draw(clean_staff)
draw_cs.line([(91, 95), (88, 99)], fill=(115, 75, 45, 255), width=2)
draw_cs.line([(88, 108), (89, 117)], fill=(115, 75, 45, 255), width=2)

def place_rigid_staff(staff_img: Image.Image, deg: float, target_hand: tuple[int, int], scale: float = 1.0) -> Image.Image:
    large_canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    large_canvas.paste(staff_img, (128 - 93, 128 - 88))
    if scale != 1.0:
        sw = int(round(256 * scale))
        sh = int(round(256 * scale))
        large_canvas = large_canvas.resize((sw, sh), Image.Resampling.LANCZOS)
    rotated = large_canvas.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hx, hy = target_hand
    out_128.paste(rotated, (hx - 128, hy - 128), rotated)
    return out_128

# In idle, deg=0, crystal is at (98, 48..58) (top), base at (90, 120) (bottom), hand at (90, 86).
# If we rotate by -60..-75 degrees (counter-clockwise):
# The top (crystal) rotates to the right!
# Let's test deg=-60, -70, -80, -90
for deg in [-50, -65, -75, -85]:
    st = place_rigid_staff(clean_staff, deg=deg, target_hand=(80, 80))
    st.save(f"/tmp/test_staff_deg_{abs(deg)}.png")
    print(f"deg={deg}, bbox={st.getbbox()}")
