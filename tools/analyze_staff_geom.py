from PIL import Image

staff = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png")
print("Staff bbox:", staff.getbbox())
px = staff.load()
assert px is not None
rows = []
for y in range(staff.height):
    xs = [x for x in range(staff.width) if px[x, y][3] > 100]
    if xs:
        rows.append((y, min(xs), max(xs)))

print(f"Total active rows: {len(rows)}")
print("Top row:", rows[0])
print("Bottom row:", rows[-1])
print("Hand grip region around y=86..92:")
for y, x0, x1 in rows:
    if 86 <= y <= 92:
        print(f"  y={y}: x={x0}..{x1}")
