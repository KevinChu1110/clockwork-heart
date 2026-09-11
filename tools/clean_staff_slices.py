from PIL import Image

staff = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png")
print("Staff size:", staff.size)
# Let's inspect where pixels are located
px = staff.load()
assert px is not None
# Let's see non-shaft, non-crystal pixels
# Crystal is at top: around x=84..108, y=39..65
# Shaft is around x=88..98, y=65..124
# Are there other disconnected components?
mask = Image.new("L", staff.size, 0)
m_px = mask.load()
assert m_px is not None
for y in range(staff.height):
    for x in range(staff.width):
        if px[x, y][3] > 20:
            m_px[x, y] = 255

mask.save("/tmp/staff_mask.png")
