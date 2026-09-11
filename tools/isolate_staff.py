from PIL import Image

staff = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
px = staff.load()
assert px is not None

# Clean any pixels far away from the staff
clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
c_px = clean_staff.load()
assert c_px is not None

for y in range(128):
    for x in range(128):
        p = px[x, y]
        # Staff is centered around x in 84..108
        if 80 <= x <= 112 and 38 <= y <= 125:
            # Check if this pixel is part of staff
            c_px[x, y] = p

clean_staff.save("/tmp/clean_staff_only.png")
print("Clean staff bbox:", clean_staff.getbbox())
